#!/usr/bin/env python3
"""Create, upload, and optionally publish the gated Zenodo v1.0 record."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import md5, sha256
import hmac
import json
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / ".zenodo.json"
DEFAULT_CERTIFICATE = (
    ROOT / "certificates" / "cycle-018-zenodo-deposition.json"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def curl_json(
    method: str,
    url: str,
    token: str,
    *,
    payload: dict | None = None,
    upload: Path | None = None,
) -> dict:
    if any(character in token for character in "\"\r\n"):
        raise ValueError("access token contains an unsafe character")
    command = ["curl", "-fsS", "-X", method]
    if payload is not None:
        command.extend(
            [
                "-H",
                "Content-Type: application/json",
                "--data-binary",
                json.dumps(payload, separators=(",", ":")),
            ]
        )
    if upload is not None:
        command.extend(["--upload-file", str(upload)])
    command.append(url)
    with tempfile.NamedTemporaryFile(
        "w",
        prefix="certified-qmc-zenodo-curl-",
        delete=True,
    ) as configuration:
        configuration.write(
            f'header = "Authorization: Bearer {token}"\n'
        )
        configuration.flush()
        os.chmod(configuration.name, 0o600)
        completed = subprocess.run(
            [
                command[0],
                "--config",
                configuration.name,
                *command[1:],
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    return json.loads(completed.stdout)


def write_state(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def file_digests(path: Path) -> tuple[str, str]:
    sha256_state = sha256()
    md5_state = md5(usedforsecurity=False)
    block = bytearray(1024 * 1024)
    view = memoryview(block)
    with path.open("rb", buffering=0) as stream:
        while count := stream.readinto(view):
            sha256_state.update(view[:count])
            md5_state.update(view[:count])
    return sha256_state.hexdigest(), md5_state.hexdigest()


def authenticate_release(release: Path) -> tuple[dict, list[Path]]:
    manifest_path = release / "release-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    supplied = manifest.pop("manifest_sha256", None)
    if supplied != canonical_sha256(manifest):
        raise ValueError("release manifest self-hash mismatch")
    manifest["manifest_sha256"] = supplied
    declared = {}
    for row in [
        *manifest.get("assets", []),
        *manifest.get("ancillary_files", []),
    ]:
        filename = row["filename"]
        if filename in declared:
            raise ValueError("release manifest has a duplicate filename")
        path = release / filename
        if (
            not path.is_file()
            or path.stat().st_size != int(row["bytes"])
            or file_digests(path)[0] != row["sha256"]
        ):
            raise ValueError(
                f"release file authentication failed: {filename}"
            )
        declared[filename] = path
    if len(manifest.get("assets", [])) != 4:
        raise ValueError("release manifest must contain four assets")
    if len(manifest.get("ancillary_files", [])) != 3:
        raise ValueError(
            "release manifest must contain three ancillary files"
        )
    actual = {
        path.name
        for path in release.iterdir()
        if path.is_file()
        and path.name != ".zenodo-deposition-state.json"
    }
    expected = {*declared, manifest_path.name}
    if actual != expected:
        raise ValueError("release directory has undeclared upload files")
    paths = sorted([manifest_path, *declared.values()])
    if len(paths) > 100:
        raise ValueError("release exceeds Zenodo's 100-file limit")
    if sum(path.stat().st_size for path in paths) > 50_000_000_000:
        raise ValueError("release exceeds Zenodo's 50 GB quota")
    return manifest, paths


def normalize_remote_file(value: dict) -> dict:
    filename = value.get("filename", value.get("key"))
    size = value.get("filesize", value.get("size"))
    checksum = value.get("checksum")
    if not isinstance(filename, str) or not filename:
        raise ValueError("Zenodo file response lacks a filename")
    if size is None:
        raise ValueError("Zenodo file response lacks a byte count")
    if not isinstance(checksum, str) or not checksum:
        raise ValueError("Zenodo file response lacks a checksum")
    algorithm, separator, digest = checksum.partition(":")
    if not separator:
        algorithm, digest = "md5", algorithm
    if algorithm.lower() != "md5" or len(digest) != 32:
        raise ValueError("Zenodo file checksum is not a valid MD5")
    return {
        "filename": filename,
        "bytes": int(size),
        "zenodo_checksum": f"md5:{digest.lower()}",
        "zenodo_md5": digest.lower(),
    }


def verify_remote_file(path: Path, value: dict) -> dict:
    remote = normalize_remote_file(value)
    local_sha256, local_md5 = file_digests(path)
    if remote["filename"] != path.name:
        raise IOError("Zenodo upload filename mismatch")
    if remote["bytes"] != path.stat().st_size:
        raise IOError("Zenodo upload size mismatch")
    if not hmac.compare_digest(remote["zenodo_md5"], local_md5):
        raise IOError("Zenodo upload checksum mismatch")
    return {
        **remote,
        "local_sha256": local_sha256,
        "local_md5": local_md5,
        "remote_content_equal": True,
    }


def verify_remote_inventory(
    paths: list[Path], values: list[dict]
) -> list[dict]:
    by_name = {}
    for value in values:
        normalized = normalize_remote_file(value)
        if normalized["filename"] in by_name:
            raise ValueError("Zenodo file inventory has a duplicate name")
        by_name[normalized["filename"]] = value
    expected = {path.name for path in paths}
    if set(by_name) != expected:
        raise ValueError("Zenodo file inventory does not match release")
    return [
        verify_remote_file(path, by_name[path.name])
        for path in sorted(paths)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-dir", type=Path, required=True)
    parser.add_argument(
        "--api-base", default="https://zenodo.org/api"
    )
    parser.add_argument(
        "--certificate", type=Path, default=DEFAULT_CERTIFICATE
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="publish irreversibly after upload and metadata checks",
    )
    args = parser.parse_args()
    release = args.release_dir.resolve()
    token = (
        os.environ.get("ZENODO_ACCESS_TOKEN")
        or os.environ.get("ZENODO_TOKEN")
    )
    if not token:
        raise SystemExit(
            "ZENODO_ACCESS_TOKEN or ZENODO_TOKEN is required"
        )
    release_manifest_path = release / "release-manifest.json"
    if not release_manifest_path.is_file():
        raise ValueError("release manifest is absent")
    state_path = release / ".zenodo-deposition-state.json"
    authenticated_manifest, upload_paths = authenticate_release(release)

    if state_path.exists():
        state = json.loads(state_path.read_text())
        deposition = curl_json(
            "GET", state["links"]["self"], token
        )
    else:
        deposition = curl_json(
            "POST",
            f"{args.api_base}/deposit/depositions",
            token,
            payload={},
        )
        state = {
            "schema": "certified-qmc-zenodo-draft-state-v1",
            "created_at_utc": utc_now(),
            "deposition_id": deposition["id"],
            "links": deposition["links"],
            "reserved_doi": deposition["metadata"][
                "prereserve_doi"
            ]["doi"],
            "published": False,
        }
        write_state(state_path, state)

    if deposition.get("submitted"):
        state["uploads"] = verify_remote_inventory(
            upload_paths, deposition["files"]
        )
        write_state(state_path, state)
        if not args.publish:
            print(state_path)
            return
        published = deposition
    else:
        doi = deposition["metadata"]["prereserve_doi"]["doi"]
        release_manifest = authenticated_manifest
        if release_manifest.get("doi") not in (None, doi):
            raise ValueError("release manifest DOI conflicts with draft")
        release_manifest.pop("manifest_sha256")
        release_manifest["doi"] = doi
        release_manifest["manifest_sha256"] = canonical_sha256(
            release_manifest
        )
        release_manifest_path.write_text(
            json.dumps(
                release_manifest, indent=2, sort_keys=True
            )
            + "\n"
        )

        bucket = deposition["links"]["bucket"]
        for path in upload_paths:
            response = curl_json(
                "PUT",
                f"{bucket}/{quote(path.name)}",
                token,
                upload=path,
            )
            verify_remote_file(path, response)

        metadata = json.loads(METADATA.read_text())
        if metadata.get("license") != "Apache-2.0":
            raise ValueError("unexpected release-code license metadata")
        metadata["license"] = "apache-2.0"
        metadata["prereserve_doi"] = True
        updated = curl_json(
            "PUT",
            deposition["links"]["self"],
            token,
            payload={"metadata": metadata},
        )
        if (
            updated["metadata"]["prereserve_doi"]["doi"]
            != doi
            or len(updated["files"]) != len(upload_paths)
        ):
            raise ValueError("Zenodo draft verification failed")
        uploaded = verify_remote_inventory(
            upload_paths, updated["files"]
        )
        state["uploaded_at_utc"] = utc_now()
        state["uploads"] = uploaded
        write_state(state_path, state)

        if not args.publish:
            print(state_path)
            return
        published = curl_json(
            "POST", updated["links"]["publish"], token
        )

    doi = published.get("doi")
    if (
        not published.get("submitted")
        or not doi
        or doi != state["reserved_doi"]
    ):
        raise ValueError("Zenodo publication response is incomplete")
    published_uploads = verify_remote_inventory(
        upload_paths, published["files"]
    )
    if state.get("uploads") != published_uploads:
        raise ValueError(
            "published Zenodo file inventory changed after verification"
        )
    state["published"] = True
    state["published_at_utc"] = utc_now()
    state["doi"] = doi
    state["record_url"] = published["record_url"]
    write_state(state_path, state)
    certificate = {
        "schema": "certified-qmc-cycle-018-zenodo-deposition-v1",
        "claim_tag": "VERIFIED_EXTERNAL_DEPOSITION_RESPONSE",
        "recorded_at_utc": utc_now(),
        "deposition_id": state["deposition_id"],
        "doi": doi,
        "record_url": state["record_url"],
        "uploads": published_uploads,
        "published": True,
        "announcement_permitted": True,
        "boundary": (
            "This records the authenticated Zenodo API response. "
            "Asset content remains authenticated by the release "
            "manifest SHA-256 values."
        ),
    }
    certificate["certificate_sha256"] = sha256(
        json.dumps(
            certificate,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()
    args.certificate.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    print(args.certificate)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create, upload, and optionally publish the gated Zenodo v1.0 record."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
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
        if not args.publish:
            print(state_path)
            return
        published = deposition
    else:
        doi = deposition["metadata"]["prereserve_doi"]["doi"]
        release_manifest = json.loads(
            release_manifest_path.read_text()
        )
        if release_manifest.get("doi") not in (None, doi):
            raise ValueError("release manifest DOI conflicts with draft")
        release_manifest.pop("manifest_sha256")
        release_manifest["doi"] = doi
        from hashlib import sha256

        release_manifest["manifest_sha256"] = sha256(
            json.dumps(
                release_manifest,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
            ).encode("ascii")
        ).hexdigest()
        release_manifest_path.write_text(
            json.dumps(
                release_manifest, indent=2, sort_keys=True
            )
            + "\n"
        )

        upload_paths = sorted(
            path
            for path in release.iterdir()
            if path.is_file()
            and path.name != state_path.name
        )
        uploaded = []
        bucket = deposition["links"]["bucket"]
        for path in upload_paths:
            response = curl_json(
                "PUT",
                f"{bucket}/{quote(path.name)}",
                token,
                upload=path,
            )
            if int(response["size"]) != path.stat().st_size:
                raise IOError("Zenodo upload size mismatch")
            uploaded.append(
                {
                    "filename": path.name,
                    "bytes": path.stat().st_size,
                    "zenodo_checksum": response["checksum"],
                }
            )

        metadata = json.loads(METADATA.read_text())
        metadata["license"] = "cc-by-4.0"
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
        "uploads": state["uploads"],
        "published": True,
        "announcement_permitted": True,
        "boundary": (
            "This records the authenticated Zenodo API response. "
            "Asset content remains authenticated by the release "
            "manifest SHA-256 values."
        ),
    }
    from hashlib import sha256

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

from __future__ import annotations

from hashlib import md5, sha256
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.zenodo_deposit_release import (
    authenticate_release,
    canonical_sha256,
    normalize_remote_file,
    verify_remote_file,
    verify_remote_inventory,
    main as zenodo_main,
)
from src.certificate import canonical_sha256 as project_canonical_sha256
from src.chunked_table import file_sha256


PROJECT = Path(__file__).resolve().parents[1]


class ZenodoDepositionTests(unittest.TestCase):
    @staticmethod
    def make_release(release: Path) -> dict:
        assets = []
        ancillary = []
        for index in range(4):
            path = release / f"asset-{index}.bin"
            path.write_bytes(bytes([index]) * (index + 1))
            assets.append(
                {
                    "filename": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
            )
        for name in ("LICENSE", "LICENSE-DATA", "REPRODUCING.md"):
            path = release / name
            path.write_text(name)
            ancillary.append(
                {
                    "filename": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
            )
        manifest = {
            "schema": "test-release",
            "assets": assets,
            "ancillary_files": ancillary,
            "doi": None,
        }
        manifest["manifest_sha256"] = canonical_sha256(manifest)
        (release / "release-manifest.json").write_text(
            json.dumps(manifest, sort_keys=True) + "\n"
        )
        return manifest

    def test_release_manifest_and_declared_file_set_are_authenticated(self):
        with tempfile.TemporaryDirectory() as directory:
            release = Path(directory)
            manifest = self.make_release(release)
            loaded, paths = authenticate_release(release)
            self.assertEqual(
                loaded["manifest_sha256"],
                manifest["manifest_sha256"],
            )
            self.assertEqual(len(paths), 8)
            undeclared = release / "extra.txt"
            undeclared.write_text("not in manifest")
            with self.assertRaisesRegex(ValueError, "undeclared"):
                authenticate_release(release)

    def test_publish_flow_reverifies_complete_remote_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release = root / "release"
            release.mkdir()
            self.make_release(release)
            certificate = root / "deposition.json"
            doi = "10.5281/zenodo.1234567"
            links = {
                "self": "https://example.test/deposit/1",
                "bucket": "https://example.test/bucket/1",
                "publish": "https://example.test/deposit/1/publish",
            }

            def remote_files() -> list[dict]:
                return [
                    {
                        "key": path.name,
                        "size": path.stat().st_size,
                        "checksum": "md5:"
                        + md5(
                            path.read_bytes(), usedforsecurity=False
                        ).hexdigest(),
                    }
                    for path in sorted(release.iterdir())
                    if path.is_file()
                    and path.name
                    != ".zenodo-deposition-state.json"
                ]

            def fake_curl(
                method: str,
                url: str,
                token: str,
                *,
                payload: dict | None = None,
                upload: Path | None = None,
            ) -> dict:
                self.assertEqual(token, "test-token")
                if upload is not None:
                    return {
                        "key": upload.name,
                        "size": upload.stat().st_size,
                        "checksum": "md5:"
                        + md5(
                            upload.read_bytes(),
                            usedforsecurity=False,
                        ).hexdigest(),
                    }
                if method == "POST" and url.endswith("/depositions"):
                    return {
                        "id": 1,
                        "submitted": False,
                        "links": links,
                        "metadata": {
                            "prereserve_doi": {"doi": doi}
                        },
                    }
                if method == "PUT" and payload is not None:
                    return {
                        "links": links,
                        "metadata": {
                            "prereserve_doi": {"doi": doi}
                        },
                        "files": remote_files(),
                    }
                if method == "POST" and url == links["publish"]:
                    return {
                        "submitted": True,
                        "doi": doi,
                        "record_url": "https://zenodo.org/records/1234567",
                        "files": remote_files(),
                    }
                raise AssertionError((method, url, payload, upload))

            arguments = [
                "zenodo_deposit_release.py",
                "--release-dir",
                str(release),
                "--certificate",
                str(certificate),
                "--publish",
            ]
            with (
                patch.dict(
                    os.environ,
                    {"ZENODO_ACCESS_TOKEN": "test-token"},
                    clear=False,
                ),
                patch(
                    "scripts.zenodo_deposit_release.curl_json",
                    side_effect=fake_curl,
                ),
                patch.object(sys, "argv", arguments),
            ):
                zenodo_main()
            result = json.loads(certificate.read_text())
            supplied = result.pop("certificate_sha256")
            self.assertEqual(supplied, canonical_sha256(result))
            self.assertTrue(result["published"])
            self.assertTrue(result["announcement_permitted"])
            self.assertEqual(result["doi"], doi)
            self.assertEqual(len(result["uploads"]), 8)
            self.assertTrue(
                all(
                    row["remote_content_equal"]
                    for row in result["uploads"]
                )
            )

    def test_bucket_and_legacy_file_responses_are_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "asset.bin"
            path.write_bytes(bytes(range(251)) * 17)
            checksum = md5(
                path.read_bytes(), usedforsecurity=False
            ).hexdigest()
            bucket = {
                "key": path.name,
                "size": path.stat().st_size,
                "checksum": f"md5:{checksum}",
            }
            legacy = {
                "filename": path.name,
                "filesize": path.stat().st_size,
                "checksum": checksum,
            }
            for response in (bucket, legacy):
                verified = verify_remote_file(path, response)
                self.assertTrue(verified["remote_content_equal"])
                self.assertEqual(
                    verified["local_sha256"],
                    sha256(path.read_bytes()).hexdigest(),
                )
                self.assertEqual(verified["local_md5"], checksum)

    def test_checksum_size_and_inventory_mismatches_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.bin"
            second = Path(directory) / "second.bin"
            first.write_bytes(b"first")
            second.write_bytes(b"second")

            def remote(path: Path) -> dict:
                return {
                    "key": path.name,
                    "size": path.stat().st_size,
                    "checksum": "md5:"
                    + md5(
                        path.read_bytes(), usedforsecurity=False
                    ).hexdigest(),
                }

            bad_checksum = remote(first)
            bad_checksum["checksum"] = "md5:" + "0" * 32
            with self.assertRaisesRegex(IOError, "checksum"):
                verify_remote_file(first, bad_checksum)
            bad_size = remote(first)
            bad_size["size"] += 1
            with self.assertRaisesRegex(IOError, "size"):
                verify_remote_file(first, bad_size)
            with self.assertRaisesRegex(ValueError, "inventory"):
                verify_remote_inventory(
                    [first, second], [remote(first)]
                )
            with self.assertRaisesRegex(ValueError, "duplicate"):
                verify_remote_inventory(
                    [first], [remote(first), remote(first)]
                )

    def test_unknown_remote_checksum_algorithm_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "valid MD5"):
            normalize_remote_file(
                {
                    "key": "asset.bin",
                    "size": 1,
                    "checksum": "sha256:" + "0" * 64,
                }
            )

    def test_banked_local_preflight_binds_current_implementation(self):
        path = (
            PROJECT
            / "certificates"
            / "cycle-018-zenodo-deposition-preflight.json"
        )
        payload = json.loads(path.read_text())
        supplied = payload.pop("certificate_sha256")
        self.assertEqual(
            supplied, project_canonical_sha256(payload)
        )
        self.assertEqual(
            payload["claim_tag"], "VERIFIED_LOCAL_PREFLIGHT"
        )
        self.assertFalse(
            payload["gate"]["external_deposition_published"]
        )
        self.assertFalse(
            payload["gate"]["announcement_permitted"]
        )
        for relative, expected in payload["source"].items():
            self.assertEqual(
                file_sha256(PROJECT / relative), expected
            )


if __name__ == "__main__":
    unittest.main()

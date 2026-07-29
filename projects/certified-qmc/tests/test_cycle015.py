from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from src.certificate import canonical_sha256
from src.chunked_table import (
    ZERO_HASH,
    append_record,
    chunk_records,
    file_sha256,
    iter_chain,
    read_chain,
)
from src.entry_replay import DatasetReplay
from scripts.build_engine_oracle_set import replay_batch


PROJECT = Path(__file__).resolve().parents[1]
DATASET = PROJECT / "artifacts" / "cycle-015-pilot"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class Cycle015Tests(unittest.TestCase):
    def test_failed_attempt_and_v2_preregistration_are_preserved(self):
        failed = (
            PROJECT / "certificates" / "cycle-015-demo-failed-v1.json"
        )
        amended = json.loads(
            (
                PROJECT / "data" / "cycle-015-preregistration-v2.json"
            ).read_text()
        )
        self.assertFalse(amended["data_run_started"])
        self.assertFalse(
            amended["predecessor"]["timestamp_preceded_attempt"]
        )
        self.assertEqual(
            amended["predecessor"]["failed_transcript_sha256"],
            digest(failed),
        )
        self.assertEqual(
            amended["unchanged_thresholds"][
                "forced_stop_after_new_chunk_counts"
            ],
            [17, 211, 503],
        )
        self.assertEqual(
            amended["unchanged_thresholds"][
                "maximum_dataset_payload_fraction"
            ],
            "0.01",
        )

    def test_chunk_manifest_and_gate_artifact_replay(self):
        artifact = json.loads(
            (
                PROJECT / "certificates" / "cycle-015-chunk-replay.json"
            ).read_text()
        )
        supplied = artifact.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied)
        self.assertTrue(artifact["gate"]["cycle_015_exit_gate_passed"])
        self.assertTrue(
            artifact["gate"][
                "three_sigkill_resume_runs_byte_identical"
            ]
        )
        self.assertEqual(
            [
                row["forced_kill_after_manifested_chunks"]
                for row in artifact["kill_and_resume"]
            ],
            [17, 211, 503],
        )
        self.assertTrue(
            all(
                row["killed_return_code"] == -9
                and row["byte_identical_to_uninterrupted"]
                for row in artifact["kill_and_resume"]
            )
        )
        replay = artifact["selected_entry_replay"]
        self.assertEqual(len(replay["entries"]), 10)
        self.assertTrue(replay["all_ten_verified"])
        self.assertTrue(replay["all_python_oracles_equal"])
        self.assertTrue(replay["all_overflow_checks_equal"])
        self.assertLessEqual(
            replay["maximum_observed_payload_fraction"],
            replay["frozen_maximum_payload_fraction"],
        )

        records = read_chain(DATASET / "manifest.jsonl")
        self.assertEqual(len(records), 939)
        self.assertEqual(records[-1]["event"], "SEAL")
        chunks = chunk_records(records)
        self.assertEqual(len(chunks), 938)
        for record in chunks:
            path = DATASET / record["path"]
            self.assertEqual(path.stat().st_size, record["bytes"])
            self.assertEqual(file_sha256(path), record["sha256"])

    def test_run_manifest_and_keyed_index_are_complete(self):
        run = json.loads((DATASET / "run-manifest.json").read_text())
        supplied = run.pop("run_manifest_sha256")
        self.assertEqual(canonical_sha256(run), supplied)
        index = json.loads((DATASET / "table-index.json").read_text())
        index_hash = index.pop("index_sha256")
        self.assertEqual(canonical_sha256(index), index_hash)
        self.assertFalse(index["vectors_embedded"])
        self.assertEqual(len(index["tables"]), 128)
        self.assertTrue(
            all("source_path" not in table for table in index["tables"])
        )
        self.assertEqual(
            digest(PROJECT / run["kernel"]["production_source"]),
            run["kernel"]["production_source_sha256"],
        )
        self.assertEqual(
            digest(PROJECT / run["kernel"]["pilot_source"]),
            run["kernel"]["pilot_source_sha256"],
        )
        self.assertFalse(run["kernel"]["optimization_changes"])
        self.assertNotIn(
            "fftw", "\n".join(run["kernel"]["linked_libraries"]).lower()
        )
        template = json.loads(
            (PROJECT / "data" / "run-manifest-template.json").read_text()
        )
        self.assertTrue(
            set(template["required_top_level_fields"])
            <= set([*run, "run_manifest_sha256"])
        )

    def test_one_command_verify_entry(self):
        completed = subprocess.run(
            [
                str(PROJECT / "bin" / "verify-entry"),
                "--dataset",
                str(DATASET),
                "--table",
                "pilot-040",
                "--N",
                "32",
                "--d",
                "13",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "VERIFIED")
        self.assertTrue(
            all(check["equal"] for check in result["overflow_checks"])
        )
        self.assertLessEqual(result["touched_payload_fraction"], 0.01)

    def test_batch_verify_entry_authenticates_manifest_once(self):
        completed = subprocess.run(
            [
                str(PROJECT / "bin" / "verify-entry"),
                "--dataset",
                str(DATASET),
                "--requests",
                str(
                    PROJECT
                    / "tests"
                    / "fixtures"
                    / "cycle015-batch-requests.json"
                ),
                "--compact",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        batch = json.loads(completed.stdout)
        self.assertEqual(batch["status"], "VERIFIED")
        self.assertEqual(batch["request_count"], 2)
        self.assertEqual(
            [row["dimension"] for row in batch["results"]],
            [7, 13],
        )
        self.assertTrue(
            all(
                all(
                    check["equal"]
                    for check in row["overflow_checks"]
                )
                for row in batch["results"]
            )
        )
        single = subprocess.run(
            [
                str(PROJECT / "bin" / "verify-entry"),
                "--dataset",
                str(DATASET),
                "--table",
                "pilot-000",
                "--N",
                "32",
                "--d",
                "7",
                "--compact",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        one = json.loads(single.stdout)
        first = batch["results"][0]
        for key in (
            "scaled_numerator",
            "scaled_denominator",
            "reduced_numerator",
            "reduced_denominator",
            "proved_numerator_bound",
            "generator_prefix_sha256",
        ):
            self.assertEqual(first[key], one[key])

    def test_oracle_extractor_streams_shared_chunks_without_value_change(self):
        schedule = json.loads(
            (
                PROJECT / "data" / "primes-schedule-v1.json"
            ).read_text()
        )
        primes = [int(row["p"]) for row in schedule["primes"]]
        requests = [
            {
                "table_id": "pilot-000",
                "N": 32,
                "dimension": dimension,
                "weight_power": 1,
            }
            for dimension in (7, 13)
        ]
        extracted, provenance = replay_batch(
            DATASET, requests, primes, "cycle-015-pilot"
        )
        completed = subprocess.run(
            [
                str(PROJECT / "bin" / "verify-entry"),
                "--dataset",
                str(DATASET),
                "--requests",
                str(
                    PROJECT
                    / "tests"
                    / "fixtures"
                    / "cycle015-batch-requests.json"
                ),
                "--compact",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        verified = json.loads(completed.stdout)["results"]
        for oracle, replayed in zip(extracted, verified):
            self.assertEqual(
                oracle["reduced_numerator"],
                replayed["reduced_numerator"],
            )
            self.assertEqual(
                oracle["reduced_denominator"],
                replayed["reduced_denominator"],
            )
        self.assertLess(
            provenance["selected_unique_chunk_count"],
            sum(
                row["authenticated_chunk_count"]
                for row in extracted
            ),
        )

    def test_batch_extension_transcript_replays(self):
        predecessor_path = (
            PROJECT
            / "certificates"
            / "cycle-015-batch-replay-extension-v1.json"
        )
        predecessor = json.loads(predecessor_path.read_text())
        predecessor_supplied = predecessor.pop("certificate_sha256")
        self.assertEqual(
            predecessor_supplied, canonical_sha256(predecessor)
        )
        artifact = json.loads(
            (
                PROJECT
                / "certificates"
                / "cycle-015-batch-replay-extension-v2.json"
            ).read_text()
        )
        supplied = artifact.pop("certificate_sha256")
        self.assertEqual(supplied, canonical_sha256(artifact))
        self.assertTrue(
            artifact["gate"]["cycle_015_streaming_extension_passed"]
        )
        self.assertEqual(
            artifact["predecessor"]["sha256"],
            file_sha256(predecessor_path),
        )
        self.assertEqual(
            artifact["single_vs_batch"]["single_result_sha256"],
            artifact["single_vs_batch"]["batch_entry_sha256"],
        )
        self.assertTrue(
            all(
                artifact["single_vs_batch"]["equal_fields"].values()
            )
        )
        for relative, expected in artifact["source"].items():
            self.assertEqual(file_sha256(PROJECT / relative), expected)

    def test_streaming_chain_and_replay_do_not_retain_manifest(self):
        materialized = read_chain(DATASET / "manifest.jsonl")
        streamed = list(iter_chain(DATASET / "manifest.jsonl"))
        self.assertEqual(streamed, materialized)
        replay = DatasetReplay(DATASET, PROJECT)
        self.assertFalse(hasattr(replay, "records"))
        self.assertFalse(hasattr(replay, "chunks"))

    def test_streaming_chain_rejects_truncation_and_link_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.jsonl"
            first = append_record(
                manifest,
                {"sequence": 0, "event": "TEST"},
                ZERO_HASH,
            )
            append_record(
                manifest,
                {"sequence": 1, "event": "TEST"},
                first["line_sha256"],
            )
            valid = manifest.read_bytes()
            manifest.write_bytes(valid[:-1])
            with self.assertRaisesRegex(ValueError, "unterminated"):
                list(iter_chain(manifest))
            lines = valid.splitlines(keepends=True)
            lines[1] = lines[1].replace(
                first["line_sha256"].encode("ascii"),
                b"f" * 64,
                1,
            )
            manifest.write_bytes(b"".join(lines))
            with self.assertRaisesRegex(
                ValueError, "previous-hash link"
            ):
                list(iter_chain(manifest))


if __name__ == "__main__":
    unittest.main()

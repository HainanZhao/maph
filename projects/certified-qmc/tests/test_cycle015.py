from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import unittest

from src.certificate import canonical_sha256
from src.chunked_table import chunk_records, file_sha256, read_chain


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


if __name__ == "__main__":
    unittest.main()

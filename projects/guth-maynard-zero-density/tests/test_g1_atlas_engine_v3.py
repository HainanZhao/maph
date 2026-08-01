"""Replay-boundary regressions for the corrected G1 v3 driver."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from discovery import run_g1_atlas_v3 as engine  # noqa: E402


class G1AtlasEngineV3Tests(unittest.TestCase):
    def test_integrity_names_distinct_replay_boundaries(self) -> None:
        report = engine.integrity_report()
        self.assertIn("read-only", report["assembly_verification"])
        self.assertIn("not replay", report["assembly_verification"])
        self.assertIn("fresh", report["full_replay"])
        self.assertEqual(report["runtime"]["optimization_level"], 0)

    def test_sealed_assembly_verification_is_read_only(self) -> None:
        observations = {"artifact_id": "observations"}
        performance = {"artifact_id": "performance"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint_path = root / "sealed.json"
            observations_path = root / "observations.json"
            performance_path = root / "performance.json"
            checkpoint_path.write_bytes(b"sealed checkpoint bytes\n")
            observations_path.write_bytes(engine.v2.json_bytes(observations))
            performance_path.write_bytes(engine.v2.json_bytes(performance))
            before = checkpoint_path.read_bytes()
            with (
                patch.object(engine, "check_runtime", return_value={"runtime": "pinned"}),
                patch.object(engine.v2, "load_checkpoint", return_value={"phase": "COMPLETE", "driver_v3": engine.driver_identity()}),
                patch.object(engine, "validate_sealed_checkpoint"),
                patch.object(engine, "assemble_v3", return_value=(observations, performance)),
            ):
                engine.verify_sealed_assembly(checkpoint_path, observations_path, performance_path)
            self.assertEqual(checkpoint_path.read_bytes(), before)

    def test_fresh_replay_rejects_existing_checkpoint_before_compute(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "already-there.json"
            target = Path(directory) / "target.json"
            checkpoint.write_text("existing", encoding="utf-8")
            with (
                patch.object(engine, "check_runtime", return_value={}),
                patch.object(engine.v2, "run_or_resume") as runner,
            ):
                with self.assertRaisesRegex(RuntimeError, "must be a new path"):
                    engine.full_replay_fresh(checkpoint, target)
                runner.assert_not_called()

    def test_fresh_replay_prepares_new_empty_checkpoint_then_recomputes(self) -> None:
        base_observations = {"artifact_id": "v2", "correction": {}}
        base_performance = {"artifact_id": "performance"}
        checkpoint_data = {"phase": "ASSEMBLY"}
        expected = engine.decorate_observations(base_observations)
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "fresh.json"
            target = Path(directory) / "target.json"
            target.write_bytes(engine.v2.json_bytes(expected))
            with (
                patch.object(engine, "prepare_v3_checkpoint") as prepare,
                patch.object(engine.v2, "run_or_resume", return_value=(base_observations, base_performance, checkpoint_data)) as runner,
            ):
                engine.full_replay_fresh(checkpoint, target)
            prepare.assert_called_once_with(checkpoint, resume=False)
            runner.assert_called_once_with(checkpoint, resume=True)
            self.assertTrue(checkpoint.is_file())
            self.assertEqual(checkpoint_data["fresh_full_replay"]["status"], "MATCH")


if __name__ == "__main__":
    unittest.main()

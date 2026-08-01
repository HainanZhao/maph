import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_mit_sword_official_bitstream_v1.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-mit-sword-official-bitstream-audit-v1.json"


class MitSwordOfficialBitstreamTests(unittest.TestCase):
    def test_offline_audit_replays(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], check=True)

    def test_sword_paths_anchors_and_author_copy_boundary(self) -> None:
        audit = json.loads(ARTIFACT.read_text())
        self.assertEqual(audit["epistemic_status"], "OBSERVED")
        entries = audit["official_sword_zip"]["required_entries"]
        self.assertEqual(
            {row["internal_path"] for row in entries},
            {
                "18-785-spring-2007/contents/lecture-notes/errorbounds.pdf",
                "18-785-spring-2007/contents/lecture-notes/von_mangoldt.pdf",
            },
        )
        self.assertTrue(all(row["exact_internal_to_frozen_official_bytes"] for row in entries))
        self.assertTrue(all(row["byte_identity"] == "NOT_ASSERTED; observed SHA-256 values differ" for row in audit["author_copy_relationship"]["pairs"]))
        self.assertEqual(audit["theorem_and_proof_anchors"]["errorbounds"]["pages"], 4)
        self.assertEqual(audit["theorem_and_proof_anchors"]["von_mangoldt"]["pages"], 6)


if __name__ == "__main__":
    unittest.main()

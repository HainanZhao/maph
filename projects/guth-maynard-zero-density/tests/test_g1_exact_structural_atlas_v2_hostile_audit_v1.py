from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof/audit_g1_exact_structural_atlas_v2_hostile_v1.py"


class G1ExactStructuralAtlasV2HostileAuditV1Tests(unittest.TestCase):
    def test_replayed_corrected_authority(self) -> None:
        data = json.loads((PROJECT / "artifacts/g1-exact-structural-atlas-v2-hostile-audit-v1.json").read_text())
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["exact_recomputation"], {"status": "PASS", "epistemic_status": "PROVED", "local_rows": 7744, "transfer_rows": 560, "energy_diagonal_rows": 704})
        self.assertEqual(data["hardening"]["status"], "PASS")
        self.assertEqual(data["decision"]["status"], "V2_AUTHORITY_REPLAYED")
        subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()

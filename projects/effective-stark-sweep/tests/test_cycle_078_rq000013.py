import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RQ000013ImprimitiveCertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = json.loads(
            (
                ROOT
                / "artifacts"
                / "rq000013-engine-a-imprimitive-certificate-v1.json"
            ).read_text()
        )
        cls.selection = json.loads(
            (
                ROOT
                / "data"
                / "census-paper-imprimitive-worked-case-selection-v1.json"
            ).read_text()
        )

    def test_preregistered_case_and_exact_result(self):
        self.assertEqual(self.selection["case"]["case_id"], "RQ-000013")
        self.assertEqual(self.selection["expected_imprimitive_euler_factor"], 2)
        self.assertEqual(self.certificate["case_id"], "RQ-000013")
        result = self.certificate["exact_result"]
        self.assertEqual(result["E_chi"], 2)
        self.assertEqual(result["I_chi"], 2)
        self.assertEqual(result["Lprime_log_coefficient"], 2)
        self.assertEqual(
            result["packet_power_identity"],
            "X_[0]=u^2; X_[1]=u^(-2)",
        )

    def test_exact_norm_kernel_orientation_and_artin_action(self):
        records = self.certificate["exact_transcript_records"]
        self.assertEqual(records["NORM_MAP"], "Mat([1, -1])")
        self.assertEqual(records["PRIMITIVE_NORM_KERNEL"], "[1; 1]")
        self.assertEqual(records["RELATIVE_INDEX"], "2")
        self.assertEqual(records["CHOSEN_ABSOLUTE_GENERATOR_ROOT_COUNT"], "1")
        self.assertEqual(records["ORIENTED_UNIT_ISOLATION_ROOT_COUNT"], "1")
        self.assertEqual(
            records["ARTIN_SIGN_CLASS_UNIT_ACTION"],
            "Mod(1, x^4 + 2*x^2 - 7)",
        )
        self.assertEqual(
            records["ARTIN_SIGN_CLASS_PACKET_ACTION"],
            "Mod(1, x^4 + 2*x^2 - 7)",
        )

    def test_numerical_cross_check_is_quarantined(self):
        cross_check = self.certificate["quarantined_numerical_cross_check"]
        self.assertEqual(cross_check["tag"], "OBSERVED")
        self.assertIn(
            "not used in the proof",
            self.certificate["claim_boundary"]["quarantined_cross_check"],
        )

    def test_replay(self):
        completed = subprocess.run(
            ["python3", "scripts/certify_rq000013_engine_a.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(
            "RQ000013_ENGINE_A_CERTIFICATE_REPLAY=PASS",
            completed.stdout,
        )

    def test_written_surfaces_include_claim_boundary(self):
        addendum = (
            ROOT
            / "paper"
            / "effective-stark-results-supplement-rq000013-addendum.tex"
        ).read_text()
        census = (ROOT / "paper" / "effective-stark-sweep-draft.md").read_text()
        self.assertIn("The identity below is \\texttt{PROVED}", addendum)
        self.assertIn("only an \\texttt{OBSERVED} cross-check", addendum)
        self.assertIn(r"E_\chi=1-\chi^\circ(\mathfrak p)=2", addendum)
        self.assertIn(r"X_{[0]}=u^2,\qquad X_{[1]}=u^{-2}", addendum)
        self.assertIn("RQ-000013", census)
        self.assertIn(r"\(E_\chi=2\)", census)

    def test_v14_correction_layer_replays_after_extraction(self):
        freeze = json.loads(
            (
                ROOT
                / "artifacts"
                / "results-paper-companion-local-freeze-v14.json"
            ).read_text()
        )
        self.assertEqual(freeze["status"], "LOCAL_FROZEN_NOT_PUBLIC")
        self.assertEqual(
            freeze["archive_sha256"],
            "6225d7660b2b6455480fd73e412b3937438d4dbb9f2f1c68cb4d7e3ac1052648",
        )
        archive = ROOT / freeze["archive"]
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall(target, filter="data")
            extracted = target / "effective-stark-results-companion-v14"
            completed = subprocess.run(
                [
                    "python3",
                    str(
                        extracted
                        / "projects/effective-stark-sweep/scripts/"
                        "verify_results_companion_v14.py"
                    ),
                    str(extracted),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_COMPANION_V14=VERIFIED", completed.stdout)


if __name__ == "__main__":
    unittest.main()

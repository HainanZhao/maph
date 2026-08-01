import hashlib
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "discovery/run_g1_exact_structural_atlas_v1.py"
ARTIFACT = PROJECT / "artifacts/cycle-3-g1-exact-structural-atlas-v1.json"
PREREGISTRATION = PROJECT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"


def f(value: str) -> Fraction:
    numerator, denominator = value.split("/", maxsplit=1)
    return Fraction(int(numerator), int(denominator))


def pairwise(values: dict[str, Fraction]) -> dict[str, str]:
    names = list(values)
    return {
        f"{left}-{right}": f"{(values[left] - values[right]).numerator}/{(values[left] - values[right]).denominator}"
        for index, left in enumerate(names)
        for right in names[index + 1:]
    }


def equality_groups(values: dict[str, Fraction]) -> list[list[str]]:
    groups = []
    seen = set()
    for value in values.values():
        if value in seen:
            continue
        seen.add(value)
        group = [name for name, candidate in values.items() if candidate == value]
        if len(group) > 1:
            groups.append(group)
    return groups


class G1ExactStructuralAtlasV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text())
        cls.preregistration = json.loads(PREREGISTRATION.read_text())

    def test_replay_and_no_complex_evaluation(self) -> None:
        completed = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(completed.stdout)["finite_complex_probes_evaluated"], 0)
        self.assertEqual(self.data["scope"]["screen_rows_evaluated"], 0)

    def test_all_local_rows_exactly_recompute_and_obey_energy_firewall(self) -> None:
        rows = self.data["local_rows"]
        self.assertEqual(len(rows), 7744)
        self.assertEqual(len({row["id"] for row in rows}), 7744)
        eligible = 0
        for row in rows:
            s, n, v, w = (f(row[key]) for key in ("s", "n", "v", "w"))
            expected_a = {"A1": 2 * n * (1 - v), "A2": n * (Fraction(18, 5) - 4 * v), "A3": 1 + n * (Fraction(12, 5) - 4 * v)}
            expected_c = {"C1": 2 * n * (1 - v), "C2": 1 + n * (1 - 2 * v), "C3": 1 + n * (4 - 6 * v)}
            self.assertEqual({key: f(value) for key, value in row["large_values"]["terms"].items()}, expected_a)
            self.assertEqual({key: f(value) for key, value in row["classical"]["terms"].items()}, expected_c)
            self.assertEqual(row["large_values"]["pairwise_signed_residuals"], pairwise(expected_a))
            self.assertEqual(row["large_values"]["max_tie_set"], [key for key, value in expected_a.items() if value == max(expected_a.values())])
            self.assertEqual(row["large_values"]["tie_groups"], equality_groups(expected_a))
            self.assertEqual(row["classical"]["pairwise_signed_residuals"], pairwise(expected_c))
            self.assertEqual(row["classical"]["tie_groups"], equality_groups(expected_c))
            all_terms = {**expected_a, **expected_c}
            self.assertEqual(row["all_formula_pairwise_signed_residuals"], pairwise(all_terms))
            self.assertEqual(row["all_formula_tie_groups"], equality_groups(all_terms))
            c = max(expected_c["C1"], min(expected_c["C2"], expected_c["C3"]))
            self.assertEqual(f(row["Delta_LV"]), c - max(expected_a.values()))
            if v == s:
                eligible += 1
                self.assertIn("energy", row)
                expected_e = {"E1": w + n * (4 - 4 * s), "E2": Fraction(21, 8) * w + Fraction(1, 4) + n * (1 - 2 * s), "E3": 3 * w + n * (1 - 2 * s)}
                self.assertEqual({key: f(value) for key, value in row["energy"]["terms"].items()}, expected_e)
                self.assertEqual(row["energy"]["pairwise_signed_residuals"], pairwise(expected_e))
                self.assertEqual(row["energy"]["tie_groups"], equality_groups(expected_e))
            else:
                self.assertNotIn("energy", row)
        self.assertEqual(eligible, 704)
        self.assertEqual(self.data["counts"]["local_energy_eligible"], eligible)

    def test_anchors_ties_and_every_preregistered_transfer_row(self) -> None:
        local = self.data["mandatory_anchors"]["local"]
        self.assertEqual(local["energy"]["terms"], {"E1": "5/3", "E2": "5/3", "E3": "5/3"})
        self.assertEqual(local["energy"]["max_tie_set"], ["E1", "E2", "E3"])
        transfers = self.data["transfer_rows"]
        self.assertEqual(len(transfers), 560)
        self.assertEqual(len({row["id"] for row in transfers}), 560)
        frozen_keys = ("s", "n0", "k", "q", "ell", "u", "alpha", "provenance", "branch")
        self.assertEqual([{key: row[key] for key in frozen_keys} for row in transfers], [{key: row[key] for key in frozen_keys} for row in self.preregistration["transfer_rows"]])
        self.assertEqual(self.data["mandatory_anchors"]["transfer"]["B"], "9/13")
        for row in transfers:
            s, value = f(row["s"]), f(row["q"])
            b = f(row["B"])
            if row["branch"] == "q<=alpha":
                expected = {"LV1": 2 * value * (1 - s), "LV2": value * (Fraction(18, 5) - 4 * s), "LV3": 1 + value * (Fraction(12, 5) - 4 * s)}
            else:
                expected = {"MVT1": 2 * value * (1 - s), "MVT2": 1 + value * (1 - 2 * s)}
            self.assertEqual({key: f(term) for key, term in row["source_term_exponents"].items()}, expected)
            self.assertEqual(row["source_term_pairwise_signed_residuals"], pairwise(expected))
            self.assertEqual(row["source_term_tie_groups"], equality_groups(expected))
            self.assertEqual({key: f(residual) for key, residual in row["B_minus_source_term"].items()}, {key: b - term for key, term in expected.items()})
            self.assertTrue(all(f(residual) >= 0 for residual in row["B_minus_source_term"].values()))
            self.assertTrue(all(f(value) <= b for value in row["source_term_exponents"].values()))
            self.assertEqual(row["feasibility"], {"n0_strictly_above_1_100": True, "k_in_1_to_77": True, "q_at_least_ell": True, "q_at_most_u_exact": True})

    def test_frozen_preregistration_identity_and_optimized_mode_fail_closed(self) -> None:
        self.assertEqual(self.data["frozen_inputs"]["preregistration"]["sha256"], hashlib.sha256(PREREGISTRATION.read_bytes()).hexdigest())
        completed = subprocess.run([sys.executable, "-O", str(SCRIPT), "--check"], cwd=PROJECT, capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("forbids -O/-OO", completed.stderr)

    def test_separate_observed_performance_record_targets_exact_artifact(self) -> None:
        performance = json.loads((PROJECT / "artifacts/cycle-3-g1-exact-structural-atlas-v1-performance.json").read_text())
        self.assertEqual(performance["epistemic_status"], "OBSERVED")
        self.assertEqual(performance["atlas_artifact"]["sha256"], hashlib.sha256(ARTIFACT.read_bytes()).hexdigest())
        self.assertEqual(performance["workload"], self.data["scope"])


if __name__ == "__main__":
    unittest.main()

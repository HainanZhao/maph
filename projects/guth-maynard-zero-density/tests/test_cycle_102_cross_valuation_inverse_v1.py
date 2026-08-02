import unittest
from fractions import Fraction
from math import gcd

from conventions.critical_fiber_atlas_v1 import FiberAtlas
from conventions.cross_valuation_inverse_v1 import (
    ExceptionalAtom,
    concentration_record,
    extract_cross_core,
    full_prime_powers,
    prime_power_count,
    theorem_record,
)


class CrossValuationInverseTests(unittest.TestCase):
    def test_exact_core_exhaustive(self) -> None:
        for W in range(2, 19):
            for N in range(1, 19):
                for R in range(1, 19):
                    if gcd(N, R) != 1:
                        continue
                    atlas = FiberAtlas(w=W, N=N, R=R, Q=30)
                    for s in range(1, W):
                        original = atlas.split(s)
                        core = extract_cross_core(
                            w=W, N=N, R=R, Q=30, s=s, payload=(W, N, R, s)
                        )
                        self.assertEqual(core.base_B, original["base_B"])
                        self.assertEqual(core.base_C, original["base_C"])
                        self.assertEqual(core.lambda_max, original["lambda_max"])
                        self.assertEqual(core.payload, (W, N, R, s))

    def test_full_prime_powers(self) -> None:
        self.assertEqual(full_prime_powers(1), ())
        self.assertEqual(set(full_prime_powers(2**4 * 3**2 * 5)), {16, 9, 5})
        self.assertEqual(prime_power_count(10), 7)  # 2,3,4,5,7,8,9

    def test_valuation_exclusions(self) -> None:
        core = extract_cross_core(w=17, N=15, R=14, Q=100, s=6)
        self.assertEqual((core.x, core.y), (2, 1))
        for _, power in core.colours:
            self.assertEqual(core.s1 % power, 0)
            self.assertEqual(core.R % power, 0)
            self.assertNotEqual(core.t1 % power, 0)
            self.assertNotEqual(core.N % power, 0)

    def test_weighted_concentration_and_payload_retention(self) -> None:
        payloads = [object() for _ in range(5)]
        atoms = [
            ExceptionalAtom(w=2 + j, x=2, y=1, weight=Fraction(3, 2), payload=payloads[j])
            for j in range(4)
        ]
        atoms.append(ExceptionalAtom(w=20, x=1, y=3, weight=1, payload=payloads[4]))
        plain = concentration_record(atoms, M=10, refined=False)
        refined = concentration_record(atoms, M=10, refined=True)
        self.assertEqual(plain["selected_colour"], ("R", 2))
        self.assertEqual(plain["support"], 4)
        self.assertTrue(all(item in plain["selected_payloads"] for item in payloads[:4]))
        self.assertGreaterEqual(Fraction(plain["support"]), plain["guaranteed_support"])
        self.assertGreaterEqual(Fraction(refined["support"]), refined["guaranteed_support"])

    def test_per_w_mass_not_atom_count(self) -> None:
        atoms = [
            ExceptionalAtom(w=7, x=2, y=1, weight=4),
            ExceptionalAtom(w=7, x=3, y=1, weight=5),
            ExceptionalAtom(w=8, x=2, y=1, weight=1),
        ]
        record = concentration_record(atoms, M=5, refined=False)
        self.assertEqual(record["per_w_cap"], 9)

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("E/(2*P(2M)*A)", record["unrefined_concentration"])
        self.assertIn("per-w cap A", record["boundary"])
        self.assertIn("common anchor", record["boundary"])


if __name__ == "__main__":
    unittest.main()

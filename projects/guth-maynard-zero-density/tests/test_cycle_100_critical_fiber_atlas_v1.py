import math
import unittest

from conventions.critical_fiber_atlas_v1 import FiberAtlas, divisor_count, theorem_record


class CriticalFiberAtlasTests(unittest.TestCase):
    def test_exact_enumeration_against_bruteforce(self) -> None:
        for W in range(2, 13):
            for N in range(1, 8):
                for R in range(1, 8):
                    if math.gcd(N, R) != 1:
                        continue
                    atlas = FiberAtlas(W, N, R, 9)
                    generated = set(atlas.enumerate_solutions())
                    brute = {
                        (s, W - s, B, C)
                        for s in range(1, W)
                        for B in range(1, 10)
                        for C in range(1, 10)
                        if C * (W - s) * R == B * s * N
                    }
                    self.assertEqual(generated, brute)
                    self.assertEqual(atlas.exact_fiber_count(), len(brute))

    def test_gcd_factorization_exhaustive(self) -> None:
        for W in range(2, 30):
            for N in range(1, 15):
                for R in range(1, 15):
                    if math.gcd(N, R) != 1:
                        continue
                    atlas = FiberAtlas(-W, N, R, 20)
                    for s in range(1, W):
                        row = atlas.split(s)
                        self.assertEqual(
                            row["total_gcd"],
                            row["g0"] * row["cross_R"] * row["cross_N"],
                        )

    def test_generic_bound(self) -> None:
        for W in range(2, 40):
            atlas = FiberAtlas(W, 5, 7, 30)
            self.assertLessEqual(atlas.generic_fiber_count(), atlas.generic_bound() + 1e-12)

    def test_cross_valuation_web(self) -> None:
        atlas = FiberAtlas(12, 5, 7, 50)
        exceptional = [atlas.split(s) for s in range(1, 12) if not atlas.split(s)["generic"]]
        self.assertTrue(exceptional)
        self.assertTrue(
            any(row["cross_R_prime_powers"] or row["cross_N_prime_powers"] for row in exceptional)
        )

    def test_divisor_count_and_boundary(self) -> None:
        self.assertEqual(divisor_count(12), 6)
        record = theorem_record()
        self.assertIn("no Mobius sign", record["sign_boundary"])
        self.assertIn("no bound", record["boundary"])


if __name__ == "__main__":
    unittest.main()

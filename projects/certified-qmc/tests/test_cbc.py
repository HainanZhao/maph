from __future__ import annotations

from fractions import Fraction
import unittest

from src.cbc import exact_cbc, unit_candidates
from src.exact_error import exact_squared_error


class ExactCbcTests(unittest.TestCase):
    def test_candidate_set_quotients_forced_sign_ties(self):
        full = unit_candidates(16, quotient_sign=False)
        quotient = unit_candidates(16, quotient_sign=True)
        self.assertEqual(full, [1, 3, 5, 7, 9, 11, 13, 15])
        self.assertEqual(quotient, [1, 3, 5, 7])

    def test_exact_cbc_decisions_are_global_argmins_per_stage(self):
        weights = [1, Fraction(1, 2), Fraction(1, 3)]
        result = exact_cbc(17, weights)
        self.assertEqual(result["generator"], [1, 5, 3])
        prefix = [1]
        candidates = unit_candidates(17)
        for dimension, winner in enumerate(
            result["generator"][1:],
            start=2,
        ):
            scores = {
                candidate: exact_squared_error(
                    17,
                    prefix + [candidate],
                    weights[:dimension],
                )
                for candidate in candidates
            }
            self.assertEqual(scores[winner], min(scores.values()))
            prefix.append(winner)

    def test_oracle_does_not_claim_production_scale(self):
        result = exact_cbc(13, [1, Fraction(1, 2)])
        self.assertFalse(result["production_scale_claimed"])
        self.assertEqual(result["tag"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()

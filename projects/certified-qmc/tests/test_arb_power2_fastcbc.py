from __future__ import annotations

from fractions import Fraction
import unittest

from flint import arb, ctx

from src.arb_power2_fastcbc import (
    arb_plus_correlation,
    arb_power2_candidate_scores,
    initial_running_product,
    update_running_product,
)
from src.shadow_decision import candidate_score_fraction


class ArbPowerTwoFastCbcTests(unittest.TestCase):
    def test_compiled_arb_correlation_contains_direct_values(self):
        with ctx.workprec(106):
            left = [arb(value) for value in (2, 3, 5, 7)]
            right = [arb(value) for value in (11, 13, 17, 19)]
            observed = arb_plus_correlation(left, right)
        expected = [
            sum(
                (2, 3, 5, 7)[index]
                * (11, 13, 17, 19)[(index + shift) % 4]
                for index in range(4)
            )
            for shift in range(4)
        ]
        self.assertTrue(
            all(ball.contains(value) for ball, value in zip(observed, expected))
        )

    def test_candidate_balls_contain_exact_direct_scores(self):
        modulus = 32
        prefix = [1, 7, 11]
        weights = [Fraction(1, index * index) for index in range(1, 5)]
        with ctx.workprec(106):
            state = initial_running_product(modulus)
            for component, weight in zip(prefix, weights[:-1]):
                state = update_running_product(
                    state, component, weight
                )
            candidates, scores = arb_power2_candidate_scores(
                modulus, state, weights[-1], precision=106
            )
        with ctx.workprec(106):
            for candidate, score in zip(candidates, scores):
                exact = candidate_score_fraction(
                    modulus, prefix, weights, candidate
                )
                target = arb(exact.numerator) / exact.denominator
                self.assertTrue(
                    score.contains(target),
                    (
                        f"candidate={candidate}, score={score}, "
                        f"target={target}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()

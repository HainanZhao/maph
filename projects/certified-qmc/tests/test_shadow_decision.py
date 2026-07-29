from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import random
import unittest

from src.shadow_decision import (
    DoubleDoubleBall,
    candidate_score_arb,
    candidate_score_dd_ball,
    candidate_score_fraction,
    compare_candidate_scores,
)


HAS_FLINT = importlib.util.find_spec("flint") is not None
PROJECT = Path(__file__).resolve().parents[1]


class DoubleDoubleBallTests(unittest.TestCase):
    def test_ball_operations_contain_exact_results(self):
        source = random.Random(20260804)
        for _ in range(100):
            left = Fraction(
                source.randint(-1000, 1000), source.randint(1, 1000)
            )
            right = Fraction(
                source.randint(-1000, 1000), source.randint(1, 1000)
            )
            left_ball = DoubleDoubleBall.exact(left)
            right_ball = DoubleDoubleBall.exact(right)
            self.assertTrue(left_ball.add(right_ball).contains(left + right))
            self.assertTrue(
                left_ball.multiply(right_ball).contains(left * right)
            )

    def test_candidate_score_ball_contains_exact_oracle(self):
        source = random.Random(20260805)
        for _ in range(20):
            modulus = source.choice((8, 16, 32))
            prefix = [1, source.randrange(1, modulus) | 1]
            weights = [
                Fraction(source.randint(0, 5), source.randint(1, 9))
                for _ in range(3)
            ]
            candidate = source.randrange(1, modulus) | 1
            exact = candidate_score_fraction(
                modulus, prefix, weights, candidate
            )
            ball = candidate_score_dd_ball(
                modulus, prefix, weights, candidate
            )
            self.assertTrue(ball.contains(exact))


@unittest.skipUnless(HAS_FLINT, "python-flint required")
class ArbDecisionTests(unittest.TestCase):
    def test_arb128_contains_higher_precision_exact_replay(self):
        import flint

        modulus = 32
        prefix = [1, 7]
        weights = [Fraction(1, j * j) for j in range(1, 4)]
        for candidate in (1, 5, 9, 13):
            low_precision = candidate_score_arb(
                modulus, prefix, weights, candidate, precision=128
            )
            high_precision = candidate_score_arb(
                modulus, prefix, weights, candidate, precision=256
            )
            with flint.ctx.workprec(256):
                self.assertTrue(low_precision.contains(high_precision))

    def test_separated_comparison_agrees_with_exact(self):
        result = compare_candidate_scores(
            32,
            [1, 7],
            [Fraction(1), Fraction(1, 4), Fraction(1, 9)],
            1,
            5,
        )
        left = candidate_score_fraction(
            32, [1, 7], [1, Fraction(1, 4), Fraction(1, 9)], 1
        )
        right = candidate_score_fraction(
            32, [1, 7], [1, Fraction(1, 4), Fraction(1, 9)], 5
        )
        self.assertEqual(
            result["comparison"], (left > right) - (left < right)
        )

    def test_forced_sign_tie_reaches_exact_layer(self):
        result = compare_candidate_scores(
            32,
            [1, 7],
            [Fraction(1), Fraction(1, 4), Fraction(1, 9)],
            5,
            27,
        )
        self.assertEqual(result["resolved_by"], "exact-crt-reference")
        self.assertTrue(result["exact_equality"])

    def test_near_overlap_escalates_from_dd_and_separates_in_arb(self):
        result = compare_candidate_scores(
            32,
            [1, 7],
            [Fraction(1), Fraction(1, 4), Fraction(1, 10**29)],
            1,
            5,
        )
        self.assertEqual(result["comparison"], 1)
        self.assertEqual(result["resolved_by"], "arb")

    def test_preflight_artifact_replays(self):
        artifact = json.loads(
            (
                PROJECT
                / "certificates"
                / "cycle-009-shadow-decision-preflight.json"
            ).read_text()
        )
        self.assertFalse(artifact["target_run_started"])
        for row in artifact["cases"]:
            weights = [
                Fraction(
                    int(weight["numerator"]),
                    int(weight["denominator"]),
                )
                for weight in row["weights"]
            ]
            result = compare_candidate_scores(
                int(row["modulus"]),
                [int(value) for value in row["prefix"]],
                weights,
                int(row["left"]),
                int(row["right"]),
                arb_precision=int(artifact["arb_precision_bits"]),
            )
            self.assertEqual(result, row["result"])

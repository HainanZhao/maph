from __future__ import annotations

from fractions import Fraction
from math import gcd
import random
import unittest

from src.ntt_prime import generate_ntt_prime_schedule
from src.power2_fastcbc import (
    direct_power2_candidate_scores,
    power2_candidate_classes,
    power2_strata,
    stratified_ntt_candidate_scores,
)


class PowerTwoFastCbcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        record = generate_ntt_prime_schedule(1)[0]
        cls.prime = int(record["prime"])
        cls.root = int(record["primitive_root"])

    def test_powers_of_five_represent_unit_sign_classes(self):
        for modulus in (8, 16, 32, 128, 1024):
            representatives = power2_candidate_classes(modulus)
            represented = {
                min(value, (-value) % modulus)
                for value in representatives
            }
            expected = {
                min(value, (-value) % modulus)
                for value in range(1, modulus)
                if gcd(value, modulus) == 1
            }
            self.assertEqual(represented, expected)
            self.assertEqual(len(representatives), modulus // 4)

    def test_strata_partition_every_nonzero_residue(self):
        for modulus in (8, 16, 64, 1024):
            represented = set()
            for row in power2_strata(modulus):
                valuation = int(row["valuation"])
                unit_modulus = int(row["unit_modulus"])
                scale = 2**valuation
                represented.update(
                    scale * odd for odd in range(1, unit_modulus, 2)
                )
            self.assertEqual(represented, set(range(1, modulus)))

    def check_scores(self, modulus, prefix, weights):
        direct_candidates, direct_scores = direct_power2_candidate_scores(
            modulus, prefix, weights, self.prime
        )
        fast_candidates, fast_scores = stratified_ntt_candidate_scores(
            modulus, prefix, weights, self.prime, self.root
        )
        self.assertEqual(fast_candidates, direct_candidates)
        self.assertEqual(fast_scores, direct_scores)

    def test_small_deterministic_cases(self):
        source = random.Random(20260802)
        for modulus in (8, 16, 32, 64, 128):
            for dimension in (2, 3, 5):
                prefix = [
                    source.randrange(1, modulus) | 1
                    for _ in range(dimension - 1)
                ]
                weights = [
                    Fraction(source.randint(0, 7), source.randint(1, 9))
                    for _ in range(dimension)
                ]
                self.check_scores(modulus, prefix, weights)

    def test_frozen_unsw_stage(self):
        prefix = [1, 275, 179, 319, 299, 451, 417, 167]
        weights = [Fraction(1, j * j) for j in range(1, 10)]
        self.check_scores(1024, prefix, weights)

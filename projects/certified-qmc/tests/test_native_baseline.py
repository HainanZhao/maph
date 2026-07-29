from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import random
import shutil
import unittest

from src.exact_error import RuleSpec
from src.modular_error import error_numerator_residue
from src.native_baseline import (
    build_native_baseline,
    native_error_numerator_residue,
)
from src.ntt_prime import generate_ntt_prime_schedule


@unittest.skipUnless(shutil.which("cc") and shutil.which("make"), "C compiler required")
class NativeBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary: Path = build_native_baseline()
        cls.primes = [
            int(item["prime"]) for item in generate_ntt_prime_schedule(2)
        ]

    def check_case(self, modulus, generator, weights):
        spec = RuleSpec.create(modulus, generator, weights)
        for prime in self.primes:
            self.assertEqual(
                native_error_numerator_residue(
                    modulus,
                    generator,
                    weights,
                    prime,
                    binary=self.binary,
                ),
                error_numerator_residue(spec, prime),
            )

    def test_frozen_unsw_prefixes(self):
        generator = [1, 275, 179, 319, 299, 451, 417, 167,
                     289, 109, 395, 81, 215, 115, 143, 361]
        for dimension in (2, 4, 8, 16):
            self.check_case(
                1024,
                generator[:dimension],
                [Fraction(1, j * j) for j in range(1, dimension + 1)],
            )

    def test_frozen_random_cases(self):
        source = random.Random(20260730)
        for _ in range(20):
            modulus = source.randint(3, 80)
            dimension = source.randint(1, 7)
            generator = [
                source.randrange(1, modulus) for _ in range(dimension)
            ]
            weights = [
                Fraction(source.randint(0, 7), source.randint(1, 11))
                for _ in range(dimension)
            ]
            self.check_case(modulus, generator, weights)

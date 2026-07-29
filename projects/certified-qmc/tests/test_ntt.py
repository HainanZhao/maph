from __future__ import annotations

import random
import unittest

from src.ntt import (
    direct_cyclic_convolution,
    ntt_cyclic_convolution,
    ntt_plus_correlation,
    radix2_ntt,
)
from src.ntt_prime import generate_ntt_prime_schedule


class RadixTwoNttTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        record = generate_ntt_prime_schedule(1)[0]
        cls.prime = int(record["prime"])
        cls.root = int(record["primitive_root"])

    def test_round_trip(self):
        source = random.Random(20260730)
        for length in (1, 2, 4, 8, 32, 256):
            values = [
                source.randrange(self.prime) for _ in range(length)
            ]
            transformed = radix2_ntt(
                values, self.prime, self.root
            )
            recovered = radix2_ntt(
                transformed, self.prime, self.root, inverse=True
            )
            self.assertEqual(recovered, values)

    def test_convolution_matches_quadratic_oracle(self):
        source = random.Random(20260731)
        for length in (1, 2, 4, 8, 16, 64):
            left = [source.randrange(self.prime) for _ in range(length)]
            right = [source.randrange(self.prime) for _ in range(length)]
            self.assertEqual(
                ntt_cyclic_convolution(
                    left, right, self.prime, self.root
                ),
                direct_cyclic_convolution(left, right, self.prime),
            )

    def test_plus_correlation_definition(self):
        source = random.Random(20260801)
        for length in (1, 2, 8, 32):
            left = [source.randrange(self.prime) for _ in range(length)]
            right = [source.randrange(self.prime) for _ in range(length)]
            expected = [
                sum(
                    left[t] * right[(t + shift) % length]
                    for t in range(length)
                ) % self.prime
                for shift in range(length)
            ]
            self.assertEqual(
                ntt_plus_correlation(
                    left, right, self.prime, self.root
                ),
                expected,
            )

    def test_invalid_transform_length_is_rejected(self):
        with self.assertRaises(ValueError):
            radix2_ntt([1, 2, 3], self.prime, self.root)

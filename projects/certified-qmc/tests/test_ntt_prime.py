from __future__ import annotations

import unittest

from src.ntt_prime import (
    audit_ntt_prime,
    factor_integer,
    generate_ntt_prime_schedule,
    is_prime_u64,
)


class NttPrimeAuditTests(unittest.TestCase):
    def test_deterministic_primality_examples(self):
        self.assertTrue(is_prime_u64(2))
        self.assertTrue(is_prime_u64(998244353))
        self.assertFalse(is_prime_u64(341550071728321))

    def test_reference_prime_and_root_are_verified(self):
        result = audit_ntt_prime(
            4611685941117976577,
            3,
            {2: 33, 311: 1, 1726273: 1},
        )
        self.assertEqual(result["tag"], "VERIFIED")
        self.assertEqual(result["two_adic_valuation"], 33)
        self.assertEqual(
            result["maximum_power_of_two_transform_length"],
            "8589934592",
        )

    def test_bad_factorization_is_rejected(self):
        with self.assertRaises(ValueError):
            audit_ntt_prime(
                4611685941117976577,
                3,
                {2: 32, 311: 1, 1726273: 1},
            )

    def test_factor_integer(self):
        self.assertEqual(factor_integer(1073741806), {2: 1, 311: 1, 1726273: 1})

    def test_schedule_is_deterministic_and_starts_with_reference(self):
        first_two = generate_ntt_prime_schedule(2)
        self.assertEqual(first_two[0]["prime"], "4611685941117976577")
        self.assertEqual(first_two[0]["primitive_root"], 3)
        self.assertEqual(first_two[1]["prime"], "4611685692009873409")
        self.assertGreaterEqual(first_two[1]["two_adic_valuation"], 32)


if __name__ == "__main__":
    unittest.main()

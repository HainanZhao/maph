import unittest
from math import lcm

from scripts.adversarial_certificate_search import scan_multiple
from src.erdos700 import (
    analyze_squarefree_triple,
    analyze_near_multiple,
    binomial_gcd_from_factors,
    binomial_valuation,
    eligible_2qr_witnesses,
    f,
    f_details,
    f_direct,
    f_squarefree_triple,
    factorize,
    find_near_multiple_witness,
    lucas_nonzero,
    lucas_first_failure,
    near_multiple_shifted_failure_depth,
    near_multiple_blind_second_digit_port,
    near_multiple_defect_port,
    near_multiple_lucas_residue_box,
    primary_pseudoperfect_candidates,
    reciprocal_defect,
    search_near_multiple_via_smallest_box,
)


class FactorizationTests(unittest.TestCase):
    def test_factorize(self):
        self.assertEqual(factorize(1), {})
        self.assertEqual(factorize(2), {2: 1})
        self.assertEqual(factorize(360), {2: 3, 3: 2, 5: 1})
        self.assertEqual(factorize(997), {997: 1})

    def test_reciprocal_defect(self):
        self.assertEqual(reciprocal_defect(30), -1)
        self.assertEqual(reciprocal_defect(1806), 1)
        self.assertEqual(reciprocal_defect(2088), 23)
        self.assertNotEqual(reciprocal_defect(36138), 0)

    def test_unbounded_prefix_construction_examples(self):
        for depth in (2, 4, 5, 10):
            exponent = 1
            while 5**exponent <= 6 ** (depth + 1):
                exponent += 1
            multiple = 6 * 5**exponent
            multiplier = 6**depth
            with self.subTest(depth=depth):
                self.assertLessEqual(multiplier, (multiple - 1) // 2)
                self.assertGreater(
                    near_multiple_shifted_failure_depth(
                        multiple, multiplier, 2
                    ),
                    depth,
                )
                self.assertGreater(
                    near_multiple_shifted_failure_depth(
                        multiple, multiplier, 3
                    ),
                    depth,
                )
                self.assertIsNone(
                    near_multiple_shifted_failure_depth(
                        multiple, multiplier, 5
                    )
                )

    def test_fixed_defect_double_log_prefix_blindness(self):
        for radical in (30, 42, 210):
            primes = tuple(factorize(radical))
            constant = lcm(*(p - 1 for p in primes))
            for depth in range(1, 7):
                exponent = constant * radical ** (depth - 1)
                with self.subTest(radical=radical, depth=depth):
                    self.assertGreaterEqual(exponent, depth)
                    for p in primes:
                        self.assertEqual(
                            pow(radical // p, exponent, p**depth),
                            1,
                        )

        self.assertEqual(reciprocal_defect(210), -37)
        for depth in range(3, 7):
            exponent = 210 ** (depth - 1)
            with self.subTest(radical=210, depth=depth, sharpened=True):
                for p in (2, 3, 5, 7):
                    self.assertEqual(
                        pow(210 // p, exponent, p**depth),
                        1,
                    )

    def test_least_synchronized_diagonal_exponent(self):
        for depth in range(5, 11):
            exponent = (
                2 ** (depth - 4)
                * 3 ** (depth - 2)
                * 5 ** (depth - 1)
            )
            with self.subTest(depth=depth):
                self.assertGreaterEqual(exponent, depth)
                self.assertEqual(pow(15, exponent, 2**depth), 1)
                self.assertEqual(pow(10, exponent, 3**depth), 1)
                self.assertEqual(pow(6, exponent, 5**depth), 1)
                self.assertNotEqual(pow(15, exponent // 2, 2**depth), 1)
                self.assertNotEqual(pow(10, exponent // 3, 3**depth), 1)
                self.assertNotEqual(pow(6, exponent // 5, 5**depth), 1)
                self.assertNotEqual(pow(6, exponent, 5 ** (depth + 1)), 1)

    def test_early_adversarial_stop_is_not_marked_complete(self):
        record = scan_multiple(
            26187,
            (3, 7, 29, 43),
            (1, 1, 1, 1),
            max_side_values=100_000,
            max_candidates_per_base=50_000,
        )
        self.assertEqual(record.pair_score, (2, 6))
        self.assertEqual(record.triple_score, 4)
        self.assertIn(29, record.processed_bases)
        self.assertNotIn(29, record.completed_bases)

    def test_deep_prime_predecessor_example(self):
        multiple = 63150
        multiplier = 5126
        self.assertEqual(factorize(multiple - 1), {63149: 1})
        self.assertEqual(reciprocal_defect(multiple), -451)
        self.assertEqual(
            {
                p: near_multiple_shifted_failure_depth(
                    multiple, multiplier, p
                )
                for p in factorize(multiple)
            },
            {2: 17, 3: 17, 5: None, 421: None},
        )

    def test_lucas_residue_box_counts(self):
        for multiple in (30, 42, 150):
            for p in factorize(multiple):
                with self.subTest(multiple=multiple, p=p):
                    box = near_multiple_lucas_residue_box(multiple, p)
                    direct_count = sum(
                        lucas_nonzero(box.shifted_upper, b, p)
                        for b in range(box.shifted_upper + 1)
                    )
                    self.assertEqual(box.allowed_residue_count, direct_count)
                    self.assertGreater(box.modulus, box.shifted_upper)

    def test_defect_port_matches_first_shifted_digit(self):
        for multiple in range(4, 250):
            factors = factorize(multiple)
            for p, exponent in factors.items():
                with self.subTest(multiple=multiple, p=p):
                    port = near_multiple_defect_port(multiple, p)
                    complement = multiple // (p**exponent)
                    shifted_upper = complement * (multiple - 1)
                    self.assertEqual(
                        port.upper_digit,
                        shifted_upper % p,
                    )
                    direct_allowed = tuple(
                        t
                        for t in range(p)
                        if (complement * t) % p
                        <= shifted_upper % p
                    )
                    self.assertEqual(
                        port.allowed_multiplier_residues,
                        direct_allowed,
                    )
                    self.assertEqual(
                        len(port.allowed_multiplier_residues),
                        port.upper_digit + 1,
                    )

    def test_blind_second_digit_port(self):
        checked = 0
        for multiple in range(4, 150):
            factors = factorize(multiple)
            for p, exponent in factors.items():
                complement = multiple // (p**exponent)
                if complement % p != 1:
                    continue
                checked += 1
                port = near_multiple_blind_second_digit_port(multiple, p)
                shifted_upper = complement * (multiple - 1)
                self.assertEqual(shifted_upper % p, p - 1)
                self.assertEqual(
                    (shifted_upper // p) % p,
                    port.upper_second_digit,
                )
                direct_count = 0
                for t in range(p**2):
                    lower = complement * t
                    if (
                        lower % p <= shifted_upper % p
                        and lower % (p**2) <= shifted_upper % (p**2)
                    ):
                        direct_count += 1
                self.assertEqual(
                    direct_count,
                    port.allowed_multiplier_residue_count,
                )
        self.assertGreater(checked, 0)

    def test_smallest_box_search_matches_exhaustive_analysis(self):
        for multiple in range(4, 100):
            if factorize(multiple - 1) != {multiple - 1: 1}:
                continue
            with self.subTest(multiple=multiple):
                box_search = search_near_multiple_via_smallest_box(multiple)
                exhaustive = analyze_near_multiple(multiple)
                self.assertTrue(box_search.complete)
                if multiple % 2 == 0:
                    self.assertEqual(
                        box_search.compatible_box_values,
                        2 * (box_search.candidate_multipliers_tested + 1),
                    )
                self.assertEqual(
                    box_search.witness_multipliers,
                    exhaustive.witness_multipliers,
                )

    def test_smallest_box_limit_is_reported(self):
        result = search_near_multiple_via_smallest_box(30, max_box_size=1)
        self.assertFalse(result.complete)
        self.assertEqual(result.compatible_box_values, 0)
        self.assertEqual(result.candidate_multipliers_tested, 0)

    def test_smallest_box_search_on_selected_prime_bases(self):
        expected = {
            (2, 3): (2,),
            (2, 5): (71,),
            (3, 5): (123,),
        }
        for primes, witnesses in expected.items():
            with self.subTest(primes=primes):
                result = search_near_multiple_via_smallest_box(
                    4500, required_primes=primes
                )
                self.assertTrue(result.complete)
                self.assertEqual(result.required_primes, primes)
                self.assertEqual(result.witness_multipliers, witnesses)

        full = search_near_multiple_via_smallest_box(4500)
        self.assertTrue(full.complete)
        self.assertEqual(full.required_primes, (2, 3, 5))
        self.assertEqual(full.witness_multipliers, ())

    def test_smallest_box_search_rejects_invalid_prime_selection(self):
        for primes in ((), (2, 2), (2, 7)):
            with self.subTest(primes=primes):
                with self.assertRaises(ValueError):
                    search_near_multiple_via_smallest_box(
                        30, required_primes=primes
                    )

    def test_direct_selected_base_witness_search(self):
        self.assertEqual(
            find_near_multiple_witness(4500, (2, 3), max_multiplier=100),
            2,
        )
        self.assertEqual(
            find_near_multiple_witness(4500, (2, 5), max_multiplier=100),
            71,
        )
        self.assertIsNone(
            find_near_multiple_witness(4500, (3, 5), max_multiplier=100)
        )
        self.assertEqual(
            find_near_multiple_witness(4500, (3, 5), max_multiplier=200),
            123,
        )
        self.assertIsNone(find_near_multiple_witness(30))


class ValuationTests(unittest.TestCase):
    def test_known_values(self):
        # C(10, 4) = 210 = 2 * 3 * 5 * 7.
        for p in (2, 3, 5, 7):
            self.assertEqual(binomial_valuation(10, 4, p), 1)

    def test_gcd_known_value(self):
        # gcd(12, C(12, 4)) = gcd(12, 495) = 3.
        self.assertEqual(binomial_gcd_from_factors(12, 4), 3)

    def test_lucas_matches_valuation(self):
        for n in range(1, 80):
            for k in range(n + 1):
                for p in (2, 3, 5, 7):
                    with self.subTest(n=n, k=k, p=p):
                        self.assertEqual(
                            lucas_nonzero(n, k, p),
                            binomial_valuation(n, k, p) == 0,
                        )
                        self.assertEqual(
                            lucas_first_failure(n, k, p) is None,
                            lucas_nonzero(n, k, p),
                        )


class FTests(unittest.TestCase):
    def test_primary_pseudoperfect_candidate_reduction(self):
        expected_counts = {6: 1, 42: 3, 1806: 7, 47058: 15}
        for multiple, expected_count in expected_counts.items():
            with self.subTest(multiple=multiple):
                candidates = primary_pseudoperfect_candidates(multiple)
                self.assertEqual(len(candidates), expected_count)
                n = multiple * (multiple - 1)
                passing_multipliers = []
                for t in range(1, (multiple - 1) // 2 + 1):
                    passes_all_primes = all(
                        lucas_nonzero(n, multiple * t, p)
                        for p in factorize(multiple)
                    )
                    if passes_all_primes:
                        self.assertIn(t, candidates)
                        passing_multipliers.append(t)
                self.assertEqual(passing_multipliers, [])

        self.assertEqual(primary_pseudoperfect_candidates(42), (6, 14, 20))

    def test_non_primary_pseudoperfect_rejected(self):
        with self.assertRaises(ValueError):
            primary_pseudoperfect_candidates(30)

    def test_one_prime_inheritance_is_killed_at_second_shifted_digit(self):
        for base in (2, 6, 42, 47058):
            multiple = base * (base + 1)
            candidates = primary_pseudoperfect_candidates(multiple)
            n = multiple * (multiple - 1)
            with self.subTest(base=base):
                self.assertTrue(candidates)
                self.assertTrue(
                    all(
                        lucas_first_failure(n, multiple * t, base + 1) == 2
                        for t in candidates
                    )
                )

    def test_optimized_equals_direct_through_250(self):
        for n in range(4, 251):
            with self.subTest(n=n):
                self.assertEqual(f_details(n), f_direct(n))

    def test_composite_prime_powers(self):
        for p in (2, 3, 5, 7, 11):
            for exponent in (2, 3, 4):
                with self.subTest(p=p, exponent=exponent):
                    self.assertEqual(f(p**exponent), p)

    def test_squarefree_products_of_two_primes(self):
        primes = (2, 3, 5, 7, 11, 13, 17, 19)
        for i, p in enumerate(primes):
            for q in primes[i + 1 :]:
                with self.subTest(p=p, q=q):
                    self.assertEqual(f(p * q), p)

    def test_fast_squarefree_triple_evaluator(self):
        primes = (2, 3, 5, 7, 11, 13, 17)
        for i, p in enumerate(primes):
            for j, q in enumerate(primes[i + 1 :], start=i + 1):
                for r in primes[j + 1 :]:
                    with self.subTest(p=p, q=q, r=r):
                        analysis = analyze_squarefree_triple(p, q, r)
                        n = p * q * r
                        self.assertEqual(analysis.value, f(n))
                        self.assertEqual(f_squarefree_triple(p, q, r), f(n))
                        for witness in analysis.witnesses:
                            self.assertEqual(
                                binomial_gcd_from_factors(n, witness.k),
                                witness.target,
                            )

    def test_specialized_2qr_witnesses(self):
        odd_primes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for i, q in enumerate(odd_primes):
            for r in odd_primes[i + 1 :]:
                if r >= 2 * q:
                    break
                with self.subTest(q=q, r=r):
                    general = analyze_squarefree_triple(2, q, r)
                    specialized = eligible_2qr_witnesses(q, r)
                    self.assertEqual(specialized, general.witnesses)
                    self.assertNotIn(2, {w.target for w in specialized})

    def test_conditional_binary_family_small_examples(self):
        for exponent in (2, 3, 5, 13):
            q = 2**exponent - 1
            r = 2 ** (exponent + 1) - 3
            with self.subTest(exponent=exponent):
                self.assertEqual(eligible_2qr_witnesses(q, r), ())
                self.assertEqual(f_squarefree_triple(2, q, r), 2 * q)

    def test_binary_family_with_composite_first_factor(self):
        # m=4: q=15 is composite but r=29 is prime.
        self.assertEqual(f(2 * 15 * 29), 30)

    def test_near_multiple_reduction_matches_general_computation(self):
        for multiple in range(4, 80):
            if factorize(multiple - 1) != {multiple - 1: 1}:
                continue
            with self.subTest(multiple=multiple):
                analysis = analyze_near_multiple(multiple)
                self.assertEqual(analysis.value, f(multiple * (multiple - 1)))
                for t in analysis.witness_multipliers:
                    self.assertEqual(
                        binomial_gcd_from_factors(
                            multiple * (multiple - 1), multiple * t
                        ),
                        multiple - 1,
                    )

    def test_base_p_family_examples(self):
        for p, exponent in ((2, 4), (3, 2), (5, 3), (11, 2)):
            q = p**exponent - 1
            multiple = p * q
            if factorize(multiple - 1) != {multiple - 1: 1}:
                continue
            with self.subTest(p=p, exponent=exponent):
                analysis = analyze_near_multiple(multiple)
                self.assertEqual(analysis.witness_multipliers, ())
                self.assertEqual(analysis.value, multiple)

    def test_affine_base_p_extension_counterexample(self):
        analysis = analyze_near_multiple(398)
        self.assertEqual(analysis.value, 397)
        self.assertIn(47, analysis.witness_multipliers)

    def test_initial_near_30_cases(self):
        checked = 0
        for multiple in range(30, 1000, 30):
            if factorize(multiple - 1) != {multiple - 1: 1}:
                continue
            checked += 1
            with self.subTest(multiple=multiple):
                self.assertEqual(analyze_near_multiple(multiple).value, multiple)
        self.assertGreater(checked, 0)

    def test_small_values(self):
        expected = {4: 2, 6: 2, 8: 2, 9: 3, 10: 2, 12: 3, 15: 3}
        for n, value in expected.items():
            with self.subTest(n=n):
                self.assertEqual(f(n), value)


if __name__ == "__main__":
    unittest.main()

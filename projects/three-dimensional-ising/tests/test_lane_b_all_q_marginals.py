import unittest

from proof.verify_lane_b_all_q_marginals import (
    _all_single_handle_walsh,
    _brute,
    _tt,
)


class AllQMarginalTests(unittest.TestCase):
    def test_exact_tt_and_marginals_on_synthetic_tensor(self):
        prime = 101
        genus = 3
        values = [(13 * index * index + 7 * index + 5) % prime for index in range(4 ** genus)]
        cores = _tt(values, genus, prime)
        weights = [[3 + 5 * i + 7 * state for state in range(4)] for i in range(genus)]
        self.assertEqual(
            _all_single_handle_walsh(cores, weights, prime),
            _brute(values, genus, weights, prime),
        )


if __name__ == "__main__":
    unittest.main()

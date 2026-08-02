import unittest
from fractions import Fraction

from conventions.powered_ray_compiler_v1 import (
    PoweredRayAtom,
    compile_powered_rays,
    exact_root_error_bound,
    max_power_under_height,
    theorem_record,
)


class PoweredRayCompilerTests(unittest.TestCase):
    def test_exact_root_error(self) -> None:
        a, b, d = Fraction(3, 2), Fraction(7, 5), 4
        error = abs(a**d - b**d)
        bound = exact_root_error_bound(a, b, d, error)
        self.assertLessEqual(abs(a - b), bound)

    def test_height_cap(self) -> None:
        self.assertEqual(max_power_under_height(3, 1000), 6)
        self.assertEqual(max_power_under_height(10, 999), 2)

    def test_repeated_and_sparse_exponents(self) -> None:
        payloads = [object(), object(), object()]
        atoms = [
            PoweredRayAtom(3, 2, d, 5, H=10**6, M=100, payload=payloads[index])
            for index, d in enumerate((2, 3, 5))
        ]
        record = compile_powered_rays(atoms)
        group = record["groups"][0]
        self.assertTrue(group["repeated"])
        self.assertFalse(group["complete_exponent_interval"])
        self.assertEqual(group["modes"], (10, 15, 25))
        self.assertEqual(group["labels"], tuple(Fraction(3, 2) ** d for d in (2, 3, 5)))
        self.assertEqual(group["payloads"], tuple(payloads))

    def test_singletons_remain_singletons(self) -> None:
        atoms = [
            PoweredRayAtom(2, 1, 2, 3, H=100, M=20),
            PoweredRayAtom(3, 2, 2, 3, H=100, M=20),
        ]
        record = compile_powered_rays(atoms)
        self.assertEqual(record["repeated_group_count"], 0)

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("w=h*d", record["powered_ray"])
        self.assertIn("missing exponents", record["boundary"])


if __name__ == "__main__":
    unittest.main()

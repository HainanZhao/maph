import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionFiveCharacterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = json.loads(
            (
                ROOT
                / "certificates/dimension-five-character-support.json"
            ).read_text()
        )

    def test_only_order_eight_characters_survive(self) -> None:
        self.assertEqual(self.audit["support_exponents"], [1, 3, 5, 7])
        self.assertEqual(self.audit["orders_on_support"], [8, 8, 8, 8])
        self.assertTrue(
            self.audit["all_supporting_characters_have_order_eight"]
        )

    def test_quadratic_character_is_annihilated(self) -> None:
        self.assertEqual(
            self.audit["unique_quadratic_character_exponent"], 4
        )
        self.assertEqual(
            self.audit["unique_quadratic_character_coefficient"], 0
        )
        self.assertFalse(
            self.audit["factors_through_quadratic_quotient"]
        )


if __name__ == "__main__":
    unittest.main()

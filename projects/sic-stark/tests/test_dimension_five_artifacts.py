import json
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


class DimensionFiveArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bridge = json.loads(
            (ROOT / "certificates/dimension-five-bridge.json").read_text()
        )

    def test_complete_characteristic_packet(self) -> None:
        records = self.bridge["records"]
        self.assertEqual(len(records), 25)
        self.assertEqual(
            sum("overlap" in record for record in records),
            24,
        )
        zero_record = records[0]
        self.assertEqual(zero_record["identity_weyl_coefficient"], "1")
        self.assertEqual(
            zero_record["reconstruction_table_entry"], "sqrt(6)"
        )
        self.assertTrue(
            self.bridge["all_24_nonexceptional_multipliers_match"]
        )

    def test_positive_lifts_and_multiplier_identity(self) -> None:
        beta_conjugate = 2 - 3**0.5
        for record in self.bridge["records"]:
            if "overlap" not in record:
                continue
            first, second = record["characteristic"]
            lifted_first, lifted_second = record["positive_kopp_lift"]
            self.assertEqual((lifted_first - first) % 5, 0)
            self.assertEqual(lifted_second, second)
            self.assertGreater(
                second * beta_conjugate - lifted_first, 0
            )
            self.assertEqual(
                parse_fraction(
                    record["theta_character_exponent_mod_1"]
                ),
                parse_fraction(record["expected_Q_over_5_mod_1"]),
            )
            self.assertEqual(
                parse_fraction(
                    record["kopp_multiplier_exponent_mod_1"]
                ),
                parse_fraction(
                    record["afk_phase_square_exponent_mod_1"]
                ),
            )

    def test_ray_class_and_sign_pairing(self) -> None:
        self.assertEqual(
            self.bridge["ray_generator"],
            "prime above 3",
        )
        for record in self.bridge["records"]:
            if "overlap" not in record:
                continue
            ray_log = record["ray_class_log_in_C8"]
            self.assertIn(ray_log, range(8))
            self.assertEqual(
                record["sign_class_partner_log"], (ray_log + 4) % 8
            )
            unsigned = record["overlap"].removeprefix("-")
            self.assertEqual(
                unsigned,
                self.bridge["ray_log_to_positive_square_root"][
                    str(ray_log)
                ],
            )
        records = {
            tuple(record["characteristic"]): record
            for record in self.bridge["records"]
        }
        self.assertEqual(
            [
                records[characteristic]["ray_class_log_in_C8"]
                for characteristic in (
                    (0, 1),
                    (0, 2),
                    (2, 4),
                    (3, 3),
                )
            ],
            [0, 6, 3, 1],
        )

    def test_reconstruction_table_is_derived_from_records(self) -> None:
        records = {
            tuple(record["characteristic"]): record
            for record in self.bridge["records"]
        }
        table = self.bridge["derived_reconstruction_table"]
        for first in range(5):
            for second in range(5):
                record = records[(first, second)]
                expected = record.get(
                    "overlap", record.get("reconstruction_table_entry")
                )
                self.assertEqual(table[first][second], expected)

    def test_sturm_transcript_is_complete(self) -> None:
        transcript = (
            ROOT / "certificates/dimension-five-root-isolation.txt"
        ).read_text()
        self.assertIn("TOTAL_REAL_ROOTS=16", transcript)
        self.assertEqual(transcript.count(" ROOT_COUNT=1"), 16)
        self.assertIn("ALL_REAL_ROOTS=", transcript)
        self.assertNotIn("POSITIVE_ROOTS=", transcript)

    def test_embedding_certificate_closes_factor_label_bridge(self) -> None:
        transcript = (
            ROOT
            / "certificates/dimension-five-embedding-certificate.txt"
        ).read_text()
        self.assertIn("W_NARROW_ROOT_COUNT=1", transcript)
        self.assertIn(
            "ALL_CONJUGATE_INTERVAL_LABELS_CERTIFIED=1", transcript
        )
        self.assertEqual(transcript.count(" CERTIFIED=1"), 8)
        self.assertIn("SQRT5_POSITIVE_EMBEDDING_CERTIFIED=1", transcript)
        self.assertIn("SQRT6_POSITIVE_EMBEDDING_CERTIFIED=1", transcript)
        self.assertIn("POSITIVE_FACTOR_COUNT=1", transcript)
        self.assertIn("POSITIVE_FACTOR_INDEX=4", transcript)

    def test_local_isolation_certificate(self) -> None:
        transcript = (
            ROOT
            / "certificates/dimension-five-local-isolation.txt"
        ).read_text()
        self.assertIn("ALL_FOUR_FAN_MINORS_ZERO=1", transcript)
        self.assertIn("FAN_JACOBIAN_DETERMINANT_ZERO=0", transcript)
        self.assertIn("LOCAL_POINT_REDUCED_AND_ISOLATED=1", transcript)

    def test_unconditional_stark_value_certificates(self) -> None:
        shintani = (
            ROOT / "certificates/dimension-five-shintani.txt"
        ).read_text()
        self.assertIn("Q_SQRT_MINUS_5_BNFCERTIFY=1", shintani)
        self.assertIn("BETA_MOD_5_ORDER=3", shintani)
        self.assertIn("NORM_MINUS_ONE_MOD_3_OBSTRUCTION=1", shintani)
        self.assertIn("MU_ONE_INFINITY_IMAGE=[0]~", shintani)
        self.assertIn("NU_ONE_INFINITY_IMAGE=[4]~", shintani)
        self.assertIn(
            "BASE_CONJUGATION_ACTION_ON_RAY_GENERATORS="
            "[[5, 0]~, [4, 1]~]",
            shintani,
        )
        self.assertIn(
            "SHINTANI_FIXED_RELATIVE_FIELD=x^2 + 5",
            shintani,
        )
        self.assertIn(
            "NORMAL_CLOSURE_IS_Q_SQRT_MINUS_5_RAY_SUBFIELD=1",
            shintani,
        )
        self.assertIn("STARK_FIELD_OCTIC_SUBFIELD_COUNT=1", shintani)
        self.assertIn(
            "UNIQUE_OCTIC_SUBFIELD_IS_Q_ZETA_60_PLUS=1",
            shintani,
        )
        self.assertIn("SHINTANI_SAFE_EXPONENT=5760", shintani)

        units = (
            ROOT / "certificates/dimension-five-unit-lattice.txt"
        ).read_text()
        self.assertIn("ABSOLUTE_BNFCERTIFY=1", units)
        self.assertIn(
            "ALL_CANDIDATE_RAY_ISOMORPHISMS_FIX_LABELED_K=1",
            units,
        )
        self.assertIn(
            "TRACE_INTERVAL_MINUS_2_2_ROOT_COUNTS_BY_BASE_EMBEDDING="
            "[8, 0]",
            units,
        )
        self.assertIn("STARK_UNIT_NARROW_INTERVAL_ROOT_COUNT=1", units)
        self.assertEqual(
            units.count("FROBENIUS_ORBIT_INTERVAL_"),
            8,
        )
        self.assertIn(
            "ALL_FROBENIUS_ORBIT_INTERVALS_CERTIFIED=1",
            units,
        )

        intervals = (
            ROOT
            / "certificates/dimension-five-double-sine-intervals.txt"
        ).read_text()
        self.assertEqual(intervals.count("CONTAINS_ZERO=True"), 4)
        self.assertIn("WEIL_HEIGHT_UPPER_BOUND=[+/- 1.24e-7]", intervals)
        self.assertIn("HEIGHT_GAP_CERTIFIED=True", intervals)


if __name__ == "__main__":
    unittest.main()

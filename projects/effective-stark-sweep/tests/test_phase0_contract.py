from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]


class PhaseZeroContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.range = json.loads(
            (ROOT / "data" / "range-v1.json").read_text()
        )
        self.anchors = json.loads(
            (ROOT / "data" / "anchor-battery-v1.json").read_text()
        )
        self.schema = json.loads(
            (ROOT / "data" / "corpus-record-schema-v1.json").read_text()
        )
        self.predicates = json.loads(
            (ROOT / "data" / "engine-predicates-v1.json").read_text()
        )
        self.literature = json.loads(
            (ROOT / "data" / "literature-perimeter-v1.json").read_text()
        )
        self.sequencing = json.loads(
            (ROOT / "data" / "sequencing-gate-v1.json").read_text()
        )
        self.activation = json.loads(
            (ROOT / "data" / "sequencing-gate-v2.json").read_text()
        )
        self.research_activation = json.loads(
            (ROOT / "data" / "research-activation-v3.json").read_text()
        )

    def test_frozen_field_count(self) -> None:
        squarefree = []
        for value in range(2, 201):
            prime = 2
            remaining = value
            is_squarefree = True
            while prime * prime <= remaining:
                if remaining % (prime * prime) == 0:
                    is_squarefree = False
                    break
                prime += 1
            if is_squarefree:
                squarefree.append(value)
        self.assertEqual(len(squarefree), 121)
        self.assertEqual(self.range["field_count"], len(squarefree))

    def test_seven_anchor_bundles_and_engine_partition(self) -> None:
        anchors = self.anchors["anchors"]
        self.assertEqual(self.anchors["expected_anchor_count"], 7)
        self.assertEqual(len(anchors), 7)
        self.assertEqual(
            {anchor["engine"] for anchor in anchors}, {"A", "B", "C"}
        )
        self.assertEqual(
            [anchor["engine"] for anchor in anchors].count("A"), 2
        )
        self.assertEqual(
            [anchor["engine"] for anchor in anchors].count("B"), 4
        )
        self.assertEqual(
            [anchor["engine"] for anchor in anchors].count("C"), 1
        )
        self.assertEqual(
            len({anchor["id"] for anchor in anchors}), len(anchors)
        )

    def test_source_tree_is_frozen(self) -> None:
        frozen_commit = self.anchors["source"]["sic_stark_commit"]
        actual = subprocess.run(
            [
                "git",
                "rev-parse",
                f"{frozen_commit}:projects/sic-stark",
            ],
            cwd=WORKSPACE,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(
            actual, self.anchors["source"]["sic_stark_tree"]
        )

    def test_final_schema_has_no_numerical_verdict(self) -> None:
        verdicts = self.schema["properties"]["verdict"]["enum"]
        tags = self.schema["properties"]["claim_tag"]["enum"]
        self.assertEqual(verdicts, ["PROVED", "FRONTIER"])
        self.assertEqual(tags, ["VERIFIED"])

    def test_proved_records_require_exactly_one_engine(self) -> None:
        all_of = self.schema["allOf"]
        proved_rule = all_of[0]["then"]
        frontier_rule = all_of[1]["then"]
        self.assertIn("proof_engine", proved_rule["required"])
        self.assertIn("obstruction", frontier_rule["required"])
        self.assertIn("obstruction", proved_rule["not"]["required"])

    def test_engine_predicate_sets_are_disjoint_and_named(self) -> None:
        predicate_sets = [
            set(self.predicates[f"engine_{engine}"]["predicates"])
            for engine in ("A", "B", "C")
        ]
        self.assertTrue(all(predicate_sets))
        self.assertFalse(predicate_sets[0] & predicate_sets[1])
        self.assertFalse(predicate_sets[0] & predicate_sets[2])
        self.assertFalse(predicate_sets[1] & predicate_sets[2])
        self.assertIn(
            "HALT_TWO_ROUTE_MISMATCH",
            self.predicates["engine_B"]["halt_conditions"],
        )

    def test_literature_perimeter_is_bounded_and_classified(self) -> None:
        sources = self.literature["sources"]
        self.assertEqual(len(sources), 11)
        self.assertEqual(len({source["id"] for source in sources}), 11)
        self.assertTrue(
            all(source["classification"] for source in sources)
        )
        self.assertIn(
            "Within this named perimeter",
            self.literature["claim_boundary"],
        )

    def test_external_sequence_gate_is_explicitly_closed(self) -> None:
        self.assertFalse(self.sequencing["activated"])
        self.assertIsNone(
            self.sequencing["prerequisites"]["paper_I"]["arxiv_id"]
        )
        self.assertIsNone(
            self.sequencing["prerequisites"]["paper_II"]["artifact_doi"]
        )
        self.assertIsNone(
            self.sequencing["prerequisites"]["kopp_correspondence"][
                "sent_at_utc"
            ]
        )

    def test_versioned_activation_preserves_unknown_identifiers(self) -> None:
        self.assertTrue(self.activation["activated"])
        self.assertEqual(
            self.activation["amends"], "data/sequencing-gate-v1.json"
        )
        for paper in ("paper_I", "paper_II"):
            self.assertIsNone(
                self.activation["prerequisites"][paper]["arxiv_id"]
            )
            self.assertIsNone(
                self.activation["prerequisites"][paper]["artifact_doi"]
            )

    def test_research_has_no_external_administrative_gate(self) -> None:
        self.assertTrue(self.research_activation["activated"])
        self.assertEqual(
            self.research_activation["verdict"],
            "RESEARCH_ACTIVE_NO_EXTERNAL_SEQUENCING_GATE",
        )
        self.assertTrue(
            all(
                value == "TRACKED_SEPARATELY_NOT_A_RESEARCH_GATE"
                for value in self.research_activation[
                    "administrative_metadata"
                ].values()
            )
        )

    def test_record_schema_accepts_proved_and_frontier_only(self) -> None:
        common = {
            "schema": "effective-stark-corpus-record-v1",
            "case_id": "D5-N1-I1",
            "field": {
                "squarefree_radicand": 5,
                "fundamental_discriminant": 5,
                "defining_polynomial": "x^2-x-1",
            },
            "modulus": {
                "finite_ideal_hnf": [[1, 0], [0, 1]],
                "finite_norm": 1,
                "real_place": 1,
            },
            "ray_data": {
                "one_place_invariants": [2],
                "two_place_invariants": [2, 2],
                "exponent": 2,
            },
            "fourier_support": {
                "character_orders": [2],
                "support_size": 1,
                "certificate": "certificate.txt",
            },
            "claim_tag": "VERIFIED",
            "evidence": {
                "files": ["certificate.txt"],
                "sha256": {"certificate.txt": "0" * 64},
            },
        }
        proved = {
            **common,
            "verdict": "PROVED",
            "proof_engine": "A",
            "packet": {"defining_polynomial": "x^2-3*x+1"},
        }
        frontier = {
            **common,
            "verdict": "FRONTIER",
            "obstruction": "INDEX_GT_2",
        }
        jsonschema.validate(proved, self.schema)
        jsonschema.validate(frontier, self.schema)
        invalid = {
            **proved,
            "obstruction": "INDEX_GT_2",
        }
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(invalid, self.schema)


if __name__ == "__main__":
    unittest.main()

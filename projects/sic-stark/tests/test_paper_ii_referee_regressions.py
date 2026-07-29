"""Regression locks for the Paper-II referee corrections."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "sic-stark-dimensions-seven-eight.tex"


class PaperIIRefereeRegressionTests(unittest.TestCase):
    def test_dimension_seven_scope_is_explicit(self) -> None:
        text = PAPER.read_text()
        self.assertIn(r"Q_{7,1}=\langle1,-4,2\rangle", text)
        self.assertIn(r"\operatorname{disc}Q_{7,1}=8", text)
        self.assertIn(r"Q_{7,2}=\langle1,-6,1\rangle", text)
        self.assertIn(r"\operatorname{disc}Q_{7,2}=32", text)
        self.assertIn(
            "For every admissible dimension-seven or dimension-eight "
            "tuple $t$",
            text,
        )
        self.assertIn("proved independently", text)
        self.assertNotIn("remains open", text)

    def test_dimension_seven_audit_artifacts_are_named(self) -> None:
        text = PAPER.read_text()
        self.assertIn("P(X)={}&X^{16}", text)
        self.assertIn("2,2,12", text)
        self.assertIn(r"\epsilon_{\log}\le 5.86\cdot10^{-11}", text)
        self.assertIn(
            "certificates/dimension-seven-shintani-divisors.txt",
            text,
        )
        self.assertIn(
            "certificates/dimension-seven-double-sine-intervals.txt",
            text,
        )
        self.assertIn("G(X)={}&X^{12}+4X^{11}", text)
        self.assertIn(
            r"\epsilon_{\log}\le2.30\cdot10^{-11}",
            text,
        )
        self.assertIn(
            r"\path{scripts/dimension_seven_maximal_exact_tcc.gp}",
            text,
        )

    def test_dimension_eight_hypotheses_and_provenance_are_named(
        self,
    ) -> None:
        text = PAPER.read_text()
        self.assertIn(
            r"\mathfrak m_M"
            "\n"
            r" =\mathfrak p_2^3\mathfrak p_3\mathfrak p_5",
            text,
        )
        self.assertIn(r"$|S_M|=4\ge3$", text)
        self.assertIn(r"$e=|\mu(E_b)|=2$", text)
        self.assertIn(
            r"\path{scripts/dimension_eight_cm_unit_lattice.gp}",
            text,
        )
        self.assertIn(r"Paper I~\cite{ZhaoI}", text)

    def test_reproducibility_section_is_complete(self) -> None:
        text = PAPER.read_text()
        self.assertIn("AMD EPYC 9354P", text)
        self.assertIn("wall time", text)
        self.assertIn("peak RSS", text)
        self.assertIn("Zenodo DOI", text)

    def test_display_tags_are_unique_and_consecutive(self) -> None:
        text = PAPER.read_text()
        tags = [int(value) for value in re.findall(r"\\tag\{(\d+)\}", text)]
        self.assertEqual(tags, list(range(1, 45)))
        references = [
            int(value)
            for value in re.findall(r"\\textup\{\((\d+)\)\}", text)
        ]
        self.assertTrue(all(value in tags for value in references))


if __name__ == "__main__":
    unittest.main()

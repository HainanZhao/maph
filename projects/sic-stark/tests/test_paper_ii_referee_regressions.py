"""Regression locks for the Paper-II referee corrections."""

from pathlib import Path
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
        self.assertIn("whose form has\ndiscriminant $32$", text)
        self.assertIn("makes no claim for\n$Q_{7,1}$", text)
        self.assertNotIn(
            "For every admissible tuple $t$ in dimension seven or eight",
            text,
        )

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


if __name__ == "__main__":
    unittest.main()

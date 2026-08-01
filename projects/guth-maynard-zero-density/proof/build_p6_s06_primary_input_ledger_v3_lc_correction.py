#!/usr/bin/env python3
"""Seal the narrow local multiplicity correction for P6 S06."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-s06-primary-input-ledger-v3-lc-correction.json"
DOC = ROOT / "docs/p6-s06-primary-input-ledger-v3-lc-correction.md"
V1 = ROOT / "artifacts/p6-s06-primary-input-ledger-v1.json"
V2 = ROOT / "artifacts/p6-s06-primary-input-ledger-v2-lpoly-correction.json"
TRANSFER = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
TZ_TEX = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1/LFZD_manuscript.tex"
TZ_TAR = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1.tar"
TZ_PDF = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1.pdf"
V1_HASH = "1fbb984c3536c45dedbba36992ef8498cccf21fb7d8e9cab7619b5d2cb14b59a"
V2_HASH = "a7846345724c5110bc37d14a1ad712182f80f8e56a42ce73309469589df5b3e0"
TRANSFER_HASH = "2edccf46d15229fb8b8ff2c9510d0912f73228da681577ca66d869a8d8acf0d7"
TZ_TEX_HASH = "e77007c73da81c239fa009f6fce8befbc72989a0fd28f2ec4ff6952ff098f8f2"
TZ_TAR_HASH = "082be65a8fc04b5795290e500e0b2d74dc7a818cb68cc5ddc02131012b178fa2"
TZ_PDF_HASH = "94ddf7864fe74d266cef42816c9621516079321c48069d848527e7d0067b866d"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict[str, object]:
    require(digest(TZ_TEX) == TZ_TEX_HASH, "pinned Thorner--Zaman TeX changed")
    require(digest(TZ_TAR) == TZ_TAR_HASH, "pinned Thorner--Zaman tar changed")
    require(digest(TZ_PDF) == TZ_PDF_HASH, "pinned Thorner--Zaman PDF changed")
    lines = TZ_TEX.read_text(encoding="utf-8").splitlines()
    require("assume that $\\chi$ is primitive" in lines[559], "primitive scope changed")
    require("$D_{\\chi} = D_K \\N\\kf_{\\chi}$" in lines[569], "conductor definition changed")
    require("\\xi(s, \\chi) = w(\\chi) \\xi(1-s, \\bar{\\chi})" in lines[581], "functional equation changed")
    require("The zeros of $\\xi(s,\\chi)$ are the" in lines[585], "completed-zero statement changed")
    require("second sum is over all zeros" in lines[620], "multiplicity convention changed")
    require("counted with multiplicity" in lines[620], "multiplicity phrase changed")
    require("Let $\\chi$ be a Hecke character" in lines[670], "circle lemma scope changed")
    require("$\\sigma > 1$ and $t \\in \\R$" in lines[670], "circle-center hypotheses changed")
    require("for $0 < r \\leq 1$" in lines[674], "circle-radius hypothesis changed")
    require("N_{\\chi}(2r; s_0)" in lines[687], "circle proof changed")
    require("\\sum_{\\rho}" in lines[689], "circle zero sum changed")
    require("Applying \\cref{ExplicitFormula}" in lines[691], "circle proof no longer invokes explicit formula")
    return {"tex": {"path": str(TZ_TEX.relative_to(ROOT)), "sha256": TZ_TEX_HASH}, "tar": {"path": str(TZ_TAR.relative_to(ROOT)), "sha256": TZ_TAR_HASH}, "pdf": {"path": str(TZ_PDF.relative_to(ROOT)), "sha256": TZ_PDF_HASH}, "locators": {"primitive_scope_and_functional_equation": "TeX 560--586", "multiplicity_logarithmic_derivative": "TeX 614--638", "circle_lemma_and_proof": "Lemma ZerosInCircle-Classical, TeX 670--700"}}


def geometry() -> dict[str, str]:
    epsilon, radius = Fraction(1, 20), Fraction(3, 4)
    maximum = (Fraction(1, 2) + epsilon) ** 2 + Fraction(1, 2) ** 2
    require(maximum < radius**2, "unit-strip rectangle does not fit in circle")
    return {"epsilon": "1/20", "radius": "3/4", "center": "1+1/20+i(u+1/2)", "rectangle": "1/2<=Re(rho)<=1 and u<=Im(rho)<=u+1", "max_distance_squared": f"{maximum.numerator}/{maximum.denominator}", "radius_squared": f"{(radius**2).numerator}/{(radius**2).denominator}", "strict_margin_squared": f"{(radius**2-maximum).numerator}/{(radius**2-maximum).denominator}"}


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    require(digest(V1) == V1_HASH, "immutable ledger-v1 changed")
    require(digest(V2) == V2_HASH, "immutable ledger-v2 changed")
    require(digest(TRANSFER) == TRANSFER_HASH, "primitive-to-all transfer changed")
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    require(v1["input_ledger"]["LOCAL_MULTIPLICITY_COUNT_LC"]["epistemic_status"] == "CONJECTURED", "v1 LC status changed")
    return {
        "artifact_id": "p6-s06-primary-input-ledger-v3-lc-correction", "epistemic_status": "OBSERVED",
        "claim_boundary": "Versioned correction of LOCAL_MULTIPLICITY_COUNT_LC only. It supplies the local multiplicity premise used by ledger-v1, but proves no fourth moment, CGL density estimate, zero-density estimate, or short-interval result.",
        "immutable_predecessors": {"ledger_v1": {"path": str(V1.relative_to(ROOT)), "sha256": V1_HASH}, "ledger_v2": {"path": str(V2.relative_to(ROOT)), "sha256": V2_HASH}, "primitive_to_all_transfer": {"path": str(TRANSFER.relative_to(ROOT)), "sha256": TRANSFER_HASH}},
        "source": source_checks(), "geometry": geometry(),
        "corrected_input": {
            "id": "LOCAL_MULTIPLICITY_COUNT_LC", "epistemic_status": "PROVED",
            "statement": "For every Dirichlet character chi modulo q, every real u, and every 1/2<=sigma<=1, the multiplicity-weighted count of zeros rho of L(s,chi) with sigma<=Re(rho)<=1 and u<=Im(rho)<u+1 is O(log(q(|u|+3))), with an absolute implied constant.",
            "primitive_upper_half": "For primitive chi* of conductor d, the exact rectangle in the geometry record lies in the radius-3/4 circle centered at 1+1/20+i(u+1/2). Thorner--Zaman's circle proof, with its logarithmic-derivative zero sum repeated by order, gives its multiplicity count O(log(d(|u|+3))).",
            "primitive_lower_half": "For a zero rho with 0<Re(rho)<1/2, the checked functional equation maps rho to 1-rho, a zero of L(s,conjugate(chi*)) of the same order, with real part >1/2 and ordinate -Im(rho). Apply the same upper-half circle bound in the reflected closed strip [-u-1,-u]. This handles negative u without a sign convention change.",
            "multiplicity_lift": "The displayed circle-lemma definition uses a cardinality sign. This correction does not assume an unstated convention: TeX 688--700 is rerun for the zero multiset. Each term is nonnegative, and the explicit logarithmic-derivative/Hadamard derivation at TeX 614--638 explicitly repeats zeros by multiplicity, so the identical displayed bound holds for the multiplicity-weighted circle count.",
            "imprimitive_transfer": "The pinned primitive-to-all transfer proves that the finite Euler quotient is nonvanishing in Re(s)>0. Thus an imprimitive chi modulo q and its primitive inducer chi* of conductor d|q have identical zero multisets there, including orders. Since log(d(|u|+3))<=log(q(|u|+3)), the primitive estimate gives the stated all-modulus estimate.",
            "endpoint_handling": "The target half-open strip is contained in the closed strip used for the circle. The reflected image of that closed strip is also closed, so no endpoint is lost; zeros on Re(rho)=1/2 are assigned to the upper half."},
        "dependency_effect": {"LOW_HEIGHT_MULTIPLICITY_COUNT": {"epistemic_status": "PROVED", "reason": "ledger-v1's proved LC-to-low-height reduction now has its sole named premise supplied by this correction"}, "FOURTH_MOMENT_H": {"epistemic_status": "CONJECTURED", "status": "OPEN_EXTERNAL_PRIMARY_THEOREM"}, "not_promoted": ["CGL-v2 zero-density theorem", "q1-sensitive intermediate formulae", "S06 as a whole", "any short-interval theorem"]},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)}, "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}, "hostile_audit": "DEFERRED_TO_PAPER_STAGE", "replay": "python3 proof/build_p6_s06_primary_input_ledger_v3_lc_correction.py --check"}


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = render(payload())
    if args.write:
        require(not OUT.exists(), "refusing to overwrite LC correction")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "LC correction artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

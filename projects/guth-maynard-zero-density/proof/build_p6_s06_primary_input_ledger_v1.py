#!/usr/bin/env python3
"""Seal the bounded P6 S06 source-ledger and low-height reduction."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-s06-primary-input-ledger-v1.json"
DOC = ROOT / "docs/p6-s06-primary-input-ledger-v1.md"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"
CGL_TEX = ROOT / "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2/Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
HSW_TAR = ROOT / "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar"
HSW_PDF = ROOT / "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.pdf"
MULTIPLICITY_TRANSFER = ROOT / "artifacts/p6-multiplicity-transfer-v1.json"
PRIMITIVE_TRANSFER = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
TAIL_CORRECTION = ROOT / "artifacts/p6-detector-qt-tail-v2-status-correction.json"

CGL_TAR_HASH = "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae"
CGL_TEX_HASH = "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f"
HSW_TAR_HASH = "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247"
HSW_PDF_HASH = "3fc4c89f49249924e61cb0d289d81559faed53fcbb838628ea32dc7ec6f89fbf"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict[str, object]:
    require(digest(CGL_TAR) == CGL_TAR_HASH, "frozen CGL tar changed")
    require(digest(CGL_TEX) == CGL_TEX_HASH, "frozen CGL TeX changed")
    require(digest(HSW_TAR) == HSW_TAR_HASH, "frozen HSW source gzip changed")
    require(digest(HSW_PDF) == HSW_PDF_HASH, "frozen HSW PDF changed")
    cgl = CGL_TEX.read_text(encoding="utf-8").splitlines()
    hsw = gzip.decompress(HSW_TAR.read_bytes()).decode("utf-8").splitlines()
    # Human TeX line n has Python index n-1.
    require("N(\\sigma, A\\log qT) \\ll (\\log qT)^{2}" in cgl[2137], "CGL low-height locator changed")
    require("N(\\sigma, T+ 1, \\chi) - N(\\sigma, T, \\chi) \\ll \\log qT" in cgl[2157], "CGL local-count locator changed")
    require("Theorem 10.3" in cgl[2168] and "MontgomeryBook" in cgl[2168], "CGL fourth-moment locator changed")
    require("(qT)^{1+\\epsilon}Y^{2-4\\sigma}" in cgl[2170], "CGL fourth-moment output changed")
    require("tails $|\\Im z| \\geq \\log^{2} T$" in cgl[2139], "CGL tail locator changed")
    require("for any divisor $q_1 \\mid q$" in cgl[121], "CGL q1 LVE locator changed")
    require("q_1^{\\frac{1}{3}}qT" in cgl[163], "CGL q1 density locator changed")
    require("where  $N(T)$ denotes the number of non-trivial zeros" in hsw[171], "HSW N(T) definition locator changed")
    require("For any $T\\ge e$, we have" in hsw[255], "HSW corollary range changed")
    require("0.1038  \\log T + 0.2573  \\log\\log T + 9.3675" in hsw[258], "HSW corollary bound changed")
    return {
        "cgl_v2": {
            "tar": {"path": str(CGL_TAR.relative_to(ROOT)), "sha256": CGL_TAR_HASH},
            "tex": {"path": str(CGL_TEX.relative_to(ROOT)), "sha256": CGL_TEX_HASH},
            "locators": {
                "tail_and_missing_growth_theorem": "TeX 2140",
                "principal_low_height_claim": "TeX 2137--2139",
                "local_count_and_well_spacing": "TeX 2154--2158",
                "fourth_moment_citation_and_output": "TeX 2169--2171",
                "q1_sensitive_large_values": "TeX 122--124",
                "q1_sensitive_density": "TeX 159--176",
            },
        },
        "hasanalizade_shen_wong_2022": {
            "source_gzip": {"path": str(HSW_TAR.relative_to(ROOT)), "sha256": HSW_TAR_HASH},
            "pdf": {"path": str(HSW_PDF.relative_to(ROOT)), "sha256": HSW_PDF_HASH},
            "locator": "Corollary 1.2, source TeX 255--261; definition TeX 188--195",
            "checked_statement": "For T>=e, an explicit Riemann--von Mangoldt estimate bounds N_zeta(T) by O(T log(T+3)).",
        },
    }


def dependency_checks() -> dict[str, object]:
    mult = json.loads(MULTIPLICITY_TRANSFER.read_text(encoding="utf-8"))
    primitive = json.loads(PRIMITIVE_TRANSFER.read_text(encoding="utf-8"))
    correction = json.loads(TAIL_CORRECTION.read_text(encoding="utf-8"))
    require(mult["external_unproved_input"]["id"] == "LOCAL_MULTIPLICITY_COUNT_LC", "LC identifier changed")
    require(primitive["epistemic_status"] == "PROVED", "primitive transfer status changed")
    require(correction["corrected_claim"]["epistemic_status"] == "PROVED", "tail correction status changed")
    require("LOW_HEIGHT_MULTIPLICITY_COUNT" in correction["corrected_claim"]["conditional_on"], "tail low-height premise changed")
    return {
        "multiplicity_transfer": {"path": str(MULTIPLICITY_TRANSFER.relative_to(ROOT)), "sha256": digest(MULTIPLICITY_TRANSFER)},
        "primitive_transfer": {"path": str(PRIMITIVE_TRANSFER.relative_to(ROOT)), "sha256": digest(PRIMITIVE_TRANSFER)},
        "tail_status_correction": {"path": str(TAIL_CORRECTION.relative_to(ROOT)), "sha256": digest(TAIL_CORRECTION)},
    }


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    return {
        "artifact_id": "p6-s06-primary-input-ledger-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Bounded primary-source ledger and conditional low-height reduction only. It proves no CGL theorem, density estimate, short-interval result, fourth moment, convexity bound, or multiplicity theorem.",
        "source_checks": source_checks(),
        "dependencies": dependency_checks(),
        "input_ledger": {
            "L_POLY_A": {
                "epistemic_status": "CONJECTURED",
                "status": "OPEN_EXTERNAL_PRIMARY_THEOREM",
                "needed_statement": "Uniformly for every relevant primitive Dirichlet character modulo q and real v, |L(1/2+iv,chi)| <= C [q(2+|v|)]^A for fixed C,A.",
                "disposition": "The frozen CGL source does not supply this exact all-modulus statement; do not substitute a remembered convexity theorem or a restricted-conductor result.",
            },
            "FOURTH_MOMENT_H": {
                "epistemic_status": "CONJECTURED",
                "status": "OPEN_EXTERNAL_PRIMARY_THEOREM",
                "needed_statement": "For selected pairs (gamma_r,chi_r) with |gamma_r|<=H and same-character spacing at least 1, sum_r |L(1/2+i gamma_r,chi_r)|^4 <<_delta (qH)^(1+delta), uniformly for the fixed modulus q and all relevant character labels.",
                "citation_boundary": "CGL cites Montgomery Theorem 10.3, but the theorem text and its exact hypotheses are not frozen locally. A continuous fourth moment is not silently upgraded to this discrete estimate.",
            },
            "LOCAL_MULTIPLICITY_COUNT_LC": {
                "epistemic_status": "CONJECTURED",
                "status": "OPEN_EXTERNAL_PRIMARY_THEOREM",
                "needed_statement": "For each relevant character and unit strip, the multiplicity-inclusive zero count is O(log(q(|u|+3))) with endpoints matching the application.",
                "citation_boundary": "CGL TeX 2158 has cardinalities and cites Davenport Chapter 16, but does not state multiplicity or exact endpoint/uniformity hypotheses.",
            },
            "LOW_HEIGHT_MULTIPLICITY_COUNT": {
                "epistemic_status": "PROVED",
                "conditional_on": ["LOCAL_MULTIPLICITY_COUNT_LC"],
                "statement": "For H0=A0 log(Q+3), the principal-character low-height zero contribution is O(log(Q+3)^2) with multiplicity.",
                "proof_route": "HSW Corollary 1.2 bounds the distinct zeta support by O(H0 log(H0+3)); LC bounds each multiplicity by O(log(H0+3)); the primitive-to-all Euler-factor lemma identifies the Re(s)>0 principal zeros with zeta zeros.",
                "scope": "Sufficient for a Q^o(1) detector loss; it does not prove LC or a CGL multiplicity convention.",
            },
        },
        "q1_sensitive_overlap": {
            "epistemic_status": "OBSERVED",
            "status": "RETAINED_UNREPAIRED",
            "source_locators": ["CGL TeX 122--124", "CGL TeX 159--176", "CGL TeX 454--504"],
            "reason": "The proved primitive-to-all transfer applies to monotone final conductor envelopes. It does not termwise transfer q1-sensitive intermediate expressions because q1|q need not survive as a divisor of the primitive conductor d, nor need the source case ranges persist.",
        },
        "gate_effect": {
            "epistemic_status": "OBSERVED",
            "result": "S06 remains open. LOW_HEIGHT_MULTIPLICITY_COUNT is reduced to LC plus the pinned HSW source; L_POLY_A, FOURTH_MOMENT_H, LC, and q1-sensitive obligations remain open.",
            "not_promoted": "No CGL-v2 7/3 estimate or downstream theorem is promoted.",
        },
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/build_p6_s06_primary_input_ledger_v1.py --check",
    }


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
        require(not OUT.exists(), "refusing to overwrite source-ledger artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "source-ledger artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

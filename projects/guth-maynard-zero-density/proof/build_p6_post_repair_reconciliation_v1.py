#!/usr/bin/env python3
"""Build the bounded post-repair reconciliation of the P6 registry."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-post-repair-reconciliation-v1.json"
DOC = ROOT / "docs/p6-post-repair-reconciliation-v1.md"

INPUTS = {
    "original_46_row_reconciliation": (ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json", "cf59aa63b97d69c672fafa0b0ca49221d9005c3da6ccd61f05d37f4bcbc68e49"),
    "primitive_to_all": (ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json", "2edccf46d15229fb8b8ff2c9510d0912f73228da681577ca66d869a8d8acf0d7"),
    "q1_reset": (ROOT / "artifacts/p6-conductor-q1-reset-v1.json", "b4c9a30bac20f8b59ecf7e8fdbcb060119d21e29376c3ce6c5ec0cd5335c8d4d"),
    "detector_tail_v1": (ROOT / "artifacts/p6-detector-qt-tail-v1.json", "c672dc559dbbd81b2b30f1a0c8e37354517e43af8da389b89a055504778a118d"),
    "detector_tail_v2_status": (ROOT / "artifacts/p6-detector-qt-tail-v2-status-correction.json", "5fef3abecd2f2def93693f2e2c849ac8585b6fe22fb930743df690b359fa34ec"),
    "multiplicity_transfer": (ROOT / "artifacts/p6-multiplicity-transfer-v1.json", "6466eabbd5b43bbc5ccd9937e9080bb8dab4ed77b27e4617b675e3546aa71772"),
    "tsmooth_v1": (ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v1.json", "5097609783b4e076b268255445e94caeb08bc23f93ad2540703c43e1401ca8af"),
    "tsmooth_v2_status": (ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v2-status-correction.json", "c8ee4e20a8e96a435e9e2031d5ed126372d8d2a2a9bb0edd4e8e7cf735ebf037"),
    "s06_v1": (ROOT / "artifacts/p6-s06-primary-input-ledger-v1.json", "1fbb984c3536c45dedbba36992ef8498cccf21fb7d8e9cab7619b5d2cb14b59a"),
    "s06_v2_lpoly": (ROOT / "artifacts/p6-s06-primary-input-ledger-v2-lpoly-correction.json", "a7846345724c5110bc37d14a1ad712182f80f8e56a42ce73309469589df5b3e0"),
    "s06_v3_lc": (ROOT / "artifacts/p6-s06-primary-input-ledger-v3-lc-correction.json", "8566226a67504c91fc2a19e98c7a74c1b805320b825852923b703fb5ce05fb49"),
    "s06_v4_fourth": (ROOT / "artifacts/p6-s06-primary-input-ledger-v4-fourth-moment-correction.json", "50330941b45a28e5d248162c5c22a1cb4a0ffe27290c9ae2fd7c6859230ed044"),
    "g0_zeta_route": (ROOT / "artifacts/g0-full-reconstruction-v3.json", "5a3ec153c843d0c89d9a987ad043cdf9513a171d581f98447a9c12930d26cc4f"),
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repaired_rows() -> dict[str, dict[str, object]]:
    source = {"epistemic_status": "OBSERVED", "classification": "SOURCE_TEXT_RECORDED_OR_UNAUDITED", "boundary": "The source row is preserved, but no new proof of its internal analytic argument is claimed."}
    external = {"epistemic_status": "CONJECTURED", "classification": "OPEN_EXTERNAL_OR_UNCHECKED_ANALYTIC_INPUT", "boundary": "No checked published/derived P6 input closes this row."}
    out: dict[str, dict[str, object]] = {key: dict(source) for key in ("S01", "S02", "S05", "L01", "L02", "L03", "L05", "L07", "L08", "L09", "L10", "L12", "M01", "M03", "M04", "M06", "M08", "Z01", "Z02", "Z09", "Z10", "F04", "F05", "F06", "F07")}
    for key in ("L04", "L06", "M05", "M07", "F01", "F02"):
        out[key] = dict(external)
    out.update({
        "S03": {"epistemic_status": "OBSERVED", "classification": "SOURCE_MULTIPLICITY_WORDING_REMAINS_A_GAP", "mathematical_repair": "PROVED: v3 supplies LC and the multiplicity-transfer artifact supplies the label-preserving consequence.", "boundary": "This does not rewrite CGL's cardinality language."},
        "S04": {"epistemic_status": "OBSERVED", "classification": "SOURCE_DOMAIN_WORDING_REMAINS_A_GAP", "mathematical_repair": "PROVED for the amended q>=2 detector: v1 tail plus v2 status and S06 v2--v4 inputs give qT-uniform transport for T>=1.", "boundary": "The original TeX is not certified as written."},
        "S06": {"epistemic_status": "CONJECTURED", "classification": "PARTIALLY_REPAIRED_EXTERNAL_INVENTORY", "mathematical_repair": "PROVED: L_POLY_A, LC, low height, and the q>=2 primitive fourth moment. Remaining L04/L06/M05/M07/F01/F02 inputs are open.", "boundary": "The inventory as a whole is not closed."},
        "L11": {"epistemic_status": "OBSERVED", "classification": "ROUTE_DISAGREEMENT_RETAINED", "boundary": "Route B's external-input concern was not independently resolved; no source-normalization claim is made."},
        "M02": {"epistemic_status": "OBSERVED", "classification": "ROUTE_DISAGREEMENT_RETAINED", "boundary": "The route-specific missing hypothesis is not repaired."},
        "Z03": {"epistemic_status": "PROVED", "classification": "AMENDED_QT_UNIFORM_DETECTOR_TAIL", "scope": "q positive, T>=1; applied to the primitive q>=2 detector after S06 v2--v4 supply its named inputs.", "boundary": "This is a repaired detector, not the CGL text as written."},
        "Z04": {"epistemic_status": "PROVED", "classification": "LOW_HEIGHT_REPAIR", "scope": "v1 reduction combined with v3 LC and the pinned primitive-to-all zero-multiset transfer.", "boundary": "No source wording is altered."},
        "Z05": {"epistemic_status": "PROVED", "classification": "PRIMITIVE_TO_ALL_ZERO_MULTISET_TRANSFER", "scope": "Re(s)>0, including multiplicities.", "boundary": "It does not establish a primitive density estimate."},
        "Z06": {"epistemic_status": "PROVED", "classification": "CONDUCTOR_PARTITION_AND_Q1_RESET", "scope": "Conditional only on a primitive monotone envelope re-run at each exact conductor d with q1'=d.", "boundary": "That primitive analytic envelope is still open; prescribed-q1 intermediate formulae are not justified."},
        "Z07": {"epistemic_status": "OBSERVED", "classification": "LC_REPAIRED_SELECTION_TEXT_REMAINS_UNAUDITED", "mathematical_repair": "PROVED: LC and multiplicity transfer remove the multiplicity factor once a saturated distinct-zero selection is available.", "boundary": "The CGL selection construction itself is not independently promoted."},
        "Z08": {"epistemic_status": "PROVED", "classification": "AMENDED_PRIMITIVE_CLASS_II_STEP", "scope": "q>=2, H>=1: v4 fourth moment plus v2 L_POLY_A, v3 LC/low-height, and amended qT tail.", "boundary": "No full CGL detector theorem is promoted; source class-II prose remains unrewritten."},
        "F03": {"epistemic_status": "CONJECTURED", "classification": "MIDDLE_RANGE_SOURCE_LEMMA_NOT_RECONSTRUCTED", "boundary": "Its repaired detector/conductor substeps do not supply the unverified primitive large-value and auxiliary-proposition chain."},
        "F08": {"epistemic_status": "PROVED", "classification": "CORRECTED_T_SMOOTH_BRANCH", "scope": "Under the amended definition every p|q has p<=T, and conditional on the stated primitive large-value/comparison inputs plus the repaired detector and transfer.", "boundary": "CGL does not define T-smooth; no original-source definition is inferred."},
        "F09": {"epistemic_status": "PROVED", "classification": "EXACT_ALGEBRA", "boundary": "This remains algebra only, not a density theorem."},
        "F10": {"epistemic_status": "PROVED", "classification": "CONDITIONAL_UNIFORM_ENVELOPE_ALGEBRA", "scope": "Conditional on the primitive two-term envelope and the repaired conductor reset, the 7/3 domination is exact.", "boundary": "The primitive envelope and outer Dirichlet comparison inputs are not closed, so no general 7/3 theorem is promoted."},
    })
    return out


def rows(original: dict[str, object]) -> list[dict[str, object]]:
    post = repaired_rows()
    raw = original["row_comparisons"]
    require(isinstance(raw, list) and len(raw) == 46, "original registry no longer has 46 rows")
    require(set(post) == {item["id"] for item in raw}, "post-repair map fails 46-row coverage")
    return [{"id": item["id"], "obligation": item["obligation"], "original_normalized_status": item["status_comparison"], "post_repair": post[item["id"]]} for item in raw]


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    for name, (path, expected) in INPUTS.items():
        require(digest(path) == expected, f"frozen input changed: {name}")
    original = json.loads(INPUTS["original_46_row_reconciliation"][0].read_text(encoding="utf-8"))
    table = rows(original)
    return {
        "artifact_id": "p6-post-repair-reconciliation-v1", "epistemic_status": "OBSERVED",
        "claim_boundary": "A bounded post-repair status reconciliation of the immutable 46-row CGL-v2 record. It reports repaired deductions and remaining boundaries; it neither edits CGL-v2 nor promotes a new density or short-interval theorem.",
        "frozen_inputs": {name: {"path": str(path.relative_to(ROOT)), "sha256": expected} for name, (path, expected) in INPUTS.items()},
        "original_registry": {"count": 46, "ids": original["canonical_registry"]["ids"], "artifact_sha256": INPUTS["original_46_row_reconciliation"][1]},
        "row_reconciliation": table,
        "proved_repairs": ["L_POLY_A for all Dirichlet characters", "LC local multiplicity count and derived LOW_HEIGHT_MULTIPLICITY_COUNT", "primitive-to-all zero multiset and conductor partition transfer", "q1 reset conditional on a primitive monotone envelope", "amended qT detector tail", "q>=2 primitive discrete FOURTH_MOMENT_H", "amended q>=2 primitive class-II step", "corrected T-smooth divisor chain and its stated conditional smooth branch", "F09 exact crossings"],
        "remaining_obligations": {"epistemic_status": "CONJECTURED", "external_or_unchecked": ["L04 low-value qT comparator", "L06 HMH comparator", "M05 approximate-functional-equation/S2 source input", "M07 Heath-Brown character-time energy input", "F01 Dirichlet Ingham analogue", "F02 Dirichlet Huxley analogue", "the primitive CGL-style large-value/two-term envelope required by F03/F10 and the q1 reset"], "source_text_gaps": ["CGL multiplicity wording", "CGL domain/tail wording", "saturated selection construction", "undefined T-smooth terminology", "q1-sensitive prescribed intermediate formulae"], "why_not_closed": "The new repairs do not prove the core primitive large-value and comparison theorem chain."},
        "general_7_over_3_envelope": {"epistemic_status": "CONJECTURED", "verdict": "NOT_PROMOTED", "proved_conditional_deduction": "If the primitive two-term envelope is established at every exact conductor d with the needed comparison ranges, then q1 reset and primitive-to-all transfer give the all-character (qT)^((7/3)(1-sigma)+o(1)) envelope.", "missing_dependencies": ["primitive CGL-style analytic envelope", "L04/L06/M05/M07 inputs", "F01/F02 Dirichlet outer envelopes", "full middle-range assembly F03"], "conclusion": "No general 7/3 envelope has been reconstructed solely from checked published/derived P6 inputs."},
        "q_equals_one": {"epistemic_status": "PROVED", "verdict": "SEPARATELY_COVERED_BY_G0_AT_30_OVER_13", "statement": "The pinned G0 route certifies the published Guth--Maynard zeta zero-density/envelope path at exponent 30/13, including its source-gate adjudication. This is a separate zeta route, not an all-character P6 7/3 reconstruction and not a replacement for v4's deliberately q>=2 primitive scope.", "non_promotion": "G0 supplies no P6 general 7/3 theorem."},
        "overall_disposition": "OBSERVED: P6 remains RECONCILED_OPEN_INPUTS. The named detector inputs are substantially repaired for the amended q>=2 primitive path, but the core primitive large-value/comparator route remains open.",
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)}, "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}, "hostile_audit": "DEFERRED_TO_PAPER_STAGE", "replay": "python3 proof/build_p6_post_repair_reconciliation_v1.py --check"}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = (json.dumps(payload(), indent=2, sort_keys=True) + "\n").encode()
    if args.write:
        require(not OUT.exists(), "refusing to overwrite post-repair reconciliation")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "post-repair reconciliation mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

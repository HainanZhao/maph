#!/usr/bin/env python3
"""Hostile reconciliation of Cycle-2 Stream-B Route A v2 and Route B v1.

The script reads frozen reports as evidence; it imports neither route's code.
Agreement is not promoted where one route merely coarsens or omits a required
node.  Every such coverage failure is retained as a mismatch row.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATHS = {
    "preregistration": "docs/cycle-2-g0-analytic-preregistration.md",
    "stream_a_ledger": "docs/cycle-2-stream-a-mp-mvt-ledger-v1.md",
    "route_a_v2": "artifacts/cycle-2-stream-b-route-a-v2.json",
    "route_b_v1": "artifacts/cycle-2-stream-b-route-b-v1.json",
    "gm_tar": "artifacts/sources/guth-maynard-2405.20552v2-source.tar",
    "gm_tex": "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
    "mp_tex": "artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex",
    "mp_tar": "artifacts/sources/maynard-pratt-2206.11729.tar",
    "montgomery_pdf": "artifacts/sources/montgomery-1969-inventiones8-gdz-volume.pdf",
    "hsw_tar": "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar",
    "bui_tar": "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar",
}
EXPECTED = {
    "gm_tar": "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc",
    "gm_tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    "mp_tex": "ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426",
    "mp_tar": "b81dbb3bb8bed014588294b5c6d7e8e4b5a14798f445baecb6680b7a9df967d3",
    "montgomery_pdf": "b240c7c07d32201ced906bd0fdc4d36cca3c11999084afeb658ffca3f978534e",
    "hsw_tar": "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    "bui_tar": "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
}
SEALED_INPUT_BYTE_HASHES = {
    "route_a_v2_artifact": "d3b86e4715ffdb8c6403781b1bafa82333950a211e706ac275ff93ce7c9a2b24",
    "route_b_v1_artifact": "927d85a06133692dd75d8f796741cd8a1b5c5a40b91faeecdad8d53556227bd1",
    "preregistration": "e07ecf8783983d20ad435bdcd1c4b0922eee0c6419b26bdd34d7a34b92a2fb63",
    "stream_a_ledger": "e1cb48f1855eeb308798ea3df7867ab94e7b61115b377b632afd27ffc388a40a",
    "route_a_v2_script": "7d86446f82770264483961995d355f07f14147763112026781a4fded8650d557",
    "route_b_v1_script": "6ab19ad3e741f34977e371ab6ddf8171aecf7686ff4be8446f0e32eb21d90974",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def self_hash() -> str:
    return sha256(Path(__file__))


def load_json(key: str) -> dict[str, Any]:
    return json.loads((ROOT / PATHS[key]).read_text(encoding="utf-8"))


def row_by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in report["rows"]}


def frozen_source_hashes() -> dict[str, str]:
    observed = {key: sha256(ROOT / PATHS[key]) for key in EXPECTED}
    for key, expected in EXPECTED.items():
        assert observed[key] == expected, f"frozen source hash mismatch: {key}"
    return observed


def canonical_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def semantic_route_identities(a: dict[str, Any], b: dict[str, Any]) -> dict[str, str]:
    a_body = {key: value for key, value in a.items() if key not in {"mathematical_and_source_audit_sha256", "replay"}}
    assert canonical_sha256(a_body) == a["mathematical_and_source_audit_sha256"]
    # Route B has no timing field and is replay-byte-stable; its script hash
    # identifies the exact semantic producer while the seal records its bytes.
    return {
        "route_a_v2_canonical_audit_hash": a["mathematical_and_source_audit_sha256"],
        "route_b_v1_script_hash": b["replay"]["script_sha256"],
        "route_b_v1_artifact_hash_at_seal": SEALED_INPUT_BYTE_HASHES["route_b_v1_artifact"],
    }


def assert_input_shapes(a: dict[str, Any], b: dict[str, Any], prereg: str, ledger: str) -> None:
    a_rows, b_rows = row_by_id(a), row_by_id(b)
    assert a["open_blockers"] == []
    assert all(row["status"] == "PROVED" for row in a_rows.values())
    assert b["label_coverage"]["unlabeled_nodes"] == []
    assert all(row["status"] == "PROVED" for row in b_rows.values())
    assert "Zero count: multiplicity counted, `|Im rho| <= T`." in prereg
    assert "Each row must be `PROVED`" in prereg
    assert "MP explicitly takes cluster zeros without multiplicity" in ledger
    assert "Theorem 1 (Davenport)" in ledger


def mapping(a: dict[str, Any], b: dict[str, Any]) -> list[dict[str, Any]]:
    ar, br = row_by_id(a), row_by_id(b)
    def av(identifier: str) -> str:
        return ar[identifier]["status"]
    def bv(identifier: str) -> str:
        return br[identifier]["status"]
    return [
        {"id": "R1-source-hashes", "prereg_requirement": "freeze hashes and source versions", "route_a": "GM/MP/Montgomery/HSW/Bui hashes checked", "route_b": "same sources checked, with additional HSW/Bui PDF hashes", "ledger": "source locators and versions frozen", "status": "AGREED", "falsifier": "Any unequal hash for a shared source invalidates comparison."},
        {"id": "R2-range-and-height", "prereg_requirement": "7/10<=sigma<=4/5 and multiplicity-counted |Im rho|<=T", "route_a": a["exact_bookkeeping"]["range"], "route_b": b["exact_rational_checks"]["sigma_range"], "ledger": "MP's local positive interval and the outer two-sided convention are distinguished", "status": "AGREED_AFTER_CONVERSION", "falsifier": "A source range excluding the frozen sigma interval, or an unconverted height convention, refutes the route."},
        {"id": "R3-detector-and-complement", "prereg_requirement": "MP must cover GM detector and Type-II transfer", "route_a": f"{av('SB-A14-MP-complement-to-Type-II')}; calls beta cutoff part of exact agreement", "route_b": f"{bv('SB-B1-complement-to-mp-type-ii')}; separately identifies GM-complement implication", "ledger": "detector/range/threshold agree; MP types may overlap", "status": "AGREED_WITH_WORDING_CAVEAT", "falsifier": "Detector, dyadic range, or threshold mismatch refutes complement inclusion."},
        {"id": "R4-multiplicity-local-count", "prereg_requirement": "multiplicity convention and local zero count checked", "route_a": av("SB-A15-local-strip-and-multiplicity"), "route_b": bv("SB-B2-multiplicity-and-two-sided-conversion"), "ledger": "initially OBSERVED before HSW/Bui conversion", "status": "AGREED_AFTER_EXTERNAL_COMPLETION", "falsifier": "A unit strip with multiplicity T^c for fixed c>0 invalidates the o(1) conversion."},
        {"id": "R5-two-sided-and-dyadic-heights", "prereg_requirement": "convert positive local proof to |Im rho|<=T", "route_a": av("SB-A16-positive-to-two-sided"), "route_b": bv("SB-B2-multiplicity-and-two-sided-conversion") + " plus " + bv("SB-B10-dyadic-reassembly-and-route-boundary"), "ledger": "initial source ledger left this OBSERVED", "status": "AGREED_WITH_ROUTE_B_STRONGER_JUSTIFICATION", "falsifier": "A real non-trivial zero or failure of conjugation/multiplicity preservation would refute the exact factor-two step."},
        {"id": "R6-smoothing-and-extraction", "prereg_requirement": "beta-dependent smoothing, tail, and 1-separated extraction", "route_a": av("SB-A17-smoothing-and-separated-extraction"), "route_b": bv("SB-B3-type-i-smoothing-and-separated-extraction"), "ledger": "outside Stream A scope", "status": "AGREED", "falsifier": "A non-uniform Fourier tail or extraction loss T^c invalidates the transfer."},
        {"id": "R7-coefficients-and-power", "prereg_requirement": "original/powered coefficient and normalization losses", "route_a": av("SB-A18-coefficients-powered-support"), "route_b": bv("SB-B4-detector-and-powered-coefficient-normalization"), "ledger": "outside Stream A scope", "status": "AGREED", "falsifier": "Powered coefficients exceeding T^o(1) for bounded k invalidate normalization."},
        {"id": "R8-both-k-regimes", "prereg_requirement": "both Cycle-1 integer-k regimes", "route_a": a["exact_bookkeeping"]["bounded_power"], "route_b": bv("SB-B5-both-k-regimes") + "; ell_max=10/13, upper_min=15/14", "ledger": "outside Stream A scope", "status": "AGREED", "falsifier": "If k is unbounded, support and divisor losses cease to be T^o(1)."},
        {"id": "R9-support-blocks-and-threshold", "prereg_requirement": "admissible dyadic block and threshold after normalization", "route_a": av("SB-A18-coefficients-powered-support") + " (coalesced row)", "route_b": bv("SB-B6-support-blocks-and-threshold"), "ledger": "outside Stream A scope", "status": "AGREED_COARSE_ROUTE_A", "falsifier": "An unbounded block count or non-comparable M/N^k invalidates the threshold transfer."},
        {"id": "R10-theorem-1-1-three-terms", "prereg_requirement": "Theorem 1.1 application hypotheses and structural terms", "route_a": "NOT EXPLICIT in v2; v2 is a v1-blocker closure and has no row/formula for all three terms", "route_b": bv("SB-B7-large-values-structural-terms"), "ledger": "outside Stream A scope", "status": "ROUTE_A_COVERAGE_GAP", "falsifier": "A claimed independent agreement requires Route A to enumerate and check L^(2-2s), L^(18/5-4s), and T L^(12/5-4s)."},
        {"id": "R11-montgomery-theorem-and-polarity", "prereg_requirement": "pin reachable mean-value theorem and all hypotheses", "route_a": av("SB-A19-Montgomery-mean-value"), "route_b": bv("SB-B8-montgomery-discrete-mvt-and-polarity"), "ledger": "printed formula (7), arbitrary coefficients, delta convention", "status": "AGREED", "falsifier": "Failure of endpoint spacing or polarity conversion invalidates the MVT application."},
        {"id": "R12-mvt-structural-terms", "prereg_requirement": "exact mean-value branch", "route_a": a["exact_bookkeeping"]["mvt_conclusion"], "route_b": bv("SB-B8-montgomery-discrete-mvt-and-polarity"), "ledger": "derives the same two terms conditionally", "status": "AGREED", "falsifier": "If coefficient l2 norm exceeds N^(k+o(1)), these terms are not licensed."},
        {"id": "R13-mvt-strict-residual", "prereg_requirement": "no finite-T endpoint upgrade and all branch losses visible", "route_a": "NOT EXPLICIT in v2", "route_b": bv("SB-B9-mvt-branch-and-strict-residual") + "; exact positive residual retained", "ledger": "outside Stream A scope", "status": "ROUTE_A_COVERAGE_GAP", "falsifier": "Independent agreement requires the positive residual, not merely a displayed GM conclusion."},
        {"id": "R14-epsilon-and-o1-losses", "prereg_requirement": "all fixed losses visible; no finite-T power upgrade", "route_a": av("SB-A20-epsilon-o1-transfer") + "; epsilon/20 finite budget", "route_b": "all rows retain T^o(1); no finite-T equality", "ledger": "final MP log power not explicit", "status": "AGREED", "falsifier": "An unbounded number of loss sources or a fixed power loss invalidates epsilon allocation."},
        {"id": "R15-final-dyadic-reassembly", "prereg_requirement": "all branch/reassembly conditions checked", "route_a": "only positive-to-two-sided geometric shell statement", "route_b": bv("SB-B10-dyadic-reassembly-and-route-boundary") + "; explicitly combines Type I and II", "ledger": "positive local result only", "status": "ROUTE_A_COVERAGE_GAP", "falsifier": "Independent agreement requires an explicit domination check 2(1-sigma)<=A(sigma) and positive-shell summation."},
        {"id": "R16-pass-label-scope", "prereg_requirement": "full G0 PASS requires every node and all downstream conditions", "route_a": a["pass_state"], "route_b": b["pass_state"], "ledger": "does not promote G0", "status": "LABEL_SCOPE_MISMATCH", "falsifier": "Using Route A's unqualified PASS as a G0 PASS contradicts the preregistration and Stream-C blocker record."},
    ]


def mismatches() -> list[dict[str, Any]]:
    return [
        {"id": "M1-route-a-pass-scope", "status": "CONTAINED", "kind": "label mismatch", "evidence": "Route A says PASS, while Route B says NARROW PASS and preregistration requires Stream C before G0 PASS.", "effect": "Canonical status is STREAM_B_NARROW_PASS; G0 remains OBSERVED.", "falsifier": "Any release labeling G0 PASS from Route A alone fails this reconciliation."},
        {"id": "M2-route-a-theorem-1-1-coverage", "status": "OPEN", "kind": "coverage mismatch", "evidence": "Route A v2 has no explicit all-three-terms Theorem 1.1 row; Route B B7 has it.", "effect": "The routes are not independently agreeing on this node.", "falsifier": "Add a Route-A-v3 exact structural-term row or withdraw independent-agreement language."},
        {"id": "M3-route-a-mvt-residual-coverage", "status": "OPEN", "kind": "coverage mismatch", "evidence": "Route A v2 gives the two MVT structural terms but no positive residual; Route B B9 checks it exactly.", "effect": "No independent two-route confirmation of the strict MVT margin.", "falsifier": "Add a Route-A-v3 residual identity with denominator/range sign checks."},
        {"id": "M4-route-a-reassembly-coverage", "status": "OPEN", "kind": "coverage mismatch", "evidence": "Route A records a two-sided shell inequality but not the Type-I/Type-II exponent comparison and final reassembly; Route B B10 does.", "effect": "No independent two-route confirmation of the final application assembly.", "falsifier": "Add a Route-A-v3 reassembly row including 2(1-sigma)<=15(1-sigma)/(3+5sigma)."},
        {"id": "M5-beta-cutoff-wording", "status": "CONTAINED", "kind": "wording mismatch", "evidence": "Route A calls a beta cutoff part of exact detector agreement; beta>=sigma is imposed in the GM/MP counting restriction, not in MP's Type-I detector definition.", "effect": "No mathematical inclusion failure; canonical wording separates detector identity from R_II(sigma,T)'s beta restriction.", "falsifier": "A source detector condition depending on beta would require a new detector comparison."},
        {"id": "M6-gm-tar-route-coverage", "status": "CONTAINED", "kind": "source-freeze coverage", "evidence": "Both routes hash the extracted GM TeX, while preregistration freezes the parent tar. This reconciliation verifies both hashes and their expected values.", "effect": "No hash conflict; future route reports should record both when claiming preregistered-source closure.", "falsifier": "A mismatch of the tar or extracted TeX hash invalidates the frozen-source link."},
        {"id": "M7-route-a-byte-reproducibility", "status": "CONTAINED", "kind": "historical reproducibility defect", "evidence": "Route A v2 stores replay.wall_time_ns, so its raw artifact hash changes after a successful replay although mathematical_and_source_audit_sha256 remains stable.", "effect": "Route A is compared by canonical audit hash; the byte hash is recorded only at seal time.", "falsifier": "A changed canonical audit hash, rather than a changed timing field, requires a new mathematical reconciliation."},
    ]


def certificate() -> dict[str, Any]:
    hashes = frozen_source_hashes()
    a, b = load_json("route_a_v2"), load_json("route_b_v1")
    prereg = (ROOT / PATHS["preregistration"]).read_text(encoding="utf-8")
    ledger = (ROOT / PATHS["stream_a_ledger"]).read_text(encoding="utf-8")
    assert_input_shapes(a, b, prereg, ledger)
    table = mapping(a, b)
    issues = mismatches()
    assert len(table) == 16
    assert [row["id"] for row in issues if row["status"] == "OPEN"] == [
        "M2-route-a-theorem-1-1-coverage", "M3-route-a-mvt-residual-coverage", "M4-route-a-reassembly-coverage"
    ]
    return {
        "artifact_id": "cycle-2-stream-b-route-reconciliation-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Hostile evidence reconciliation only. It detects no contradictory checked formula, but it does not certify independent two-route agreement where Route A v2 omits a node.",
        "canonical_status": "STREAM_B_NARROW_PASS only; G0 remains OBSERVED pending Stream C and the three Route-A coverage rows.",
        "frozen_source_hashes": hashes,
        "semantic_route_identities": semantic_route_identities(a, b),
        "input_byte_hashes_at_seal": SEALED_INPUT_BYTE_HASHES,
        "historical_reproducibility_defect": {
            "status": "OBSERVED",
            "affected_input": "cycle-2-stream-b-route-a-v2.json",
            "cause": "Route A v2 embeds replay.wall_time_ns, so a successful rerun changes its artifact bytes while preserving its canonical mathematical_and_source_audit_sha256.",
            "containment": "This reconciliation compares Route A by the asserted canonical audit hash and records the current-at-seal byte hash only as provenance. Byte drift is not a mathematical mismatch.",
        },
        "canonical_mapping_table": table,
        "mismatch_and_falsifier_rows": issues,
        "agreement_summary": {
            "agreed_or_agreed_with_caveat": sum(row["status"].startswith("AGREED") for row in table),
            "coverage_gaps": sum(row["status"] == "ROUTE_A_COVERAGE_GAP" for row in table),
            "label_scope_mismatches": sum(row["status"] == "LABEL_SCOPE_MISMATCH" for row in table),
            "formula_contradictions": 0,
        },
        "next_authorized_action": "Open a versioned Route A continuation only if independent two-route agreement is required; add its Theorem-1.1 terms, strict MVT residual, and full reassembly. Do not alter either frozen route artifact.",
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": self_hash(),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_b_routes_v1.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-reconciliation-v1.json",
        },
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Hostile, deterministic reconciliation of Stream-C Routes A v3 and B v4."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    "route_a_v1": ("artifacts/cycle-2-stream-c-route-a-v1.json", ""),
    "route_a_v3": ("artifacts/cycle-2-stream-c-route-a-v3.json", ""),
    "route_a_v3_replay": ("proof/replay_cycle2_stream_c_route_a_v3.py", ""),
    "route_b_v2": ("artifacts/cycle-2-stream-c-route-b-v2.json", ""),
    "route_b_v2_replay": ("proof/replay_short_intervals_stream_c_route_b_v2.py", "9757c4a241ffd6b08abe1f084ca037697d96b714ddf0596e5264ba438e021b5d"),
    "route_b_v4": ("artifacts/cycle-2-stream-c-route-b-v4.json", "a8c7be629b8bff5cce4ce4a7ee5e5c1e52969b0681a45008834f7e548a8db249"),
    "route_b_v4_replay": ("proof/replay_short_intervals_stream_c_route_b_v4.py", "1be7195a890046e7aff63069137a5ab224bd2496f180fb87f12de9410723882a"),
    "formula_ledger_v1": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v1.json", "24248e58028651ba2903b023fe2b9f660ab5dff9606b2ca2c879f462dd94b297"),
    "formula_ledger_v2": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json", "3433e974b9751d310447847d75abbf529e5b4ed7e21e87a0224e4efb8ea0fde3"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def verify() -> dict[str, str]:
    checked: dict[str, str] = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        if expected:
            assert actual == expected, f"hash mismatch: {relative}"
        checked[name] = actual
    for command in (
        ["python3", str(ROOT / "proof/replay_cycle2_stream_c_route_a_v3.py"), "--check"],
        ["python3", str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v2.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-c-route-b-v2.json")],
        ["python3", str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v4.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-c-route-b-v4.json")],
    ):
        subprocess.run(command, check=True, capture_output=True, text=True)
    return checked


def coverage() -> list[dict[str, str]]:
    # Route A v1 supplies the exact secondary arithmetic retained by v3, but
    # Route A v3's source checker still imports only access-ledger v1.  That
    # ledger's archival source-access status is OBSERVED, so no v3 source node
    # may be silently upgraded by Route B's later v2 ledger.
    a_source_gap = "OBSERVED"
    return [
        {"label": "formula theorem", "route_a_v3": a_source_gap, "route_b_v4": "PROVED", "evidence": "A v3 imports access-ledger v1; B v4 imports CC/OCW ledger v2."},
        {"label": "formula arbitrary-T range", "route_a_v3": a_source_gap, "route_b_v4": "PROVED", "evidence": "A's v1 ledger is the only pinned authority in its replay; B pins the licensed arbitrary-T course theorem."},
        {"label": "formula remainder", "route_a_v3": a_source_gap, "route_b_v4": "PROVED", "evidence": "Same source-authority gap; B v4 transfers its stated remainder."},
        {"label": "formula endpoint/half-weight", "route_a_v3": a_source_gap, "route_b_v4": "PROVED", "evidence": "A v3 asserts the transfer through v1; B v4 imports ledger v2's integer-endpoint audit."},
        {"label": "formula multiplicity", "route_a_v3": a_source_gap, "route_b_v4": "PROVED", "evidence": "A v3 does not pin the proof unit; B v4 pins the residue multiplicity source."},
        {"label": "formula |rho|-|gamma| bridge", "route_a_v3": a_source_gap, "route_b_v4": "PROVED", "evidence": "A's asserted bridge rests on the unupgraded formula path; B v4 imports the v2 boundary audit."},
        {"label": "Huxley theorem", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v3 pins the classical ledger statement; B v2/v4 pins the original source."},
        {"label": "Huxley range", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both use 4/5<=sigma<=1, joined to GM's 7/10<=sigma<=4/5 branch."},
        {"label": "Huxley logarithmic loss", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both retain Huxley log^44 and absorb it only asymptotically."},
        {"label": "Ford high-height VK", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both pin Ford Theorem 5."},
        {"label": "Platt all-height completion", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both pin Platt--Trudgian's finite-height RH verification."},
        {"label": "VK cutoff weakening", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both retain 5/7-2/3=1/21>0."},
        {"label": "all-height cutoff", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Ford plus Platt--Trudgian is the common completed path."},
        {"label": "local pair kernel", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both pin HSW plus Bui--Heath-Brown multiplicity-inclusive unit-strip counting."},
        {"label": "uniform T", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 retained arithmetic and B v2 both give T=x/y E(x)^2."},
        {"label": "uniform epsilon margin", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 and B v2 retain the eventual subpower absorption; B v2 records eta<=b^2 epsilon/4."},
        {"label": "uniform density supremum", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 retained exact cutoff arithmetic and v3 closes its non-formula inputs; B v2 gives the explicit margin."},
        {"label": "uniform upper range", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both retain y<=x^0.99 and 2<=T<=x eventually."},
        {"label": "uniform truncation error", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both retain x(log x)^3/T=O(yE(x)^-1)."},
        {"label": "uniform prime conversion", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v3 and B v2 retain prime-power/partial-summation transfer."},
        {"label": "almost-all delta", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both retain delta=X^(-13/15+epsilon/2)."},
        {"label": "almost-all T", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 retained arithmetic and B v2 give T=delta^-1 E(X)^4."},
        {"label": "almost-all epsilon margin", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 and B v2 retain subpower absorption; B v2 records eta<=b^2 epsilon/12."},
        {"label": "almost-all L2 pair reduction", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v3 and B v2 pin the local pair kernel and displayed reduction."},
        {"label": "almost-all Cauchy--Schwarz remainder", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 and B v2 retain delta^2 X^3/(y^2 X)<=X^-epsilon."},
        {"label": "almost-all Chebyshev/exceptional conversion", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v1 and B v2 retain threshold yE(X)^-1 and O(XE(X)^-1) starts."},
        {"label": "almost-all upper range", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "Both retain y<=X^0.99."},
        {"label": "almost-all prime conversion", "route_a_v3": "PROVED", "route_b_v4": "PROVED", "evidence": "A v3 and B v2 retain the prime-power/partial-summation control."},
    ]


def certificate() -> dict[str, Any]:
    hashes = verify()
    a1 = load("artifacts/cycle-2-stream-c-route-a-v1.json")
    a3 = load("artifacts/cycle-2-stream-c-route-a-v3.json")
    b2 = load("artifacts/cycle-2-stream-c-route-b-v2.json")
    b4 = load("artifacts/cycle-2-stream-c-route-b-v4.json")
    ledger1 = load("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v1.json")
    ledger2 = load("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json")
    a_script = (ROOT / "proof/replay_cycle2_stream_c_route_a_v3.py").read_text()
    assert "explicit-formula-access-ledger-v1.md" in a_script
    assert "explicit-formula-source-closure-v2" not in a_script
    assert "kedlaya-2007-von-mangoldt-author.pdf" not in a_script
    assert ledger1["epistemic_status"] == "OBSERVED"
    assert ledger2["epistemic_status"] == "PROVED"
    assert a1["exact_bookkeeping"]["uniform"]["theta"] == a3["result_labels"]["uniform_theta"] == b2["frozen_parameters"]["uniform_theta"] == b4["exact_transfer_invariants"]["uniform_theta"] == "17/30"
    assert a1["exact_bookkeeping"]["almost_all"]["theta"] == a3["result_labels"]["almost_all_theta"] == b2["frozen_parameters"]["almost_all_theta"] == b4["exact_transfer_invariants"]["almost_all_theta"] == "2/15"
    rows = coverage()
    gaps = [row["label"] for row in rows if row["route_a_v3"] != "PROVED" or row["route_b_v4"] != "PROVED"]
    assert gaps == [
        "formula theorem", "formula arbitrary-T range", "formula remainder", "formula endpoint/half-weight", "formula multiplicity", "formula |rho|-|gamma| bridge"
    ]
    return {
        "artifact_type": "stream-c-two-route-reconciliation-certificate",
        "certificate_version": 1,
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Hostile reconciliation of Route A v3 and Route B v4 against every Stream-C preregistration label. Exact exponent agreement is PROVED; the full independent-route Stream-C PASS is withheld because Route A v3 does not pin the later archival formula closure.",
        "frozen_hashes": hashes,
        "exact_agreements": {
            "status": "PROVED",
            "uniform_theta": "17/30",
            "almost_all_theta": "2/15",
            "upper_range": "y<=Z^(99/100) in both branches",
            "epsilon_domain": "0<epsilon<127/300 is recorded by Route B v2; this is nonvacuous for both published lower endpoints."
        },
        "coverage": rows,
        "source_authority_correction": {
            "status": "PROVED",
            "finding": "Route A v3's replay pins only access-ledger v1 and errorbounds.pdf. It neither pins access-ledger v2 nor the von-Mangoldt proof PDF. Ledger v1 labels its archival source access OBSERVED, while ledger v2 closes that gate PROVED.",
            "effect": "Route B v4 cannot retroactively supply Route A v3's independent formula source chain. The six formula/convention labels remain OBSERVED on Route A v3.",
            "required_followup": "Issue a Route A v4 correction that pins access-ledger v2 and both frozen Kedlaya course units, then rerun this reconciliation."
        },
        "full_independent_route_pass": {
            "status": "OBSERVED",
            "result": "NOT PASS",
            "open_coverage_labels": gaps,
            "reason": "A second route must independently close every formula/convention label; the current Route A v3 does not meet that source-authority requirement."
        },
        "preservation": "Route A v1/v2/v3 and Route B v1/v2/v3/v4 are read-only evidence; no historical artifact was edited.",
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_c_two_routes_v1.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-two-route-reconciliation-v1.json"
        }
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path)
    mode.add_argument("--check", type=Path)
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.write_text(output, encoding="utf-8")
    else:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")


if __name__ == "__main__":
    main()

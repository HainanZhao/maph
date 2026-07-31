#!/usr/bin/env python3
"""Check that the census manuscript states only frozen artifact facts."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-census.tex"
PDF = ROOT / "paper/effective-stark-census.pdf"
LAYER0 = ROOT / "artifacts/census-paper-layer0-reconciliation-v1.json"
Q_AUDIT = ROOT / "artifacts/census-q-packet-corpus-audit-v1.json"
H_TAXONOMY = ROOT / "artifacts/census-h-taxonomy-v1.json"
TRANSPORT = ROOT / "artifacts/engine-b-transport-manifest-v5.json"
IMPRIMITIVE = ROOT / "artifacts/rq000013-engine-a-imprimitive-certificate-v1.json"


def require(text: str, snippets: tuple[str, ...]) -> None:
    absent = [snippet for snippet in snippets if snippet not in text]
    if absent:
        raise RuntimeError(f"manuscript missing: {absent}")


def main() -> None:
    source = PAPER.read_text(encoding="utf-8")
    layer0 = json.loads(LAYER0.read_text(encoding="utf-8"))
    q = json.loads(Q_AUDIT.read_text(encoding="utf-8"))
    h = json.loads(H_TAXONOMY.read_text(encoding="utf-8"))
    transport = json.loads(TRANSPORT.read_text(encoding="utf-8"))
    imprimitive = json.loads(IMPRIMITIVE.read_text(encoding="utf-8"))

    split = layer0["structural_trichotomy"]
    require(source, (
        f"|T|={split['T_empty_support']}",
        f"|Q|={split['Q_nonempty_quadratic_support']}",
        f"|H|={split['H_nonempty_higher_order_support']}",
        str(q["chain"]["row_count"]),
        q["chain"]["final_sha256"],
        str(h["counts"]["H_rows"]),
        str(h["counts"]["all_known_mechanisms_fail"]),
        str(transport["counts"]["member_transport_completed"]),
        "no new higher-order packet identity",
        "does not promote another member",
        imprimitive["case_id"],
        f"E_\\chi={imprimitive['exact_result']['E_chi']}",
        f"I_\\chi={imprimitive['exact_result']['I_chi']}",
    ))
    if "all registered mechanisms fail & 1359" not in source:
        raise RuntimeError("H all-mechanisms-fail table cell drifted")
    if "incomplete legacy quartic construction & 5" not in source:
        raise RuntimeError("H incomplete-quartic table cell drifted")
    if not PDF.exists():
        raise RuntimeError("compiled census PDF missing")
    rendered = subprocess.run(
        ["mutool", "draw", "-F", "txt", str(PDF)],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    ).stdout
    require(rendered, (
        "A Certified Census of One-Place Stark Invariants",
        "Exhaustive quadratic stratum",
        "Engine-B transport scope",
        "zero completed member transports",
        "A worked imprimitive row",
    ))
    print("CENSUS_PAPER_AUDIT=PASS")


if __name__ == "__main__":
    main()

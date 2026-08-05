#!/usr/bin/env python3
"""Audit C62's exact finite KKT packet and scoped exchange no-gos."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle62-kkt-exchange"


def audit() -> dict[str, object]:
    grid = json.loads((OUT / "summary.json").read_text())
    assert (grid["height"], grid["rows"], grid["negative_rows"]) == (24, 118755, 0)
    assert grid["grid_kkt_rows"] == 61
    with (OUT / "grid-kkt.tsv").open() as source:
        kkt = list(csv.DictReader(source, delimiter="\t"))
    assert len(kkt) == 61 and all(row["central"] == "1" for row in kkt)
    factor = json.loads((OUT / "exchange-factor-audit.json").read_text())
    for name in ("transposition_exchange", "cycle_exchange"):
        assert factor[name]["quotient_terms"] == 7082
        assert factor[name]["positive_coefficients"] == 3087
        assert factor[name]["negative_coefficients"] == 3995
    polya = json.loads((OUT / "exchange-polya-summary.json").read_text())
    assert polya["rows"][0]["negative_coefficients"] == 3087
    assert polya["rows"][-1] == {"degree": 24, "negative_coefficients": 44584, "terms": 849805}
    random_results = [json.loads((OUT / f"random-{seed}-bigint-result.json").read_text()) for seed in (620621, 620622, 620623)]
    assert sum(row["rows"] for row in random_results) == 300000
    assert sum(row["negative_rows"] for row in random_results) == 0
    return {
        "status": "PASS",
        "exact_finite": {"epistemic_status": "PROVED", "grid_rows": 118755, "negative_rows": 0, "kkt_rows": 61, "noncentral_kkt_rows": 0},
        "exchange_no_go": {"epistemic_status": "PROVED", "mixed_quotient_terms": 7082, "polya_cap": 24, "negative_coefficients_at_cap": 44584},
        "random_probe": {"epistemic_status": "OBSERVED", "rows": 300000, "negative_rows": 0},
        "claim_boundary": "Finite S3 KKT packet and two certificate-family no-gos only; no continuous S3, arbitrary-group Zhao, or Sidorenko conclusion.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))

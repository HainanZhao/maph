#!/usr/bin/env python3
"""Audit C68's exact fixed-S3 comparison certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle68-interior-chord"


def checked(path: Path) -> dict:
    payload = json.loads(path.read_text())
    assert payload["status"] == "PASS", path
    assert payload["epistemic_status"] == "PROVED", path
    return payload


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> dict:
    c67 = json.loads((ROOT / "artifacts/cycle-67-b067-s3-boundary-positivity-v1.json").read_text())
    assert c67["status"] == "SEALED"
    assert c67["epistemic_status"] == "PROVED"
    assert c67["record_type"] == "PROVED_FIXED_S3_ENDPOINT_BOUNDARY_THEOREM"
    secant = checked(OUT / "secant/secant-summary.json")
    assert secant["coefficientwise_identity"] == "P=P|s2=0+s2*G"
    factors = checked(OUT / "secant-stripped/factor-report.json")
    assert all(row["factors"] == {"1-x": 1} for row in factors["charts"].values())
    primary = checked(OUT / "secant-blowup/blowup-summary.json")
    assert len(primary["charts"]) == 12
    assert all(row["removed_radial_factor"] == "rho^1" for row in primary["charts"].values())
    secondary = checked(OUT / "secant-secondary-blowup/secondary-blowup-summary.json")
    assert len(secondary["charts"]) == 6
    assert all(row["removed_radial_factor"] == "eta^1" for row in secondary["charts"].values())
    sparse = checked(OUT / "secant-blowup-sparse-audit.json")
    assert sparse["primary_charts"] + sparse["secondary_charts"] == 18
    cover = checked(OUT / "secant-cover-audit.json")
    assert cover["terminal_sign_charts"] == 18
    assert cover["direct_source_homogeneous_degree"] == 15
    evidence = [
        OUT / "secant/secant-summary.json", OUT / "secant-stripped/factor-report.json",
        OUT / "secant-blowup/blowup-summary.json", OUT / "secant-secondary-blowup/secondary-blowup-summary.json",
        OUT / "secant-blowup-sparse-audit.json", OUT / "secant-cover-audit.json",
    ]
    return {"status":"PASS", "epistemic_status":"PROVED", "certificate_charts":18,
            "claim":"For every nonnegative a:S3->R, N(a)>=N(a_cl).",
            "claim_boundary":"PROVED only for the fixed S3 host comparison; this neither proves Zhao's universal condition nor Sidorenko for the target graph.",
            "evidence_hashes":{str(p.relative_to(ROOT)):digest(p) for p in evidence}}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))

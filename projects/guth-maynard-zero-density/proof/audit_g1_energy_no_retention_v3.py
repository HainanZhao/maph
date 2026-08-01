#!/usr/bin/env python3
"""Machin-identity closure for the corrected finite G1 energy certificate v2."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from proof import audit_g1_energy_no_retention_v2 as previous


OUTPUT = ROOT / "artifacts/g1-energy-no-retention-audit-v3.json"
PREVIOUS_ARTIFACT = ROOT / "artifacts/g1-energy-no-retention-audit-v2.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def machin_identity_certificate() -> dict[str, str]:
    """Exact tangent/branch proof of pi/4=4 atan(1/5)-atan(1/239)."""
    t = Fraction(1, 5)
    tan_double = 2 * t / (1 - t * t)
    tan_fourfold = 2 * tan_double / (1 - tan_double * tan_double)
    require(tan_fourfold == Fraction(120, 119), "fourfold tangent algebra mismatch")
    rational_tangent = (tan_fourfold - Fraction(1, 239)) / (1 + tan_fourfold * Fraction(1, 239))
    require(rational_tangent == 1, "Machin tangent identity mismatch")
    pi_lower, pi_upper = previous.machin_pi_bounds()
    require(pi_lower > 3, "Machin enclosure does not establish pi>3")
    # If theta=atan(1/5), then 0<theta<1/5, so 4theta<4/5<pi/2.
    # On (0,pi/2), tan is strictly increasing; tan(4theta)=120/119>1/239,
    # hence delta=4theta-atan(1/239) is also positive. Therefore delta is in
    # (0,pi/2); its tangent is one, so uniqueness gives delta=atan(1)=pi/4.
    require(Fraction(4, 5) < pi_lower / 2, "Machin branch upper bound failed")
    require(tan_fourfold > Fraction(1, 239), "Machin branch lower bound failed")
    return {
        "status": "CERTIFIED_NUMERICAL",
        "identity": "pi/4=4*atan(1/5)-atan(1/239)",
        "tan_2atan_1_5": previous.route.q(tan_double),
        "tan_4atan_1_5": previous.route.q(tan_fourfold),
        "tan_difference": previous.route.q(rational_tangent),
        "branch": "0<4*atan(1/5)-atan(1/239)<pi/2, so tan(delta)=1 identifies delta=pi/4",
        "pi_lower": previous.route.q(pi_lower),
        "pi_upper": previous.route.q(pi_upper),
        "pi_radius": previous.route.q((pi_upper - pi_lower) / 2),
        "branch_upper_margin": previous.route.q(pi_lower / 2 - Fraction(4, 5)),
        "branch_lower_tangent_margin": previous.route.q(tan_fourfold - Fraction(1, 239)),
    }


def certificate() -> dict[str, Any]:
    payload = previous.certificate()
    require(PREVIOUS_ARTIFACT.is_file() and PREVIOUS_ARTIFACT.read_text(encoding="utf-8") == previous.render(payload), "v2 energy certificate is not sealed/replayable")
    identity = machin_identity_certificate()
    payload["artifact_id"] = "g1-energy-no-retention-audit-v3"
    payload["supersedes"] = {
        "artifact": "g1-energy-no-retention-audit-v2.json",
        "reason": "V2 stated the Machin identity but did not mechanically record its tangent algebra and principal-branch check.",
    }
    payload["frozen_hashes"]["v2_energy_artifact"] = digest(PREVIOUS_ARTIFACT)
    payload["frozen_hashes"]["v2_energy_audit"] = digest(ROOT / "proof/audit_g1_energy_no_retention_v2.py")
    payload["exact_method"]["W5_step"]["machin_identity_verified"] = identity
    payload["replay"] = {
        "script_sha256": digest(Path(__file__)),
        "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v3.py --write",
        "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v3.py --check",
    }
    return payload


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite corrected v3 energy artifact")
        OUTPUT.write_text(payload, encoding="utf-8")
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text(encoding="utf-8") == payload, "v3 G1 energy certificate mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "ZERO_ENERGY_RETENTION_ROWS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)

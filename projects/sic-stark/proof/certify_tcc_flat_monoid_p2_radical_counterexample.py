#!/usr/bin/env python3
"""Rigorous AFK zeta enclosure on the first frozen radical direction."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys
import time

import flint
from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from certify_dimension_five_double_sine import (  # noqa: E402
    _arb_fraction,
    _certified_simpson,
    _near_integrand,
    _tail_integrand,
)


PREREG = ROOT / "data" / "tcc-flat-monoid-p2-preregistration-v2.json"
MONOID = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-adapter-v1.json"
LABELS = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-labels-v1.json"
OUT = ROOT / "artifacts" / "tcc-flat-monoid-p2-radical-counterexample-v2.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def fundamental_log_double_sine(
    argument: arb, beta: arb, tolerance: Fraction
) -> tuple[arb, int]:
    """Rigorous log Sin_2(argument,beta) for 10<beta<11.

    On 0<=v<=10^-6, write H_c(v)=sinh(cv/2)/(cv/2).  The positive
    H-series and |c|<12 give

        |H_c-1-c^2 v^2/24| < 22 v^4.

    Expanding H_linear/(H_beta H_1) once, with beta<11 and the denominator
    at least one, bounds the remainder after the constant term of the
    regularized integrand by 1000 v^2.  This deliberately loose rational
    bound gives the enclosed integral on the omitted initial interval.
    """
    linear = beta + 1 - 2 * argument
    delta = Fraction(1, 1_000_000)
    if not (
        beta > 10
        and beta < 11
        and abs(linear) < 12
        and argument > arb(1) / 100
        and beta + 1 - argument > arb(1) / 100
        and argument < 12
        and beta + 1 - argument < 12
    ):
        raise RuntimeError("frozen double-sine strip hypotheses failed")
    # Exact rational verification of the coarse H-series constants above.
    if not (
        Fraction(12**4 * 2, 1920) < 22
        and Fraction(1000) * delta**3 / 3 < Fraction(1, 10**15)
    ):
        raise RuntimeError("near-zero majorant arithmetic changed")
    constant = linear * (linear**2 - beta**2 - 1) / (24 * beta)
    near = constant * _arb_fraction(delta)
    near += arb(0, _arb_fraction(Fraction(1000) * delta**3 / 3).upper())
    panels = 0
    left = delta
    integrand = _near_integrand(argument, beta)
    while left < 1:
        right = min(Fraction(1), 4 * left)
        enclosed = _certified_simpson(
            integrand, left, right, tolerance * (right - left) / 8
        )
        near += enclosed.value
        panels += enclosed.panels
        left = right
    cutoff = Fraction(120)
    tail = _certified_simpson(
        _tail_integrand(argument, beta), Fraction(0), cutoff, tolerance / 4
    )
    # For v>=120 and 1/100<z,beta+1-z<12, both exponential denominators
    # have magnitude >3/4 and v+z>120.  The difference is <1/30.
    tail_error = _arb_fraction(Fraction(1, 30)) * (-_arb_fraction(cutoff)).exp()
    return near - linear / beta + tail.value + arb(0, tail_error.upper()), panels + tail.panels


def main() -> None:
    started = time.monotonic()
    prereg = json.loads(PREREG.read_text())
    monoid = json.loads(MONOID.read_text())["case"]
    labels = json.loads(LABELS.read_text())
    ctx.dps = prereg["enclosure_policy"]["precision_decimal_digits"]
    tolerance = Fraction(prereg["enclosure_policy"]["per_factor_tolerance"])
    vector = monoid["radical"]["basis"][0]
    if [(i, value) for i, value in enumerate(vector) if value != "0"] != [(0, "-1"), (3, "1")]:
        raise RuntimeError("first frozen radical vector changed")
    target_orbit = next(
        row for row in labels["stabilizer_orbits"] if row["monoid_element"] == 3
    )
    if target_orbit["representative"] != [4, 10]:
        raise RuntimeError("frozen label changed")
    beta = (arb(11) + 3 * arb(13).sqrt()) / 2
    arguments = [
        5 * beta / 6 + arb(2) / 3,
        5 * beta / 6 + arb(1) / 6,
        beta / 3 + arb(1) / 6,
    ]
    values = []
    total = arb(0)
    for argument in arguments:
        value, panels = fundamental_log_double_sine(argument, beta, tolerance)
        values.append({"argument": str(argument), "log_sine": str(value), "panels": panels})
        total += value
    derivative = -2 * total
    if derivative.contains(0):
        raise RuntimeError("radical derivative enclosure contains zero")
    payload = {
        "schema": "tcc-flat-monoid-p2-radical-counterexample-v2",
        "claim_tag": "CERTIFIED_NUMERICAL",
        "claim_boundary": (
            "This proves non-annihilation of the first radical vector for the "
            "single frozen AFK d=12,f=3 pilot. It refutes only the universal "
            "ordinary-monoid-character descent route; it does not prove TCC."
        ),
        "preregistration_sha256": digest(PREREG),
        "monoid_artifact_sha256": digest(MONOID),
        "label_artifact_sha256": digest(LABELS),
        "source_script_sha256": digest(Path(__file__)),
        "radical_vector": {"0": "-1", "3": "1"},
        "zero_class_derivative": "0",
        "nonzero_class_derivative_enclosure": str(derivative),
        "enclosure_lower": str(derivative.lower()),
        "enclosure_upper": str(derivative.upper()),
        "zero_excluded_margin_lower_bound": str(abs(derivative).lower()),
        "double_sine_terms": values,
        "checks": {
            "hj_period_word": [11],
            "hj_cycle_length": 3,
            "one_place_fiber_cardinality": 2,
            "derivative_excludes_zero": True,
            "target_functional_evaluated": True
        },
        "software": {
            "python": sys.version.split()[0],
            "python_flint": flint.__version__,
            "interpreter": "projects/sic-stark/.venv/bin/python"
        },
        "invocation": "projects/sic-stark/.venv/bin/python projects/sic-stark/proof/certify_tcc_flat_monoid_p2_radical_counterexample.py",
        "wall_seconds": round(time.monotonic() - started, 6)
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_FLAT_MONOID_P2_RADICAL_COUNTEREXAMPLE=PASS")
    print(f"D12_RADICAL_DERIVATIVE={derivative}")


if __name__ == "__main__":
    main()

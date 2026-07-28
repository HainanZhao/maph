#!/usr/bin/env python3
"""Exact linear-algebra reduction of the remaining d=6 Stark bridge.

Write D_j for the three independent differenced ray-class derivatives,
Lambda for the primitive order-six component, and q for the quadratic
component.  In the Artin convention certified elsewhere,

    Lambda = D_0 + zeta_6 D_1 + zeta_6^2 D_2,
    q      = D_0 - D_1 + D_2.

This script verifies over Q that D_0=(2 Re(Lambda)+q)/3 and records the
orientation formula Im(Lambda)=sqrt(3)(D_1+D_2)/2.
"""

from __future__ import annotations

from fractions import Fraction
import json


LinearForm = tuple[Fraction, Fraction, Fraction]


def add(left: LinearForm, right: LinearForm) -> LinearForm:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def scale(value: Fraction, form: LinearForm) -> LinearForm:
    return tuple(value * coefficient for coefficient in form)  # type: ignore[return-value]


def main() -> None:
    real_primitive: LinearForm = (
        Fraction(1),
        Fraction(1, 2),
        Fraction(-1, 2),
    )
    imaginary_primitive_without_sqrt3: LinearForm = (
        Fraction(0),
        Fraction(1, 2),
        Fraction(1, 2),
    )
    quadratic: LinearForm = (
        Fraction(1),
        Fraction(-1),
        Fraction(1),
    )
    recovered_identity = scale(
        Fraction(1, 3),
        add(scale(Fraction(2), real_primitive), quadratic),
    )
    assert recovered_identity == (
        Fraction(1),
        Fraction(0),
        Fraction(0),
    )

    result = {
        "schema": "sic-stark-dimension-six-scalar-closure-v1",
        "primitive_component": (
            "Lambda=D_0+zeta_6*D_1+zeta_6^2*D_2"
        ),
        "real_primitive_coefficients": [
            str(value) for value in real_primitive
        ],
        "quadratic_component_coefficients": [
            str(value) for value in quadratic
        ],
        "recovered_identity_coefficients": [
            str(value) for value in recovered_identity
        ],
        "identity_formula": "D_0=(2*Re(Lambda)+q)/3",
        "imaginary_formula": (
            "Im(Lambda)=sqrt(3)*(D_1+D_2)/2"
        ),
        "imaginary_coefficients_without_sqrt3": [
            str(value)
            for value in imaginary_primitive_without_sqrt3
        ],
        "closure_lemma": (
            "If |Lambda|=|R|, q=r_0-r_1+r_2, D_0=r_0, "
            "Im(Lambda)>0, and Im(R)>0, then Lambda=R."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact source/convention audit for the local B1 theorem note."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "paper" / "quartic-stark-phase-note.tex"
GAUGE = ROOT / "docs" / "gauge-ambiguity-lemma-v1.md"
PREREG = ROOT / "docs" / "cycles-072-074-b1-preregistration.md"
AMENDMENT = (
    ROOT
    / "docs"
    / "cycles-072-074-b1-preregistration-amendment-v1.md"
)
ACTION_AUDIT = ROOT / "artifacts" / "b1-action-convention-audit-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"{label}: missing {needle!r}")


def gaussian_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    a, b = left
    c, d = right
    return (a * c - b * d, a * d + b * c)


def gaussian_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] + right[0], left[1] + right[1])


def gaussian_conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return (value[0], -value[1])


def gaussian_scale(scale: int, value: tuple[int, int]) -> tuple[int, int]:
    return (scale * value[0], scale * value[1])


I_POWERS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def i_power(exponent: int) -> tuple[int, int]:
    return I_POWERS[exponent % 4]


def exact_convention_checks() -> dict[str, bool]:
    right_covariance = True
    left_covariance = True
    signed_values: set[tuple[int, int]] = set()
    for sign in (-1, 1):
        for shift in range(4):
            character = gaussian_scale(sign, i_power(shift))
            signed_values.add(character)
            character_inverse = gaussian_conjugate(character)
            original_weights = [i_power(index) for index in range(4)]
            right_weights = [
                gaussian_scale(sign, i_power(index - shift))
                for index in range(4)
            ]
            expected_right = [
                gaussian_mul(character_inverse, weight)
                for weight in original_weights
            ]
            right_covariance &= right_weights == expected_right

            left_weights = [
                gaussian_scale(sign, i_power(index + shift))
                for index in range(4)
            ]
            expected_left = [
                gaussian_mul(character, weight)
                for weight in original_weights
            ]
            left_covariance &= left_weights == expected_left

    fourier_orthogonality = True
    for left_character in range(4):
        for right_character in range(4):
            inner = (0, 0)
            for group_index in range(4):
                left_value = i_power(left_character * group_index)
                right_value = gaussian_conjugate(
                    i_power(right_character * group_index)
                )
                inner = gaussian_add(
                    inner, gaussian_mul(left_value, right_value)
                )
            expected = (4, 0) if left_character == right_character else (0, 0)
            fourier_orthogonality &= inner == expected

    # The anti-unit log orbit is (x, y, -x, -y).
    log_basis = ((1, 0), (0, 1), (-1, 0), (0, -1))
    even_vanishing = True
    for even_character in (0, 2):
        coefficient = (0, 0)
        for group_index, basis_pair in enumerate(log_basis):
            weight = i_power(even_character * group_index)[0]
            coefficient = gaussian_add(
                coefficient, gaussian_scale(weight, basis_pair)
            )
        even_vanishing &= coefficient == (0, 0)

    return {
        "right_covariance_all_signed_c4_actions": right_covariance,
        "left_covariance_all_signed_c4_actions": left_covariance,
        "signed_character_image_is_mu4":
            signed_values == set(I_POWERS),
        "c4_fourier_matrix_exactly_invertible": fourier_orthogonality,
        "even_characters_cancel_on_anti_unit_orbit": even_vanishing,
    }


def main() -> int:
    note = NOTE.read_text()
    gauge = GAUGE.read_text()
    amendment = AMENDMENT.read_text()
    action = json.loads(ACTION_AUDIT.read_text())

    checks = {
        "root_of_unity_rider": r"\muK=\{\pm1\}" in note,
        "right_action_inverse_covariance":
            r"c_\psi(u^a)=\psi(a)^{-1}c_\psi(u)" in note,
        "left_action_covariance":
            r"c_\psi(a\mathbin{\cdot}u)=\psi(a)c_\psi(u)" in note,
        "even_component_step":
            "Step 1: even-component vanishing on both sides" in note,
        "conjugate_pair_step":
            "Step 2: conjugate-pair determination" in note,
        "abelian_step":
            "Step 3: inheritance of the abelian condition" in note,
        "representative_formula":
            r"\epsilon=\rho\,\eta^{h^{-1}}" in note,
        "human_only":
            "All email, messaging, submission, and other outbound actions"
            in note,
        "no_submission_before_b3":
            "before the preregistered B3 screen exists" in note,
        "roblot_doi":
            "10.2140/pjm.2013.266.391" in note,
        "observed_boundary":
            r"\textsc{observed}" in note,
        "ball_overlap_nonproof":
            "never proof of equality" in note,
    }
    failed = sorted(key for key, passed in checks.items() if not passed)
    if failed:
        raise AssertionError(f"failed note checks: {failed}")

    require(
        gauge,
        r"c_\chi(\eta^{\gamma^j})=i^{-j}c_\chi(\eta)",
        "gauge source",
    )
    require(
        amendment,
        r"c_\chi(u^a)=\chi(a)^{-1}c_\chi(u)",
        "amendment",
    )
    if action["status"] != "CONTAINED_NOTATIONAL_CORRECTION":
        raise AssertionError("unexpected action-audit status")

    exact_checks = exact_convention_checks()
    failed_exact = sorted(
        key for key, passed in exact_checks.items() if not passed
    )
    if failed_exact:
        raise AssertionError(f"failed exact convention checks: {failed_exact}")

    result = {
        "schema": "dedekind-stark-b1-note-audit-v1",
        "status": "PASS",
        "claim_tags": {
            "certified_case_theorem": "PROVED",
            "equivalence_theorem": "PROVED",
            "five_control_phase_statement": "OBSERVED",
        },
        "checks": checks,
        "exact_checks": exact_checks,
        "source_hashes": {
            "paper/quartic-stark-phase-note.tex": sha256(NOTE),
            "docs/gauge-ambiguity-lemma-v1.md": sha256(GAUGE),
            "docs/cycles-072-074-b1-preregistration.md": sha256(PREREG),
            "docs/cycles-072-074-b1-preregistration-amendment-v1.md":
                sha256(AMENDMENT),
            "artifacts/b1-action-convention-audit-v1.json":
                sha256(ACTION_AUDIT),
        },
        "circulation_authorized": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("B1_NOTE_AUDIT=PASS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Certify the mixed-signature Q(sqrt(35)) Engine-C packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from flint import acb, ctx, fmpq, fmpz_poly


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
BRIDGE = ROOT / "artifacts/engine-c-packet-bridge-v1.json"
OUTPUT = ROOT / "artifacts/engine-c-packet-root-reality-v1.json"
PRIOR_PACKET_FILES = [
    ROOT / "data/q7-p7-case-v1.json",
    ROOT / "data/q14-p7-case-v1.json",
    ROOT / "data/q57-norm27-case-v1.json",
    ROOT / "data/rq000021-case-v1.json",
    ROOT / "data/rq000108-case-v1.json",
    ROOT / "data/rq002955-case-v1.json",
    ROOT / "data/q33-p11-order10-case-v1.json",
    ROOT / "data/rq000458-dual-case-v1.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(coefficients: list[list[int]], argument: acb) -> acb:
    value = acb(0)
    for numerator, denominator in reversed(coefficients):
        value = value * argument + fmpq(numerator, denominator)
    return value


def integral_polynomial(coefficients: list[list[int]]) -> fmpz_poly:
    if any(denominator != 1 for _, denominator in coefficients):
        raise RuntimeError("defining polynomial is not integral")
    return fmpz_poly([numerator for numerator, _ in coefficients])


def parse_integer_polynomial(expression: str) -> fmpz_poly:
    compact = expression.replace(" ", "").replace("-", "+-")
    terms = [term for term in compact.split("+") if term]
    coefficients: dict[int, int] = {}
    for term in terms:
        match = re.fullmatch(r"([+-]?\d*)\*?x(?:\^(\d+))?", term)
        if match:
            raw, exponent = match.groups()
            coefficient = -1 if raw == "-" else 1 if raw in ("", "+") else int(raw)
            power = int(exponent) if exponent else 1
        else:
            coefficient = int(term)
            power = 0
        coefficients[power] = coefficients.get(power, 0) + coefficient
    degree = max(coefficients)
    return fmpz_poly([coefficients.get(power, 0) for power in range(degree + 1)])


def absolute_packet(payload: dict) -> str:
    for path in (
        ("w3", "absolute_packet_polynomial"),
        ("identification", "absolute_packet_polynomial"),
        ("packet", "absolute_polynomial"),
    ):
        value = payload
        try:
            for key in path:
                value = value[key]
            return value
        except KeyError:
            continue
    raise RuntimeError("missing prior packet polynomial")


def classified_roots(polynomial: fmpz_poly) -> tuple[list[acb], list[acb]]:
    real_roots = []
    nonreal_roots = []
    for root, multiplicity in polynomial.complex_roots():
        if multiplicity != 1:
            raise RuntimeError("packet root is not simple")
        if root.imag == 0:
            real_roots.append(root)
        elif not root.imag.contains(0):
            nonreal_roots.append(root)
        else:
            raise RuntimeError("root-reality ball is undecided")
    return real_roots, nonreal_roots


def main() -> None:
    ctx.dps = 90
    bridge = json.loads(BRIDGE.read_text())
    route_records = [
        row for row in bridge["records"] if row["case_id"] == "RQ-001280"
    ]
    if len(route_records) != 2:
        raise RuntimeError("Q(sqrt(35)) route count changed")

    route_results = []
    for record in route_records:
        if not all(record["artin_norms_conjugation_fixed"]):
            raise RuntimeError("exact conjugation-fixed assertion failed")
        normal_polynomial = integral_polynomial(
            record["normal_field_polynomial_coefficients"]
        )
        packet_polynomial = integral_polynomial(
            record["artin_labeled_packet_polynomial_coefficients"]
        )
        normal_roots = [
            root
            for root, multiplicity in normal_polynomial.complex_roots()
            if multiplicity == 1
        ]
        if len(normal_roots) != normal_polynomial.degree():
            raise RuntimeError("normal field roots are not simple")
        compatible = []
        for root_index, root in enumerate(normal_roots):
            residual = (
                evaluate(record["complex_conjugation_coefficients"], root)
                - root.conjugate()
            )
            if residual.real.contains(0) and residual.imag.contains(0):
                compatible.append((root_index, root))
        if len(compatible) != 8:
            raise RuntimeError(
                f"{record['route_id']}: expected 8 compatible embeddings"
            )

        real_roots, nonreal_roots = classified_roots(packet_polynomial)
        if len(real_roots) != 4 or len(nonreal_roots) != 4:
            raise RuntimeError("packet signature is not [4,2]")
        embedding_matches = []
        for root_index, root in compatible:
            permutation = []
            value_balls = []
            for coefficients in record["artin_norm_coefficients"]:
                value = evaluate(coefficients, root)
                if not value.imag.contains(0) or not value.real > 0:
                    raise RuntimeError("Artin norm is not positive real")
                matches = [
                    index
                    for index, packet_root in enumerate(real_roots)
                    if value.real.overlaps(packet_root.real)
                ]
                if len(matches) != 1:
                    raise RuntimeError("Artin norm/root match is not unique")
                permutation.append(matches[0])
                value_balls.append(str(value.real))
            if sorted(permutation) != [0, 1, 2, 3]:
                raise RuntimeError("Artin classes do not cover four real roots")
            embedding_matches.append(
                {
                    "normal_root_index": root_index,
                    "artin_label_to_real_root_index": permutation,
                    "positive_real_value_balls": value_balls,
                }
            )
        route_results.append(
            {
                "route_id": record["route_id"],
                "packet_signature": [4, 2],
                "compatible_normal_embedding_count": len(compatible),
                "conjugation_fixed_artin_class_count": 4,
                "embedding_matches": embedding_matches,
                "real_root_balls": [str(root.real) for root in real_roots],
                "nonreal_root_balls": [str(root) for root in nonreal_roots],
            }
        )

    prior = []
    for path in PRIOR_PACKET_FILES:
        payload = json.loads(path.read_text())
        polynomial = parse_integer_polynomial(absolute_packet(payload))
        real_roots, nonreal_roots = classified_roots(polynomial)
        prior.append(
            {
                "source": str(path.relative_to(ROOT)),
                "degree": polynomial.degree(),
                "real_root_count": len(real_roots),
                "nonreal_root_count": len(nonreal_roots),
                "signature": [
                    len(real_roots),
                    len(nonreal_roots) // 2,
                ],
            }
        )

    output = {
        "schema": "effective-stark-engine-c-packet-root-reality-v1",
        "claim_tag": "ENCLOSED_ROOT_REALITY_MATCH",
        "case_ids": ["RQ-001280", "RQ-001297"],
        "field": "Q(sqrt(35))",
        "packet_signature": [4, 2],
        "pattern": (
            "first packet produced by the generic Engine-C tranche; "
            "mixed signature [4,2], but not the first mixed-signature "
            "VERIFIED packet in the full corpus"
        ),
        "statement": (
            "For both imaginary-base routes, each of the four exact "
            "conjugation-fixed Artin norm classes matches exactly one of "
            "the four real roots. The remaining four roots form two "
            "nonreal conjugate pairs."
        ),
        "routes": route_results,
        "prior_verified_packet_reality_audit": prior,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (BRIDGE, SELF, *PRIOR_PACKET_FILES)
        },
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print("ROUTE_COUNT=2")
    print("REAL_ROOT_COUNT=4")
    print("NONREAL_CONJUGATE_PAIR_COUNT=2")
    print("FIRST_GENERIC_ENGINE_C_PACKET_IS_NON_TOTALLY_REAL=1")
    print("FIRST_NON_TOTALLY_REAL_PACKET_IN_FULL_CORPUS=0")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()

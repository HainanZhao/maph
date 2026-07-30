#!/usr/bin/env python3
"""Match conjugation-fixed Artin classes to real roots for three e=6 packets."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from flint import acb, ctx


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
BRIDGE = ROOT / "artifacts/engine-c-e6-tranche-01-packet-bridge-v1.json"
GENERIC = ROOT / "scripts/certify_engine_c_packet_root_reality.py"
OUTPUT = ROOT / "artifacts/engine-c-e6-tranche-01-root-reality-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generic():
    spec = importlib.util.spec_from_file_location("root_reality", GENERIC)
    if spec is None or spec.loader is None:
        raise RuntimeError("root-reality import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    ctx.dps = 90
    generic = load_generic()
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    results = []
    for record in bridge["records"]:
        key = (record["case_id"], record["route_id"])
        if not all(record["artin_norms_conjugation_fixed"]):
            raise RuntimeError(f"{key}: exact conjugation-fixed gate failed")
        normal_polynomial = generic.integral_polynomial(
            record["normal_field_polynomial_coefficients"]
        )
        packet_polynomial = generic.integral_polynomial(
            record["artin_labeled_packet_polynomial_coefficients"]
        )
        normal_roots = [
            root
            for root, multiplicity in normal_polynomial.complex_roots()
            if multiplicity == 1
        ]
        compatible = []
        for root_index, root in enumerate(normal_roots):
            residual = (
                generic.evaluate(
                    record["complex_conjugation_coefficients"], root
                )
                - root.conjugate()
            )
            if residual.real.contains(0) and residual.imag.contains(0):
                compatible.append((root_index, root))
        if len(compatible) != 8:
            raise RuntimeError(f"{key}: compatible embedding count changed")
        real_roots, nonreal_roots = generic.classified_roots(
            packet_polynomial
        )
        if len(real_roots) != 4 or len(nonreal_roots) != 4:
            raise RuntimeError(f"{key}: packet signature is not [4,2]")
        matches = []
        for root_index, root in compatible:
            permutation = []
            for coefficients in record["artin_norm_coefficients"]:
                value = generic.evaluate(coefficients, root)
                if not value.imag.contains(0) or not value.real > 0:
                    raise RuntimeError(f"{key}: norm is not positive real")
                overlap = [
                    index
                    for index, packet_root in enumerate(real_roots)
                    if value.real.overlaps(packet_root.real)
                ]
                if len(overlap) != 1:
                    raise RuntimeError(f"{key}: root match not unique")
                permutation.append(overlap[0])
            if sorted(permutation) != [0, 1, 2, 3]:
                raise RuntimeError(f"{key}: Artin roots not exhaustive")
            matches.append(
                {
                    "normal_root_index": root_index,
                    "artin_label_to_real_root_index": permutation,
                }
            )
        results.append(
            {
                "case_id": record["case_id"],
                "route_id": record["route_id"],
                "packet_signature": [4, 2],
                "compatible_normal_embedding_count": 8,
                "conjugation_fixed_artin_class_count": 4,
                "embedding_matches": matches,
                "real_root_balls": [str(root.real) for root in real_roots],
                "nonreal_root_balls": [str(root) for root in nonreal_roots],
            }
        )
    payload = {
        "schema": "effective-stark-engine-c-e6-tranche-01-root-reality-v1",
        "claim_tag": "ENCLOSED_ROOT_REALITY_MATCH",
        "field_count": 3,
        "route_count": 6,
        "all_packet_signatures": [4, 2],
        "statement": (
            "For every route, the four exact conjugation-fixed Artin "
            "norm classes match the four real packet roots uniquely; "
            "the remaining roots form two nonreal conjugate pairs."
        ),
        "records": results,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (BRIDGE, GENERIC, SELF)
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("FIELD_COUNT=3")
    print("ROUTE_COUNT=6")
    print("ALL_FOUR_REAL_ROOT_MATCHES_ENCLOSED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()

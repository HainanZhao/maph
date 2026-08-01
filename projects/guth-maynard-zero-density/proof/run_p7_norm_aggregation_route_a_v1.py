#!/usr/bin/env python3
"""Route A: exact finite residue-ring calculation for the P7 witness.

This route does not import the preselected character values.  It enumerates
the relevant finite quotients of Z[i] and calculates the nontrivial quotient
characters and their values from multiplication tables.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_norm_aggregation_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-norm-aggregation-route-a-v1.json"
SELF = Path(__file__).resolve()


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] + w[0], z[1] + w[1]


def sub(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] - w[0], z[1] - w[1]


def mul(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def conjugate(z: tuple[int, int]) -> tuple[int, int]:
    return z[0], -z[1]


def power(z: tuple[int, int], exponent: int) -> tuple[int, int]:
    value = (1, 0)
    for _ in range(exponent):
        value = mul(value, z)
    return value


def divides(z: tuple[int, int], divisor: tuple[int, int]) -> bool:
    """Whether divisor divides z in Z[i], using exact rationalized division."""
    numerator = mul(z, conjugate(divisor))
    norm = divisor[0] * divisor[0] + divisor[1] * divisor[1]
    return numerator[0] % norm == 0 and numerator[1] % norm == 0


def equivalent_mod_pi_power(z: tuple[int, int], w: tuple[int, int], exponent: int) -> bool:
    return divides(sub(z, w), power((1, 1), exponent))


def residue_classes_pi(exponent: int) -> list[tuple[int, int]]:
    """Represent O/(1+i)^e by exact lattice equivalence, not a stored list."""
    expected = 2**exponent
    representatives: list[tuple[int, int]] = []
    bound = 2**exponent
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            z = (a, b)
            if not any(equivalent_mod_pi_power(z, r, exponent) for r in representatives):
                representatives.append(z)
                if len(representatives) == expected:
                    return representatives
    raise RuntimeError("failed to find all residue classes in certified finite box")


def residue_product_index(classes: list[tuple[int, int]], z: tuple[int, int], w: tuple[int, int], exponent: int) -> int:
    product = mul(z, w)
    indices = [index for index, candidate in enumerate(classes) if equivalent_mod_pi_power(product, candidate, exponent)]
    require(len(indices) == 1, "residue product did not have a unique class")
    return indices[0]


def pi_power_unit_quotient(exponent: int) -> dict[str, object]:
    classes = residue_classes_pi(exponent)
    pi = (1, 1)
    units = [z for z in classes if not divides(z, pi)]
    mu4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    image_indices = {
        next(index for index, candidate in enumerate(classes) if equivalent_mod_pi_power(unit, candidate, exponent))
        for unit in mu4
    }
    unit_indices = {classes.index(z) for z in units}
    quotient_orbits: list[set[int]] = []
    unassigned = set(unit_indices)
    while unassigned:
        seed = min(unassigned)
        orbit = {
            residue_product_index(classes, classes[seed], unit, exponent)
            for unit in mu4
        }
        require(orbit <= unit_indices, "unit orbit left unit group")
        quotient_orbits.append(orbit)
        unassigned -= orbit
    require(not unassigned, "unassigned quotient orbit")
    return {
        "e": exponent,
        "ring_cardinality": len(classes),
        "unit_cardinality": len(units),
        "mu4_image_cardinality": len(image_indices),
        "quotient_cardinality": len(quotient_orbits),
        "quotient_orbit_sizes": sorted(len(orbit) for orbit in quotient_orbits),
    }


def mod_three_classes() -> list[tuple[int, int]]:
    return [(a, b) for a in range(3) for b in range(3)]


def mod_three_product(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    product = mul(z, w)
    return product[0] % 3, product[1] % 3


def mod_three_unit_quotient() -> dict[str, object]:
    classes = mod_three_classes()
    units = [z for z in classes if z != (0, 0)]
    mu4 = {(1, 0), (2, 0), (0, 1), (0, 2)}
    require(len(units) == 8 and len(mu4) == 4, "F_9 unit data incorrect")
    quotient_orbits: list[set[tuple[int, int]]] = []
    unassigned = set(units)
    while unassigned:
        seed = min(unassigned)
        orbit = {mod_three_product(seed, unit) for unit in mu4}
        require(orbit <= set(units), "F_9 unit orbit escaped")
        quotient_orbits.append(orbit)
        unassigned -= orbit
    require(len(quotient_orbits) == 2, "(O/(3))^*/mu_4 is not order two")
    identity_orbit = next(orbit for orbit in quotient_orbits if (1, 0) in orbit)
    nonidentity_orbit = next(orbit for orbit in quotient_orbits if (1, 0) not in orbit)
    def quotient_character(z: tuple[int, int]) -> int:
        return 1 if z in identity_orbit else -1
    plus = (4 % 3, 1 % 3)
    minus = (4 % 3, (-1) % 3)
    return {
        "field_cardinality": len(classes),
        "unit_cardinality": len(units),
        "mu4_cardinality": len(mu4),
        "quotient_cardinality": len(quotient_orbits),
        "character_values": {"4+i": quotient_character(plus), "4-i": quotient_character(minus)},
        "fourth_powers": {"1+i": power((1, 1), 4), "1-i": power((1, -1), 4)},
    }


def mod_four_unit_quotient_and_values() -> dict[str, object]:
    data = pi_power_unit_quotient(4)
    classes = residue_classes_pi(4)
    mu4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # The quotient has two classes.  The nontrivial quotient character is 1 on
    # the mu_4 orbit, so only membership is needed for these two prime ideals.
    plus = (4, 1)
    minus = (4, -1)
    values: dict[str, int] = {}
    for label, z in (("4+i", plus), ("4-i", minus)):
        values[label] = 1 if any(equivalent_mod_pi_power(z, unit, 4) for unit in mu4) else -1
    data["character_values"] = values
    data["congruences"] = {"4+i": "i mod (1+i)^4", "4-i": "-i mod (1+i)^4"}
    return data


def source_integrity() -> dict[str, object]:
    values: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(digest(path) == row["sha256"], f"pinned source hash mismatch: {label}")
        values[label] = {"path": row["path"], "sha256": row["sha256"]}
    text = (ROOT / C.SOURCES["zaman_tex"]["path"]).read_text(encoding="utf-8")
    require("\\Cl(\\kq) := I(\\kq)/P_{\\kq}" in text, "Zaman ray-class definition not found")
    require("The \\emph{conductor}" in text and "primitive modulo" in text, "Zaman conductor convention not found")
    return values


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    pi_rows = [pi_power_unit_quotient(e) for e in range(1, 5)]
    for row, expected in zip(pi_rows, (1, 1, 1, 2), strict=True):
        require(row["quotient_cardinality"] == expected, "incorrect proper pi-power quotient")
    mod3 = mod_three_unit_quotient()
    mod4 = mod_four_unit_quotient_and_values()
    require(mod3["character_values"] == {"4+i": -1, "4-i": -1}, "(3)-character values incorrect")
    require(mod4["character_values"] == {"4+i": 1, "4-i": 1}, "(1+i)^4-character values incorrect")
    return {
        "artifact_id": "p7-norm-aggregation-route-a-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "claim_boundary": "Exact finite ray-quotient and conductor calculation only. It does not establish a joint Hecke large-value, density, or short-interval theorem.",
        "route": "A: exhaustive exact residue-ring quotient calculation",
        "source_integrity": source_integrity(),
        "ray_class_reduction": {
            "status": "PROVED",
            "statement": "Since h(Q(i))=1 and there are no real places, Cl(f) is identified with (Z[i]/f)^*/image(mu_4) for the finite moduli used here.",
            "source_locator": C.SOURCES["zaman_tex"]["locators"],
        },
        "mod_3": {"status": "PROVED", **mod3, "exact_conductor": "(3): only proper divisor is (1), while the quotient character is nontrivial."},
        "pi_power_quotients": {"status": "PROVED", "rows": pi_rows},
        "mod_pi4": {"status": "PROVED", **mod4, "exact_conductor": "(1+i)^4: all proper pi-power quotients after mu_4 are trivial, whereas the displayed quotient has order two."},
        "witness": {
            "status": "PROVED",
            "factorization": C.SPLIT_FACTORIZATION,
            "A_chi_3_17": sum(mod3["character_values"].values()),
            "A_chi_pi4_17": sum(mod4["character_values"].values()),
            "type_mismatch": "The two fixed-character norm-coefficient vectors differ at n=17 (in the dyadic block 16<n<=32).",
        },
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/run_p7_norm_aggregation_route_a_v1.py --write", "check_command": "python3 proof/run_p7_norm_aggregation_route_a_v1.py --check"},
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    started = time.monotonic_ns()
    data = render(report())
    elapsed = time.monotonic_ns() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "route A exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "route A exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed Route A artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "Route A artifact mismatch; issue a correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)

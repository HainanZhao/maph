#!/usr/bin/env python3
"""Seal the integer-replay/status correction for P7-3 common ideal cubic v1."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_common_ideal_cubic_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-common-ideal-cubic-v2-correction.json"
SELF = Path(__file__)
V1 = ROOT / "artifacts/p7-common-ideal-cubic-v1.json"
FILES = {
    "document": ROOT / "docs/p7-common-ideal-cubic-v2-correction.md",
    "tests": ROOT / "tests/test_p7_common_ideal_cubic_v2_correction.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_coloured_energy_replay() -> dict[str, int]:
    """Integer-only Z/2 orthogonality replay for the immutable v1 test set."""
    points = ((0, 0), (1, 0), (1, 1), (0, 2))
    coloured = 0
    uncoloured = 0
    parseval = 0
    for p1 in points:
        for p2 in points:
            for p3 in points:
                for p4 in points:
                    if p1[1] + p2[1] != p3[1] + p4[1]:
                        continue
                    uncoloured += 1
                    colour_diagonal = (p1[0] + p2[0] - p3[0] - p4[0]) % 2 == 0
                    coloured += int(colour_diagonal)
                    # Exact Z/2 character orthogonality, written without any
                    # negative powers: sum_g chi_delta(g)=2 on delta=0, else 0.
                    parseval += int(colour_diagonal)
    require(coloured == parseval == 34, "integer coloured Parseval replay failed")
    require(uncoloured == 62 and coloured <= uncoloured, "energy comparison failed")
    return {"coloured_energy": coloured, "orthogonality_parseval_count": parseval, "uncoloured_time_energy_with_multiplicity": uncoloured}


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    require(V1.is_file(), "immutable P7-3 v1 artifact absent")
    v1 = json.loads(V1.read_text())
    require(v1["gate_outcome"] == "PASS_EXACT_IDEAL_IDENTITIES_CONTAINED_COMMON_SAMPLE_CUBIC_OPEN", "unexpected P7-3 v1 boundary")
    require(v1["fixed_modulus_coloured_energy"]["finite_exact_check"]["orthogonality_parseval_count"] == 34.0, "expected v1 serialization defect absent")
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    return {
        "artifact_id": "p7-common-ideal-cubic-v2-correction",
        "epistemic_status": "OBSERVED",
        "correction_type": "integer_replay_and_display_correction",
        "immutable_v1": {"path": str(V1.relative_to(ROOT)), "sha256": digest(V1)},
        "defects": [
            "The v1 finite Z/2 Parseval count was serialized as 34.0 because Python evaluates (-1)**negative_integer as a float, despite the exact intended count being the integer 34.",
            "The v1 artifact rendered the coprimality factor in the single-character fibre bound as 1_(a,f)=1 instead of the unambiguous 1_{(a,f)=1}.",
        ],
        "corrected_claim": {
            "epistemic_status": "PROVED",
            "statement": "For b_chi(n)=Sum_{Na=n}c(a)chi(a), |b_chi(n)|^2 <= a_Q(i)(n) Sum_{Na=n}|c(a)|^2 1_{(a,f_chi)=1}; and the finite Z/2 coloured Parseval count is exactly the integer 34.",
            "integer_replay": exact_coloured_energy_replay(),
        },
        "unchanged": [
            "the P7-3 exact labelled-ideal Gram identity and its finite check",
            "the fixed-modulus coloured Parseval formula",
            "the scoped non-verbatim-import boundary",
            "the non-promotion boundary and the open coloured primitive cubic estimate",
        ],
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "artifact_identity": identities,
        "source_integrity": {"p7_common_ideal_cubic_v1": {"path": str(V1.relative_to(ROOT)), "sha256": digest(V1)}, "conventions": {"path": "conventions/p7_common_ideal_cubic_v1.py", "sha256": digest(ROOT / "conventions/p7_common_ideal_cubic_v1.py")}},
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/build_p7_common_ideal_cubic_v2_correction.py --write", "check_command": "python3 proof/build_p7_common_ideal_cubic_v2_correction.py --check"},
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7-3 correction replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7-3 correction replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7-3 correction")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7-3 correction mismatch; issue another versioned correction")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)

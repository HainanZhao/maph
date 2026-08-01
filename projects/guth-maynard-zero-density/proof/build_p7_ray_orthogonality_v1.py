#!/usr/bin/env python3
"""Seal the P7-2 exact projector and scoped Hecke L2 large-sieve gate."""
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
from conventions import p7_ray_orthogonality_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-ray-orthogonality-v1.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_ray_orthogonality_v1.py",
    "document": ROOT / "docs/p7-ray-orthogonality-v1.md",
    "tests": ROOT / "tests/test_p7_ray_orthogonality_v1.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def moebius(exponents: tuple[int, ...]) -> int:
    """Ideal Moebius value on a formal prime-ideal factorization."""
    if any(e >= 2 for e in exponents):
        return 0
    return -1 if sum(exponents) % 2 else 1


def divisors(exponents: tuple[int, ...]):
    if not exponents:
        yield ()
        return
    head, *tail = exponents
    for e in range(head + 1):
        for rest in divisors(tuple(tail)):
            yield (e,) + rest


def exact_convolution_checks() -> list[dict[str, object]]:
    """Finite exact checks of mu*1=epsilon on representative ideal lattices."""
    rows = []
    for exponents in ((), (1,), (2,), (3,), (1, 1), (2, 1), (1, 1, 1)):
        value = sum(moebius(tuple(e - d for e, d in zip(exponents, divisor))) for divisor in divisors(exponents))
        rows.append({"factor_exponents": list(exponents), "sum_{d|f}mu(f/d)": value, "expected": 1 if not exponents else 0})
    require(all(row["sum_{d|f}mu(f/d)"] == row["expected"] for row in rows), "ideal Moebius convolution check failed")
    return rows


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    source_rows = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"pinned source mismatch: {label}")
        source_rows[label] = dict(row)
    prereg = json.loads((ROOT / C.SOURCES["p7_preregistration_v2"]["path"]).read_text())
    gate = next(item for item in prereg["gates"] if item["id"] == C.GATE_ID)
    require(gate["state"] == "UNEXECUTED", "P7-2 preregistration state unexpectedly changed")
    p7_1 = json.loads((ROOT / C.SOURCES["p7_norm_aggregation_v2"]["path"]).read_text())
    require(p7_1["gate_outcome"] == "PASS_SCOPED_TYPE_MISMATCH_AND_NORMALIZATION", "P7-1 prerequisite missing")
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    return {
        "artifact_id": "p7-ray-orthogonality-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "PASS_EXACT_PROJECTOR_AND_SCOPED_L2_LARGE_SIEVE",
        "claim_boundary": "Exact ray-class character projectors and a source-scoped L2 large-sieve specialization only. No cubic-energy, large-value, zero-density, detector, or prime-ideal theorem is proved.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "family_indexing": {
            "field": C.FIELD,
            "shell": C.SHELL,
            "primitive_member": "one pair (f,chi) for every finite ray-class character chi with exact finite conductor f; characters are not quotiented by inverse, conjugation, or Galois action",
            "archimedean_type": C.ARCHIMEDEAN_TYPE,
            "coefficient_extension": C.IDEAL_EXTENSION,
        },
        "exact_projectors": {
            "complete_domain": "For integral ideals a,b with (ab,f)=1, let Cl(f)=I(f)/P_f and X(f)=Hom(Cl(f),C^x).",
            "complete_identity": "C_f(a,b):=sum_{chi in X(f)}chi(a)conj(chi(b))=|Cl(f)| if [a]_f=[b]_f in Cl(f), and 0 otherwise.",
            "conductor_partition": "For (ab,f)=1, C_f(a,b)=sum_{d|f}P_d(a,b), where P_d sums characters of exact finite conductor d evaluated on a,b.",
            "primitive_identity": "For arbitrary integral ideals a,b, P_f^0(a,b)=1_{(ab,f)=1} sum_{d|f} mu_K(f/d)|Cl(d)|1_{[a]_d=[b]_d in Cl(d)}.",
            "proof_route": "finite abelian-character orthogonality; unique finite conductor (Zaman lines 298--303); ideal Moebius inversion on the divisor lattice",
            "finite_convolution_checks": exact_convolution_checks(),
            "coprimality_warning": "Dropping the outside indicator 1_{(ab,f)=1} makes the primitive formula false for the zero-extended character convention.",
        },
        "large_sieve": {
            "source_theorem": C.THORNER_2019_LARGE_SIEVE["source"],
            "source_statement": C.THORNER_2019_LARGE_SIEVE["statement"],
            "checked_specialization": C.THORNER_2019_LARGE_SIEVE["checked_specialization"],
            "shell_conclusion": C.THORNER_2019_LARGE_SIEVE["conclusion"],
            "common_coefficient_requirement": "c(a) is a single function of the ideal a, fixed before f, chi, m, and t are summed. The selected family uses m=0 only, hence lambda_0=1.",
            "character_dependent_boundary": "After norm collapse, b_chi(n)=sum_{Na=n}c(a)chi(a) generally depends on chi. P7-1 proved that the basic A_chi(n) already differs within one shell. The ideal-form source theorem still applies when such b_chi is the collapse of one common c, but it cannot be invoked for arbitrary independently chosen b_chi(n), nor converted verbatim into a common integer coefficient vector.",
            "projector_boundary": "The signed Moebius primitive projector is exact; it is not a positive replacement for the source primitive large sieve and does not itself control a modulus sum.",
            "unresolved_for_p7_3": "An ideal-indexed common-sample cubic/energy inequality with repeated-norm and character-coupled terms remains open.",
        },
        "source_integrity": source_rows,
        "artifact_identity": identities,
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {
            "script": str(SELF.relative_to(ROOT)),
            "script_sha256": digest(SELF),
            "runtime": runtime,
            "write_command": "python3 proof/build_p7_ray_orthogonality_v1.py --write",
            "check_command": "python3 proof/build_p7_ray_orthogonality_v1.py --check",
        },
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7-2 replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7-2 replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7-2 artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7-2 artifact mismatch; issue a versioned correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""Certified primitive Engine-C L'(0) targets from exact coefficients.

For gamma shifts [0,1], write Q=sqrt(N)/(2*pi) and
theta(t)=sum a_n exp(-n*t/Q).  Splitting its Mellin transform at one
gives

  L'(0,chi) = I_0 + W I_1,
  I_0 = sum a_n Gamma(0,n/Q),
  I_1 = sum conjugate(a_n) Q exp(-n/Q)/n,

where W=theta(1)/conjugate(theta(1)).  All finite sums are Arb balls.
The omitted coefficients use |a_n| <= d(n) <= n, producing explicit
geometric tail balls.  PARI supplies exact coefficients only; none of
its floating-point L-value machinery enters the certificate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-theta-evaluator-cases-v1.json"
CHARACTER_CERT = ROOT / "artifacts/engine-c-character-selection-v1.json"
GP_SOURCE = ROOT / "scripts/export_engine_c_lfunction_coefficients.gp"
OUTPUT = ROOT / "artifacts/engine-c-theta-targets-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-theta-targets-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def complex_error(radius: arb) -> acb:
    upper = radius.upper()
    return acb(arb(0, upper), arb(0, upper))


def run_gp(record: dict, limit: int, source: str) -> tuple[int, list[tuple[int, int]], str]:
    prelude = "\n".join(
        [
            f"CM_BASE_POLYNOMIAL={record['cm_base_polynomial']};",
            f"CM_CONDUCTOR={record['cm_conductor']};",
            f"CM_CHARACTER={record['selected_cm_character']};",
            f"COEFFICIENT_LIMIT={limit};",
        ]
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=prelude + "\n" + source,
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=600,
        check=False,
    )
    if (
        completed.returncode != 0
        or "EXACT_COEFFICIENT_EXPORT_COMPLETE=1" not in completed.stdout
    ):
        raise RuntimeError(completed.stdout + "\n" + completed.stderr)
    match = re.search(r"^ANALYTIC_CONDUCTOR=(\d+)$", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("missing analytic conductor")
    conductor = int(match.group(1))
    coefficients: list[tuple[int, int]] = []
    for line in completed.stdout.splitlines():
        if not line.startswith("A "):
            continue
        _, index, real, imag = line.split()
        if int(index) != len(coefficients) + 1:
            raise RuntimeError("coefficient index discontinuity")
        coefficients.append((int(real), int(imag)))
    if len(coefficients) != limit:
        raise RuntimeError(f"expected {limit} coefficients")
    return conductor, coefficients, completed.stdout


def evaluate(conductor: int, coefficients: list[tuple[int, int]]) -> dict:
    limit = len(coefficients)
    Q = arb(conductor).sqrt() / (2 * arb.pi())
    c = 1 / Q
    q = (-c).exp()
    theta = acb(0)
    integral_zero = acb(0)
    integral_one = acb(0)
    for n, (real, imag) in enumerate(coefficients, start=1):
        coefficient = acb(real, imag)
        argument = arb(n) * c
        exponential = (-argument).exp()
        theta += coefficient * exponential
        integral_zero += coefficient * acb(argument).gamma_upper(0)
        integral_one += (
            coefficient.conjugate() * (Q / arb(n)) * exponential
        )

    # d(n) <= n.  The theta tail retains the extra n; the two
    # integral tails each lose it against 1/n.
    theta_tail = q ** (limit + 1) * (
        arb(limit + 1) - arb(limit) * q
    ) / (1 - q) ** 2
    integral_tail = Q * q ** (limit + 1) / (1 - q)
    theta += complex_error(theta_tail)
    integral_zero += complex_error(integral_tail)
    integral_one += complex_error(integral_tail)
    if theta.contains(0):
        raise RuntimeError("theta(1) ball contains zero")
    root_number = theta / theta.conjugate()
    target = integral_zero + root_number * integral_one
    return {
        "analytic_conductor": conductor,
        "Q_ball": str(Q),
        "theta_tail_bound": str(theta_tail),
        "integral_tail_bound_each": str(integral_tail),
        "theta_one_ball": str(theta),
        "root_number_ball": str(root_number),
        "root_number_modulus_ball": str(abs(root_number)),
        "lprime_zero_ball": str(target),
        "lprime_zero_modulus_ball": str(abs(target)),
        "maximum_component_radius": str(
            max(target.real.rad(), target.imag.rad())
        ),
    }


def overlaps(left: acb, right: acb) -> bool:
    return left.real.overlaps(right.real) and left.imag.overlaps(right.imag)


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    character_cert = json.loads(CHARACTER_CERT.read_text(encoding="utf-8"))
    selected = {
        (row["case_id"], row["route_id"]): row["selected_cm_character"]
        for row in character_cert["records"]
    }
    source = GP_SOURCE.read_text(encoding="utf-8")
    ctx.dps = config["working_digits"]
    records = []
    transcripts = []
    target_balls: dict[tuple[str, str], acb] = {}
    for record in config["records"]:
        key = (record["case_id"], record["route_id"])
        if selected.get(key) != record["selected_cm_character"].replace(",", ", "):
            raise RuntimeError(f"selected-character artifact mismatch for {key}")
        conductor, coefficients, transcript = run_gp(
            record, config["coefficient_limit"], source
        )
        if conductor != record["expected_analytic_conductor"]:
            raise RuntimeError(f"analytic conductor changed for {key}")
        result = evaluate(conductor, coefficients)
        records.append({**record, **result})
        transcripts.append(
            f"===== {record['case_id']} {record['route_id']} =====\n"
            f"{transcript}"
        )
        # Recompute only for the exact overlap assertion; cost is negligible.
        parsed = result["lprime_zero_ball"].replace("j", "")
        del parsed  # string output is archival; retain live ball below.
        Q = arb(conductor).sqrt() / (2 * arb.pi())
        c = 1 / Q
        q = (-c).exp()
        theta = acb(0)
        i0 = acb(0)
        i1 = acb(0)
        for n, (real, imag) in enumerate(coefficients, start=1):
            aa = acb(real, imag)
            z = arb(n) * c
            ez = (-z).exp()
            theta += aa * ez
            i0 += aa * acb(z).gamma_upper(0)
            i1 += aa.conjugate() * Q / arb(n) * ez
        theta_tail = q ** (len(coefficients) + 1) * (
            arb(len(coefficients) + 1) - arb(len(coefficients)) * q
        ) / (1 - q) ** 2
        integral_tail = Q * q ** (len(coefficients) + 1) / (1 - q)
        theta += complex_error(theta_tail)
        i0 += complex_error(integral_tail)
        i1 += complex_error(integral_tail)
        target_balls[key] = i0 + (theta / theta.conjugate()) * i1

    new_left = target_balls[("RQ-001280", "Qsqrt(-10)")]
    new_right = target_balls[("RQ-001280", "Qsqrt(-14)")]
    if not overlaps(new_left, new_right):
        raise RuntimeError("two exact-reinduction routes give disjoint targets")

    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-theta-targets-v1",
        "claim_tag": "ENCLOSED_PRIMITIVE_LPRIME_TARGETS",
        "method": "theta Mellin split with explicit d(n)<=n tails",
        "coefficient_limit": config["coefficient_limit"],
        "working_digits": config["working_digits"],
        "records": records,
        "new_case_two_route_target_overlap": True,
        "trusted_base": (
            "exact PARI lfunan coefficients; Arb elementary, incomplete-"
            "gamma, and ball arithmetic; explicit geometric tails"
        ),
        "excluded_from_proof_chain": "PARI lfun and bnrL1 point values",
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (CONFIG, CHARACTER_CERT, GP_SOURCE, SELF)
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"ROUTE_COUNT={len(records)}")
    print("TWO_ROUTE_TARGET_OVERLAP=1")
    print("ENCLOSED_PRIMITIVE_LPRIME_TARGETS=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Replay the corrected-hypothesis T-smooth divisor-chain repair for P6 F08.

The pinned CGL v2 TeX uses the phrase ``q is T-smooth`` but does not define
it.  This record never supplies a meaning to that preprint.  Instead it
proves a separate, explicitly amended statement with the standard hypothesis
that every prime divisor p of q satisfies p <= T, where T >= 1.

The repair is deliberately narrow.  It proves the elementary divisor chain
and its use in the smooth subdivision range, conditional on the already
separate large-value, detector, primitive-transfer, multiplicity, and cited
analytic inputs.  It neither revises the source nor repairs arbitrary
q1-sensitive formulae.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import sys
import tarfile
import time
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v1.json"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"
PREREG = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
RECONCILIATION = ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json"
PRIMITIVE_TRANSFER = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
DETECTOR_REPAIR = ROOT / "artifacts/p6-detector-qt-tail-v1.json"
CONVENTIONS = ROOT / "conventions/baseline.py"
CGL_TAR_SHA256 = "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae"
TEX_MEMBER = "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
WALL_CAP_NS = 60_000_000_000
# The active container's CPython baseline is roughly 600 MiB.  The finite
# check is small relative to that baseline; retain a one-GiB hard ceiling.
RSS_CAP_KIB = 1_048_576


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prime_factors(n: int) -> list[int]:
    require(n >= 1, "prime factorization requires a positive integer")
    output: list[int] = []
    divisor = 2
    remaining = n
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            output.append(divisor)
            remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        output.append(remaining)
    return output


def divisors(n: int) -> list[int]:
    output = [1]
    for prime in prime_factors(n):
        output += [value * prime for value in output]
    return sorted(set(output))


def is_t_smooth(q: int, t: Fraction) -> bool:
    require(q >= 1 and t >= 1, "smoothness range requires q positive and T>=1")
    return all(Fraction(prime, 1) <= t for prime in set(prime_factors(q)))


def max_divisor_below(q: int, threshold: Fraction) -> int:
    """Largest d|q with d^(5/6)<threshold, for rational test thresholds."""
    candidates = [d for d in divisors(q) if Fraction(d**5, 1) < threshold**6]
    require(candidates, "d=1 must be available whenever threshold>1")
    return max(candidates)


def finite_chain(q: int, t: Fraction, threshold: Fraction) -> list[int]:
    """Construct the general proof's chain for finite rational sanity checks."""
    require(q >= 1 and t >= 1 and threshold > 1, "finite chain range changed")
    require(is_t_smooth(q, t), "finite chain requires corrected T-smoothness")
    if Fraction(q**5, 1) < threshold**6:
        return [q]
    current = max_divisor_below(q, threshold)
    output = [current]
    while current < q:
        quotient = q // current
        require(q % current == 0 and quotient > 1, "chain divisor lost")
        prime = prime_factors(quotient)[0]
        next_value = current * prime
        require(q % next_value == 0, "prime-power extension is not a divisor")
        require(current < next_value <= current * t, "one-prime smooth extension failed")
        output.append(next_value)
        current = next_value
    return output


def source_checks() -> dict[str, object]:
    require(digest(CGL_TAR) == CGL_TAR_SHA256, "pinned CGL v2 tar hash changed")
    with tarfile.open(CGL_TAR, "r") as archive:
        member = archive.getmember(TEX_MEMBER)
        extracted = archive.extractfile(member)
        require(extracted is not None, "pinned CGL TeX member is absent")
        lines = extracted.read().decode("utf-8").splitlines()
    require("If $q$ is $T$-smooth" in lines[181], "CGL TeX 182 smooth conclusion changed")
    require("If $q$ is $T$-smooth then we have" in lines[2265], "CGL TeX 2266 smooth LVE claim changed")
    require("Now suppose that $q$ is $T$-smooth" in lines[2345], "CGL TeX 2346 chain anchor changed")
    require("largest divisor of $q$" in lines[2345], "CGL TeX 2346 maximal-divisor anchor changed")
    require("we can pick $q_2>q_1$" in lines[2349], "CGL TeX 2350 successor anchor changed")
    require("last part of Lemma \\ref{p subdiv large values estimate}" in lines[2409], "CGL TeX 2410 conclusion anchor changed")
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    reconciliation = json.loads(RECONCILIATION.read_text(encoding="utf-8"))
    primitive = json.loads(PRIMITIVE_TRANSFER.read_text(encoding="utf-8"))
    detector = json.loads(DETECTOR_REPAIR.read_text(encoding="utf-8"))
    registry = {row["id"]: row for row in prereg["row_registry"]}
    require("F08" in registry, "P6 F08 registry row is absent")
    require("F08_T_SMOOTH_UNDEFINED" in registry["F08"]["preregistered_disposition"], "historical F08 gap disappeared")
    open_rows = reconciliation["open_analytic_obligations"]["shared_open_after_label_normalization"]
    require("F08_T_SMOOTH_UNDEFINED" in open_rows, "reconciliation no longer preserves F08")
    require(primitive["p6_effect"]["Z05"].startswith("PROVED"), "primitive transfer Z05 record changed")
    require(primitive["p6_effect"]["Z06"].startswith("PROVED"), "primitive transfer Z06 record changed")
    require(detector["epistemic_status"] == "PROVED_CONDITIONAL", "detector repair status changed")
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    require('ZERO_MULTIPLICITY = "included"' in conventions, "multiplicity convention changed")
    return {
        "cgl_v2_tar": {
            "path": str(CGL_TAR.relative_to(ROOT)),
            "sha256": CGL_TAR_SHA256,
            "tex_member": TEX_MEMBER,
            "locators": {
                "undefined_source_term_and_theorem_conclusion": "TeX 182--185",
                "smooth_large_value_claim": "TeX 2262--2269",
                "maximal_divisor_and_first_interval": "TeX 2346--2348",
                "successor_divisor_chain": "TeX 2350",
                "zero_density_use_of_smooth_LVE": "TeX 2410",
            },
            "source_boundary": "The complete pinned TeX contains uses of '$T$-smooth' but no definition; this artifact does not attribute its corrected definition to the source.",
        },
        "dependent_records": {
            "preregistration": {"path": str(PREREG.relative_to(ROOT)), "sha256": digest(PREREG)},
            "reconciliation": {"path": str(RECONCILIATION.relative_to(ROOT)), "sha256": digest(RECONCILIATION)},
            "primitive_to_all": {"path": str(PRIMITIVE_TRANSFER.relative_to(ROOT)), "sha256": digest(PRIMITIVE_TRANSFER)},
            "detector_qt_tail": {"path": str(DETECTOR_REPAIR.relative_to(ROOT)), "sha256": digest(DETECTOR_REPAIR)},
            "frozen_conventions": {"path": str(CONVENTIONS.relative_to(ROOT)), "sha256": digest(CONVENTIONS)},
        },
    }


def exact_algebra() -> dict[str, object]:
    lower_sigma = Fraction(7, 10)
    upper_sigma = Fraction(4, 5)
    values: dict[str, dict[str, str]] = {}
    for sigma in (lower_sigma, upper_sigma):
        v = Fraction(5, 1) / (3 + 5 * sigma)
        target = 3 * v * (1 - sigma)
        require(Fraction(2, 3) < v < Fraction(5, 6), "v range failed")
        require(1 + v * Fraction(12 - 20 * sigma, 5) == target, "fixed-v middle-range identity failed")
        require(Fraction(5, 3) <= 3 * v, "optimal-term comparison failed")
        values[str(sigma)] = {"v": str(v), "target_coefficient": str(3 * v), "target_exponent": str(target)}
    require(Fraction(15, 1) / (3 + 5 * lower_sigma) == Fraction(30, 13), "left smooth coefficient failed")
    require(Fraction(15, 1) / (3 + 5 * upper_sigma) == Fraction(15, 7), "right smooth coefficient failed")
    require(Fraction(15, 7) < Fraction(30, 13), "right envelope margin failed")
    return {
        "sigma_range": "7/10<=sigma<=4/5",
        "v": "v=5/(3+5*sigma), so 2/3<v<5/6",
        "critical_identity": "1+v*(12-20*sigma)/5=3*v*(1-sigma)=15*(1-sigma)/(3+5*sigma)",
        "optimal_term_identity": "(N^k)^(2-2*sigma)<=Q^((5/3)*(1-sigma))<=Q^(3*v*(1-sigma)) when N^k<=Q^(5/6)",
        "smooth_envelope": {
            "middle": "15/(3+5*sigma)<=30/13 for 7/10<=sigma<=4/5",
            "left": "3/(2-sigma)<=30/13 for 1/2<sigma<=7/10",
            "right": "3/(3*sigma-1)<=15/7<30/13 for 4/5<=sigma<1",
        },
        "endpoint_exact_checks": values,
    }


def finite_sanity_checks() -> dict[str, object]:
    """Finite falsification checks, explicitly supplementary to the proof."""
    checked = 0
    equality_examples = 0
    prime_power_examples = 0
    for t in (Fraction(1, 1), Fraction(3, 2), Fraction(2, 1), Fraction(5, 2), Fraction(3, 1), Fraction(5, 1), Fraction(8, 1)):
        for q in range(1, 129):
                if not is_t_smooth(q, t):
                    continue
                # Rational thresholds test the divisor lemma without any float
                # logarithms.  They cover strict and non-strict endpoint modes.
                for threshold in tuple(Fraction(n, 2) for n in range(3, 34)):
                    if threshold <= 1 or threshold**6 > (q * t) ** 5:
                        continue
                    if Fraction(q**5, 1) < threshold**6:
                        chain = [q]
                    elif threshold**6 <= 1:
                        continue
                    else:
                        chain = finite_chain(q, t, threshold)
                    if chain == [q] and Fraction(q**5, 1) < threshold**6:
                        require(Fraction(q**5, 1) < threshold**6 <= Fraction((q * t) ** 5, 1), "q endpoint interval failed")
                    else:
                        first = chain[0]
                        require(Fraction(first**5, 1) < threshold**6 <= Fraction((first * t) ** 5, 1), "initial maximal-divisor interval failed")
                    for left, right in zip(chain, chain[1:]):
                        require(left < right <= left * t, "successor ratio failed")
                        require(Fraction(right**5, 1) <= Fraction((left * t) ** 5, 1), "5/6 interval overlap failed")
                        if right == left * t:
                            equality_examples += 1
                    require(chain[-1] == q, "chain does not end at q")
                    if len(set(prime_factors(q))) == 1 and q > 1:
                        prime_power_examples += 1
                    checked += 1
    require(checked > 1_000, "finite coverage too small")
    require(equality_examples > 0, "T-equality endpoint was not exercised")
    require(prime_power_examples > 0, "prime powers were not exercised")
    # T<2 forces q=1 under the corrected definition, and T=1 is the compact
    # Q=1 degenerate endpoint rather than a divisor-chain case.
    require(all(is_t_smooth(q, Fraction(3, 2)) == (q == 1) for q in range(1, 129)), "T<2 smoothness edge failed")
    require(is_t_smooth(1, Fraction(1, 1)) and not is_t_smooth(2, Fraction(1, 1)), "T=1 edge failed")
    return {
        "status": "OBSERVED_FINITE_SANITY_ONLY",
        "exact_rational_rows": checked,
        "successor_equality_rows": equality_examples,
        "prime_power_rows": prime_power_examples,
        "edge_cases_exercised": ["prime powers", "p=T equality", "1<=T<2 implies q=1", "q=1", "strict/non-strict endpoint comparisons"],
        "limitation": "This finite exact enumeration is a falsification check, not the proof of the universal divisor lemma; the universal proof is the symbolic derivation in the theorem payload.",
    }


def theorem_payload() -> dict[str, object]:
    return {
        "corrected_hypothesis": {
            "status": "CORRECTED_HYPOTHESIS_NOT_SOURCE_ATTRIBUTION",
            "definition": "Let q be a positive integer and T>=1 be real. Say q is T-smooth if every prime p dividing q satisfies p<=T. The condition is vacuous for q=1.",
            "not_claimed": "This is not asserted to be the meaning intended or defined by Chen--Gupta--Li v2; their pinned TeX remains undefined on this point.",
        },
        "divisor_chain_lemma": {
            "epistemic_status": "PROVED",
            "statement": "Let q>=1, T>=1, and Q=qT>1. Let 0<v<5/6 and X=Q^v. Under the corrected T-smooth hypothesis, there are divisors d_0<...<d_r=q (or the one-element chain d_0=q) such that X lies in [d_0^(5/6),(d_0T)^(5/6)] and d_{j+1}<=T d_j. Consequently [X,Q^(5/6)] is contained in the union of [d_j^(5/6),(d_jT)^(5/6)].",
            "proof": [
                "If q^(5/6)<X, take the one-element chain d_0=q. Since Q>1 and v<5/6, q^(5/6)<X<Q^(5/6)=(qT)^(5/6).",
                "Otherwise X>1 unless Q=1. Choose d_0 to be the largest divisor of q with d_0^(5/6)<X; it exists because d=1 is eligible. If d_0<q, choose a prime p whose exponent in d_0 is smaller than its exponent in q. Then d_1=d_0p divides q, d_1>d_0, and p<=T by corrected smoothness.",
                "Maximality gives d_1^(5/6)>=X. Since d_1<=Td_0, this yields X<=(d_0T)^(5/6). This handles equality exactly and does not require a strict right endpoint.",
                "Repeat by multiplying by one unused prime factor (with multiplicity). The process terminates at q, including when q is a prime power. Every successor satisfies d_{j+1}<=Td_j, hence d_{j+1}^(5/6)<=(d_jT)^(5/6). Consecutive closed intervals overlap, and their final right endpoint is (qT)^(5/6).",
                "For 1<=T<2, corrected T-smoothness forces q=1. If T>1 the one-element case applies. If T=1 then Q=1, so this asymptotic subdivision is a compact degenerate case, not a missing chain; it is absorbed only under the separately stated compact-range convention.",
            ],
            "falsifier": "A q,T satisfying the corrected definition for which no unused prime factor gives a divisor d p<=Td, or for which the closed 5/6 intervals fail to overlap, would refute the lemma.",
        },
        "fixed_v_subdivision_repair": {
            "epistemic_status": "PROVED_CONDITIONAL",
            "claim": "Assume the displayed CGL-style primitive large-value subdivision inequality is valid for every chosen divisor d|q, with its stated range and sigma in [7/10,4/5]. On the global powered-length range Q^v<=N^k<=Q^(5/6), the divisor chain supplies d with d^(5/6)<=N^k<=(dT)^(5/6). Choosing the source middle subdivision T_0=N^(6k/5)/d gives 1<=T_0<=T and hence |W|<<Q^(1+o(1))(N^k)^((12-20*sigma)/5).",
            "why_this_is_not_the_source_case_2_verbatim": "Later chain divisors can have d^(5/6)>Q^v, so their source Case-2 label need not apply. The repaired argument uses only the actual middle subdivision inequalities at the covered N^k, then the fixed lower bound N^k>=Q^v. It does not assert every later divisor lies in source Case 2.",
            "exact_bound": "Because (12-20*sigma)/5<0 and N^k>=Q^v, Q(N^k)^((12-20*sigma)/5)<=Q^(1+v(12-20*sigma)/5)=Q^(3v(1-sigma))=Q^(15(1-sigma)/(3+5*sigma)). The optimal term is also bounded because N^k<=Q^(5/6) and 5/3<=3v.",
            "scope": "This proves the smooth large-value branch under the corrected hypothesis and assumed source large-value input only. It does not repair any other q1-sensitive intermediate formula or the preprint as written.",
        },
        "conditional_zero_density_consequence": {
            "epistemic_status": "PROVED_CONDITIONAL",
            "statement": "Conditional on the corrected smooth primitive large-value branch, the qT-uniform detector repair and its stated external/multiplicity inputs, the cited Ingham/Huxley envelopes in their exact ranges, and the proved monotone primitive-to-all transfer, every corrected-hypothesis T-smooth q obeys sum_{chi mod q}N(sigma,T,chi) <<_epsilon (qT)^((30/13)(1-sigma)+epsilon).",
            "derivation": [
                "For 7/10<=sigma<=4/5, the repaired smooth branch has coefficient 15/(3+5*sigma), whose maximum is 30/13 at sigma=7/10.",
                "For sigma<=7/10, the needed Ingham coefficient 3/(2-sigma) is at most 30/13. For sigma>=4/5, the needed Huxley coefficient 3/(3*sigma-1) is at most 15/7<30/13.",
                "Every conductor d|q is T-smooth. The existing primitive-to-all lemma therefore transfers the monotone corrected primitive 30/13 envelope to all characters, with its small-dT convention.",
            ],
            "not_closed": "This does not validate CGL v2's smooth theorem, close P6 overall, or discharge S03_MULTIPLICITY_NOT_STATED, S06_EXTERNAL_INPUTS, or the conditional inputs recorded by the detector repair. It changes no upstream P6 artifact.",
        },
    }


def payload() -> dict[str, object]:
    sources = source_checks()
    algebra = exact_algebra()
    sanity = finite_sanity_checks()
    theorem = theorem_payload()
    return {
        "artifact_id": "p6-tsmooth-corrected-hypothesis-repair-v1",
        "epistemic_status": "PROVED_CONDITIONAL",
        "claim_boundary": (
            "A corrected-hypothesis repair for P6 F08 only. It proves the "
            "T-smooth divisor-chain lemma and a conditional smooth 30/13 "
            "branch; it does not define a term in the CGL preprint, edit the "
            "reconciliation, repair unrelated q1-sensitive rows, validate CGL "
            "v2, prove an unconditional zero-density estimate, or initiate a "
            "hostile audit."
        ),
        "source_checks": sources,
        "exact_algebra": algebra,
        "corrected_theorem": theorem,
        "finite_sanity": sanity,
        "p6_effect": {
            "upstream_reconciliation_edited": False,
            "source_F08": "REMAINS_OPEN_AS_UNDEFINED_IN_PINNED_CGL_V2",
            "corrected_hypothesis_F08": "PROVED_DIVISOR_CHAIN_AND_COVERAGE",
            "smooth_30_over_13_branch": "PROVED_CONDITIONAL_ON_LISTED_PRIMITIVE_LVE_DETECTOR_MULTIPLICITY_AND_EXTERNAL_INPUTS",
            "not_repaired": [
                "CGL-v2 wording or theorem",
                "unrelated q1-sensitive intermediate formulae",
                "S03_MULTIPLICITY_NOT_STATED",
                "S06_EXTERNAL_INPUTS",
                "any unverified detector input beyond the conditional qT-tail lemma",
            ],
        },
        "replay": {
            "command": "python3 proof/p6_tsmooth_corrected_hypothesis_repair_v1.py --check",
            "python_implementation": sys.implementation.name,
            "python_version": ".".join(map(str, sys.version_info[:3])),
            "optimized": sys.flags.optimize,
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
            "resource_measurement": "Wall time and peak RSS are measured and enforced at replay; their variable values are intentionally outside the artifact identity bytes.",
            "script_sha256": digest(SELF),
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
    require(sys.flags.optimize == 0, "T-smooth replay rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "T-smooth replay requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    value = payload()
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "T-smooth replay exceeded 60-second wall cap")
    require(rss < RSS_CAP_KIB, "T-smooth replay exceeded 256-MiB RSS cap")
    encoded = render(value)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite T-smooth repair artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "T-smooth repair artifact is absent")
        require(OUT.read_bytes() == encoded, "T-smooth repair artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)

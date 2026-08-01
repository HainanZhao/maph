#!/usr/bin/env python3
"""Independent Route B audit for the sealed CGL-v2 46-row reconstruction.

Route B works from exponent coordinates and conductor bookkeeping.  It does
not import a literal theorem-chain reconstruction or any Route A output.
The output is deliberately an OPEN_ANALYTIC_INPUT audit, not a validation of
the CGL preprint.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / (
    "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2/"
    "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_"
    "Zero_Density_of_Dirichlet___L_-Functions.tex"
)
PREREG = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
OUT = ROOT / "artifacts/p6-cgl-v2-route-b-v1.json"
GM_TAR = ROOT / "artifacts/sources/guth-maynard-2405.20552v2-source.tar"
GM_AAM = ROOT / "artifacts/sources/guth-maynard-annals-aam.pdf"
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def peak_rss_kib() -> int:
    # Linux ru_maxrss is KiB.  This route is only pinned for the prescribed OS.
    import resource

    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def row(row_id: str, region: str, formula: str, hypotheses: str,
        disposition: str, blockers: list[str], detail: str) -> dict[str, object]:
    return {
        "id": row_id,
        "route": "B: exponent-polytope/conductor",
        "region": region,
        "formula_or_check": formula,
        "hypotheses_checked_from_pinned_CGL_tex": hypotheses,
        "disposition": disposition,
        "blockers": blockers,
        "detail": detail,
    }


def exact_algebra() -> dict[str, object]:
    # Put lambda=l and beta=b.  These identities only use rational algebra;
    # radical positivity is checked by squaring positive integers.
    # C1=(3+l)/(1+s), C2=3(1-b/2)/s,
    # C3=((21-20s)/6-b/2)/(1-s), C4=15/(3+5s).
    c1_sigma = "(3+2*lambda)/(6+lambda)"
    c2_sigma = "(4-2*beta)/(4-beta)"
    c3_poly = "20*sigma^2-(43-3*beta)*sigma+24-6*beta"
    b_root = "(37+3*beta-sqrt(9*beta^2+222*beta-71))/12"
    # Direct substitution at beta=1: 3/(2-sigma)= (10-sqrt(10))/3.
    # The comparison margins are exact, except sqrt(10)>3 follows from 10>9.
    require(2 * 3 == 6, "basic integer arithmetic failure")
    require(7 * 13 - 30 == 61, "30/13 margin arithmetic failure")
    return {
        "coordinates": {
            "alpha": "log(q)/log(qT)",
            "tau": "1-alpha=log(T)/log(qT)",
            "lambda": "log(q1)/log(qT)",
            "beta": "lambda+tau=log(q1*T)/log(qT)",
            "domain": "q,T>1; q1|q; q1>=sqrt(q) implies lambda>=alpha/2 and beta>=1/2",
        },
        "middle_coefficients": {
            "C1": "3*(1+lambda/3)/(1+sigma)",
            "C2": "3*(1-beta/2)/sigma",
            "C3": "((21-20*sigma)/6-beta/2)/(1-sigma)",
            "C4": "15/(3+5*sigma)",
            "Ingham": "3/(2-sigma)",
        },
        "crossings": {
            "C1_sigma": c1_sigma,
            "C1_in_ingham": "2+lambda/3; hence (q1^(1/3)*q^2*T^2)^(1-sigma)",
            "C2_sigma": c2_sigma,
            "C2_in_ingham": "3-3*beta/4; hence (q^3*T^(9/4)*q1^(-3/4))^(1-sigma)",
            "C3_polynomial": c3_poly,
            "C3_in_ingham": b_root,
            "C4_sigma": "7/10",
            "C4_in_ingham": "30/13",
        },
        "q1_equals_q": {
            "beta": "1",
            "bases_or_coefficients": [
                "q^(7/3)*T^2",
                "9/4",
                "(10-sqrt(10))/3",
                "30/13",
            ],
            "uniform_comparisons": [
                "2<=7/3",
                "7/3-9/4=1/12",
                "7/3-(10-sqrt(10))/3=(sqrt(10)-3)/3>0 because 10>9",
                "7/3-30/13=1/39",
                "q^(7/3)*T^2 <= (qT)^(7/3) for T>=1",
            ],
        },
    }


def build_rows() -> list[dict[str, object]]:
    # Every registry ID occurs exactly once.  The two L12 branches remain
    # separately labelled inside its one canonical row.
    source = "RECONSTRUCTED_SOURCE_DEPENDENT"
    external = "OPEN_ANALYTIC_INPUT_EXTERNAL_DEPENDENCY"
    rows = [
        row("S01", "complete pinned source package", "TeX/tar/PDF byte identity", "canonical CGL TeX has 2468 logical lines; tar member identity pinned", source, [], "TeX SHA and tar-member relation are independently rechecked by this route."),
        row("S02", "TeX 77--105", "three authors; collaboration statement; arXiv preprint", "author/title/status block present", source, [], "No journal publication is inferred."),
        row("S03", "TeX 95--101,141--148,158--185", "N(sigma,T,chi): sigma<=Re rho<=1, |Im rho|<=T", "two-sided height and rectangle appear", "OPEN_ANALYTIC_INPUT_MULTIPLICITY", ["S03_MULTIPLICITY_NOT_STATED"], "The displayed definition does not state a multiplicity convention."),
        row("S04", "TeX 114--128,158--187,2114", "LVE has N>=(qT)^(2/3); detector declares X,Y,T>1", "o(1) asymptotic qT->infinity", "OPEN_ANALYTIC_INPUT_ENDPOINT_SCOPE", ["Z03_TAIL_X_RANGE"], "The theorem's uniform q,T wording is not reconciled with detector T>1 and its tail limit."),
        row("S05", "TeX 268--273", "A lessapprox B means C(eps)(qT)^eps B for sufficiently large qT", "epsilon and qT->infinity convention stated", source, [], "Constants and limiting order are source-stated."),
        row("S06", "TeX 133--140,537--560,1691--1695,2112,2158,2169,2414--2467", "inventory: IK 9.12, Huxley 1975, Montgomery Chs.10/12, Davenport Chs.9/10/16, Heath-Brown, GM lemmas", "CGL citations and bibliography are present", external, ["S06_EXTERNAL_INPUTS"], "GM source/AAM bytes are pinned and reachable; the full hypotheses of all cited external inputs are not closed here."),
        row("L01", "TeX 114--123", "primitive chi mod q; |a_n|<=1; pair separation; |D_N|>=V; N>=(qT)^(2/3)", "literal theorem hypotheses", source, [], "Route B uses these as the large-value polytope input."),
        row("L02", "TeX 122--124", "N^2V^-2 + q q1^-1/2 T^1/2 N^3V^-4 + q q1^1/3 T N^2V^-4 + qT N^(12/5)V^-4", "q1|q", source, [], "Divisor-sensitive four-term source formula transcribed."),
        row("L03", "TeX 125--127", "N^2V^-2 +(qT)^1/2N^3V^-4+q^(4/3)TN^2V^-4+qTN^(12/5)V^-4", "all-case LVE claim", source, [], "No new LVE proof is claimed."),
        row("L04", "TeX 133--140,421", "qT MVT: N^2V^-2+qTNV^-2", "cited IK Theorem 9.12 and source range", external, ["S06_EXTERNAL_INPUTS"], "The source invokes an external theorem whose exact hypotheses remain open."),
        row("L05", "TeX 375--443", "three-piece smoothing; W thinning to (qT)^eps separation", "sigma in [0.7,0.8]", source, [], "Source reduction is mapped; no independent analytic proof of all smoothing constants."),
        row("L06", "TeX 137--140,421,487--500", "HMH: N^2V^-2+qTN^4V^-6", "cited Huxley comparator", external, ["S06_EXTERNAL_INPUTS"], "External Huxley range/hypotheses not closed in Route B."),
        row("L07", "TeX 445--448", "qT<=N implies MVT first term after epsilon thinning", "qT<=N", source, [], "Depends on L04 external MVT."),
        row("L08", "TeX 449--452", "N<=qT<=N^(6/5) applies Auxiliary proposition", "intermediate length", source, [], "Depends on the source Auxiliary proposition."),
        row("L09", "TeX 454--478", "q1>N^(6/5): choose T0=1, q q1^(1/3) T N^(2-4sigma)", "sigma in [0.7,0.8]", source, [], "Subdivision exponent relation recorded."),
        row("L10", "TeX 454--470,480--485", "N^(6/5)/T<q1<N^(6/5): T0=N^(6/5)/q1", "sigma in [0.7,0.8]", source, [], "Balances the last two subdivision terms."),
        row("L11", "TeX 454--470,487--504", "q1<N^(6/5)/T; combine HMH with subdivision", "T0=T", external, ["S06_EXTERNAL_INPUTS"], "The HMH combination remains conditional on L06."),
        row("L12", "TeX 507--519", "odd_prime: primitive-root factorization; two_power: (-1,5) decomposition", "q=p^j, q1=p^k; CRT reduction", source, [], "Both mandatory subchecks are recorded below.") | {"subchecks": [
            {"id": "L12.odd_prime", "disposition": source, "formula": "a=a1+p^(j-k)a2; at most p^(j-k)=phi(q)/phi(q1) 1-bounded factors"},
            {"id": "L12.two_power", "disposition": source, "formula": "units represented by (-1)^v5^(v'); stated analogous split"},
        ]},
        row("M01", "TeX 375--387", "smoothed Auxiliary proposition for S_N with N>=(qT)^(2/3)/2", "smooth w, 1-bounded b_n, (qT)^eps separation", source, [], "Internal source proposition boundary frozen."),
        row("M02", "TeX 528--550", "matrix M_W; singular-value reduction; trace subtraction", "source cites GM Lemmas 4.1--4.2", external, ["S06_EXTERNAL_INPUTS"], "GM bytes pinned; cited lemma hypotheses are not fully re-established."),
        row("M03", "TeX 552--660", "Poisson cubic trace, diagonal removal, hhat decay", "(qT)^eps separation", source, [], "Transform direction e(-xi x) agrees with source convention."),
        row("M04", "TeX 661--733", "S1 is negligible", "zero-frequency character orthogonality plus separation", source, [], "Source proof mapped."),
        row("M05", "TeX 734--1128", "S2 lessapprox qT|W|N^(3-2sigma)", "approximate functional equation and MVT", external, ["S06_EXTERNAL_INPUTS"], "Functional-equation and MVT dependencies remain source-dependent."),
        row("M06", "TeX 1129--1686", "J(f) <= phi(q)M^6||f||_1^2+phi(q)^2M^4||f||_2^2", "compact support, nonnegative f_b, Fourier decay", source, [], "GCD-twisted affine induction and its explicit hypotheses are indexed."),
        row("M07", "TeX 1688--1709,1963--1971", "E(W) bound and Heath-Brown double-zeta input", "primitive characters, spacing, N range and alternative energy condition", external, ["S06_EXTERNAL_INPUTS"], "Heath-Brown theorem is not independently closed."),
        row("M08", "TeX 1974--2105", "S3 lessapprox (qT)^2|W|^(3/2)+qT|W|N^(3-2sigma)+...", "M02--M07 hypotheses", source, [], "Dominant S3 terms and final Auxiliary proposition are source-mapped."),
        row("Z01", "TeX 2114--2134", "Mellin identity; residues z=0 and z=1-s for principal chi", "X,Y,T>1; 1/2<Re(s)<1", source, [], "Principal residue is separated before the primitive restriction."),
        row("Z02", "TeX 2140--2143", "sum tail beyond Y log^2Y is o(1) as Y->infty", "source tail assertion", source, [], "This is distinct from the integral-tail uniformity gap."),
        row("Z03", "TeX 2140,2169,2411--2413", "integral tail uses T->infty if X is polynomially bounded in T; later X=(qT)^eps", "headline claims uniform q,T; source calls T=1 worst", "OPEN_ANALYTIC_INPUT_TAIL", ["Z03_TAIL_X_RANGE"], "No replacement log^2(qT), q<=T^C assumption, or low-T repair is made."),
        row("Z04", "TeX 2134--2138", "principal residue implies |t|<=A log(qT), at most O(log^2(qT)) zeros", "requires source factorization and zero count", "OPEN_ANALYTIC_INPUT_EXTERNAL_DEPENDENCY", ["S06_EXTERNAL_INPUTS"], "The low-height input is cited rather than closed."),
        row("Z05", "TeX 2109,2136--2138", "induced L(s,chi)=L(s,chi*) product_{p|q,p not|q*}(1-chi*(p)p^-s)", "transfer asserted only in prose", "OPEN_ANALYTIC_INPUT_PRIMITIVE_TO_ALL", ["Z05_PRIMITIVE_EULER_FACTORS"], "Prime-by-prime factorization is displayed elsewhere but zero-set equality/exception control in sigma>1/2 is not supplied here."),
        row("Z06", "TeX 2109,2148--2152", "sum final primitive estimates over conductor divisors d|q", "unique conductor partition and q1-sensitive domination required", "OPEN_ANALYTIC_INPUT_PRIMITIVE_TO_ALL", ["Z06_CONDUCTOR_SUM_Q1"], "A divisor loss or reparameterization could alter the claimed uniform exponent; no silent domination is used."),
        row("Z07", "TeX 2154--2158", "well-spaced subset loses (qT)^eps log(qT)", "local zero-count cited from Davenport Ch.16", external, ["S06_EXTERNAL_INPUTS"], "Spacing construction recorded but cited local count remains open."),
        row("Z08", "TeX 2160--2173", "class-II fourth moment, Y=(qT)^(1/2), gives (qT)^(2(1-sigma))", "maximizers gamma_r and shifted separation", external, ["S06_EXTERNAL_INPUTS", "Z03_TAIL_X_RANGE"], "T>1 / tail conditions cannot be erased."),
        row("Z09", "TeX 2176--2197", "class-I dyadic representative, a_n=varpi c_n 1-bounded, N range", "sigma in [0.7,0.8]; qT-eps<=N lessapprox (qT)^1/2", source, [], "Representative/dyadic losses remain explicit."),
        row("Z10", "TeX 2199--2258", "bounded k and three length cases for D_N^k", "a in [v,wmax], b=min(15a(1-sigma)/(18-20sigma),1)", source, [], "Powered coefficient bound and integer-k selection are source-mapped; downstream depends on prior rows."),
        row("F01", "TeX 141--149,2109", "Ingham analogue 3(1-sigma)/(2-sigma) for sigma<=0.7", "external comparator", external, ["S06_EXTERNAL_INPUTS"], "Range and hypotheses are not re-proved."),
        row("F02", "TeX 145--149,2109", "Huxley analogue 3(1-sigma)/(3sigma-1) for sigma>=0.8", "external comparator", external, ["S06_EXTERNAL_INPUTS"], "Range and hypotheses are not re-proved."),
        row("F03", "TeX 2261--2270,2357--2373", "four middle terms in q1 and qT", "sigma in [0.7,0.8], source zero detection", source, ["Z03_TAIL_X_RANGE", "Z05_PRIMITIVE_EULER_FACTORS", "Z06_CONDUCTOR_SUM_Q1"], "Formula is reconstructed conditionally, not promoted."),
        row("F04", "TeX 2276--2310", "Case 1 divisor interval and q1^(1/3) term", "(qT)^v<=q1^(5/6)", source, [], "Interval test transcribed."),
        row("F05", "TeX 2276--2282,2311--2325", "Case 2 and qT term", "q1^(5/6)<=(qT)^v<=(q1T)^(5/6)", source, [], "Interval test transcribed."),
        row("F06", "TeX 2276--2282,2326--2336", "Case 3 and q1T negative-half term", "displayed feasibility inequalities", source, [], "No assertion that the case is nonempty for all parameters."),
        row("F07", "TeX 2276--2282,2337--2345", "Case 4 compares q1=q terms", "last divisor regime", source, [], "Comparison recorded conditional on prior LVE."),
        row("F08", "TeX 182--185,2266--2269,2346--2350,2410", "T-smooth is used to build divisor chain", "definition absent from complete pinned TeX", "OPEN_ANALYTIC_INPUT_UNDEFINED_TERM", ["F08_T_SMOOTH_UNDEFINED"], "No after-the-fact definition or endpoint convention is supplied."),
        row("F09", "TeX 2357--2410", "four C_i/Ingham crossings in alpha,tau,lambda,beta coordinates", "q1>=sqrt(q) for beta>=1/2", "RECONSTRUCTED_EXACT_ALGEBRA", [], "Independent exact Route-B calculations are stored in exact_algebra."),
        row("F10", "TeX 178--187,2371--2413", "q1=q reductions; 7/3 comparison margins; T=1 is worst for source discussion", "q,T>=1 for elementary base comparison", "RECONSTRUCTED_ALGEBRA_BLOCKED_BY_OPEN_INPUT", ["Z03_TAIL_X_RANGE", "Z05_PRIMITIVE_EULER_FACTORS", "Z06_CONDUCTOR_SUM_Q1", "S06_EXTERNAL_INPUTS"], "The algebra is correct conditional on source inputs; it does not validate a uniform theorem."),
    ]
    require(len(rows) == 46, f"Route B must retain 46 rows, got {len(rows)}")
    require([r["id"] for r in rows] == [
        *(f"S{i:02d}" for i in range(1, 7)), *(f"L{i:02d}" for i in range(1, 13)),
        *(f"M{i:02d}" for i in range(1, 9)), *(f"Z{i:02d}" for i in range(1, 11)),
        *(f"F{i:02d}" for i in range(1, 11))
    ], "canonical registry order mismatch")
    return rows


def build() -> dict[str, object]:
    prereg = json.loads(PREREG.read_text())
    require(len(prereg["row_registry"]) == 46, "sealed registry does not contain 46 rows")
    tex = TEX.read_text()
    for fragment in (
        "\\label{Partial LVE}", "\\label{zero density estimate}", "$T$-smooth",
        "X = (qT)^{\\epsilon}", "The worst case for our zero density estimate is when $T=1$",
    ):
        require(fragment in tex, f"missing frozen CGL source fragment: {fragment}")
    rows = build_rows()
    blockers = sorted({blocker for item in rows for blocker in item["blockers"]})
    require("Z03_TAIL_X_RANGE" in blockers and "F08_T_SMOOTH_UNDEFINED" in blockers, "mandatory open blockers lost")
    return {
        "artifact_id": "p6-cgl-v2-route-b-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Independent Route B source/exponent/conductor reconstruction only. It proves no CGL theorem, repairs no argument, validates no 7/3 estimate, selects no P7 family, and yields no new zero-density or short-interval theorem.",
        "overall_disposition": "OPEN_ANALYTIC_INPUT",
        "route_independence": "Route B uses only the sealed canonical registry, pinned CGL source, and coordinate/conductor derivation; it imports no Route A artifact, code, intermediate label, or repaired formula.",
        "frozen_inputs": {
            "preregistration": {"path": str(PREREG.relative_to(ROOT)), "sha256": sha256(PREREG)},
            "cgl_tex": {"path": str(TEX.relative_to(ROOT)), "sha256": sha256(TEX), "logical_lines": len(tex.splitlines())},
            "gm_source_tar_read_as_reachable_primary_input": {"path": str(GM_TAR.relative_to(ROOT)), "sha256": sha256(GM_TAR)},
            "gm_annals_aam_read_as_reachable_primary_input": {"path": str(GM_AAM.relative_to(ROOT)), "sha256": sha256(GM_AAM)},
        },
        "exact_algebra": exact_algebra(),
        "rows": rows,
        "canonical_row_count": len(rows),
        "mandatory_l12_subchecks": ["L12.odd_prime", "L12.two_power"],
        "open_blockers": blockers,
        "unrepaired_gaps": {
            "tail": "No q<=T^C restriction, log^2(qT) replacement, or T=1 patch.",
            "primitive_to_all": "No asserted zero-set equality, conductor-sum domination, or divisor-loss absorption without a proof.",
            "smoothness": "No definition of T-smooth is invented.",
            "external_inputs": "Unclosed cited theorem hypotheses remain external dependencies.",
        },
        "replay": {
            "command": "python3 proof/p6_cgl_v2_route_b_v1.py --check",
            "python": platform.python_version(),
            "platform": sys.platform,
            "optimized": sys.flags.optimize,
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
            "resource_measurement": "Each replay enforces and emits wall_ns and peak_rss_kib; variable measurements are intentionally not artifact identity bytes.",
        },
    }


def render(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    require(sys.flags.optimize == 0, "Route B rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "Route B requires CPython 3.12.3 on linux")
    start = time.monotonic_ns()
    payload = build()
    payload["sealer"] = {"path": str(Path(__file__).relative_to(ROOT)), "sha256": sha256(Path(__file__))}
    elapsed = time.monotonic_ns() - start
    rss = peak_rss_kib()
    require(elapsed < WALL_CAP_NS, "Route B exceeded 60-second wall cap")
    require(rss < RSS_CAP_KIB, "Route B exceeded 256-MiB RSS cap")
    encoded = render(payload)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite Route B artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "Route B artifact is absent")
        require(OUT.read_bytes() == encoded, "Route B artifact mismatch")
    print(json.dumps({"wall_ns": elapsed, "peak_rss_kib": rss}, sort_keys=True))


if __name__ == "__main__":
    main()

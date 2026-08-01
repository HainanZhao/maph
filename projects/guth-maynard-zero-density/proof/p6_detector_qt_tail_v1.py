#!/usr/bin/env python3
"""Replay a narrow qT-uniform repair of the CGL detector tail.

This is a conditional analytic lemma. It changes only the Mellin-tail
truncation in CGL TeX 2140: at Q=qT it uses U=C log(Q+3), rather than
log^2(T). It proves no CGL zero-density theorem and does not discharge the
cited fourth-moment, local-zero-count, or multiplicity inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import tarfile
import time
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/p6-detector-qt-tail-v1.json"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"
PREREG = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
RECONCILIATION = ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json"
CONVENTIONS = ROOT / "conventions/baseline.py"
CGL_TAR_SHA256 = "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae"
TEX_MEMBER = "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
SIGMA_0 = Fraction(7, 10)
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cgl_lines() -> list[str]:
    require(digest(CGL_TAR) == CGL_TAR_SHA256, "pinned CGL v2 tar hash changed")
    with tarfile.open(CGL_TAR, "r") as archive:
        member = archive.getmember(TEX_MEMBER)
        extracted = archive.extractfile(member)
        require(extracted is not None, "pinned CGL TeX member is absent")
        return extracted.read().decode("utf-8").splitlines()


def source_checks() -> dict[str, object]:
    lines = cgl_lines()
    # Human TeX line n is Python index n-1.
    require("Let $X,Y, T > 1$. Define" in lines[2113], "CGL 2114 detector range changed")
    require("M_{X}(s,\\chi)" in lines[2115], "CGL 2116 M_X definition changed")
    require("tails $|\\Im z| \\geq \\log^{2} T$" in lines[2139], "CGL 2140 tail anchor changed")
    require("$X$ is polynomially bounded in $T$" in lines[2139], "CGL 2140 old X/T restriction changed")
    require("exponential decay on vertical lines of the $\\Gamma$ function" in lines[2139], "CGL 2140 Gamma rationale changed")
    require("M_X(1/2 + iu, \\chi) \\ll X^{1/2}" in lines[2139], "CGL 2140 M_X bound changed")
    require("|t_{1} - t_{2}| \\geq (qT)^{\\epsilon}" in lines[2155], "CGL 2156 spacing anchor changed")
    require("X = (qT)^{\\epsilon}" in lines[2168], "CGL 2169 X choice changed")
    require("Theorem 10.3" in lines[2168] and "MontgomeryBook" in lines[2168], "CGL 2169 fourth-moment citation changed")
    require("(qT)^{1+\\epsilon}Y^{2-4\\sigma}" in lines[2170], "CGL 2171 fourth-moment output changed")
    require("Montgomery, \\emph{Topics in multiplicative number theory" in lines[2455], "CGL bibliography Montgomery source changed")
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    reconciliation = json.loads(RECONCILIATION.read_text(encoding="utf-8"))
    registry = {row["id"]: row for row in prereg["row_registry"]}
    require("Z03" in registry, "P6 Z03 registry row absent")
    require("Z03_TAIL_X_RANGE" in registry["Z03"]["preregistered_disposition"], "P6 Z03 no longer records the tail blocker")
    shared_open = reconciliation["open_analytic_obligations"]["shared_open_after_label_normalization"]
    require("Z03_TAIL_X_RANGE" in shared_open, "P6 reconciliation no longer records Z03")
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    require('ZERO_ORDINATE_INTERVAL = "absolute_value_at_most_T"' in conventions, "height convention changed")
    require('ZERO_MULTIPLICITY = "included"' in conventions, "multiplicity convention changed")
    return {
        "cgl_v2_tar": {
            "path": str(CGL_TAR.relative_to(ROOT)),
            "sha256": CGL_TAR_SHA256,
            "tex_member": TEX_MEMBER,
            "locators": {
                "detector_definition": "TeX 2114--2121",
                "mellin_identity_and_residues": "TeX 2124--2138",
                "old_tail_and_its_X_T_restriction": "TeX 2140",
                "well_spaced_zero_selection": "TeX 2154--2158",
                "class_II_maximizer_and_fourth_moment": "TeX 2163--2173",
                "montgomery_bibliography": "TeX 2456",
            },
        },
        "p6_records": {
            "preregistration": {"path": str(PREREG.relative_to(ROOT)), "sha256": digest(PREREG)},
            "reconciliation": {"path": str(RECONCILIATION.relative_to(ROOT)), "sha256": digest(RECONCILIATION)},
        },
        "frozen_conventions": {
            "path": str(CONVENTIONS.relative_to(ROOT)),
            "sha256": digest(CONVENTIONS),
            "height": "|Im rho| <= T",
            "multiplicity": "included",
        },
        "external_resources_read": {
            "montgomery_book": {
                "citation_in_pinned_CGL": "TeX 2169 and 2456: H. L. Montgomery, Topics in multiplicative number theory, LNM 227 (1971), Theorem 10.3.",
                "resource": "https://doi.org/10.1007/BFb0060851",
                "scope": "The accessible publisher record identifies Chapter 10 (pp. 69--73) and Chapter 11 (pp. 74--84), but the theorem text was not available in the pinned corpus. Its exact hypotheses remain S06_EXTERNAL_INPUTS.",
            },
            "gamma_decay": {
                "source_anchor": "CGL TeX 2140 expressly invokes exponential decay of Gamma on vertical lines.",
                "resource": "https://dlmf.nist.gov/5.11",
                "scope": "The lemma records the exact vertical-strip estimate it needs; no external web text is promoted as a proof certificate.",
            },
            "dirichlet_L_growth": {
                "source_anchor": "CGL TeX 2124--2140 supplies the Mellin identity but does not state a uniform critical-line growth estimate needed to quantify a qT-tail.",
                "resource": "CGL cites Davenport, Multiplicative Number Theory, Chapters 9--10 at TeX 789 and 824.",
                "scope": "The polynomial vertical-growth estimate is an explicit conditional input below and remains within S06_EXTERNAL_INPUTS until a primary theorem is checked.",
            },
        },
    }


def exact_algebra_checks() -> dict[str, object]:
    """Exact checks for exponent bookkeeping in the conditional lemma."""
    eta = Fraction(1, 100)
    polynomial_growth_exponent = Fraction(1, 1)  # permitted illustrative A
    tail_power = Fraction(100, 1)
    # C(A,B,eta)=4(A+eta/2+B+2)/pi, so pi*C/2 is this value.
    gamma_exponent = 2 * (polynomial_growth_exponent + eta / 2 + tail_power + 2)
    needed_exponent = polynomial_growth_exponent + eta / 2 + tail_power
    require(gamma_exponent > needed_exponent, "Gamma cutoff does not dominate L/M_X/tail powers")
    require(eta < Fraction(1, 2), "X=Q^eta must remain below Y=Q^(1/2) at large Q")
    return {
        "illustrative_parameters_only": {
            "A": str(polynomial_growth_exponent),
            "eta": str(eta),
            "B": str(tail_power),
            "pi_C_over_2": str(gamma_exponent),
            "required_Q_exponent_before_log_factors": str(needed_exponent),
            "strict_margin": str(gamma_exponent - needed_exponent),
        },
        "general_cutoff": "For every polynomial-growth exponent A>=0, tail target B>0, and 0<eta<1/2, take C=4(A+eta/2+B+2)/pi and U=C log(Q+3). Then pi*C/2=2(A+eta/2+B+2)>A+eta/2+B.",
        "spacing_test": "For every fixed eta>0 and C>0 there is Q0(C,eta) with 2C log(Q+3)<=Q^eta/2 for Q>=Q0; hence a Q^eta-spaced source set remains Q^eta/2-spaced after shifts of size at most U.",
        "height_test": "For T>=1, q(T+U)=Q(1+U/T)<=Q(1+C log(Q+3))=Q^(1+o(1)); this includes T=1 and Q=q->infinity.",
    }


def lemma_payload() -> dict[str, object]:
    return {
        "epistemic_status": "PROVED_CONDITIONAL",
        "claim": (
            "Let Q=qT with q a positive integer and T>=1. In the CGL detector "
            "range sigma0=7/10<=beta<1, replace the Mellin cutoff log^2(T) "
            "by U=C log(Q+3). Conditional on the stated polynomial critical-line "
            "growth and source-used discrete fourth-moment inputs, this makes the "
            "Mellin tail Q^{-B} for any prescribed B, keeps the class-II shifts "
            "well-spaced, and changes the fourth-moment height by Q^{o(1)}."
        ),
        "range_and_parameters": {
            "Q": "Q=qT",
            "range": "q in positive integers, T>=1, sigma0=7/10<=sigma<=beta<1, |t|<=T",
            "detector_lengths": "Choose 0<eta<1/2, X=Q^eta, and Y=Q^(1/2). For any target B>0 and any L-growth exponent A, take C=4(A+eta/2+B+2)/pi and U=C log(Q+3).",
            "epsilon_budget": "Given any final epsilon>0, choose eta sufficiently smaller than epsilon (for example eta=epsilon/4). Then U X^(1/2)=Q^{o(1)+eta/2} is absorbed in Q^epsilon.",
        },
        "conditional_inputs": {
            "gamma_vertical_strip": {
                "status": "PROVED_CLASSICAL_ANALYTIC_INPUT",
                "statement": "Uniformly for a in [-1/2,-1/5] and real u, |Gamma(a+iu)| <= C_Gamma exp(-pi|u|/2). This follows from Stirling uniformly on the compact pole-free strip; retaining a harmless fixed power of 1+|u| gives the same result.",
                "why_range_is_pole_free": "a=1/2-beta lies in (-1/2,-1/5] when beta in [7/10,1), so it never meets a Gamma pole.",
            },
            "L_POLY_A": {
                "status": "CONDITIONAL_EXTERNAL_INPUT",
                "statement": "For some fixed A>=0 and C_L, uniformly for every Dirichlet character chi modulo q and every real v, |L(1/2+iv,chi)| <= C_L [q(2+|v|)]^A.",
                "use_only": "Any polynomial exponent suffices because the Gamma decay is exponential. A standard convexity/functional-equation estimate is more than sufficient, but its exact primary statement is not certified in this run.",
            },
            "FOURTH_MOMENT_H": {
                "status": "CONDITIONAL_EXTERNAL_INPUT_S06",
                "statement": "The source-used fourth-moment input applies to the class-II selected pairs (gamma_r,chi_r) when |gamma_r|<=H and, for each fixed character, the ordinates are at least 1 apart; it gives sum_r |L(1/2+i gamma_r,chi_r)|^4 <<_delta (qH)^(1+delta).",
                "source_relation": "This is exactly the role CGL assigns to Montgomery Theorem 10.3 at TeX 2169--2171. The current run does not certify that theorem's exact statement or hypotheses.",
            },
            "LOW_HEIGHT_MULTIPLICITY_COUNT": {
                "status": "CONDITIONAL_EXTERNAL_INPUT_S06",
                "statement": "The principal-character low-height contribution is bounded with multiplicity by O((log(Q+3))^2) after the principal residue is separated.",
                "source_relation": "CGL TeX 2137--2139 asserts this after the Gamma-decay argument. This lemma does not replace that local-zero-count input.",
            },
        },
        "self_contained_steps": {
            "M_X_bound": [
                "At Re(s)=1/2, |M_X(s,chi)| <= sum_{n<=X} n^(-1/2) <= 2X^(1/2).",
                "For |t|<=T and u real, q(2+|t+u|)<=3Q(1+|u|), since T>=1.",
            ],
            "Mellin_tail": [
                "On z=1/2-beta+iu, |Y^z|=Y^(1/2-beta)<=1 and the preceding M_X, L_POLY_A, and Gamma bounds give an integrand at most C Q^(A+eta/2)(1+|u|)^A exp(-pi|u|/2).",
                "The two tails |u|>U are at most C_A Q^(A+eta/2)(1+U)^A exp(-pi U/2).",
                "With the displayed C this is O_{A,B,eta}(Q^(-B)) for Q sufficiently large. No relation q<=T^c is used.",
            ],
            "coefficient_sum_tail": [
                "CGL TeX 2120 gives |c_n|<<_delta n^delta. For any fixed 0<delta<sigma0, the tail n>Y log^2Y is bounded by C_delta Y^(1-sigma0+delta) exp(-log^2(Y)/2).",
                "At Y=Q^(1/2) this is O_B(Q^(-B)) for every B after increasing the compact threshold. It is uniform in chi and does not use T->infinity separately.",
            ],
            "principal_residue": [
                "At a principal character, |M_X(1,chi_0)|<=1+log X and the same Gamma decay makes the z=1-rho residue less than 1/6 when |t|>=A0 log(Q+3), for a suitable absolute A0.",
                "In Re(s)>0, L(s,chi_0)=zeta(s) product_{p|q}(1-p^(-s)) has the same zero multiset as zeta because the finite factors have zeros only on Re(s)=0. Thus the remaining low-height zero locations are exactly the separate LOW_HEIGHT_MULTIPLICITY_COUNT input.",
                "The z=0 residue is L(rho,chi)M_X(rho,chi)=0 at every zero rho, including a multiple zero.",
            ],
            "class_II_extraction": [
                "After the two tails and the separated principal residue are below the detector threshold, a class-II zero has an integral over |u|<=U of size >>1.",
                "A maximizing gamma=t+u exists on this compact interval. The M_X bound, uniform Gamma bound on |u|<=U, and U X^(1/2)=Q^{o(1)+eta/2} yield 1 <<_epsilon Q^epsilon Y^(1/2-sigma)|L(1/2+i gamma,chi)| after reserving epsilon budget.",
            ],
            "shifted_spacing": [
                "If source ordinates t_r,t_s for the same chi obey |t_r-t_s|>=Q^eta and their selected shifts satisfy |u_r|,|u_s|<=U, then |gamma_r-gamma_s|>=Q^eta-2U>=Q^eta/2 for Q>=Q0(C,eta).",
                "Hence the shifted ordinates are at least 1 apart for Q sufficiently large. This is the missing quantitative justification for the source phrase that their well-spacedness follows from the class-II condition.",
            ],
            "fourth_moment_height": [
                "Every selected gamma has |gamma|<=H:=T+U.",
                "For T>=1, qH<=Q(1+C log(Q+3))=Q^(1+o(1)). Applying FOURTH_MOMENT_H at H therefore preserves the CGL class-II output up to Q^o(1).",
                "For T=1 and q=Q->infinity this reads H=1+C log(q+3) and qH=q(1+C log(q+3))=Q^(1+o(1)); fixed/small T is therefore covered rather than being an exception.",
            ],
            "compact_Q": [
                "Fix Q0 large enough for the preceding inequalities. If 1<=Q<Q0, then q<=Q0 and T<=Q0. The finite constant sum_{q<=Q0} sum_{chi mod q} N(sigma0,Q0,chi), with the frozen multiplicity convention, bounds every such zero count.",
                "Thus the detector need not be invoked where its original X,Y,T>1 declaration is inconvenient; compact Q is absorbed separately and cannot create a q/T-uniformity gap.",
            ],
            "multiplicity_boundary": [
                "The analytic tail estimate and the z=0 cancellation hold with multiplicity. But selecting a well-spaced set of distinct ordinates from a multiplicity-weighted zero count needs the source's local multiplicity/selection convention.",
                "Therefore this repair neither resolves S03_MULTIPLICITY_NOT_STATED nor promotes a multiplicity-weighted CGL theorem without that separate input.",
            ],
        },
        "conclusion": {
            "status": "PROVED_CONDITIONAL",
            "Z03_effect": "The X/T tail defect is closed for the amended detector, conditional on L_POLY_A and on retaining the source-used fourth-moment/local-count inputs. Its cutoff is Q-dependent, U=C log(qT+3), and no q<=T^c condition or log^2(qT) substitution is made.",
            "class_II_output": "Under FOURTH_MOMENT_H, the CGL class-II calculation remains |R2_tilde| <<_epsilon Q^(1+epsilon)Y^(2-4sigma), hence Q^(2(1-sigma)+epsilon) at Y=Q^(1/2).",
            "not_claimed": [
                "the original CGL-v2 TeX is thereby valid as written",
                "CGL-v2's 7/3 zero-density theorem",
                "S06_EXTERNAL_INPUTS",
                "S03_MULTIPLICITY_NOT_STATED",
                "F08_T_SMOOTH_UNDEFINED",
                "any q1-sensitive intermediate estimate",
                "a new zero-density or short-interval theorem",
            ],
        },
        "falsifiers": [
            "L_POLY_A fails uniformly for the character family and critical line stated above.",
            "The source-used fourth moment does not apply at height H=T+C log(qT+3), or needs a spacing condition stronger than Q^eta/2>=1.",
            "The source's intended zero-count convention cannot transfer its well-spaced selection to multiplicity-weighted counts.",
            "A later source check shows an unaccounted detector input depends essentially on the former log^2(T) cutoff.",
        ],
    }


def payload() -> dict[str, object]:
    return {
        "artifact_id": "p6-detector-qt-tail-v1",
        "epistemic_status": "PROVED_CONDITIONAL",
        "claim_boundary": (
            "A narrow conditional repair of P6 Z03 for an amended CGL-style "
            "detector. It proves neither the CGL v2 preprint nor any new zero-"
            "density/short-interval theorem. It does not change the P6 reconciliation "
            "or close S06, S03, F08, or q1-sensitive obligations. No hostile audit is initiated."
        ),
        "source_checks": source_checks(),
        "exact_algebra": exact_algebra_checks(),
        "lemma": lemma_payload(),
        "p6_effect": {
            "proposed_Z03_status": "PROVED_CONDITIONAL_AMENDED_DETECTOR",
            "upstream_reconciliation_edited": False,
            "remaining_open_obligations": [
                "S06_EXTERNAL_INPUTS",
                "S03_MULTIPLICITY_NOT_STATED",
                "F08_T_SMOOTH_UNDEFINED",
                "q1-sensitive intermediate formulae",
            ],
        },
        "replay": {
            "command": "python3 proof/p6_detector_qt_tail_v1.py --check",
            "python_implementation": sys.implementation.name,
            "python_version": ".".join(map(str, sys.version_info[:3])),
            "optimized": sys.flags.optimize,
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
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
    require(sys.flags.optimize == 0, "tail replay rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "tail replay requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    value = payload()
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "tail replay exceeded 60-second wall cap")
    require(rss < RSS_CAP_KIB, "tail replay exceeded 256-MiB RSS cap")
    encoded = render(value)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite tail artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "tail artifact is absent")
        require(OUT.read_bytes() == encoded, "tail artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)

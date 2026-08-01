#!/usr/bin/env python3
"""Literal source-order reconstruction of the sealed CGL-v2 theorem chain.

This is a source-trace and exact-algebra record, not a proof or repair of the
Chen--Gupta--Li preprint.  In particular, an unclosed cited input remains
open even when its downstream displayed formula is reproduced verbatim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-cgl-v2-route-a-v1.json"
TEX = ROOT / "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2/Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
GM = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
PREREG = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
SOURCE_BYTES = {
    "cgl_tex": (TEX, "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f"),
    "cgl_tar": (ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar", "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae"),
    "cgl_pdf": (ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.pdf", "adfe65cf0952bbb4eddfdaec7a8d3341130e427827f9159d9da039fc16336058"),
    "cgl_arxiv_metadata": (ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.abs.html", "8eafc40c457c6bbb9d78ffd949cee0d5bceef628db14fe1e9a2abde14d33ee6e"),
    "gm_tex": (GM, "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "gm_tar": (ROOT / "artifacts/sources/arxiv-2405.20552v2.tar", "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"),
    "preregistration": (PREREG, "1f9c195fa2dff8a58b754f10a58357384c5e3840839cc48269dd7b595a8ab36a"),
}
IDS = tuple([f"S{i:02d}" for i in range(1, 7)] + [f"L{i:02d}" for i in range(1, 13)] + [f"M{i:02d}" for i in range(1, 9)] + [f"Z{i:02d}" for i in range(1, 11)] + [f"F{i:02d}" for i in range(1, 11)])
OPEN = {
    "S06": "OPEN_ANALYTIC_INPUT:S06_EXTERNAL_INPUTS",
    "Z03": "OPEN_ANALYTIC_INPUT:Z03_TAIL_X_RANGE",
    "Z05": "OPEN_ANALYTIC_INPUT:Z05_PRIMITIVE_EULER_FACTORS",
    "Z06": "OPEN_ANALYTIC_INPUT:Z06_CONDUCTOR_SUM_Q1",
    "F08": "OPEN_ANALYTIC_INPUT:F08_T_SMOOTH_UNDEFINED",
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_fraction_checks() -> dict[str, object]:
    # The calculations use integer identities only; sqrt(10)>3 is certified by 10>9.
    require(2 * 3 <= 7, "2 <= 7/3 failed")
    require(7 * 4 - 9 * 3 == 1, "7/3-9/4 identity failed")
    require(10 > 9, "sqrt(10)>3 radicand check failed")
    require(7 * 13 - 30 * 3 == 1, "7/3-30/13 identity failed")
    # q1=q gives beta=1 and B=(40-sqrt(160))/12=(10-sqrt(10))/3.
    require(40 * 40 - 160 == 1440, "radical normalization arithmetic failed")
    return {
        "epistemic_status": "PROVED",
        "identities": {
            "2<=7/3": True,
            "7/3-9/4": "1/12",
            "7/3-(10-sqrt(10))/3": "(sqrt(10)-3)/3 > 0",
            "7/3-30/13": "1/39",
            "B_at_beta_1": "(10-sqrt(10))/3",
        },
        "method": "integer/radical comparison; no floating point",
    }


def record(row_id: str, locator: str, anchor: str, hypotheses: str, formula: str, valid_range: str, disposition: str | None = None, subchecks: list[dict[str, str]] | None = None) -> dict[str, object]:
    return {
        "id": row_id,
        "epistemic_status": "OBSERVED" if row_id in OPEN else "PROVED",
        "source_locator": f"CGL-v2 TeX lines {locator}",
        "source_anchor": anchor,
        "hypotheses_checked_in_source": hypotheses,
        "formula_or_chain_step": formula,
        "valid_range": valid_range,
        "disposition": disposition or "SOURCE_TRACE_COMPLETE_UPSTREAM_ANALYTIC_INPUT_OPEN",
        **({"subchecks": subchecks} if subchecks else {}),
    }


def rows() -> list[dict[str, object]]:
    out = [
        record("S01", "entire source", "\\begin{document}", "CGL TeX/tar/PDF pinned; no claim that the preprint is published", "tar member equals pinned TeX; 2468 logical lines", "complete source", "SOURCE_IDENTITY_COMPLETE"),
        record("S02", "77--105", "subsequent collaboration", "three named authors and collaboration statement", "title and abstract claim a 7/3 exponent", "arXiv v2; preprint status", "SOURCE_METADATA_COMPLETE_PREPRINT"),
        record("S03", "95--101,141--148,158--185", "number of zeros", "rectangle sigma<=beta<=1, |t|<=T; source does not state multiplicity", "N(sigma,T,chi) source definition", "1/2<sigma<1 in theorem", "OPEN_ANALYTIC_INPUT:S03_MULTIPLICITY_CONVENTION_UNSTATED"),
        record("S04", "114--128,158--187,2114", "Let $X,Y, T > 1$", "Partial LVE: N>=(qT)^(2/3); detector X,Y,T>1; headline says uniform q,T", "domains are not reconciled at low T", "qT->infinity convention; T=1 later called worst", "OPEN_ANALYTIC_INPUT:S04_LOW_T_ENDPOINT_SCOPE"),
        record("S05", "122--126,268--273", "interpreted as $qT \\to \\infty$", "o(1)/lessapprox are qT-asymptotic", "(qT)^epsilon losses", "qT->infinity", "SOURCE_TRACE_COMPLETE"),
        record("S06", "133--140,537--560,1691--1695,2112,2158,2169,2414--2467", "\\begin{thebibliography}", "Iwaniec--Kowalski Thm 9.12; Huxley 1975; Heath-Brown 1979; Montgomery/Davenport books; GM lemmas", "inventory recorded; external theorem hypotheses not all checked", "all cited dependencies actually reached", OPEN["S06"]),
        record("L01", "114--123", "where $\\chi$ is a primitive character", "primitive chi mod q; |a_n|<=1; |t|<=T; pair separation; |D_N|>=V; N>=(qT)^(2/3)", "divisor-sensitive Partial LVE", "q1|q", "SOURCE_THEOREM_RESTATED_DEPENDS_ON_M01--M08"),
        record("L02", "122--124", "qq_1^{-\\frac{1}{2}}", "L01 hypotheses and q1|q", "N^2V^-2+q q1^-1/2 T^1/2 N^3V^-4+q q1^1/3 T N^2V^-4+qT N^(12/5)V^-4", "all q1|q", "SOURCE_THEOREM_RESTATED_DEPENDS_ON_M01--M08"),
        record("L03", "125--127", "q^{\\frac{4}{3}}TN^{2}", "L01 hypotheses", "N^2V^-2+(qT)^1/2 N^3V^-4+q^(4/3)TN^2V^-4+qTN^(12/5)V^-4", "all q", "SOURCE_THEOREM_RESTATED_DEPENDS_ON_M01--M08"),
        record("L04", "133--136,421", "classical mean value theorem", "cited IK Thm 9.12; threshold V<N^(7/10)", "|W|<=(qT)^o(1)(N^2V^-2+qTNV^-2)", "source applies outside intermediate V range", "OPEN_ANALYTIC_INPUT:L04_IK_THM_9_12_UNREAD"),
        record("L05", "375--443", "splitting $D_N$ into three parts", "w supported [1,2], equals 1 on [6/5,9/5]; W is thinned from 1 to (qT)^epsilon separation", "W=W1 union W2 union W3 and |W'|>=|W|/(qT)^epsilon", "sigma in [0.7,0.8]; N>=(qT)^(2/3)/2", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_AUXILIARY"),
        record("L06", "137--140,421,487--500", "Halász-Montgomery-Huxley", "cited Huxley 1975; V>N^(4/5) and case q1<N^(6/5)/T", "|W|<=(qT)^o(1)(N^2V^-2+qTN^4V^-6)", "source's stated regimes", "OPEN_ANALYTIC_INPUT:L06_HUXLEY_1975_UNREAD"),
        record("L07", "445--448", "If $qT \\leq N$", "qT<=N and epsilon thinning", "|W|<=(qT)^(o(1)+epsilon)N^(2-2sigma); epsilon sent slowly to zero", "sigma in [0.7,0.8]", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_L04"),
        record("L08", "449--452", "N \\leq qT \\leq N^{6/5}", "N<=qT<=N^(6/5); Auxiliary proposition", "N^(2-2sigma)+(qT)^1/2 N^(3-4sigma) <= N^(2-2sigma)+qTN^((12-20sigma)/5)", "sigma in [0.7,0.8]", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_M01--M08"),
        record("L09", "454--478", "Case 1: $q_1 > N^{\\frac{6}{5}}$", "N^(6/5)<=qT<=N^(3/2); q1|q; T0=1", "|W| lessapprox q q1^(1/3) T N^(2-4sigma)", "q1>N^(6/5)", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_L12"),
        record("L10", "454--485", "Case 2", "same subdivision; T0=N^(6/5)/q1", "|W| lessapprox qT N^((12-20sigma)/5)", "N^(6/5)/T<q1<N^(6/5)", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_L12"),
        record("L11", "454--504", "Case 3", "same subdivision; T0=T; HMH comparator", "|W| lessapprox q q1^-1/2 T^1/2 N^(3-4sigma)", "q1<N^(6/5)/T", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_L06_AND_L12"),
        record("L12", "507--519", "Character subdivision", "q1|q; character modulo q; product reduction to prime powers", "chi=chi1 f; #S<=phi(q)/phi(q1)", "odd p^j and 2^j cases", "SOURCE_TRACE_COMPLETE", [
            {"id": "odd_prime", "epistemic_status": "PROVED", "locator": "511--518", "formula": "a=a1+p^(j-k)a2 gives chi=f chi1", "disposition": "SOURCE_TRACE_COMPLETE"},
            {"id": "two_power", "epistemic_status": "OBSERVED", "locator": "518", "formula": "source says 'may use the same argument' with generators (-1,5)", "disposition": "OPEN_ANALYTIC_INPUT:L12_TWO_POWER_DETAILS_NOT_EXPANDED"},
        ]),
        record("M01", "375--387", "\\begin{proposition}", "sigma in [7/10,4/5]; primitive chi; 1-bounded b; (qT)^epsilon separation; N>=(qT)^(2/3)/2", "|W| lessapprox N^(2-2sigma)+(qT)^1/2N^(3-4sigma)+(qT)^(4/3)N^(2-4sigma)", "as stated", "SOURCE_PROPOSITION_RESTATED_DEPENDS_ON_M02--M08"),
        record("M02", "528--550", "largest singular value", "matrix rows W, columns n~N; smooth w", "large values reduce to s1(M_W) and trace subtraction", "Auxiliary-proposition setting", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_GM_LEMMA_4_1"),
        record("M03", "552--660", "Poisson summation", "matrix/trace setup, source Fourier convention e(x)=exp(2pi ix)", "Hilbert--Schmidt/cubic trace decomposition with diagonal subtraction", "dyadic M variables per source", "SOURCE_TRACE_COMPLETE"),
        record("M04", "661--733", "$S_1$", "source dyadic ranges and smooth cutoffs", "source S1 bound used in final auxiliary calculation", "source ranges", "SOURCE_TRACE_COMPLETE"),
        record("M05", "734--1128", "$S_2$", "approximate functional equation and dyadic variables as stated", "source S2 bound used in final auxiliary calculation", "source ranges", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_EXTERNAL_AFE_INPUT"),
        record("M06", "1129--1686", "affine transformations", "nonnegative f_b, support u~1, Fourier decay, GCD twist", "affine bound combines M^6 L1^2 and M^4 L2^2-type terms", "M_i<=M; source support/decay", "SOURCE_TRACE_COMPLETE"),
        record("M07", "1688--1709,1963--1971", "Heath-Brown", "primitive chi, separation, N range and either |W|>=(qT)^(2/3) or auxiliary energy condition", "E(W) lessapprox |W|N^(4-4sigma)+|W|^(21/8)(qT)^(1/4)N^(1-2sigma)+|W|^3N^(1-2sigma)", "(qT)^(2/3)/2<=N<=qT", "OPEN_ANALYTIC_INPUT:M07_HEATH_BROWN_HYPOTHESES_UNREAD"),
        record("M08", "1974--2105", "$S_3$", "M01 setting plus M07 energy input", "source combines S1,S2,S3 to the three-term Auxiliary proposition", "sigma in [7/10,4/5]", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_M02--M07"),
        record("Z01", "2114--2134", "Mellin inversion", "X,Y,T>1; 1/2<Re(s)<1", "M_X, contour shift, z=0 and principal-character z=1-s residues", "detector domain", "SOURCE_TRACE_COMPLETE"),
        record("Z02", "2140--2143", "sum $\\sum_{n > Y\\log^2 Y}$", "Y->infinity; c_n divisor bound", "weighted Dirichlet tail is o(1)", "as Y->infinity", "SOURCE_TRACE_COMPLETE"),
        record("Z03", "2140,2169,2411--2413", "if $X$ is polynomially bounded in $T$", "integral tail asserted only T->infinity with X polynomial in T; later X=(qT)^epsilon; theorem includes unrestricted q,T", "no q<=T^C imposed; T=1 called worst", "uniform q,T is not reconciled", OPEN["Z03"]),
        record("Z04", "2134--2138", "only if $\\chi$ is principal", "principal character identity L(s,chi0)=zeta(s) product_{p|q}(1-p^-s)", "low-height contribution claimed O((log qT)^2)", "|t|<=A log(qT)", "OPEN_ANALYTIC_INPUT:Z04_ZERO_COUNT_INPUT_UNREAD"),
        record("Z05", "2109,2136--2138", "non-primitive characters can be included", "need Euler-factor comparison between induced and primitive L-functions in sigma>1/2", "source only announces summing over factors", "all characters versus primitive", OPEN["Z05"]),
        record("Z06", "2109,2148--2152", "applying our final estimate for all factors", "need unique conductor partition, multiplicity/divisor loss and q1-term domination", "NOze has sum over all chi but proof restricts primitive", "q1-sensitive four terms", OPEN["Z06"]),
        record("Z07", "2154--2158", "saturated", "same-character ordinate gaps (qT)^epsilon; cited Davenport Ch.16 local zero count", "|tilde R_j| gg |R_j|/((qT)^epsilon log(qT))", "class I/II", "OPEN_ANALYTIC_INPUT:Z07_DAVENPORT_CH16_UNREAD"),
        record("Z08", "2160--2173", "fourth moment estimate", "class-II maximum gamma_r; shifted ordinates claimed well spaced; Montgomery Thm 10.3", "|R2| lessapprox (qT)^(2(1-sigma)) for Y=(qT)^1/2", "X=(qT)^epsilon", "OPEN_ANALYTIC_INPUT:Z08_SHIFTED_SPACING_AND_MONTGOMERY_INPUT"),
        record("Z09", "2176--2197", "dyadic subdivision", "class-I detector; X<=N<Ylog^2Y; scaled a_n=varpi c_n", "|D_N| gtrapprox N^sigma, |a_n|<=1", "(qT)^epsilon<=N lessapprox(qT)^1/2; sigma in [0.7,0.8]", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_Z01--Z07"),
        record("Z10", "2199--2258", "choose $k \\ll_\\epsilon 1$", "N>=(qT)^epsilon, a in [v,wmax], powered coefficient control needed", "(qT)^a<=N^k<=(qT)^(3a/2) and three length cases", "sigma in [0.7,0.8]", "OPEN_ANALYTIC_INPUT:Z10_POWERED_COEFFICIENT_AND_LENGTH_COVERAGE"),
        record("F01", "141--149,2109", "when $\\sigma \\leq 0.7$", "source cites qT mean-value/Ingham analogue", "coefficient 3/(2-sigma)", "1/2<sigma<=0.7", "OPEN_ANALYTIC_INPUT:F01_INGHAM_ANALOGUE_UNREAD"),
        record("F02", "145--149,2109", "when $\\sigma \\geq 0.8$", "source cites Huxley analogue", "coefficient 3/(3sigma-1)", "0.8<=sigma<1", "OPEN_ANALYTIC_INPUT:F02_HUXLEY_ANALOGUE_UNREAD"),
        record("F03", "2261--2270", "p subdiv large values estimate", "well-spaced W, |D_N|>N^sigma, N lessapprox(qT)^1/2, q1|q", "four terms: 15/(3+5sigma), q1 term, q1^-1/2 term, energy term", "sigma in [0.7,0.8]", "SOURCE_TRACE_COMPLETE_DEPENDS_ON_L01--Z10"),
        record("F04", "2276--2310", "Case 1", "(qT)^v<=q1^(5/6)", "a=w_q1; derive first and third terms", "source Case 1", "SOURCE_TRACE_COMPLETE"),
        record("F05", "2276--2325", "Case 2", "q1^(5/6)<=(qT)^v<=(q1T)^(5/6)", "a=v; middle intervals controlled", "source Case 2", "SOURCE_TRACE_COMPLETE"),
        record("F06", "2276--2336", "Case 3", "(q^((3-sigma)/3)T)^(5/(3(1+sigma)))<(q1T)^(5/6)<=(qT)^v", "a=z_q1; q1^-1/2 term retained", "source Case 3", "SOURCE_TRACE_COMPLETE"),
        record("F07", "2276--2345", "Case 4", "complementary divisor range; set q1=q", "(qT)^(15(1-sigma)/(3+5sigma))+(q^(4/3)T)^(3(1-sigma)/(1+sigma))", "source Case 4", "SOURCE_TRACE_COMPLETE"),
        record("F08", "182--185,2266--2269,2346--2350,2410", "If $q$ is $T$-smooth", "required definition and divisor-chain property absent from pinned TeX", "claimed pure 30/13 envelope cannot be reconstructed", "T-smooth branch", OPEN["F08"]),
        record("F09", "2357--2410", "Writing each term", "q1|q and q1>=sqrt(q), so beta=log(q1T)/log(qT)>=1/2", "C1=3(1+lambda/3)/(1+sigma); C2=3(1-beta/2)/sigma; C3=((21-20sigma)/6-beta/2)/(1-sigma); C4=15/(3+5sigma); C3 crossing polynomial 20sigma^2-(43-3beta)sigma+24-6beta", "1/2<sigma<1", "PROVED_EXACT_ALGEBRA_CONDITIONAL_ON_SOURCE_INPUTS"),
        record("F10", "178--187,2371--2413", "The worst case", "q1=q gives beta=1; exact rational/radical comparison", "bases/constants q^(7/3)T^2, 9/4, (10-sqrt(10))/3, 30/13; maximum 7/3", "algebraic q1=q specialization; does not repair uniform T scope", "OPEN_ANALYTIC_INPUT:F10_UNIFORM_7_OVER_3_DEPENDS_ON_Z03_Z05_Z06"),
    ]
    require(tuple(item["id"] for item in out) == IDS, "Route A row ordering/count mismatch")
    require(len(out) == 46, "Route A must preserve all 46 canonical rows")
    return out


def certificate() -> dict[str, object]:
    pinned: dict[str, dict[str, str]] = {}
    for key, (path, wanted) in SOURCE_BYTES.items():
        require(path.is_file(), f"missing pinned input: {key}")
        got = digest(path)
        require(got == wanted, f"hash mismatch for {key}")
        pinned[key] = {"path": str(path.relative_to(ROOT)), "sha256": got}
    cgl = TEX.read_text(encoding="utf-8")
    gm = GM.read_text(encoding="utf-8")
    for anchor in ("\\label{Partial LVE}", "\\label{zero density estimate}", "if $X$ is polynomially bounded in $T$", "If $q$ is $T$-smooth, then", "The worst case for our zero density estimate is when $T=1"):
        require(anchor in cgl, f"CGL source anchor missing: {anchor}")
    for anchor in ("we work with $r=3$", "For the purposes of proving a zero density estimate", "E(W) :="):
        require(anchor in gm, f"GM source anchor missing: {anchor}")
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    require([x["id"] for x in prereg["row_registry"]] == list(IDS), "sealed preregistration IDs mismatch")
    r = rows()
    return {
        "artifact_id": "p6-cgl-v2-route-a-v1",
        "epistemic_status": "OBSERVED",
        "status": "OPEN_ANALYTIC_INPUT",
        "claim_boundary": "Literal source-order reconstruction only. It proves no Chen--Gupta--Li theorem, makes no repair (in particular no q<=T^C restriction), promotes no 7/3 result, and proves no new zero-density or short-interval theorem.",
        "route": "A: literal CGL-v2 theorem-chain source order",
        "source_disposition": "OBSERVED: CGL-v2 is a three-author arXiv preprint and prior work, not a result of this project.",
        "pinned_inputs": pinned,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "command": "python3 proof/reconstruct_p6_cgl_v2_route_a_v1.py --check"},
        "row_count": 46,
        "l12_subcheck_count": 2,
        "rows": r,
        "exact_algebra": exact_fraction_checks(),
        "open_blockers": [
            {"id": "S06_EXTERNAL_INPUTS", "rows": ["S06", "L04", "L06", "M07", "Z04", "Z07", "Z08", "F01", "F02"], "status": "OPEN_ANALYTIC_INPUT"},
            {"id": "Z03_TAIL_X_RANGE", "rows": ["Z03", "F10"], "status": "OPEN_ANALYTIC_INPUT", "forbidden_repair": "q<=T^C or log^2(qT) substitution"},
            {"id": "PRIMITIVE_TO_ALL", "rows": ["Z05", "Z06"], "status": "OPEN_ANALYTIC_INPUT"},
            {"id": "F08_T_SMOOTH_UNDEFINED", "rows": ["F08"], "status": "OPEN_ANALYTIC_INPUT"},
        ],
        "conclusion": "OBSERVED: all 46 registry rows and both L12 subchecks have a source-order trace. PROVED: the stated q1=q exact comparison algebra is correct conditional on the displayed source terms. The reconstruction remains OPEN_ANALYTIC_INPUT because the listed analytic sources and transfer/tail/smoothness obligations are not closed.",
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    started = time.monotonic_ns()
    value = certificate()
    encoded = render(value)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite Route A artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "Route A artifact mismatch")
    elapsed_ns = time.monotonic_ns() - started
    require(elapsed_ns < 60_000_000_000, "Route A replay exceeded 60 seconds")
    require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 262_144, "Route A replay exceeded 256 MiB")
    print(json.dumps({"artifact": OUT.name, "rows": 46, "status": value["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)

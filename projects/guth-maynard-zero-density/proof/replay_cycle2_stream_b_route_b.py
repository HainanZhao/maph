#!/usr/bin/env python3
"""Independent exact Stream-B Route-B application audit.

This script deliberately does not import Route A.  It records the source
matching, convention conversions, and rational power calculations behind the
GM section 13.1 application of MP Lemmas 23--24, GM Theorem 1.1, and
Montgomery's discrete mean-value theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GM = "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
MP = "artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex"
FROZEN = {
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    MP: "ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426",
    "artifacts/sources/montgomery-1969-inventiones8-gdz-volume.pdf": "b240c7c07d32201ced906bd0fdc4d36cca3c11999084afeb658ffca3f978534e",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.pdf": "3fc4c89f49249924e61cb0d289d81559faed53fcbb838628ea32dc7ec6f89fbf",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar": "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.pdf": "b1c5a4d6cdba59d0fc552a18cb2465c442a8534be0c4e51a23db126316f83077",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar": "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
}


def q(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_hashes() -> dict[str, str]:
    checked: dict[str, str] = {}
    for relative, expected in FROZEN.items():
        observed = digest(ROOT / relative)
        assert observed == expected, f"frozen source hash mismatch: {relative}"
        checked[relative] = observed
    return checked


def require_source_anchors() -> None:
    gm = (ROOT / GM).read_text(encoding="utf-8")
    mp = (ROOT / MP).read_text(encoding="utf-8")
    for phrase in (
        "If it is not a Type I zero then it is a `Type II zero'",
        "the number of Type II zeros is $\\le T^{2-2\\sigma}(\\log{T})^{O(1)}$ by \\cite[Lemma 24]{MP}",
        "let $\\psi(u)$ be a smooth function equal to $e^{u(\\sigma-\\beta)}$",
        "There are $O(\\log{T})$ non-trivial zeros",
        "We can then choose a value of $k\\ll 1$",
        "If instead we have $N^k>T^\\alpha$, then we apply the usual Mean Value Theorem",
    ):
        assert phrase in gm, f"GM source anchor missing: {phrase}"
    for phrase in (
        "either a Type I zero or a Type II zero (or both)",
        "R_{II}(\\sigma,T) \\ll T^{2(1-\\sigma)}(\\log T)^{O(1)}",
        "the zeros in a cluster are taken without multiplicity",
        "multiplicities only contribute harmless logarithmic factors",
    ):
        assert phrase in mp, f"MP source anchor missing: {phrase}"


def a(s: Fraction) -> Fraction:
    return 15 * (1 - s) / (3 + 5 * s)


def ell(s: Fraction) -> Fraction:
    return Fraction(10, 1) / (6 + 10 * s)


def upper(s: Fraction) -> Fraction:
    return Fraction(15, 1) / (6 + 10 * s)


def alpha(s: Fraction) -> Fraction:
    return 15 * (1 - s) / ((3 + 5 * s) * (Fraction(18, 5) - 4 * s))


def exact_checks() -> dict[str, str]:
    lo, mid, hi = Fraction(7, 10), Fraction(3, 4), Fraction(4, 5)
    assert ell(lo) == Fraction(10, 13)
    assert upper(hi) == Fraction(15, 14)
    assert all(ell(s) <= upper(s) for s in (lo, mid, hi))
    # Small-N choice k=ceil(ell/n): n>1/100 and ell<=10/13 imply k<=77.
    assert Fraction(10, 13) / Fraction(1, 100) < 77
    # Large-N choice k=2 has 2n>ell and 2n<=1+o(1)<upper+o(1).
    assert upper(hi) - 1 == Fraction(1, 14)
    # The three structural terms in the GM Theorem-1.1 branch.
    for s in (lo, mid, hi):
        assert 2 * (1 - s) * upper(s) == a(s)
        assert (Fraction(18, 5) - 4 * s) * alpha(s) == a(s)
        assert 1 + (Fraction(12, 5) - 4 * s) * ell(s) == a(s)
        assert 2 * (1 - s) * upper(s) == a(s)  # MVT first term too.
    # Cross-multiplying the stated residual has degree at most two; exact
    # agreement at three distinct rational points verifies that identity.
    for s in (lo, mid, hi):
        residual = (250 * (s - Fraction(3, 4)) ** 2 + Fraction(3, 8)) / (
            2 * (3 + 5 * s) * (9 - 10 * s)
        )
        assert 1 + (1 - 2 * s) * alpha(s) == a(s) - residual
        assert residual > 0
    return {
        "sigma_range": "[7/10,4/5]",
        "ell_max": q(ell(lo)),
        "upper_min": q(upper(hi)),
        "large_regime_gap": q(upper(hi) - 1),
        "mvt_residual": "[250(s-3/4)^2+3/8]/[2(3+5s)(9-10s)] > 0",
    }


def rows() -> list[dict[str, Any]]:
    return [
        {
            "id": "SB-B1-complement-to-mp-type-ii",
            "status": "PROVED",
            "locator": "GM §13.1, TeX lines 2310-2318; MP Definition Type I/II and Lemma 23, lines 975-1005",
            "hypotheses_checked": [
                "GM and MP use identical D_N: the truncated Mobius divisor sum, exp(-n/T^(1/2)), n~N, the same dyadic N range, and threshold 1/(3 log T)",
                "GM Type II means not GM Type I", "MP Lemma 23 says each positive-height zero is MP Type I or MP Type II (or both)"
            ],
            "transfer": "A GM-complement zero is not MP Type I, hence MP Lemma 23 places it in MP Type II. MP Lemma 24 gives the distinct-zero bound T^(2(1-sigma))(log T)^O(1).",
            "falsifier": "Any mismatch in detector, length range, or threshold would invalidate this inclusion.",
        },
        {
            "id": "SB-B2-multiplicity-and-two-sided-conversion",
            "status": "PROVED",
            "locator": "MP remark after Definition Cluster, lines 851-870; Hasanalizade-Shen-Wong Corollary 1.1; Bui-Heath-Brown introduction",
            "hypotheses_checked": [
                "MP explicitly treats cluster zeros without multiplicity", "Bui-Heath-Brown defines N(T) with multiplicity", "Hasanalizade-Shen-Wong gives N(T)=main term+O(log T) for T>=e"
            ],
            "transfer": "Subtract the Riemann-von Mangoldt bounds at u+1 and u-1 to get O(log(T+2)) multiplicity in each unit strip. Thus an MP distinct-zero bound loses only log T when converted to multiplicity. Since zeta(s)<0 on 0<s<1 (eta(s)>0 and eta(s)=(1-2^(1-s))zeta(s)), there is no real non-trivial zero; conjugation gives exactly twice the positive-height multiplicity count. Both conversions preserve T^o(1).",
            "falsifier": "A unit-strip multiplicity bound of size T^c, c>0, would invalidate the retained o(1) conversion.",
        },
        {
            "id": "SB-B3-type-i-smoothing-and-separated-extraction",
            "status": "PROVED",
            "locator": "GM §13.1, TeX lines 2319-2337; HSW/Bui local count as in SB-B2",
            "hypotheses_checked": [
                "psi(log n)=n^(sigma-beta) on n~N", "GM supplies rapid Fourier decay and truncation xi lessapprox 1", "a multiplicity-inclusive O(log T) unit-strip bound is pinned"
            ],
            "transfer": "Fourier inversion moves each Type-I value from gamma to gamma-2pi xi with |xi|<=T^epsilon after a T^-100 tail. A maximal 1-separated subset of shifted values covers only O(T^epsilon log T) source zeros per selected point. After the O(log T) detector pigeonhole, R is at least the positive-height multiplicity Type-I count times T^-o(1). Translation and endpoint padding put the set in an interval of length O(T), preserving coefficient and value moduli.",
        },
        {
            "id": "SB-B4-detector-and-powered-coefficient-normalization",
            "status": "PROVED",
            "locator": "GM §13.1, TeX lines 2310-2318 and 2334-2358",
            "hypotheses_checked": [
                "N>T^(1/100), because GM states b_n vanishes below this range", "|sum_(d|n,d<=2T^(1/100)) mu(d)|<=tau(n)", "n~N and N<=T^(1/2+o(1))", "both k regimes have k<=77"
            ],
            "transfer": "|tilde b_n|<=tau(n)=T^o(1). A coefficient of tilde D^k is bounded by a fixed-order divisor function times T^o(1), hence by T^o(1). Dividing the powered polynomial by this common sup norm supplies the coefficient hypothesis |c_m|<=1 and changes its value threshold only by T^-o(1).",
        },
        {
            "id": "SB-B5-both-k-regimes",
            "status": "PROVED",
            "locator": "GM §13.1, TeX lines 2339-2348",
            "hypotheses_checked": ["7/10<=sigma<=4/5", "N>T^(1/100)", "N<T^(1/2+o(1))"],
            "transfer": "For n=log N/log T<=5/(6+10sigma), take k=ceil(ell(sigma)/n); then ell<=kn<=upper and k<=77. For n>5/(6+10sigma), take k=2; then kn>ell and kn<=1+o(1)<upper+o(1), with exact endpoint gap upper(4/5)-1=1/14.",
            "loss": "Only the displayed o(1) from N<T^(1/2+o(1)) is used in the large-N regime.",
        },
        {
            "id": "SB-B6-support-blocks-and-threshold",
            "status": "PROVED",
            "locator": "GM §13.1, lines 2349-2358; GM Theorem 1.1, lines 68-81",
            "hypotheses_checked": ["L=N^k", "supp(tilde D^k) is contained in [L,2^k L]", "k<=77", "each Type-I selected value has |tilde D(t)|>=N^sigma T^-o(1)"],
            "transfer": "The k-th power has value at least L^sigma T^-o(1). Partition its support into O(k) dyadic blocks and pigeonhole a common block over W. Its length M satisfies M/L=O_k(1), so after coefficient normalization its threshold is V=M^sigma T^-o(1) on a 1-separated set in an interval of length O(T).",
        },
        {
            "id": "SB-B7-large-values-structural-terms",
            "status": "PROVED",
            "locator": "GM Theorem 1.1 and §13.1, lines 2349-2358",
            "hypotheses_checked": ["SB-B3 1-separation/interval transfer", "SB-B4 coefficient normalization", "SB-B6 one dyadic support block and V=M^sigma T^-o(1)", "L<=T^alpha in this branch"],
            "transfer": "Theorem 1.1 gives L^(2-2sigma)+L^(18/5-4sigma)+T L^(12/5-4sigma), up to T^o(1). The upper L bound, alpha definition, and lower L bound respectively make all three exponents exactly A(sigma)=15(1-sigma)/(3+5sigma).",
        },
        {
            "id": "SB-B8-montgomery-discrete-mvt-and-polarity",
            "status": "PROVED",
            "locator": "H. L. Montgomery, Mean and Large Values of Dirichlet Polynomials, Invent. Math. 8 (1969), Theorem 1 / formula (7), printed p. 335, frozen volume PDF p. 348",
            "hypotheses_checked": ["arbitrary complex coefficients", "1-separated selected heights", "endpoint-padded enclosing interval has delta>=1 and length O(T)", "the block is supported on m<=2M"],
            "transfer": "Montgomery bounds the discrete sum of |sum a_m m^(-it_r)|^2 by (T+O(M log M))(delta^-1+log M) sum|a_m|^2. Complex conjugation converts GM's m^(it_r) to m^(-it_r) without changing moduli. With |a_m|<=1, sum|a_m|^2<=O(M), yielding R<=T^o(1)(M^(2-2sigma)+T M^(1-2sigma)).",
        },
        {
            "id": "SB-B9-mvt-branch-and-strict-residual",
            "status": "PROVED",
            "locator": "GM §13.1 equation (13.2), TeX lines 2359-2368",
            "hypotheses_checked": ["L=N^k>T^alpha", "1-2sigma<0", "L<=T^upper", "7/10<=sigma<=4/5<9/10"],
            "transfer": "The first MVT term is at most T^A. The second is at most T^(1+(1-2sigma)alpha), and A-[1+(1-2sigma)alpha]=[250(sigma-3/4)^2+3/8]/[2(3+5sigma)(9-10sigma)]>0. Thus it is strictly below T^A; no finite-T equality is asserted.",
        },
        {
            "id": "SB-B10-dyadic-reassembly-and-route-boundary",
            "status": "PROVED",
            "locator": "GM §13.1 opening reduction, lines 2305-2308; SB-B1-SB-B9",
            "hypotheses_checked": ["positive-height shell bound for sigma in [7/10,4/5]", "a=2(1-sigma)>0", "multiplicity and conjugation conversion in SB-B2"],
            "transfer": "The Type-II contribution is T^(2(1-sigma)+o(1))<=T^(A(sigma)+o(1)); Type-I is bounded by the two application branches. Summing positive dyadic shells is dominated by the largest shell, and conjugation gives the frozen two-sided convention. Hence this source route reproduces GM's stated density exponent on [7/10,4/5].",
            "claim_boundary": "This is a source-hypothesis and exact-transfer audit, not an independent reproving of MP Lemmas 23-24, their twisted-fourth-moment input, GM Theorem 1.1, or GM Theorem 1.2.",
        },
    ]


def certificate() -> dict[str, Any]:
    hashes = frozen_hashes()
    require_source_anchors()
    exact = exact_checks()
    audit_rows = rows()
    assert all(row["status"] == "PROVED" for row in audit_rows)
    return {
        "artifact_id": "cycle-2-stream-b-route-b-v1",
        "route": "B",
        "stream": "B",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED only as a pinned-source application audit. No new zero-density theorem, no independent proof of MP/GM analytic theorems, and no full G0 promotion are claimed.",
        "pass_state": "NARROW PASS: every preregistered Stream-B application node (including MP complement inclusion, multiplicity/two-sided conversion, and MVT branch) is source-pinned and checked. Stream C's external explicit-formula node remains outside this audit.",
        "frozen_source_hashes": hashes,
        "exact_rational_checks": exact,
        "rows": audit_rows,
        "label_coverage": {"required_nodes": 10, "labeled_rows": len(audit_rows), "unlabeled_nodes": []},
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": digest(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_b_route_b.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-b-v1.json",
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()

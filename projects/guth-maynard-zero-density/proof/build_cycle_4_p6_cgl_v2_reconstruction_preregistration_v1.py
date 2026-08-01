#!/usr/bin/env python3
"""Seal the bounded 46-row CGL-v2 reconstruction preregistration."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import signal
import sys
import tarfile
import time


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
TEX_NAME = "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "optimization_level": 0,
    "platform": "linux",
}
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144
INPUTS: dict[str, tuple[Path, str]] = {
    "authorization_snapshot": (
        ROOT / "artifacts/cycle-4-p6-cgl-v2-authorization-snapshot-v1.json",
        "c8183266cbfab602ba3c05c120a80293b7741284d6c46a08a88c03c3b46f25b3",
    ),
    "preregistration_document": (
        ROOT / "docs/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.md",
        "2208164bdb207c0322fe376c21553f7dc4f307625328b8542fa2abe358dafd47",
    ),
    "cgl_v2_tex": (
        ROOT / "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2" / TEX_NAME,
        "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f",
    ),
    "cgl_v2_tar": (
        ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar",
        "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae",
    ),
    "cgl_v2_pdf": (
        ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.pdf",
        "adfe65cf0952bbb4eddfdaec7a8d3341130e427827f9159d9da039fc16336058",
    ),
    "bounded_literature_audit_v1": (
        ROOT / "artifacts/g1-current-literature-audit-v1.json",
        "49da2e838ce60699ba870e0c532aab5ec8ba564c560811d9683ac92f0afbe6be",
    ),
    "bounded_literature_correction_v2": (
        ROOT / "artifacts/g1-current-literature-audit-v2-correction.json",
        "f56529c5919971385cc583b51255636022a5b33fb0cfd4857a587f1d3e099076",
    ),
}
EXPECTED_ROW_IDS = (
    tuple(f"S{index:02d}" for index in range(1, 7))
    + tuple(f"L{index:02d}" for index in range(1, 13))
    + tuple(f"M{index:02d}" for index in range(1, 9))
    + tuple(f"Z{index:02d}" for index in range(1, 11))
    + tuple(f"F{index:02d}" for index in range(1, 11))
)
EXPECTED_BLOCKERS = (
    "S06_EXTERNAL_INPUTS",
    "Z03_TAIL_X_RANGE",
    "Z05_PRIMITIVE_EULER_FACTORS",
    "Z06_CONDUCTOR_SUM_Q1",
    "F08_T_SMOOTH_UNDEFINED",
)
SOURCE_FRAGMENTS = (
    "\\author{Bin Chen}",
    "\\author{Vishal Gupta}",
    "\\author{Yung Chi Li}",
    "\\begin{theorem}[Large value estimate for Dirichlet polynomials with characters]\\label{Partial LVE}",
    "where $\\chi$ is a primitive character modulo $q$ and $|a_{n}| \\leq1$",
    "Asymptotic quantities such as $o(1)$ are interpreted as $qT \\to \\infty$.",
    "\\begin{lemma}[Character subdivision]\\label{character subdivision}",
    "For a character modulo $2^j$ we may use the same argument",
    "\\section{Energy bound}\\label{Engb}",
    "\\section{\\texorpdfstring{Application to Dirichlet $L$-functions}",
    "The tail of the sum $\\sum_{n > Y\\log^2 Y}",
    "if $X$ is polynomially bounded in $T$",
    "where we have set $X = (qT)^{\\epsilon}$.",
    "If $q$ is $T$-smooth, then",
    "The worst case for our zero density estimate is when $T=1$",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def check_runtime() -> dict[str, Any]:
    observed = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
        "platform": sys.platform,
    }
    require(
        observed == EXPECTED_RUNTIME,
        "P6 CGL-v2 preregistration requires non-optimized CPython 3.12.3 on linux",
    )
    return observed


def row(
    row_id: str,
    obligation: str,
    locator: str,
    disposition: str = "UNEXECUTED",
    subchecks: tuple[str, ...] = (),
) -> dict[str, object]:
    value: dict[str, object] = {
        "id": row_id,
        "initial_status": "UNEXECUTED",
        "locator": locator,
        "obligation": obligation,
        "preregistered_disposition": disposition,
    }
    if subchecks:
        value["mandatory_subchecks"] = list(subchecks)
    return value


def registry() -> list[dict[str, object]]:
    rows = [
        row("S01", "TeX/tar-member/PDF identity and complete-source boundary", "entire TeX; tar member; PDF"),
        row("S02", "authors, collaboration/version statement, title, and preprint status", "77--105"),
        row("S03", "zero-count definition, two-sided height, rectangle, and multiplicity audit", "95--101, 141--148, 158--185"),
        row("S04", "domains for q,T,X,Y,sigma, endpoints, and qT-to-infinity interpretation", "114--128, 158--187, 268--270, 2114"),
        row("S05", "o(1), epsilon, lessapprox, constants, and limiting-order convention", "122--126, 268--273"),
        row("S06", "external-input inventory with exact theorem hypotheses and primary-source locators", "133--140, 537--560, 1691--1695, 2112, 2158, 2169, 2414--2467", "EXPECTED_OPEN:S06_EXTERNAL_INPUTS"),
        row("L01", "Partial-LVE primitive-character, coefficient, separation, threshold, and length hypotheses", "114--123"),
        row("L02", "divisor-sensitive four-term Partial-LVE formula", "122--124"),
        row("L03", "all-case four-term Partial-LVE formula", "125--127"),
        row("L04", "low-value qT mean-value comparator and valid range", "133--136, 421"),
        row("L05", "intermediate-value reduction, three-piece smoothing, and separation thinning", "375--443"),
        row("L06", "high-value HMH comparator and valid range", "137--140, 421, 487--500"),
        row("L07", "qT<=N case and epsilon-limit step", "445--448"),
        row("L08", "N<=qT<=N^(6/5) Auxiliary-proposition case", "449--452"),
        row("L09", "subdivision case q1>N^(6/5)", "454--478"),
        row("L10", "subdivision case N^(6/5)/T<q1<N^(6/5)", "454--470, 480--485"),
        row("L11", "subdivision case q1<N^(6/5)/T including HMH combination", "454--470, 487--504"),
        row("L12", "character subdivision for odd-prime and 2-power moduli", "507--519", subchecks=("odd_prime", "two_power")),
        row("M01", "smoothed Auxiliary proposition, bump normalization, hypotheses, and conclusion", "375--387"),
        row("M02", "matrix and singular-value reductions, trace subtraction, constants, and hypotheses", "528--550"),
        row("M03", "Hilbert-Schmidt/cubic-trace expansion, Poisson conventions, diagonal subtraction, and errors", "552--660"),
        row("M04", "S1 partition and estimate with all ranges", "661--733"),
        row("M05", "S2, approximate functional equation, dyadic variables, and bound", "734--1128"),
        row("M06", "affine/GCD-twist estimate, induction, Fourier decay, and norm comparisons", "1129--1686"),
        row("M07", "character-time energy, Heath-Brown input, hypotheses, and closing estimate", "1688--1709, 1963--1971"),
        row("M08", "S3 estimate and dominance calculation closing the Auxiliary proposition", "1974--2105"),
        row("Z01", "Mellin identity, contour shift, and both residues", "2114--2134"),
        row("Z02", "weighted Dirichlet-series sum tail beyond Y log^2 Y", "2140--2143"),
        row("Z03", "integral tail, X-versus-T hypothesis, uniform q,T scope, and T=1 endpoint", "2140, 2169, 2411--2413", "EXPECTED_OPEN:Z03_TAIL_X_RANGE"),
        row("Z04", "principal-character residue and low-height-zero contribution after primitive restriction", "2134--2138", "UNEXECUTED_WITH_WATCH"),
        row("Z05", "induced-character Euler factors and zero-set equality in sigma>1/2", "2109, 2136--2138", "EXPECTED_OPEN:Z05_PRIMITIVE_EULER_FACTORS"),
        row("Z06", "conductor partition, multiplicity/divisor loss, and q1-sensitive termwise domination", "2109, 2148--2152", "EXPECTED_OPEN:Z06_CONDUCTOR_SUM_Q1"),
        row("Z07", "saturated well-spacing selection and local zero-count input", "2154--2158"),
        row("Z08", "class-II maximizers, shifted spacing, fourth moment, and Y=(qT)^(1/2)", "2160--2173", "UNEXECUTED_WITH_WATCH"),
        row("Z09", "class-I dyadic selection, normalization, representative loss, and length range", "2176--2197"),
        row("Z10", "bounded k, powered coefficient control, and complete length-case coverage", "2199--2258", "UNEXECUTED_WITH_WATCH"),
        row("F01", "outer sigma<=0.7 range via the stated Ingham analogue", "141--149, 2109"),
        row("F02", "outer sigma>=0.8 range via the stated Huxley analogue", "145--149, 2109"),
        row("F03", "middle-range four-term zero-density lemma and hypotheses", "2261--2270"),
        row("F04", "divisor Case 1 and complete interval coverage", "2276--2310"),
        row("F05", "divisor Case 2 and complete interval coverage", "2276--2282, 2311--2325"),
        row("F06", "divisor Case 3, feasibility, and complete interval coverage", "2276--2282, 2326--2336"),
        row("F07", "divisor Case 4 and comparison with desired terms", "2276--2282, 2337--2345"),
        row("F08", "T-smooth definition, divisor-chain existence, endpoints, and coverage", "182--185, 2266--2269, 2346--2350, 2410", "EXPECTED_OPEN:F08_T_SMOOTH_UNDEFINED"),
        row("F09", "four coefficient crossings with Ingham including quadratic/radical branch", "2357--2410"),
        row("F10", "q1=q reductions, exact inequalities, uniform 7/3, and worst-T scope", "178--187, 2371--2413"),
    ]
    ids = tuple(item["id"] for item in rows)
    require(len(rows) == 46, "canonical registry does not contain exactly 46 rows")
    require(ids == EXPECTED_ROW_IDS, "canonical row IDs or ordering changed")
    require(len(set(ids)) == 46, "canonical row IDs are not unique")
    require("L13" not in ids, "retired draft L13 alias became an executable row")
    l12 = rows[ids.index("L12")]
    require(l12.get("mandatory_subchecks") == ["odd_prime", "two_power"], "L12 subchecks changed")
    return rows


def verify_inputs() -> tuple[dict[str, dict[str, str]], str]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        observed = sha256(path)
        require(observed == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": observed}

    tex_bytes = INPUTS["cgl_v2_tex"][0].read_bytes()
    with tarfile.open(INPUTS["cgl_v2_tar"][0], mode="r:*") as archive:
        members = archive.getnames()
        require(TEX_NAME in members, "canonical CGL TeX member missing from tar")
        member = archive.getmember(TEX_NAME)
        require(member.isfile(), "canonical CGL TeX tar member is not a regular file")
        extracted = archive.extractfile(member)
        require(extracted is not None, "canonical CGL TeX tar member cannot be read")
        require(extracted.read() == tex_bytes, "canonical CGL TeX tar member byte mismatch")

    tex = tex_bytes.decode("utf-8")
    require(len(tex.splitlines()) == 2468, "canonical CGL TeX logical-line count changed")
    require(tex_bytes.count(b"\n") == 2467, "canonical CGL TeX newline count changed")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in tex, f"CGL source fragment missing: {fragment}")

    snapshot = load_json(INPUTS["authorization_snapshot"][0])
    require(snapshot.get("artifact_id") == "cycle-4-p6-cgl-v2-authorization-snapshot-v1", "wrong authorization snapshot")
    historical = snapshot.get("historical_replay", {})
    require(historical.get("live_plan_hash_pinned") is False, "authorization snapshot pins mutable plan hash")
    require(historical.get("live_plan_read_required") is False, "authorization snapshot requires mutable plan read")
    correction = snapshot.get("registry_count_correction", {})
    require(correction.get("draft_arithmetic") == "6+13+8+10+10=47, not 46", "draft count inconsistency not preserved")
    require(correction.get("canonical_count") == 46, "authorization snapshot canonical count changed")
    require(correction.get("retired_draft_aliases") == {"L13": "L12.two_power"}, "draft L13 alias resolution changed")
    require(correction.get("no_obligation_dropped") is True, "count correction drops an obligation")
    semantic = snapshot.get("semantic_authorization", {})
    require(semantic.get("expected_gate_outcome") == "OPEN_ANALYTIC_INPUT", "authorization expected outcome changed")

    literature = load_json(INPUTS["bounded_literature_audit_v1"][0])
    source_hashes = literature.get("source_verification", {}).get("source_hashes", {})
    require(source_hashes.get("chen_tex", {}).get("sha256") == INPUTS["cgl_v2_tex"][1], "literature audit TeX identity mismatch")
    require(source_hashes.get("chen_tar", {}).get("sha256") == INPUTS["cgl_v2_tar"][1], "literature audit tar identity mismatch")
    require(source_hashes.get("chen_pdf", {}).get("sha256") == INPUTS["cgl_v2_pdf"][1], "literature audit PDF identity mismatch")
    source_status = literature.get("sources", {}).get("chen_gupta_li_2507_08296v2", {}).get("status", "")
    require("OBSERVED arXiv preprint; three-author v2" in source_status, "CGL v2 preprint status mismatch")
    correction_v2 = load_json(INPUTS["bounded_literature_correction_v2"][0])
    preserved = correction_v2.get("integrity", {}).get("preserved_v1", {}).get("v1_artifact", {})
    require(preserved.get("sha256") == INPUTS["bounded_literature_audit_v1"][1], "literature correction does not preserve v1")
    return frozen, TEX_NAME


def certificate() -> dict[str, object]:
    runtime = check_runtime()
    frozen, tar_member = verify_inputs()
    rows = registry()
    blockers = [
        {
            "id": "S06_EXTERNAL_INPUTS",
            "row": "S06",
            "epistemic_status": "OBSERVED",
            "reason": "Reachable primary external theorem hypotheses are not closed by the pinned CGL bytes.",
        },
        {
            "id": "Z03_TAIL_X_RANGE",
            "row": "Z03",
            "epistemic_status": "OBSERVED",
            "reason": "TeX 2140 uses T-to-infinity and X polynomial in T; TeX 2169 sets X=(qT)^epsilon, while the theorem is uniform and TeX 2412 names T=1 as worst.",
        },
        {
            "id": "Z05_PRIMITIVE_EULER_FACTORS",
            "row": "Z05",
            "group": "PRIMITIVE_TO_ALL",
            "epistemic_status": "OBSERVED",
            "reason": "The induced-character Euler-factor zero comparison in sigma>1/2 is not supplied at TeX 2109.",
        },
        {
            "id": "Z06_CONDUCTOR_SUM_Q1",
            "row": "Z06",
            "group": "PRIMITIVE_TO_ALL",
            "epistemic_status": "OBSERVED",
            "reason": "Conductor partition, divisor loss, and q1-sensitive termwise domination are not supplied at TeX 2109.",
        },
        {
            "id": "F08_T_SMOOTH_UNDEFINED",
            "row": "F08",
            "epistemic_status": "OBSERVED",
            "reason": "T-smooth is used at TeX 182, 2266, and 2346--2350 but is not defined in the complete pinned TeX.",
        },
    ]
    require(tuple(item["id"] for item in blockers) == EXPECTED_BLOCKERS, "expected blocker registry changed")
    return {
        "artifact_id": "cycle-4-p6-cgl-v2-reconstruction-preregistration-v1",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_PREREGISTRATION_EXPECTED_OPEN_ANALYTIC_INPUT",
        "expected_reconstruction_outcome": "OPEN_ANALYTIC_INPUT",
        "claim_boundary": (
            "Bounded preregistration only: no reconstruction is executed, no CGL theorem is proved or repaired, no 7/3 result is promoted, "
            "no novelty claim is made, no P7 family is selected, and no zero-density or short-interval theorem follows."
        ),
        "source_disposition": "OBSERVED three-author arXiv:2507.08296v2 preprint and prior work",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_inputs": frozen,
        "source_integrity": {
            "canonical_tar_member": tar_member,
            "tar_member_equals_canonical_tex": True,
            "logical_line_count": 2468,
            "newline_count": 2467,
        },
        "historical_replay": {
            "authorization_source": "immutable authorization snapshot",
            "mutable_research_plan_read": False,
            "mutable_research_plan_hash_pinned": False,
            "operational_preflight": "EXCLUDED_NOT_NEEDED_FOR_HISTORICAL_REPLAY",
        },
        "registry_count_correction": {
            "draft_arithmetic": "6+13+8+10+10=47, not 46",
            "canonical_ranges": "S01-S06,L01-L12,M01-M08,Z01-Z10,F01-F10",
            "canonical_count": 46,
            "resolution": "L12 has mandatory odd_prime and two_power subchecks; draft L13 is retired alias L12.two_power",
            "retired_draft_aliases": {"L13": "L12.two_power"},
            "no_obligation_dropped": True,
        },
        "conventions": {
            "zero_count": "N(sigma,T,chi): sigma<=Re rho<=1 and |Im rho|<=T; multiplicity is an audit obligation",
            "character_scope": "Partial LVE primitive; headline zero-density sum all characters; no transfer before Z05/Z06",
            "q1": "q1 divides q",
            "asymptotic": "o(1) and lessapprox are interpreted as qT->infinity with (qT)^epsilon losses",
            "separation": "distinct pairs differ in character or meet the row-specific ordinate gap",
            "fourier": "e(x)=exp(2*pi*i*x); Fourier transform integral f(x)e(-xi*x) dx",
            "detector_domain": "source states X,Y,T>1; uniform q,T and T=1 scope must be audited",
            "forbidden_repairs": ["q<=T^C", "replace log^2 T by log^2(qT)", "invent T-smooth definition", "supply primitive/all proof without source or proved derivation"],
        },
        "route_b_coordinates": {
            "alpha": "log(q)/log(qT)",
            "tau": "1-alpha",
            "lambda": "log(q1)/log(qT)",
            "beta": "lambda+tau=log(q1*T)/log(qT)",
            "q1_at_least_sqrt_q": "beta>=1/2",
        },
        "frozen_crossing_formulas": {
            "C1": "3*(1+lambda/3)/(1+sigma)",
            "C2": "3*(1-beta/2)/sigma",
            "C3": "((21-20*sigma)/6-beta/2)/(1-sigma)",
            "C4": "15/(3+5*sigma)",
            "crossing_C1": "(q1^(1/3)*q^2*T^2)^(1-sigma)",
            "crossing_C2": "(q^3*T^(9/4)*q1^(-3/4))^(1-sigma)",
            "crossing_C3_polynomial": "20*sigma^2-(43-3*beta)*sigma+24-6*beta=0",
            "B": "(37+3*beta-sqrt(9*beta^2+222*beta-71))/12",
            "crossing_C4": "sigma=7/10 and coefficient=30/13",
            "q1_equals_q_reductions": ["q^(7/3)*T^2", "9/4", "(10-sqrt(10))/3", "30/13"],
            "uniform_7_over_3_checks": ["2<=7/3", "7/3-9/4=1/12", "sqrt(10)>3 because 10>9", "7/3-30/13=1/39"],
        },
        "row_registry": rows,
        "expected_blockers": blockers,
        "route_design": {
            "route_A": "literal source-order theorem chain with exact rational/radical algebra and expanded cited hypotheses",
            "route_B": "independent alpha/tau/lambda/beta exponent-polytope and prime-by-prime conductor audit using cleared denominators",
            "independence": "Route B may not import Route A code, artifacts, intermediate outputs, inferred labels, or repaired formulas.",
            "reconciliation": "Compare all 46 IDs, both L12 subchecks, locators, hypotheses, formulas, valid regions, blocker labels, and dispositions.",
        },
        "gate_rule": {
            "pass": "all 46 rows and both L12 subchecks close independently by both routes and reconcile exactly",
            "open": "any analytic input remains open, including any expected blocker or unread reachable source",
            "fail_closed": "source mismatch, route disagreement, missing row/subcheck, cap breach, optimized mode, or unregistered repair",
            "expected": "OPEN_ANALYTIC_INPUT",
        },
        "resource_policy": {
            "wall_time": "strictly less than 60 seconds",
            "peak_rss": "strictly less than 262144 KiB (256 MiB) on linux",
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
            "floating_point": "PROHIBITED",
            "rng": "PROHIBITED",
            "network": "PROHIBITED",
            "method_substitution_after_cap_failure": "PROHIBITED",
        },
        "falsifier": (
            "Any frozen-byte or tar-member mismatch, row-count/alias inconsistency, missing mandatory subcheck, source-fragment mismatch, "
            "runtime/resource violation, silent analytic repair, or historical dependence on mutable operational state invalidates this seal."
        ),
        "replay": {
            "write_command": "python3 proof/build_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py --write",
            "check_command": "python3 proof/build_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py -v",
        },
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def enforce_resources(started_ns: int) -> None:
    elapsed_ns = time.monotonic_ns() - started_ns
    peak_rss_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed_ns < WALL_CAP_NS, "P6 CGL-v2 preregistration exceeded 60-second wall cap")
    require(peak_rss_kib < RSS_CAP_KIB, "P6 CGL-v2 preregistration exceeded 256-MiB RSS cap")


def alarm_handler(signum: int, frame: object) -> None:
    del signum, frame
    raise RuntimeError("P6 CGL-v2 preregistration exceeded 60-second wall cap")


def main() -> int:
    started_ns = time.monotonic_ns()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(60)
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument("--write", action="store_true")
        mode.add_argument("--check", action="store_true")
        args = parser.parse_args()
        payload = certificate()
        encoded = render(payload)
        if args.write:
            enforce_resources(started_ns)
            require(not OUTPUT.exists(), "refusing to overwrite P6 CGL-v2 preregistration v1 artifact")
            with OUTPUT.open("xb") as handle:
                handle.write(encoded)
        else:
            require(OUTPUT.is_file(), "P6 CGL-v2 preregistration v1 artifact is absent")
            require(OUTPUT.read_bytes() == encoded, "P6 CGL-v2 preregistration v1 artifact mismatch")
            enforce_resources(started_ns)
    finally:
        signal.alarm(0)
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)

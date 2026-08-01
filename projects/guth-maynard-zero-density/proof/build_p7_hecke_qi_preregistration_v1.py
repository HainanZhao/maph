#!/usr/bin/env python3
"""Seal the source-pinned, unexecuted P7 Q(i) Hecke preregistration."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import tarfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_hecke_qi_v1 as C


OUT = ROOT / "artifacts/p7-hecke-qi-preregistration-v1.json"
DOC = ROOT / "docs/p7-hecke-qi-preregistration-v1.md"
CONVENTIONS = ROOT / "conventions/p7_hecke_qi_v1.py"
ZAMAN_PDF = ROOT / "artifacts/sources/p7-hecke-v1/zaman-1502.05679v4.pdf"
ZAMAN_TAR = ROOT / "artifacts/sources/p7-hecke-v1/zaman-1502.05679v4.tar"
ZAMAN_TEX = "Explicit_estimates_for_the_zeros_of_Hecke_L-functions.tex"
TZ_PDF = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1.pdf"
TZ_TAR = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1.tar"
TZ_TEX = "LFZD_manuscript.tex"
THORNER_MRL = ROOT / "artifacts/sources/p7-hecke-v1/thorner-2019-mrl-v26n3-a9.pdf"
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144

PINS = {
    ZAMAN_PDF: "ca1ab8d8844994b999f99d7a97dfa0ae4770a8f8687f07886e81946f94d25941",
    ZAMAN_TAR: "f530b910a9aa7bed81f6fb9ed6119cdb619f8e78b4c49593ec0a2a32d8707746",
    TZ_PDF: "94ddf7864fe74d266cef42816c9621516079321c48069d848527e7d0067b866d",
    TZ_TAR: "082be65a8fc04b5795290e500e0b2d74dc7a818cb68cc5ddc02131012b178fa2",
    THORNER_MRL: "463bd56afd679444e4cf3417228230e9996b1202daeac47c3b436b4b2776d1b3",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tar_text(path: Path, member_name: str) -> tuple[str, str]:
    with tarfile.open(path, "r") as archive:
        member = archive.getmember(member_name)
        extracted = archive.extractfile(member)
        require(extracted is not None, f"missing {member_name} in {path.name}")
        data = extracted.read()
    return data.decode("utf-8"), hashlib.sha256(data).hexdigest()


def source_checks() -> dict[str, object]:
    for path, expected in PINS.items():
        require(path.is_file(), f"missing frozen source {path.name}")
        require(digest(path) == expected, f"source hash changed for {path.name}")
    zaman, zaman_tex_hash = tar_text(ZAMAN_TAR, ZAMAN_TEX)
    tz, tz_tex_hash = tar_text(TZ_TAR, TZ_TEX)
    require("\\label{HeckeL-functions}" in zaman, "Zaman Hecke conventions locator changed")
    require("primitive modulo $\\kq$" in zaman, "Zaman primitive convention locator changed")
    require("\\label{MainTheorem-ZD}" in zaman, "Zaman density locator changed")
    require("\\label{LFZD-MainTheorem}" in tz, "Thorner--Zaman density theorem locator changed")
    require("nontrivial zeros $\\rho$ of $L(s,\\chi)$ are counted with multiplicity" in tz, "Thorner--Zaman multiplicity locator changed")
    return {
        "zaman_1502_05679v4": {
            "primary_source": "arXiv:1502.05679v4 (29 Mar 2016)",
            "pdf": {"path": str(ZAMAN_PDF.relative_to(ROOT)), "sha256": PINS[ZAMAN_PDF], "pages": 53},
            "source_tar": {"path": str(ZAMAN_TAR.relative_to(ROOT)), "sha256": PINS[ZAMAN_TAR]},
            "tex_member": {"name": ZAMAN_TEX, "sha256": zaman_tex_hash},
            "checked_locators": {
                "ray_class_and_euler_product": "TeX 68--91; PDF p.1",
                "primitive_exact_conductor_and_zero_extension": "TeX 295--303; PDF p.6",
                "explicit_near_one_density_scope": "TeX 225--253; PDF pp.3--4",
            },
            "role": "family definitions and prior explicit near-one zero-density context only",
        },
        "thorner_zaman_1510_08086v1": {
            "primary_source": "arXiv:1510.08086v1 (27 Oct 2015)",
            "pdf": {"path": str(TZ_PDF.relative_to(ROOT)), "sha256": PINS[TZ_PDF], "pages": 32},
            "source_tar": {"path": str(TZ_TAR.relative_to(ROOT)), "sha256": PINS[TZ_TAR]},
            "tex_member": {"name": TZ_TEX, "sha256": tz_tex_hash},
            "checked_locators": {
                "zero_count_and_multiplicity": "TeX 425--448; PDF p.4",
                "explicit_log_free_density": "Theorem 1.1, TeX 441--449; PDF p.4",
                "detector_and_hecke_large_sieve_mechanism": "TeX 468--472; PDF pp.4--5",
                "finite_euler_factor_for_induction": "TeX 1162--1166",
            },
            "role": "prior log-free density, primitive/conductor conventions, and detector comparison only",
        },
        "thorner_mrl_2019": {
            "primary_source": "J. Thorner, Math. Res. Lett. 26 (2019), 875--901",
            "publisher_pdf": {"path": str(THORNER_MRL.relative_to(ROOT)), "sha256": PINS[THORNER_MRL], "pages": 28},
            "checked_locators": {
                "title_abstract_bv_and_bounded_gaps": "PDF p.1 (printed p.875)",
                "fixed_K_hecke_context": "PDF pp.2--3 (printed pp.876--877)",
                "hecke_large_sieve": "Theorem 2.1, PDF pp.9--10 (printed pp.883--884)",
                "averaged_density": "Theorem 2.3, PDF p.11 (printed p.885)",
                "primitive_ray_class_embedding": "PDF p.21 (printed p.895)",
            },
            "role": "prior Hecke large-sieve/density, Bombieri--Vinogradov, and bounded-gap work to concede",
        },
        "bgl_rejected_comparison": {
            "status": "NOT_USED_AS_AUTHORITY",
            "reason": "The selected finite ray-class family is not the BGL comparison family. No theorem, definition, or transfer claim in this preregistration relies on BGL.",
        },
    }


def gates() -> list[dict[str, object]]:
    return [
        {
            "id": "P7-0-SOURCE-FAMILY",
            "state": "UNEXECUTED",
            "purpose": "Check the selected Q(i) finite-ray-class family against the pinned source definitions and exclude angular characters.",
            "pass_rule": "Every exact-conductor, height, multiplicity, Euler-product, and archimedean convention agrees with the frozen conventions module; all departures receive a versioned correction.",
            "failure_rule": "Contain the family statement and do not aggregate sources or begin a theorem search.",
        },
        {
            "id": "P7-1-NORM-AGGREGATION",
            "state": "UNEXECUTED",
            "first_falsifiable_gate": True,
            "purpose": "Determine whether divisor-bounded norm aggregation can be absorbed in the target epsilon bookkeeping while recording why it does not supply a direct joint-character application of a single-polynomial Guth--Maynard theorem.",
            "frozen_identities": [
                "A_chi(n)=sum_{Na=n}chi(a), |A_chi(n)|<=a_K(n)=sum_{d|n}chi_{-4}(d)<=tau(n)",
                "for every epsilon>0, max_{n<=2N}tau(n)<<_epsilon N^epsilon",
                "for split p=pi*pi_bar with p not dividing f, A_chi(p)=chi(pi)+chi(pi_bar)",
            ],
            "preselected_witness": C.REPEATED_NORM_WITNESS,
            "pass_rule": "Prove that the exact prospective ideal/character large-value inequality is stable under the displayed N^epsilon normalization, and verify the fixed Q=8 witness. Record PASS_TYPE_MISMATCH if its two aggregated coefficients differ; that outcome blocks only a direct single-coefficient-vector import, not an adapted character theorem.",
            "failure_rule": "If the epsilon normalization is not stable, label COEFFICIENT_LOSS_NOT_HARMLESS. If the fixed witness arithmetic fails, label WITNESS_OR_CONVENTION_ERROR and issue a correction; neither outcome licenses a density claim.",
            "direct_import_boundary": "The Guth--Maynard single-polynomial theorem has one coefficient vector shared by all sample points. Here A_chi varies with chi, so it cannot be applied verbatim to the joint set of (chi,t) samples. Applying it separately in chi and summing is a distinct route with a separate family-size accounting gate.",
        },
        {
            "id": "P7-2-RAY-CLASS-ORTHOGONALITY",
            "state": "UNEXECUTED",
            "purpose": "Build the correct complete- and primitive-character projectors over Cl(f), including exact-conductor inclusion-exclusion and all ideal coprimality conditions.",
            "pass_rule": "State and prove the complete-character identity sum_chi chi(a)conj(chi(b))=|Cl(f)| times the ray-class diagonal, then derive the primitive projector without silently replacing it by the complete one.",
            "failure_rule": "If primitive inclusion-exclusion or its local conductor factors are unresolved, retain PRIMITIVE_PROJECTOR_OPEN and do not claim family orthogonality.",
        },
        {
            "id": "P7-3-IDEAL-CUBIC-ENERGY",
            "state": "UNEXECUTED",
            "purpose": "Formulate ideal-indexed large values, cubic trace, and energy with character orthogonality before any Guth--Maynard comparison.",
            "pass_rule": "Give an exact common sample space, separation convention, ideal-product/ratio relation, diagonal convention for equal norms, and an error term that includes repeated norms rather than treating them as integer diagonals.",
            "failure_rule": "If equal-norm ideals or primitive projection introduce an uncontrolled term, retain IDEAL_ENERGY_OPEN; no cubic transfer is licensed.",
        },
        {
            "id": "P7-4-DETECTOR-TAIL",
            "state": "UNEXECUTED",
            "purpose": "Check a zero detector and its ideal-sum tail uniformly in the frozen Q,T,sigma ranges, including principal/pole and low-height conventions.",
            "pass_rule": "A pinned theorem/proof supplies a detector with every length, smoothness, conductor, and tail hypothesis checked for primitive finite-order Q(i) characters.",
            "failure_rule": "Retain DETECTOR_OR_TAIL_OPEN; do not use a formal large-value result to state a density estimate.",
        },
        {
            "id": "P7-5-PRIME-IDEAL-SHORT-INTERVALS",
            "state": "UNEXECUTED",
            "purpose": "Translate only a proof-grade density result into a clearly defined prime-ideal interval statement.",
            "pass_rule": "Check the explicit formula, zero-free/exceptional-zero treatment, prime-power remainder, exact family average, and uniformity in the interval [x,x+x^theta] before naming theta.",
            "failure_rule": "Retain SHORT_INTERVAL_BRIDGE_OPEN. Existing Bombieri--Vinogradov or bounded-gap results are not substitutes for this uniform short-interval gate.",
        },
    ]


def payload() -> dict[str, object]:
    return {
        "artifact_id": "p7-hecke-qi-preregistration-v1",
        "epistemic_status": "OBSERVED",
        "status": "PREREGISTERED_UNEXECUTED",
        "claim_boundary": "This source-pinned preregistration selects one finite-order Hecke family and freezes transfer gates. It proves no new Hecke zero-density estimate, no Guth--Maynard transfer, no prime-ideal short-interval theorem, and no bounded-gap theorem. It initiates no hostile audit and authorizes no theorem search.",
        "selection": {
            "selected_family": "primitive finite-order ray-class Hecke L-functions over fixed K=Q(i), trivial at infinity, Q<Nf_chi<=2Q",
            "selection_rationale": "The field is fixed of degree two and class number one; finite ray-class characters give a finite conductor aspect and ideal-indexed coefficients, while excluding angular characters avoids an unregistered archimedean spectral parameter.",
            "deferred": ["angular characters", "varying K", "varying discriminant", "higher-degree or automorphic families"],
            "family": C.FAMILY_CONVENTION,
            "field": C.FIELD,
            "zero_count": C.ZERO_CONVENTION,
            "L_function": C.L_FUNCTION_CONVENTION,
        },
        "collective_count": "N_F(sigma,T;Q)=sum_{f:Q<Nf<=2Q} sum_{chi primitive mod f} N(sigma,T,chi), with each zero counted with multiplicity and each exact-conductor character pair counted once.",
        "source_checks": source_checks(),
        "prior_work_conceded": [
            "Zaman arXiv:1502.05679v4 supplies explicit zero-free/near-one-density context for ray-class Hecke L-functions; it is not a Guth--Maynard theorem.",
            "Thorner--Zaman arXiv:1510.08086v1 proves an explicit log-free Hecke zero-density estimate by a Hecke large sieve and Turan detector; no improvement or replacement is claimed here.",
            "Thorner, MRL 2019, proves a Hecke-character large sieve/averaged density result and a Bombieri--Vinogradov/Maynard bounded-gap application; those are prior work, not downstream consequences of P7.",
            "BGL is retained only as a rejected comparison and supplies no authority for the selected family.",
        ],
        "dependency_graph": {
            "start": "P7-0-SOURCE-FAMILY",
            "first_branch": "P7-1-NORM-AGGREGATION",
            "analytic_chain": ["P7-2-RAY-CLASS-ORTHOGONALITY", "P7-3-IDEAL-CUBIC-ENERGY", "P7-4-DETECTOR-TAIL", "P7-5-PRIME-IDEAL-SHORT-INTERVALS"],
            "edges": [
                ["P7-0-SOURCE-FAMILY", "P7-1-NORM-AGGREGATION"],
                ["P7-1-NORM-AGGREGATION", "P7-2-RAY-CLASS-ORTHOGONALITY"],
                ["P7-2-RAY-CLASS-ORTHOGONALITY", "P7-3-IDEAL-CUBIC-ENERGY"],
                ["P7-3-IDEAL-CUBIC-ENERGY", "P7-4-DETECTOR-TAIL"],
                ["P7-3-IDEAL-CUBIC-ENERGY", "P7-5-PRIME-IDEAL-SHORT-INTERVALS"],
                ["P7-4-DETECTOR-TAIL", "P7-5-PRIME-IDEAL-SHORT-INTERVALS"],
            ],
        },
        "gates": gates(),
        "non_promotion": list(C.NO_GO_OR_NON_PROMOTION),
        "artifact_identity": {
            "conventions": {"path": str(CONVENTIONS.relative_to(ROOT)), "sha256": digest(CONVENTIONS)},
            "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
            "builder": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__))},
        },
        "replay": {
            "command": "python3 proof/build_p7_hecke_qi_preregistration_v1.py --check",
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
    require(sys.flags.optimize == 0, "P7 preregistration rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "P7 preregistration requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    encoded = render(payload())
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "P7 preregistration exceeded wall cap")
    require(rss < RSS_CAP_KIB, "P7 preregistration exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 preregistration")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "sealed P7 preregistration is absent")
        require(OUT.read_bytes() == encoded, "sealed P7 preregistration mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)

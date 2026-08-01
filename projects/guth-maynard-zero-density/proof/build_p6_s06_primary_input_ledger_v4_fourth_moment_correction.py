#!/usr/bin/env python3
"""Seal the primitive-detector fourth-moment correction for P6 S06."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-s06-primary-input-ledger-v4-fourth-moment-correction.json"
DOC = ROOT / "docs/p6-s06-primary-input-ledger-v4-fourth-moment-correction.md"
V1 = ROOT / "artifacts/p6-s06-primary-input-ledger-v1.json"
V2 = ROOT / "artifacts/p6-s06-primary-input-ledger-v2-lpoly-correction.json"
V3 = ROOT / "artifacts/p6-s06-primary-input-ledger-v3-lc-correction.json"
TRANSFER = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
BHB_TEX = ROOT / "artifacts/sources/bui-heath-brown-0903.4008v1.tex.gz"
BHB_PDF = ROOT / "artifacts/sources/bui-heath-brown-2010-acta-arithmetica.pdf"
TZ_TEX = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1/LFZD_manuscript.tex"
CS_TEX = ROOT / "artifacts/sources/chourasiya-simonic-2025-explicit-ingham/InghamPostArXiv.tex"
CS_TAR = ROOT / "artifacts/sources/chourasiya-simonic-2025-explicit-ingham.tar"
CS_PDF = ROOT / "artifacts/sources/chourasiya-simonic-2025-explicit-ingham.pdf"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"

V1_HASH = "1fbb984c3536c45dedbba36992ef8498cccf21fb7d8e9cab7619b5d2cb14b59a"
V2_HASH = "a7846345724c5110bc37d14a1ad712182f80f8e56a42ce73309469589df5b3e0"
V3_HASH = "8566226a67504c91fc2a19e98c7a74c1b805320b825852923b703fb5ce05fb49"
TRANSFER_HASH = "2edccf46d15229fb8b8ff2c9510d0912f73228da681577ca66d869a8d8acf0d7"
BHB_TEX_HASH = "25e6aa0186dade9b1b71771eb4ca8552e7f1094c88cb12990342cc5cb844a5ca"
BHB_PDF_HASH = "a9bdfaa0f5190e59d0da5f5edcfa324390cbbefc21e59cebf9bf5e8422475011"
TZ_TEX_HASH = "e77007c73da81c239fa009f6fce8befbc72989a0fd28f2ec4ff6952ff098f8f2"
CS_TEX_HASH = "94dba3641503540475e1f245af1782cdc197e22750cbd08024cbeaf63b20ddd1"
CS_TAR_HASH = "eaac858e0a450fbbd77e02a9b4ac8a4e5fbe8674e74d21233d4e6a02c25de297"
CS_PDF_HASH = "11ebae58b467d14a20835eb732130c2c084f9440ef5e2fdbe38d697ba1e0d261"
CGL_TAR_HASH = "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cgl_lines() -> list[str]:
    with tarfile.open(CGL_TAR, "r") as archive:
        name = next(member.name for member in archive.getmembers() if member.name.endswith(".tex"))
        stream = archive.extractfile(name)
        require(stream is not None, "CGL TeX member missing")
        return stream.read().decode("utf-8").splitlines()


def source_checks() -> dict[str, object]:
    for path, expected in ((BHB_TEX, BHB_TEX_HASH), (BHB_PDF, BHB_PDF_HASH), (TZ_TEX, TZ_TEX_HASH), (CS_TEX, CS_TEX_HASH), (CS_TAR, CS_TAR_HASH), (CS_PDF, CS_PDF_HASH), (CGL_TAR, CGL_TAR_HASH)):
        require(digest(path) == expected, f"pinned source changed: {path.name}")
    with gzip.open(BHB_TEX, "rt", encoding="utf-8") as handle:
        bhb = handle.read().splitlines()
    require("For $q,T\\ge 2$ we have" in bhb[68], "BHB Theorem 1 range changed")
    require("\\int_{0}^{T}|L(" in bhb[71], "BHB fourth-moment integral changed")
    require("(\\log qT)^{4}" in bhb[74], "BHB main-term logarithm changed")
    require("O(qT(\\log qT)^{\\frac{7}{2}})" in bhb[75], "BHB error term changed")
    tz = TZ_TEX.read_text(encoding="utf-8").splitlines()
    require("assume that $\\chi$ is primitive" in tz[559], "TZ primitive scope changed")
    require("$\\xi(s, \\chi) = w(\\chi) \\xi(1-s, \\bar{\\chi})$" not in tz[581], "unexpected TZ source punctuation")
    require("\\xi(s, \\chi) = w(\\chi) \\xi(1-s, \\bar{\\chi})" in tz[581], "TZ functional equation changed")
    require("Let $\\chi$ be a primitive Hecke character" in tz[645], "TZ Rademacher scope changed")
    cs = CS_TEX.read_text(encoding="utf-8").splitlines()
    require("label{thm:FXbyGabriel}" in "\n".join(cs[474:496]), "corroborating Gabriel source changed")
    cgl = cgl_lines()
    require("restrict our analysis to primitive characters modulo $q$" in cgl[2108], "CGL primitive detector scope changed")
    return {
        "published_bui_heath_brown": {"status": "PROVED_SOURCE", "citation": "Bui--Heath-Brown, Acta Arith. 141 (2010), 335--344, DOI 10.4064/aa141-4-3", "tex": {"path": str(BHB_TEX.relative_to(ROOT)), "sha256": BHB_TEX_HASH}, "publisher_pdf": {"path": str(BHB_PDF.relative_to(ROOT)), "sha256": BHB_PDF_HASH}, "locator": "Theorem 1, TeX 68--78"},
        "published_thorner_zaman": {"status": "PROVED_SOURCE", "tex": {"path": str(TZ_TEX.relative_to(ROOT)), "sha256": TZ_TEX_HASH}, "locators": ["functional equation TeX 580--585", "Rademacher TeX 644--651"]},
        "cgl_scope": {"path": str(CGL_TAR.relative_to(ROOT)), "sha256": CGL_TAR_HASH, "locator": "TeX 2109"},
        "submitted_chourasiya_simonic": {"epistemic_status": "OBSERVED", "role": "corroboration only; not theorem authority", "tex": {"path": str(CS_TEX.relative_to(ROOT)), "sha256": CS_TEX_HASH}, "tar_sha256": CS_TAR_HASH, "pdf_sha256": CS_PDF_HASH, "locator": "Theorem thm:FXbyGabriel, TeX 475--545"},
    }


def analytic_lemma() -> dict[str, object]:
    return {
        "epistemic_status": "PROVED",
        "name": "finite_gaussian_three_lines_fourth_moment",
        "statement": "For q>=2, U>=2, and 1/2<=x<=3/2, sum over primitive chi modulo q of integral_{-U}^U |L(x+it,chi)|^4 dt <<_epsilon (qU)^(1+epsilon).",
        "self_contained_derivation": [
            "For each primitive chi modulo q>=2, chi is nonprincipal, so L(s,chi) is holomorphic in the closed strip 1/2<=Re(s)<=3/2. On Re(s)=3/2 its absolutely convergent Dirichlet series gives |L(s,chi)|<=zeta(3/2).",
            "Multiply L(s,chi) by exp((s/U)^2). Applying the maximum principle to the usual truncated rectangles and then letting their heights tend to infinity gives the finite Gaussian three-lines inequality. With fourth-power exponent on both boundaries, it bounds the weighted L^4 integral at x by the weight-w geometric mean of the weighted boundary integrals, where w=(3/2-x). This is the standard proof, included here as a derivation rather than imported from the submitted corroborating preprint.",
            "At x=1/2, Bui--Heath-Brown Theorem 1 and conjugation chi<->conjugate(chi) give the required weighted boundary integral: partition the Gaussian tail dyadically, apply its q,V>=2 theorem on each positive interval, and use the elementary divisor bound tau(q)<<_epsilon q^epsilon to absorb omega(q) and q/phi(q) from its displayed formula. The result is <<_epsilon(qU)^(1+epsilon).",
            "At x=3/2, absolute convergence gives a weighted boundary integral O(phi*(q)U)<=O(qU). Summing the per-character three-lines inequalities and using Holder yields the stated family estimate uniformly in x.",
        ],
        "checked_hypotheses": ["q>=2 excludes the only primitive principal character (modulus 1), hence no pole at s=1", "U>=2 supplies the Bui--Heath--Brown height range", "TZ Rademacher supplies polynomial vertical growth in the closed strip used in the truncated-rectangle limit", "all boundary and intermediate integrals are finite after Gaussian damping"],
    }


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    for path, expected in ((V1, V1_HASH), (V2, V2_HASH), (V3, V3_HASH), (TRANSFER, TRANSFER_HASH)):
        require(digest(path) == expected, f"immutable predecessor changed: {path.name}")
    return {
        "artifact_id": "p6-s06-primary-input-ledger-v4-fourth-moment-correction", "epistemic_status": "OBSERVED",
        "claim_boundary": "Versioned correction only for the primitive-character fourth-moment premise actually used by the CGL detector. It does not validate CGL-v2, repair q1-sensitive formulae, or prove a zero-density or short-interval theorem.",
        "immutable_predecessors": {"ledger_v1": V1_HASH, "ledger_v2": V2_HASH, "ledger_v3": V3_HASH, "primitive_to_all_transfer": TRANSFER_HASH},
        "source": source_checks(), "analytic_lemma": analytic_lemma(),
        "corrected_input": {"id": "FOURTH_MOMENT_H", "epistemic_status": "PROVED", "precise_scope": "q>=2, H>=1, and selected pairs (gamma_r,chi_r) with chi_r primitive modulo the fixed q, |gamma_r|<=H, and |gamma_r-gamma_s|>=1 whenever chi_r=chi_s and r!=s.", "statement": "For every delta>0, sum_r |L(1/2+i gamma_r,chi_r)|^4 <<_delta (qH)^(1+delta).", "discrete_conversion": "Let U=H+1 and r=1/(10 log(q(H+3))). The radius-r disks about the selected critical-line points are disjoint within each character. Subharmonicity of |L|^4 bounds the selected sum by r^(-2) times the two-dimensional strip integral. For Re(s)>=1/2 use the proved finite Gaussian three-lines lemma; for Re(s)<1/2 use the TZ functional equation, which costs [q(H+3)]^(4r)=O(1) after fourth powers. The r^(-2) loss is polylogarithmic and is absorbed into delta.", "compact_and_endpoint_handling": "H>=1 implies U>=2. The disks lie in |Im(s)|<=H+r<U and 1/2-r<=Re(s)<=1/2+r. Their closed disks remain disjoint because r<1/4. The q=1 zeta-only case is not asserted here, because the CGL primitive-detector reduction being repaired is recorded at q>=2.", "all_character_boundary": "This proves exactly the primitive detector premise at CGL TeX 2109. It does not relabel the immutable v1 all-character wording as a separate theorem; that broader form is unnecessary before the pinned conductor transfer."},
        "dependency_effect": {"LOW_HEIGHT_MULTIPLICITY_COUNT": {"epistemic_status": "PROVED", "source": "v1 reduction plus v3 LC correction"}, "L_POLY_A": {"epistemic_status": "PROVED", "source": "v2 correction"}, "FOURTH_MOMENT_H_for_primitive_detector": {"epistemic_status": "PROVED", "source": "this correction"}, "remaining_p6_boundaries": ["q1-sensitive intermediate formulae", "Z03 tail X-range", "F08 T-smooth definition", "the CGL-v2 theorem and all downstream density/short-interval claims"], "gate_status": "OBSERVED: named external analytic inputs for the q>=2 primitive detector are now supplied, but P6 remains RECONCILED_OPEN_INPUTS because independent retained gates are not repaired."},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)}, "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}, "hostile_audit": "DEFERRED_TO_PAPER_STAGE", "replay": "python3 proof/build_p6_s06_primary_input_ledger_v4_fourth_moment_correction.py --check"}


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = render(payload())
    if args.write:
        require(not OUT.exists(), "refusing to overwrite fourth-moment correction")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "fourth-moment correction mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

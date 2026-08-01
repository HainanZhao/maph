#!/usr/bin/env python3
"""Build/check the bounded G1/P2 primary-literature audit, version 1.

This is a source-provenance and overlap audit.  It deliberately does not
validate any theorem in either arXiv preprint, choose a G1 route, or make a
novelty claim outside the two pinned source versions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tarfile
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
AUDIT_ROOT = PROJECT / "artifacts" / "sources" / "g1-literature-audit-v1"
ARTIFACT = PROJECT / "artifacts" / "g1-current-literature-audit-v1.json"

PINS = {
    "guth_pdf": (
        "arxiv-2503.07410v1.pdf",
        "3ad0ad37a6f1e08a5d29d624a254b4750d32503f9cc8aa2cf5a5b0df8204f487",
    ),
    "guth_tar": (
        "arxiv-2503.07410v1.tar",
        "9a9bcdb909133794ad898c653a1eeab4f7f776e4bd6f48f91f519a81ed9583bc",
    ),
    "guth_abs": (
        "arxiv-2503.07410v1.abs.html",
        "b89e2b4ff12780d9766912ac6ea6ab2cae45ffebaff7828af6514b0050615ef8",
    ),
    "guth_tex": (
        "extracted-2503.07410v1/PerspectivesDirichlet6.tex",
        "5cc056b8e470d0889dafef674cffd0fc03bad66f0bfb464f275559bd9e05b04f",
    ),
    "chen_pdf": (
        "arxiv-2507.08296v2.pdf",
        "adfe65cf0952bbb4eddfdaec7a8d3341130e427827f9159d9da039fc16336058",
    ),
    "chen_tar": (
        "arxiv-2507.08296v2.tar",
        "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae",
    ),
    "chen_abs": (
        "arxiv-2507.08296v2.abs.html",
        "8eafc40c457c6bbb9d78ffd949cee0d5bceef628db14fe1e9a2abde14d33ee6e",
    ),
    "chen_tex": (
        "extracted-2507.08296v2/Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex",
        "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f",
    ),
}

PAGE_ANCHORS = {
    "guth": {
        "p12": ("arxiv-2503.07410v1.p12.txt", "no meaningful numerical evidence"),
        "p20": ("arxiv-2503.07410v1.p20.txt", "The Schatten tensor"),
        "p23": ("arxiv-2503.07410v1.p23.txt", "additive energy"),
        "p24": ("arxiv-2503.07410v1.p24.txt", "The additive energy can be rewritten"),
        "p25": ("arxiv-2503.07410v1.p25.txt", "a cyclic\ndifference"),
        "p27": ("arxiv-2503.07410v1.p27.txt", "if r = 3"),
        "p34": ("arxiv-2503.07410v1.p34.txt", "Low degree testing"),
        "p37": ("arxiv-2503.07410v1.p37.txt", "A barrier related to the Kakeya problem"),
        "p40": ("arxiv-2503.07410v1.p40.txt", "Bourgain-Kakeya problem"),
    },
    "chen": {
        "p1": ("arxiv-2507.08296v2.p1.txt", "Theorem 1.1"),
        "p2": ("arxiv-2507.08296v2.p2.txt", "Theorem 1.1 recovers"),
        "p3": ("arxiv-2507.08296v2.p3.txt", "Theorem 1.2"),
        "p7": ("arxiv-2507.08296v2.p7.txt", "affine transformations"),
        "p13": ("arxiv-2507.08296v2.p13.txt", "Expansion of the cubic trace"),
        "p26": ("arxiv-2507.08296v2.p26.txt", "Summing over affine transformations"),
        "p40": ("arxiv-2507.08296v2.p40.txt", "Energy bound"),
        "p57": ("arxiv-2507.08296v2.p57.txt", "worst case for our zero density estimate"),
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def content(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_fragment(text: str, fragment: str, label: str) -> None:
    require(fragment in text, f"missing fragment for {label}: {fragment!r}")


def source_path(pin: str) -> Path:
    return AUDIT_ROOT / PINS[pin][0]


def verify_runtime() -> dict[str, object]:
    require(sys.implementation.name == "cpython", "requires CPython")
    require(sys.version_info[:3] == (3, 12, 3), "requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "optimized Python is not permitted")
    return {
        "implementation": sys.implementation.name,
        "version": ".".join(map(str, sys.version_info[:3])),
        "optimize": sys.flags.optimize,
    }


def verify_pins() -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    for key, (relative, expected) in PINS.items():
        path = AUDIT_ROOT / relative
        require(path.is_file(), f"missing pinned source {relative}")
        actual = digest(path)
        require(actual == expected, f"hash mismatch for {relative}: {actual}")
        rows[key] = {"relative_path": f"artifacts/sources/g1-literature-audit-v1/{relative}", "sha256": actual}
    return rows


def verify_extraction(tar_key: str, tex_key: str) -> None:
    archive = source_path(tar_key)
    extracted = source_path(tex_key)
    member_name = Path(PINS[tex_key][0]).name
    with tarfile.open(archive, "r:gz") as handle:
        member = handle.getmember(member_name)
        member_file = handle.extractfile(member)
        require(member_file is not None, f"cannot read {member_name} from {archive.name}")
        require(member_file.read() == extracted.read_bytes(), f"extracted TeX does not match {archive.name}:{member_name}")


def verify_page_anchors(group: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for page, (relative, fragment) in PAGE_ANCHORS[group].items():
        path = AUDIT_ROOT / relative
        require(path.is_file(), f"missing rendered-page anchor {relative}")
        require_fragment(content(path), fragment, f"{group} PDF {page}")
        result[page] = {"relative_path": f"artifacts/sources/g1-literature-audit-v1/{relative}", "contains": fragment}
    return result


def verify_source_content() -> None:
    guth_tex = content(source_path("guth_tex"))
    guth_abs = content(source_path("guth_abs"))
    chen_tex = content(source_path("chen_tex"))
    chen_abs = content(source_path("chen_abs"))

    for fragment in (
        "[Submitted on 10 Mar 2025]",
        "Authors:</span><a",
        "Larry Guth",
        "Large value estimates in number theory, harmonic analysis, and computer science",
    ):
        require_fragment(guth_abs, fragment, "Guth arXiv metadata")
    require("Journal reference" not in guth_abs, "Guth v1 metadata unexpectedly contains a journal-reference field")
    for fragment in (
        "The paper \\cite{GM} carefully studies the tensor $S_{M_{Dir}, 3}$",
        "for $r \\ge 3$",
        "D^r \\Phi :=",
        "if $r=3$,  then $D^3 \\Phi$",
        "there is no meaningful numerical evidence supporting the main conjectures",
        "It is also worth mentioning that assuming the Bourgain-Kakeya conjecture as a black box does not currently lead",
    ):
        require_fragment(guth_tex, fragment, "Guth survey")
    require_fragment(guth_tex, "t_1 + t_2 = t_3 -t_4", "Guth energy-definition sign audit")
    require_fragment(guth_tex, "E(W) = \\frac{1}{2 \\pi} \\int_0^{2 \\pi} |\\hat W(\\xi)|^4 d \\xi", "Guth energy-Fourier identity")

    for fragment in (
        "last revised 27 Jul 2026 (this version, v2)",
        "Bin Chen</a>, <a",
        "Vishal Gupta</a>, <a",
        "Yung Chi Li</a>",
        "58 pages.",
    ):
        require_fragment(chen_abs, fragment, "Chen--Gupta--Li arXiv metadata")
    require("Journal reference" not in chen_abs, "Chen--Gupta--Li v2 metadata unexpectedly contains a journal-reference field")
    for fragment in (
        "\\author{Bin Chen}",
        "\\author{Vishal Gupta}",
        "\\author{Yung Chi Li}",
        "independently obtained the exponent $7/3$",
        "We therefore take $r=3$",
        "Expansion of the cubic trace",
        "Summing over affine transformations with GCD twists",
        "\\section{Energy bound}",
        "\\section{\\texorpdfstring{Application to Dirichlet $L$-functions}",
        "The best exponent $A$",
    ):
        require_fragment(chen_tex, fragment, "Chen--Gupta--Li v2")
    for excluded in ("quartic", "cyclic difference", "Kakeya"):
        require(excluded not in chen_tex.lower(), f"bounded literal-absence check failed for {excluded!r}")


def build() -> dict[str, Any]:
    runtime = verify_runtime()
    source_hashes = verify_pins()
    verify_extraction("guth_tar", "guth_tex")
    verify_extraction("chen_tar", "chen_tex")
    verify_source_content()
    return {
        "artifact_id": "g1-current-literature-audit-v1",
        "schema": 1,
        "created_utc": "2026-08-01",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED bounded primary-source provenance, locator, and overlap audit of arXiv:2503.07410v1 and arXiv:2507.08296v2 only. It proves no theorem in either work, makes no global novelty claim, selects no G1/P2 route, and does not broaden the audit to other literature.",
        "source_verification": {
            "algorithm": "SHA-256",
            "runtime": runtime,
            "source_hashes": source_hashes,
            "archive_extraction_checks": {
                "guth_v1": "tar member PerspectivesDirichlet6.tex equals extracted canonical TeX bytes",
                "chen_gupta_li_v2": "tar member Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex equals extracted canonical TeX bytes",
            },
            "pdf_page_anchors": {"guth": verify_page_anchors("guth"), "chen_gupta_li": verify_page_anchors("chen")},
        },
        "sources": {
            "guth_2503_07410v1": {
                "citation": "Larry Guth, Large value estimates in number theory, harmonic analysis, and computer science, arXiv:2503.07410v1 [math.NT], submitted 10 March 2025.",
                "status": "OBSERVED arXiv preprint/survey; the pinned v1 arXiv metadata has no Journal reference field. This audit does not determine publication status beyond that pinned metadata snapshot.",
                "urls": {
                    "abstract": "https://arxiv.org/abs/2503.07410v1",
                    "pdf": "https://arxiv.org/pdf/2503.07410v1",
                    "source": "https://export.arxiv.org/e-print/2503.07410v1",
                },
                "pdf_pages": 49,
                "anchors": [
                    {"id": "GUTH-NUM", "tex_lines": "526-552", "pdf_pages": "12", "status": "OBSERVED", "finding": "The survey says there is no meaningful numerical evidence for its main Dirichlet-polynomial large-value conjectures and says they cannot be checked numerically even for N=200. This is a methodological warning, not a prohibition on the frozen finite G1 screen and not a theorem about its output."},
                    {"id": "GUTH-TRACE", "tex_lines": "864-962", "pdf_pages": "20-22", "status": "OBSERVED", "finding": "The survey says Guth--Maynard carefully studies the cubic Schatten tensor S_{M_Dir,3}; it says r=2 is tied to MM* and motivates r>=3. It does not prove a quartic-trace no-go or a saturation result. The commented-out TeX-only r=4 flattening sentence at line 960 is excluded from the PDF-source claims."},
                    {"id": "GUTH-CYCLIC", "tex_lines": "1026-1137", "pdf_pages": "25-27", "status": "OBSERVED", "finding": "The survey defines the cyclic difference multiset D^r Phi, discusses cancellation for r>=3, and gives a qualitative r=3 smooth-plus-curves picture. It is a survey discussion, not a checked quantitative theorem for r=4 or general r."},
                    {"id": "GUTH-ENERGY-CORRECTION", "tex_lines": "988-1019", "pdf_pages": "23-24", "status": "OBSERVED", "finding": "CONTAINED_SOURCE_SIGN_INCONSISTENCY: the displayed definition uses t1+t2=t3-t4, while the immediately displayed |What|^4 identity and asserted usual energy range are the standard plus-sign convention. The survey v1 is therefore not an authority for this project's energy convention; use the separately pinned published Guth--Maynard source/conventions instead."},
                    {"id": "GUTH-COMPUTATIONAL", "tex_lines": "1284-1484", "pdf_pages": "34-36", "status": "OBSERVED", "finding": "The low-degree/sum-of-squares discussion is partly theorem citation and partly explicitly conjectural transfer to M_Dir. It does not establish a no-go for the present G1 architecture or for any quartic/energy refinement."},
                    {"id": "GUTH-KAKEYA", "tex_lines": "1516-1608", "pdf_pages": "37-40", "status": "OBSERVED", "finding": "The Bourgain--Kakeya discussion identifies a conditional structural barrier and explicitly says a black-box Bourgain--Kakeya conjecture does not currently improve known Dirichlet-polynomial large-value bounds. It is neither a P2 saturation theorem nor a route-selection criterion."},
                ],
            },
            "chen_gupta_li_2507_08296v2": {
                "citation": "Bin Chen, Vishal Gupta, and Yung Chi Li, Large Value Estimates for Dirichlet Polynomials with Characters and Zero Density of Dirichlet L-Functions, arXiv:2507.08296v2 [math.NT], submitted 11 July 2025 and last revised 27 July 2026.",
                "status": "OBSERVED arXiv preprint; three-author v2. The pinned v2 arXiv metadata has no Journal reference field. Its displayed theorems and exponent 7/3 are recorded as source claims, not PROVED in this audit.",
                "urls": {
                    "abstract": "https://arxiv.org/abs/2507.08296v2",
                    "pdf": "https://arxiv.org/pdf/2507.08296v2",
                    "source": "https://export.arxiv.org/e-print/2507.08296v2",
                },
                "pdf_pages": 58,
                "anchors": [
                    {"id": "CGL-RESULT-SCOPE", "tex_lines": "77-187", "pdf_pages": "1-3", "status": "OBSERVED", "finding": "The preprint states a character-twisted large-values theorem and a Dirichlet-L zero-density result, with uniform exponent 7/3. The proof/hypotheses have not been independently checked here."},
                    {"id": "CGL-CUBIC-S3", "tex_lines": "275-373, 524-660, 1979-2072", "pdf_pages": "7, 13, 48", "status": "OBSERVED", "finding": "Exact overlap with the G1 background: a refined cubic trace, an S3 decomposition, and a final S3 estimate. This is prior work for any claim that merely reuses that character-twisted cubic S3 mechanism."},
                    {"id": "CGL-AFFINE-ENERGY", "tex_lines": "1129-1160, 1688-1765, 1979-2072", "pdf_pages": "26, 40, 48", "status": "OBSERVED", "finding": "Exact overlap with affine/energy work: the paper proves an affine-transformation estimate with a GCD twist, defines energy on (t,chi) pairs, and inserts it into S3. This is a structural antecedent to P2B, but not the proposed un-twisted, scale-sensitive G1 energy profile or a theorem about the frozen G1 families."},
                    {"id": "CGL-ZERO-DETECTION", "tex_lines": "2107-2140", "pdf_pages": "49", "status": "OBSERVED", "finding": "The paper contains a Dirichlet-L zero-detection section. This bounded audit does not compare it with the project's zeta six-factor short-interval decomposition beyond recording that P2C cannot claim its general zero-detection template as new."},
                    {"id": "CGL-HIGHER-TRACE-SEARCH", "tex_lines": "entire 2467-line pinned TeX; literal searches", "pdf_pages": "not applicable", "status": "OBSERVED", "finding": "The pinned v2 TeX contains the cubic-trace mechanism but no literal occurrences of 'quartic', 'cyclic difference', or 'Kakeya'. This is only a bounded textual-absence result; it does not prove that no related higher-trace method exists."},
                    {"id": "CGL-OBSTRUCTION", "tex_lines": "2411-2413", "pdf_pages": "58", "status": "OBSERVED", "finding": "The preprint identifies its own worst case as an S3 term lacking joint cancellation in R and m sums. This is a preprint discussion, not a general obstruction theorem for the zeta architecture."},
                ],
            },
        },
        "overlap_disposition": {
            "P2A_higher_trace": "OBSERVED: no direct quartic/higher-cyclic-difference theorem is found in the bounded Chen--Gupta--Li v2 source; Guth v1 supplies only survey motivation. No novelty clearance outside this two-source scope is implied.",
            "P2B_energy": "OBSERVED: Chen--Gupta--Li v2 is direct prior work for cubic S3 plus affine-GCD-twist plus character-pair energy. Any future P2B statement must distinguish its scale-sensitive un-twisted target and cite this preprint.",
            "P2C_zero_detection": "OBSERVED: Chen--Gupta--Li v2 contains a Dirichlet-L zero-detection application. Any future P2C statement must concede that template and separately show what differs in the zeta/short-interval architecture.",
            "P6_dirichlet_L": "OBSERVED: the three-author v2 preprint is prior work for a Dirichlet-L extension and its claimed 7/3 exponent. This project must concede it and may not attribute that result to itself.",
        },
        "route_decision": "NOT_MADE: this audit is not an authorized substitute for the frozen G1 atlas or its route-selection gate.",
        "required_follow_up_before_novelty_claim": "Read and compare any further primary sources implicated by the selected G1 route; check theorem hypotheses and proof details rather than relying on this bounded source map.",
        "verification": {
            "builder": "proof/audit_g1_current_literature_v1.py",
            "builder_sha256": digest(Path(__file__).resolve()),
            "write_command": "python3 proof/audit_g1_current_literature_v1.py --write",
            "check_command": "python3 proof/audit_g1_current_literature_v1.py --check",
        },
    }


def encoded(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = encoded(build())
    if args.write:
        ARTIFACT.write_bytes(payload)
        print(f"wrote {ARTIFACT.relative_to(PROJECT)}")
        return 0
    require(ARTIFACT.is_file(), f"missing artifact {ARTIFACT}")
    require(ARTIFACT.read_bytes() == payload, "literature audit artifact differs; rerun --write only after reviewing the correction")
    print(json.dumps({"verified": True, "artifact": ARTIFACT.name}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

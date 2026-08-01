#!/usr/bin/env python3
"""Correct P6 S06 ledger v1 after a pinned all-modulus growth source match."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
V1 = ROOT / "artifacts/p6-s06-primary-input-ledger-v1.json"
DOC = ROOT / "docs/p6-s06-primary-input-ledger-v2-lpoly-correction.md"
OUT = ROOT / "artifacts/p6-s06-primary-input-ledger-v2-lpoly-correction.json"
TZ_TEX = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1/LFZD_manuscript.tex"
TZ_TAR = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1.tar"
TZ_PDF = ROOT / "artifacts/sources/p7-hecke-v1/thorner-zaman-1510.08086v1.pdf"
V1_HASH = "1fbb984c3536c45dedbba36992ef8498cccf21fb7d8e9cab7619b5d2cb14b59a"
TZ_TEX_HASH = "e77007c73da81c239fa009f6fce8befbc72989a0fd28f2ec4ff6952ff098f8f2"
TZ_TAR_HASH = "082be65a8fc04b5795290e500e0b2d74dc7a818cb68cc5ddc02131012b178fa2"
TZ_PDF_HASH = "94ddf7864fe74d266cef42816c9621516079321c48069d848527e7d0067b866d"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict[str, object]:
    require(digest(TZ_TEX) == TZ_TEX_HASH, "pinned Thorner--Zaman TeX changed")
    require(digest(TZ_TAR) == TZ_TAR_HASH, "pinned Thorner--Zaman tar changed")
    require(digest(TZ_PDF) == TZ_PDF_HASH, "pinned Thorner--Zaman PDF changed")
    lines = TZ_TEX.read_text(encoding="utf-8").splitlines()
    # Human TeX line n has Python index n-1.
    require("For the entirety of this section, assume that $\\chi$ is primitive." in lines[559], "primitive scope changed")
    require("$D_{\\chi} = D_K \\N\\kf_{\\chi}$" in lines[569], "conductor definition changed")
    require("Let $\\chi$ be a primitive Hecke character and $\\eta \\in (0, 1/2]$" in lines[645], "Rademacher hypotheses changed")
    require("uniformly in the strip $-\\eta \\leq \\sigma \\leq 1+\\eta$" in lines[649], "Rademacher strip changed")
    require("\\Big| \\frac{1+s}{1-s}\\Big|^{\\delta(\\chi)}" in lines[647], "principal ratio changed")
    require("(3+|t|)^{n_K}" in lines[647], "height factor changed")
    return {
        "tex": {"path": str(TZ_TEX.relative_to(ROOT)), "sha256": TZ_TEX_HASH},
        "tar": {"path": str(TZ_TAR.relative_to(ROOT)), "sha256": TZ_TAR_HASH},
        "pdf": {"path": str(TZ_PDF.relative_to(ROOT)), "sha256": TZ_PDF_HASH},
        "locator": "Lemma Rademacher, TeX 642--651; completed conductor definition TeX 565--585",
    }


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    require(digest(V1) == V1_HASH, "immutable ledger-v1 changed")
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    require(v1["input_ledger"]["L_POLY_A"]["epistemic_status"] == "CONJECTURED", "v1 L_POLY_A status changed")
    return {
        "artifact_id": "p6-s06-primary-input-ledger-v2-lpoly-correction",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Versioned correction of L_POLY_A only. It proves no fourth moment, local multiplicity theorem, CGL theorem, density estimate, or short-interval result.",
        "immutable_v1": {"path": str(V1.relative_to(ROOT)), "sha256": V1_HASH},
        "source": source_checks(),
        "corrected_input": {
            "id": "L_POLY_A",
            "epistemic_status": "PROVED",
            "statement": "For every Dirichlet character chi modulo q and every real v, |L(1/2+iv,chi)| << [q(2+|v|)]^(3/2), with an absolute implied constant.",
            "primitive_specialization": "Set K=Q, n_K=D_K=1, eta=1/2, sigma=1/2 in Thorner--Zaman Lemma Rademacher. For primitive conductor d, this gives |L(1/2+iv,chi*)| << [d(3+|v|)]^(1/2); the trivial-character ratio is at most 3 on the critical line.",
            "imprimitive_transfer": "If chi is induced by chi* of conductor d|q, its finite Euler quotient has critical-line modulus at most product_{p|q,p not|d}(1+p^(-1/2)) <= 2^omega(q) <= q. Thus |L| << q[d(3+|v|)]^(1/2) <= [q(2+|v|)]^(3/2) up to an absolute constant.",
            "detector_effect": "The qT tail repair may take A=3/2. Gamma decay remains the only tail-decay mechanism; no q<=T^C condition is introduced.",
        },
        "retained_inputs": {
            "FOURTH_MOMENT_H": {"epistemic_status": "CONJECTURED", "status": "OPEN_EXTERNAL_PRIMARY_THEOREM"},
            "LOCAL_MULTIPLICITY_COUNT_LC": {"epistemic_status": "CONJECTURED", "status": "OPEN_EXTERNAL_PRIMARY_THEOREM"},
            "LOW_HEIGHT_MULTIPLICITY_COUNT": {"epistemic_status": "PROVED", "conditional_on": ["LOCAL_MULTIPLICITY_COUNT_LC"], "source": "ledger-v1 reduction"},
            "q1_sensitive_intermediate_formulae": {"epistemic_status": "OBSERVED", "status": "RETAINED_UNREPAIRED"},
        },
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/build_p6_s06_primary_input_ledger_v2_lpoly_correction.py --check",
    }


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
        require(not OUT.exists(), "refusing to overwrite L_POLY_A correction")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "L_POLY_A correction artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

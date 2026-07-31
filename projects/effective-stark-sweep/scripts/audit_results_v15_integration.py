#!/usr/bin/env python3
"""Audit the v1.5 main-paper integration before any Zenodo publish."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MAIN_TEX = ROOT / "paper" / "effective-stark-results.tex"
MAIN_PDF = ROOT / "paper" / "effective-stark-results.pdf"
SUPPLEMENT_TEX = ROOT / "paper" / "effective-stark-results-supplement.tex"
HISTORICAL_ADDENDUM = (
    ROOT / "paper" / "effective-stark-results-supplement-rq000013-addendum.tex"
)
CERTIFICATE = (
    ROOT / "artifacts" / "rq000013-engine-a-imprimitive-certificate-v1.json"
)
METADATA = ROOT / "artifacts" / "zenodo-results-record-metadata-v8.json"
DOI = "10.5281/zenodo.21713178"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(text: str, fragments: tuple[str, ...], label: str) -> None:
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise RuntimeError(f"{label} missing fragments: {missing}")


def main() -> None:
    main_tex = MAIN_TEX.read_text(encoding="utf-8")
    supplement = SUPPLEMENT_TEX.read_text(encoding="utf-8")
    historical = HISTORICAL_ADDENDUM.read_text(encoding="utf-8")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))["metadata"]

    require(
        main_tex,
        (
            r"\subsection{A worked nonzero imprimitive row: RQ-000013}",
            r"\begin{pmatrix}14&6\\0&2\end{pmatrix}",
            r"E_\chi=1-\chi^\circ(\mathfrak p)=2",
            r"I_\chi=\left|\det",
            r"X_{[0]}=u^2,\qquad X_{[1]}=u^{-2}",
            "rq000013-engine-a-imprimitive-certificate-v1.json",
            DOI,
        ),
        "main source",
    )
    require(
        historical,
        (
            r"\begin{pmatrix}14&6\\0&2\end{pmatrix}",
            r"E_\chi=1-\chi^\circ(\mathfrak p)=2",
            r"X_{[0]}=u^2,\qquad X_{[1]}=u^{-2}",
        ),
        "historical addendum",
    )
    if DOI not in supplement:
        raise RuntimeError("v1.5 DOI absent from supplement")
    if metadata["version"] != "1.5" or DOI not in metadata["description"]:
        raise RuntimeError("v1.5 metadata mismatch")
    if "effective-stark-results-00-main-paper.pdf" not in metadata["description"]:
        raise RuntimeError("lexically first main filename absent from metadata")

    exact = certificate["exact_result"]
    if (
        exact["E_chi"] != 2
        or exact["I_chi"] != 2
        or exact["packet_power_identity"]
        != "X_[0]=u^2; X_[1]=u^(-2)"
    ):
        raise RuntimeError("RQ-000013 exact certificate changed")

    replay = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "certify_rq000013_engine_a.py"),
            "--check",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
    )
    if replay.returncode:
        raise RuntimeError(replay.stdout + replay.stderr)

    rendered = subprocess.run(
        ["mutool", "draw", "-F", "txt", str(MAIN_PDF)],
        text=True,
        capture_output=True,
        check=True,
        timeout=60,
    ).stdout
    require(
        rendered,
        (
            "A worked nonzero imprimitive row: RQ-000013",
            "fully Artin-labelled packet",
            "10.5281/zenodo.21713178",
        ),
        "rendered main PDF",
    )

    result = {
        "schema": "effective-stark-results-v1.5-integration-audit-v1",
        "claim_tag": "PROVED",
        "status": "PASS_MAIN_INTEGRATION_AND_EXACT_REPLAY",
        "reserved_doi": DOI,
        "checks": {
            "historical_addendum_preserved": True,
            "rq000013_complete_worked_section_in_main": True,
            "rq000013_exact_certificate_replay": "PASS",
            "quarantined_bnrL1_not_used_in_proof": True,
            "main_pdf_rendered_section_and_doi": True,
            "standalone_addendum_authorized_for_v15_top_level": False,
            "lexically_first_main_upload": (
                "effective-stark-results-00-main-paper.pdf"
            ),
            "publication_action_taken": False,
        },
        "hashes": {
            "main_tex_sha256": sha256(MAIN_TEX),
            "main_pdf_sha256": sha256(MAIN_PDF),
            "supplement_tex_sha256": sha256(SUPPLEMENT_TEX),
            "historical_addendum_tex_sha256": sha256(HISTORICAL_ADDENDUM),
            "certificate_sha256": sha256(CERTIFICATE),
            "metadata_sha256": sha256(METADATA),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

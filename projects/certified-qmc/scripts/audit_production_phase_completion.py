#!/usr/bin/env python3
"""Audit every required Cycles 013-019 completion artifact."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256, read_chain


def result(
    name: str,
    status: str,
    evidence: str,
    detail: str,
) -> dict:
    if status not in ("PASSED", "PENDING", "FAILED"):
        raise ValueError("invalid completion-audit status")
    return {
        "requirement": name,
        "status": status,
        "evidence": evidence,
        "detail": detail,
    }


def self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha256(value) != supplied:
        raise ValueError(f"{path.name}: self-hash mismatch")
    value[field] = supplied
    return value


def certificate_gate(
    name: str,
    relative: str,
    gate: str,
    *,
    field: str = "certificate_sha256",
) -> dict:
    path = ROOT / relative
    if not path.is_file():
        return result(name, "PENDING", relative, "artifact is absent")
    try:
        value = self_hashed(path, field)
    except Exception as error:
        return result(name, "FAILED", relative, str(error))
    passed = value.get("gate", {}).get(gate)
    if passed is True:
        return result(name, "PASSED", relative, f"{gate}=true")
    return result(
        name,
        "FAILED",
        relative,
        f"{gate} is {passed!r}, not true",
    )


def engine_oracle() -> dict:
    relative = "certificates/engine-oracle-set-v1.json"
    path = ROOT / relative
    if not path.is_file():
        return result(
            "Cycle 018 compact engine oracle",
            "PENDING",
            relative,
            "artifact is absent",
        )
    try:
        value = self_hashed(path, "oracle_sha256")
        if (
            value["claim_tag"] != "VERIFIED"
            or value["counts"]["total"] != 298
            or len(value["table_merits"]) != 290
            or len(value["adversarial_decision_cases"]) != 8
        ):
            raise ValueError("oracle tag/count contract failed")
    except Exception as error:
        return result(
            "Cycle 018 compact engine oracle",
            "FAILED",
            relative,
            str(error),
        )
    return result(
        "Cycle 018 compact engine oracle",
        "PASSED",
        relative,
        "298/298 cases present under VERIFIED self-hash",
    )


def release_package(release: Path) -> dict:
    manifest_path = release / "release-manifest.json"
    evidence = str(manifest_path)
    if not manifest_path.is_file():
        return result(
            "Cycle 018 deterministic release package",
            "PENDING",
            evidence,
            "release manifest is absent",
        )
    try:
        manifest = self_hashed(manifest_path, "manifest_sha256")
        if len(manifest["assets"]) != 4:
            raise ValueError("release must contain four authenticated assets")
        for asset in manifest["assets"]:
            path = release / asset["filename"]
            if (
                not path.is_file()
                or path.stat().st_size != int(asset["bytes"])
                or file_sha256(path) != asset["sha256"]
            ):
                raise ValueError(
                    f"release asset mismatch: {asset['filename']}"
                )
        if len(manifest.get("ancillary_files", [])) != 3:
            raise ValueError(
                "release must authenticate three ancillary files"
            )
        for ancillary in manifest["ancillary_files"]:
            path = release / ancillary["filename"]
            if (
                not path.is_file()
                or path.stat().st_size != int(ancillary["bytes"])
                or file_sha256(path) != ancillary["sha256"]
            ):
                raise ValueError(
                    "release ancillary mismatch: "
                    f"{ancillary['filename']}"
                )
    except Exception as error:
        return result(
            "Cycle 018 deterministic release package",
            "FAILED",
            evidence,
            str(error),
        )
    return result(
        "Cycle 018 deterministic release package",
        "PASSED",
        evidence,
        "manifest, four assets, and three ancillary files authenticate",
    )


def repository_tag() -> dict:
    tag = "certified-qmc-v1.0"
    completed = subprocess.run(
        ["git", "rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return result(
            "Cycle 018 repository release tag",
            "PENDING",
            tag,
            "tag is absent",
        )
    return result(
        "Cycle 018 repository release tag",
        "PASSED",
        tag,
        completed.stdout.strip(),
    )


def zenodo_deposition() -> dict:
    relative = "certificates/cycle-018-zenodo-deposition.json"
    path = ROOT / relative
    if not path.is_file():
        return result(
            "Cycle 018 DOI-backed external deposition",
            "PENDING",
            relative,
            "authenticated deposition response is absent",
        )
    try:
        value = self_hashed(path, "certificate_sha256")
        if (
            value.get("published") is not True
            or value.get("announcement_permitted") is not True
            or not value.get("doi")
            or not value.get("record_url")
        ):
            raise ValueError("deposition is not published with DOI")
    except Exception as error:
        return result(
            "Cycle 018 DOI-backed external deposition",
            "FAILED",
            relative,
            str(error),
        )
    return result(
        "Cycle 018 DOI-backed external deposition",
        "PASSED",
        relative,
        f"DOI {value['doi']}",
    )


def cycle009_result(output: Path) -> dict:
    relative = str(output / "cycle-009-result.json")
    path = output / "cycle-009-result.json"
    manifest_path = output / "manifest.jsonl"
    if not path.is_file() or not manifest_path.is_file():
        return result(
            "Cycle 019 Cycle-009 Arb-106 histogram gate",
            "PENDING",
            relative,
            "sealed result is absent",
        )
    try:
        value = self_hashed(path, "certificate_sha256")
        records = read_chain(manifest_path)
        if (
            not records
            or records[-1]["event"] != "SEAL"
            or records[-1]["result_sha256"] != file_sha256(path)
        ):
            raise ValueError("Cycle-009 manifest is not validly sealed")
        histogram = value["histogram"]
        if (
            value["comparison_count"] != 802767
            or histogram["double_double_resolved"] != 0
            or histogram["arb_resolved"]
            + histogram["exact_crt_resolved"]
            != 802767
        ):
            raise ValueError("Cycle-009 histogram count contract failed")
        if value["acceptance"]["passed"] is not True:
            raise ValueError(
                "preregistered exact-escalation predicate failed"
            )
    except Exception as error:
        return result(
            "Cycle 019 Cycle-009 Arb-106 histogram gate",
            "FAILED",
            relative,
            str(error),
        )
    return result(
        "Cycle 019 Cycle-009 Arb-106 histogram gate",
        "PASSED",
        relative,
        (
            f"exact={histogram['exact_crt_resolved']} "
            "over 802767 comparisons"
        ),
    )


def paper_sections() -> dict:
    relative = "docs/paper-supply-side-draft.md"
    path = ROOT / relative
    if not path.is_file():
        return result(
            "Cycle 019 supply-side paper sections",
            "PENDING",
            relative,
            "draft is absent",
        )
    pending = path.read_text().count("`PENDING`")
    if pending:
        return result(
            "Cycle 019 supply-side paper sections",
            "PENDING",
            relative,
            f"{pending} result markers remain pending",
        )
    return result(
        "Cycle 019 supply-side paper sections",
        "PASSED",
        relative,
        "no result marker remains pending",
    )


def workstream_d_decision() -> dict:
    relative = "data/workstream-d-decision.json"
    path = ROOT / relative
    if not path.is_file():
        return result(
            "Cycle 019 Workstream-D human escalation",
            "PENDING",
            relative,
            "human decision has not been recorded",
        )
    try:
        value = self_hashed(path, "decision_sha256")
        if value.get("human_decision") not in (
            "internal-pricing-stack",
            "public-benchmark",
            "defer-workstream-d",
        ):
            raise ValueError("unrecognized Workstream-D decision")
    except Exception as error:
        return result(
            "Cycle 019 Workstream-D human escalation",
            "FAILED",
            relative,
            str(error),
        )
    return result(
        "Cycle 019 Workstream-D human escalation",
        "PASSED",
        relative,
        value["human_decision"],
    )


def static_register() -> dict:
    relative = "docs/post-release-optimization-register.md"
    path = ROOT / relative
    if not path.is_file():
        return result(
            "Cycle 019 post-release optimization register",
            "PENDING",
            relative,
            "register is absent",
        )
    required = (
        "Montgomery",
        "SIMD",
        "dual-shadow",
        "bit-identical",
    )
    text = path.read_text()
    missing = [token for token in required if token not in text]
    if missing:
        return result(
            "Cycle 019 post-release optimization register",
            "FAILED",
            relative,
            f"missing required controls: {missing}",
        )
    return result(
        "Cycle 019 post-release optimization register",
        "PASSED",
        relative,
        "all frozen post-release controls are recorded",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--release-dir",
        type=Path,
        default=ROOT / "artifacts" / "release-v1.0",
    )
    parser.add_argument(
        "--cycle009-dir",
        type=Path,
        default=ROOT / "artifacts" / "cycle009-arb106",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    checks = [
        certificate_gate(
            "Cycle 013 licensing/vendoring gate",
            "certificates/cycle-013-licensing.json",
            "cycle_013_licensing_gate_passed",
        ),
        certificate_gate(
            "Cycle 013 clean-room dependency gate",
            "certificates/cycle-013-dependency-manifest.json",
            "cycle_013_dependency_gate_passed",
        ),
        certificate_gate(
            "Cycle 014 verified full prime schedule",
            "certificates/cycle-014-prime-schedule-manifest.json",
            "cycle_014_exit_gate_passed",
        ),
        certificate_gate(
            "Cycle 015 chunking/resume/selected-entry gate",
            "certificates/cycle-015-chunk-replay.json",
            "cycle_015_exit_gate_passed",
        ),
        certificate_gate(
            "Cycles 016-017 fidelity exit gate",
            "certificates/cycles-016-017-production-audit.json",
            "cycles_016_017_exit_gate_passed",
        ),
        certificate_gate(
            "Cycle 018 usability/reuse gate",
            "certificates/cycle-018-usability-audit.json",
            "cycle_018_data_gate_passed",
        ),
        engine_oracle(),
        release_package(args.release_dir.resolve()),
        repository_tag(),
        zenodo_deposition(),
        paper_sections(),
        cycle009_result(args.cycle009_dir.resolve()),
        static_register(),
        workstream_d_decision(),
    ]
    counts = {
        status.lower(): sum(row["status"] == status for row in checks)
        for status in ("PASSED", "PENDING", "FAILED")
    }
    overall = (
        "COMPLETE"
        if counts["pending"] == 0 and counts["failed"] == 0
        else "FAILED"
        if counts["failed"]
        else "IN_PROGRESS"
    )
    payload = {
        "schema": "certified-qmc-production-phase-completion-audit-v1",
        "overall": overall,
        "counts": counts,
        "checks": checks,
        "boundary": (
            "COMPLETE requires every named Cycles 013-019 artifact and "
            "external-state predicate to pass; absence is PENDING, never "
            "inferred success."
        ),
    }
    payload["audit_sha256"] = canonical_sha256(payload)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.resolve().write_text(rendered)
    print(rendered, end="")
    if args.require_complete and overall != "COMPLETE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Replace paper result markers only from passed self-hashed artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from src.certificate import canonical_sha256


FIDELITY = ROOT / "certificates" / "cycles-016-017-production-audit.json"
USABILITY = ROOT / "certificates" / "cycle-018-usability-audit.json"
ORACLE = ROOT / "certificates" / "engine-oracle-set-v1.json"
DEPOSITION = ROOT / "certificates" / "cycle-018-zenodo-deposition.json"
DEFAULT_CYCLE009 = (
    ROOT / "artifacts" / "cycle009-arb106" / "cycle-009-result.json"
)
DEFAULT_PAPER = ROOT / "docs" / "paper-supply-side-draft.md"


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha256(value) != supplied:
        raise ValueError(f"{path.name}: self-hash mismatch")
    value[field] = supplied
    return value


def passed_gate(path: Path, gate: str) -> dict:
    value = load_self_hashed(path, "certificate_sha256")
    if value["gate"].get(gate) is not True:
        raise ValueError(f"{path.name}: {gate} is not passed")
    return value


def replace_block(
    text: str, name: str, replacement: str
) -> str:
    begin = f"<!-- BEGIN GENERATED {name} -->"
    end = f"<!-- END GENERATED {name} -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"paper marker contract failed: {name}")
    prefix, remainder = text.split(begin, 1)
    _, suffix = remainder.split(end, 1)
    return (
        prefix
        + begin
        + "\n\n"
        + replacement.rstrip()
        + "\n\n"
        + end
        + suffix
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper", type=Path, default=DEFAULT_PAPER)
    parser.add_argument(
        "--cycle009", type=Path, default=DEFAULT_CYCLE009
    )
    args = parser.parse_args()
    fidelity = passed_gate(
        FIDELITY, "cycles_016_017_exit_gate_passed"
    )
    usability = passed_gate(
        USABILITY, "cycle_018_data_gate_passed"
    )
    oracle = load_self_hashed(ORACLE, "oracle_sha256")
    if (
        oracle["claim_tag"] != "VERIFIED"
        or oracle["counts"]["total"] != 298
    ):
        raise ValueError("compact oracle is not VERIFIED 298/298")
    deposition = load_self_hashed(
        DEPOSITION, "certificate_sha256"
    )
    if (
        deposition.get("published") is not True
        or not deposition.get("doi")
    ):
        raise ValueError("DOI deposition is not published")
    cycle009 = load_self_hashed(
        args.cycle009.resolve(), "certificate_sha256"
    )
    histogram = cycle009["histogram"]
    if (
        cycle009["comparison_count"] != 802767
        or histogram["arb_resolved"]
        + histogram["exact_crt_resolved"]
        != 802767
    ):
        raise ValueError("Cycle-009 histogram count mismatch")

    fidelity_lines = "\n".join(
        (
            "- fidelity manifest: `VERIFIED`, "
            f"{fidelity['dataset']['chunk_count']:,} authenticated "
            f"chunks and {fidelity['dataset']['payload_bytes']:,} "
            "payload bytes;",
            "- selected replay: 100/100 `VERIFIED`, both overflow "
            "checks equal for every entry, maximum touched payload "
            f"fraction {fidelity['selected_entry_replay']['maximum_touched_payload_fraction']:.8g};",
            "- independent direct oracles: 3/3 equal;",
            "- measured production throughput: "
            f"{fidelity['throughput']['aggregate_ns_per_update']:.6f} "
            "ns/update under the versioned VPS monitor;",
            "- usability grid: 36/36 alternate-profile entries "
            "`VERIFIED`; 18/18 \\(j^{-2}\\) entries reused by hash "
            "without recomputation;",
            "- compact engine oracle: 298/298 cases `VERIFIED`, "
            f"self-hash `{oracle['oracle_sha256']}`;",
            "- archived release: "
            f"[{deposition['doi']}]({deposition['record_url']}).",
        )
    )
    exact_count = histogram["exact_crt_resolved"]
    cycle009_lines = "\n".join(
        (
            "- escalation histogram: "
            f"DD-resolved 0, Arb-resolved "
            f"{histogram['arb_resolved']:,}, exact-CRT-resolved "
            f"{exact_count:,}, exact equalities "
            f"{histogram['exact_equalities']:,};",
            "- exact-CRT acceptance predicate: "
            f"`{exact_count} < 803` is "
            f"`{'PASSED' if cycle009['acceptance']['passed'] else 'FAILED'}`;",
            "- exact final-vector merit: `VERIFIED`; the complete "
            "reduced rational is stored in the result artifact under "
            f"certificate hash `{cycle009['certificate_sha256']}` and "
            "generator hash "
            f"`{cycle009['final_merit']['generator_sha256']}`.",
        )
    )
    paper = args.paper.resolve()
    text = paper.read_text()
    text = replace_block(
        text, "PRODUCTION OUTCOME", fidelity_lines
    )
    text = replace_block(text, "CYCLE009 OUTCOME", cycle009_lines)
    if "`PENDING`" in text:
        raise ValueError("paper still contains pending result markers")
    paper.write_text(text)
    print(paper)


if __name__ == "__main__":
    main()

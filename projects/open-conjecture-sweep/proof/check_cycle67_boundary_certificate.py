#!/usr/bin/env python3
"""Audit the complete exact C67 endpoint-boundary certificate."""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "discovery/out/cycle67-boundary-positivity"
SOURCE_SCALE = 11_943_936
INVARIANT_SCALE = 64


def load_integer_tsv(path: Path) -> dict[tuple[int, ...], int]:
    result = {}
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            result[tuple(map(int, row[:4]))] = int(row[4])
    return result


def checked_json(path: Path) -> dict:
    payload = json.loads(path.read_text())
    assert payload["status"] == "PASS", path
    assert payload["epistemic_status"] == "PROVED", path
    return payload


def assert_complete_tensor(path: Path, expected: int, maximum_degree: int = 63) -> None:
    payload = checked_json(path)
    assert payload["complete_cover"] is True
    assert len(payload["charts"]) == expected
    for chart in payload["charts"].values():
        assert chart["complete"] is True
        assert chart["unresolved"] == 0
        assert max(chart["degrees"]) <= maximum_degree


def evidence_hashes(output_dir: Path) -> dict[str, str]:
    root_files = [
        "pullback-summary.json", "cycle_equal.tsv", "cycle_zero.tsv",
        "trans_equal.tsv", "trans_zero.tsv", "chart-forms.tsv",
        "pullback-chart-forms.tsv",
    ]
    directories = [
        "grid", "blowup-fast", "blowup-source-fast", "blowup-stripped",
        "equal-hessian-quotients", "equal-hessian-tensor",
        "equal-curve-restrictions", "equal-curve-tensor",
        "equal-joint-blowup", "equal-joint-tensor",
        "transzero-joint-blowup", "transzero-joint-tensor",
        "cyclezero-corner-blowup", "cyclezero-corner-tensor",
        "cyclezero-trans-direct-tensor",
    ]
    paths = [output_dir / name for name in root_files]
    for directory in directories:
        paths.extend(path for path in (output_dir / directory).rglob("*") if path.is_file())
    return {
        path.relative_to(output_dir).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(paths)
    }


def audit(output_dir: Path = DEFAULT_OUT) -> dict:
    OUT = output_dir
    pullbacks = checked_json(OUT / "pullback-summary.json")
    assert set(pullbacks["families"]) == {
        "cycle_equal", "cycle_zero", "trans_equal", "trans_zero"
    }
    assert all(row["independent_invariant_controls"] == 3 for row in pullbacks["families"].values())

    grid = checked_json(OUT / "grid/grid-summary.json")
    assert grid["total_rows"] == 19_380
    assert grid["total_negative"] == 0

    invariant_dir = OUT / "blowup-fast"
    source_dir = OUT / "blowup-source-fast"
    names = sorted(path.stem for path in invariant_dir.glob("*.tsv"))
    assert len(names) == 9
    ratio = SOURCE_SCALE // INVARIANT_SCALE
    assert SOURCE_SCALE % INVARIANT_SCALE == 0
    for name in names:
        invariant = load_integer_tsv(invariant_dir / f"{name}.tsv")
        source = load_integer_tsv(source_dir / f"{name}.tsv")
        assert source == {exponent: ratio * coefficient for exponent, coefficient in invariant.items()}, name

    factors = checked_json(OUT / "blowup-stripped/factor-report.json")["charts"]
    assert factors["cycle_equal"]["factors"] == {"1-x": 3, "y": 3}
    for name in names:
        if name.startswith("trans_equal"):
            assert factors[name]["factors"] == {"1-x": 3}
        elif name != "cycle_equal":
            assert factors[name]["factors"] == {}

    equal_hessian = checked_json(OUT / "equal-hessian-quotients/hessian-factor-report.json")
    assert equal_hessian["factor"] == "(1-y-3*x+x*y)^2"
    assert len(equal_hessian["charts"]) == 5
    assert all(row["exact_zero_remainder"] for row in equal_hessian["charts"].values())
    assert_complete_tensor(OUT / "equal-hessian-tensor/tensor-summary.json", 5)

    equal_curve = checked_json(OUT / "equal-curve-restrictions/curve-restriction-report.json")
    assert len(equal_curve["charts"]) == 5
    assert all(row["radial_factor"] == "r^2" for row in equal_curve["charts"].values())
    assert_complete_tensor(OUT / "equal-curve-tensor/tensor-summary.json", 5)

    equal_joint = checked_json(OUT / "equal-joint-blowup/joint-blowup-report.json")
    assert len(equal_joint["charts"]) == 20
    assert all(row["radial_factor"] == "rho^2" for row in equal_joint["charts"].values())
    assert all(row["exact_rational_control"] == "PASS" for row in equal_joint["charts"].values())
    assert_complete_tensor(OUT / "equal-joint-tensor/tensor-summary.json", 20)

    transzero = checked_json(OUT / "transzero-joint-blowup/joint-blowup-report.json")
    assert len(transzero["charts"]) == 8
    assert all(row["radial_factor"] == "rho^2" for row in transzero["charts"].values())
    assert all(row["exact_rational_control"] == "PASS" for row in transzero["charts"].values())
    assert_complete_tensor(OUT / "transzero-joint-tensor/tensor-summary.json", 8)

    corner = checked_json(OUT / "cyclezero-corner-blowup/corner-blowup-report.json")
    assert len(corner["charts"]) == 2
    assert all(row["radial_factor"] == "rho^2" for row in corner["charts"].values())
    assert all(row["exact_rational_control"] == "PASS" for row in corner["charts"].values())
    assert_complete_tensor(OUT / "cyclezero-corner-tensor/tensor-summary.json", 2)
    assert_complete_tensor(OUT / "cyclezero-trans-direct-tensor/tensor-summary.json", 1)

    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "source_invariant_charts": 9,
        "final_certificate_charts": 31,
        "endpoint_families": 4,
        "claim": "N(a)-N(a_cl)>=0 on all four C64 endpoint families",
        "claim_boundary": (
            "PROVED only on the four C64 endpoint families; interior fiber "
            "critical points and the full fixed-S3 comparison remain open."
        ),
        "evidence_hashes": evidence_hashes(OUT),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", nargs="?", type=Path, default=DEFAULT_OUT)
    checked = audit(parser.parse_args().output_dir)
    print(json.dumps(checked, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

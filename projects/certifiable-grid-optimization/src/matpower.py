"""Safe parser for the numeric subset of MATPOWER case files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np


@dataclass(frozen=True)
class MatpowerCase:
    """The core numeric matrices of a MATPOWER v2 case."""

    base_mva: float
    bus: np.ndarray
    gen: np.ndarray
    branch: np.ndarray
    gencost: np.ndarray | None
    source: str


def _without_comments(text: str) -> str:
    return "\n".join(line.split("%", 1)[0] for line in text.splitlines())


def _parse_matrix(text: str, field: str, *, required: bool) -> np.ndarray | None:
    match = re.search(
        rf"\bmpc\.{re.escape(field)}\s*=\s*\[(.*?)\]\s*;",
        text,
        flags=re.DOTALL,
    )
    if match is None:
        if required:
            raise ValueError(f"missing mpc.{field} matrix")
        return None
    rows = []
    for raw_row in match.group(1).split(";"):
        tokens = raw_row.replace(",", " ").split()
        if tokens:
            try:
                rows.append([float(token) for token in tokens])
            except ValueError as error:
                raise ValueError(
                    f"mpc.{field} contains a nonnumeric expression"
                ) from error
    if not rows:
        raise ValueError(f"mpc.{field} is empty")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError(f"mpc.{field} has inconsistent row lengths")
    return np.asarray(rows, dtype=float)


def parse_matpower_text(text: str, *, source: str = "<memory>") -> MatpowerCase:
    """Parse data without evaluating the surrounding MATLAB program."""

    cleaned = _without_comments(text)
    version = re.search(r"\bmpc\.version\s*=\s*['\"]([^'\"]+)['\"]\s*;", cleaned)
    if version is None or version.group(1) != "2":
        raise ValueError("only explicit MATPOWER case version 2 is supported")
    base_match = re.search(
        r"\bmpc\.baseMVA\s*=\s*"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)\s*;",
        cleaned,
    )
    if base_match is None:
        raise ValueError("missing numeric mpc.baseMVA")
    base_mva = float(base_match.group(1))
    if base_mva <= 0:
        raise ValueError("mpc.baseMVA must be positive")

    bus = _parse_matrix(cleaned, "bus", required=True)
    gen = _parse_matrix(cleaned, "gen", required=True)
    branch = _parse_matrix(cleaned, "branch", required=True)
    gencost = _parse_matrix(cleaned, "gencost", required=False)
    assert bus is not None and gen is not None and branch is not None
    if bus.shape[1] < 13:
        raise ValueError("mpc.bus must contain at least 13 columns")
    if gen.shape[1] < 10:
        raise ValueError("mpc.gen must contain at least 10 columns")
    if branch.shape[1] < 13:
        raise ValueError("mpc.branch must contain at least 13 columns")
    return MatpowerCase(base_mva, bus, gen, branch, gencost, source)


def load_matpower_case(path: str | Path) -> MatpowerCase:
    case_path = Path(path)
    return parse_matpower_text(
        case_path.read_text(encoding="utf-8"), source=str(case_path)
    )

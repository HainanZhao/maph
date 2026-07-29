"""Build and invoke the compiled Cycle-009 exact NTT scorer."""

from __future__ import annotations

from pathlib import Path
import struct
import subprocess
import tempfile
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
BINARY = ROOT / "build" / "native" / "cycle009_ntt"


def build_cycle009_ntt() -> Path:
    subprocess.run(
        ["make", "-C", str(ROOT / "native"), str(BINARY)],
        check=True,
        capture_output=True,
        text=True,
    )
    return BINARY


def compiled_candidate_scores(
    modulus: int,
    prime: int,
    primitive_root: int,
    prefix: Sequence[int],
    *,
    binary: Path | None = None,
) -> list[int]:
    executable = binary or build_cycle009_ntt()
    if not prefix:
        raise ValueError("Cycle-009 prefix must contain z1=1")
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-cycle009-"
    ) as directory:
        output = Path(directory) / "scores.bin"
        subprocess.run(
            [
                str(executable),
                str(modulus),
                str(prime),
                str(primitive_root),
                ",".join(str(value) for value in prefix),
                str(output),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        raw = output.read_bytes()
    expected = (modulus // 4) * 8
    if len(raw) != expected:
        raise ValueError("compiled Cycle-009 score length mismatch")
    return [
        item[0]
        for item in struct.iter_unpack("<Q", raw)
    ]

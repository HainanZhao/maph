#!/usr/bin/env python3
"""Self-test the project-local immutable sealing scaffold."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile

from cycle_seal_v1 import freeze_inputs, render


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source.txt"
        source.write_bytes(b"frozen\n")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        frozen = freeze_inputs(root, {"source": (source, digest)})
        payload = {"status": "TEST", "frozen": frozen}
        first = render(payload)
        second = render(json.loads(first))
        if first != second:
            raise AssertionError("render is not deterministic")
    print(json.dumps({"status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()

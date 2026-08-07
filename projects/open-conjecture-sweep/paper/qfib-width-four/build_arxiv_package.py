#!/usr/bin/env python3
"""Build a deterministic arXiv source tarball from the released paper."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path


PAPER = Path(__file__).resolve().parent
FILES = ("main.tex", "main.bbl", "references.bib")
EPOCH = 1785974400


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name in FILES:
            data = (PAPER / name).read_bytes()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = EPOCH
            info.mode = 0o644
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            archive.addfile(info, io.BytesIO(data))
    with args.output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=EPOCH) as compressed:
            compressed.write(tar_buffer.getvalue())
    payload = args.output.read_bytes()
    result = {
        "bytes": len(payload),
        "files": list(FILES),
        "package": args.output.name,
        "sha256": hashlib.sha256(payload).hexdigest(),
    }
    checksum_path = args.output.with_suffix(args.output.suffix + ".json")
    checksum_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Optimization-robust pinned interpreter convention for proof replays."""
from __future__ import annotations

import platform
import sys


IMPLEMENTATION = "CPython"
VERSION = (3, 12, 3)
OPTIMIZE = 0
JSON_POLICY = "stdlib json sort_keys=True; UTF-8; LF; trailing newline"


def require_pinned_runtime() -> dict[str, object]:
    actual = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    if platform.python_implementation() != IMPLEMENTATION:
        raise RuntimeError(f"proof replay requires {IMPLEMENTATION}")
    if actual != VERSION:
        raise RuntimeError(f"proof replay requires {VERSION}, got {actual}")
    if sys.flags.optimize != OPTIMIZE:
        raise RuntimeError("proof replay forbids -O/-OO because subordinate exact checks use assertions")
    return {
        "implementation": IMPLEMENTATION,
        "version": ".".join(map(str, VERSION)),
        "optimize": OPTIMIZE,
        "json_policy": JSON_POLICY,
    }

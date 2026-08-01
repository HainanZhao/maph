"""Pinned interpreter convention for deterministic proof replays."""
from __future__ import annotations

import platform
import sys


IMPLEMENTATION = "CPython"
VERSION = (3, 12, 3)
JSON_POLICY = "stdlib json sort_keys=True; UTF-8; LF; trailing newline"


def assert_pinned_runtime() -> dict[str, object]:
    actual = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    assert platform.python_implementation() == IMPLEMENTATION, "proof replay requires CPython"
    assert actual == VERSION, f"proof replay requires CPython {VERSION}, got {actual}"
    return {
        "implementation": IMPLEMENTATION,
        "version": ".".join(map(str, VERSION)),
        "json_policy": JSON_POLICY,
    }

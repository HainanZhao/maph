#!/usr/bin/env python3
"""Replay the proved Q(sqrt(14)) packet with Taylor quadrature."""

from __future__ import annotations

import sys

import certify_q14_p7_packet as q14
from certified_taylor_quadrature import certified_taylor


q14.certified_simpson = certified_taylor

if __name__ == "__main__":
    sys.argv = [
        sys.argv[0],
        "--digits",
        "80",
        "--tolerance",
        "1e-11",
    ]
    q14.main()

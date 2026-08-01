"""Versioned correction convention for P7 detector local occupancy v2."""
from __future__ import annotations

from conventions.p7_detector_local_occupancy_v1 import (  # re-export frozen scope
    ARCHIMEDEAN_TYPE,
    FIELD,
    GATE_ID,
    IDEAL_EXTENSION,
    RESOURCE_LIMITS,
    SHELL,
)


SCHEMA_VERSION = "p7-detector-local-occupancy-v2"
SOURCES = {
    "p7_detector_local_occupancy_v1": {
        "path": "artifacts/p7-detector-local-occupancy-v1.json",
        "sha256": "3d8d9971ce48104b27390aa26ce3f1bfd1a11a95aeb7d4cab4ba545995539ce4",
        "locators": "sealed v1 result; v2 corrects only two case-sensitive regression-test assertions",
    },
}

NON_PROMOTION = (
    "The v1 mathematical claims, source pins, exact-conductor convention, and zero extension are unchanged.",
    "The correction does not create a P7 detector or an unconditional source-scale D_Delta bound.",
    "P7-3 still requires the cross-character local occupancy input and the separate averaged-block A_0 cubic input.",
)

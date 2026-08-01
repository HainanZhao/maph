"""Second versioned harness correction for P7 detector local occupancy."""
from __future__ import annotations

from conventions.p7_detector_local_occupancy_v2 import (
    ARCHIMEDEAN_TYPE,
    FIELD,
    GATE_ID,
    IDEAL_EXTENSION,
    RESOURCE_LIMITS,
    SHELL,
)


SCHEMA_VERSION = "p7-detector-local-occupancy-v3"
SOURCES = {
    "p7_detector_local_occupancy_v2": {
        "path": "artifacts/p7-detector-local-occupancy-v2-correction.json",
        "sha256": "98562bf5f90b818dbc0332bff0941dcb1533ea90873ea4ce94cf05679186dba5",
        "locators": "sealed v2 correction; v3 corrects one remaining prose-substring regression assertion only",
    },
}

NON_PROMOTION = (
    "The v1 mathematical result and v2 corrected companion document are unchanged.",
    "The v3 correction does not create an unconditional source-scale D_Delta bound or a P7 detector.",
    "P7-3 remains open, including the separate averaged-block A_0 cubic input.",
)

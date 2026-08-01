"""v3 correction wrapper for the executable CRR finite-analogue protocol.

All schedule, construction, precision, and threshold conventions are exactly
those of v2.  This version makes the dimensional cubic trace identity explicit
so it cannot be implemented as a 2M-by-2M shifted trace.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path


_V2_PATH = Path(__file__).with_name("crr_finite_analogue_probe_v2.py")
_SPEC = importlib.util.spec_from_file_location("crr_finite_analogue_probe_v2_base", _V2_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("cannot load v2 finite-probe conventions")
_V2 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_V2)

CUBIC_DIMENSIONAL_IDENTITY = (
    "Let A_R=U diag(w) U^* be R-by-R and G=U^*U.  For k>=1, "
    "tr(A_R^k)=tr((diag(w)G)^k), but the diagonal removal is performed "
    "in ambient dimension R: tr(B_M^3)=tr((diag(w)G)^3)-3M tr((diag(w)G)^2) "
    "+3M^2 tr(diag(w)G)-R M^3.  Never use tr((diag(w)G-M I_(2M))^3)."
)

CONSTRUCTION_CONTRACT = dict(_V2.CONSTRUCTION_CONTRACT)
CONSTRUCTION_CONTRACT["cubic"] = CUBIC_DIMENSIONAL_IDENTITY

for _name in (
    "MASTER_SEED", "MASK64", "SPLITMIX64_GAMMA", "SPLITMIX64_MUL1", "SPLITMIX64_MUL2",
    "N_VALUES", "REPLICATES", "FAMILY_ORDER", "FAMILY_VARIANTS", "MUTATIONS_PER_ROW",
    "PROXY_QUADRATURE_NODES", "FINAL_QUADRATURE_NODES", "PROXY_CUBIC_MODE", "FINAL_CUBIC_MODE",
    "WALL_SECONDS", "RSS_BYTES", "MARGIN", "PROXY_INCREMENT", "SplitMix64", "nth_root_floor",
    "floor_power", "scales", "expected_scale_rows", "scheduled_rows",
):
    globals()[_name] = getattr(_V2, _name)


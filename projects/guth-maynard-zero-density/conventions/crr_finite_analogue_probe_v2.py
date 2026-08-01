"""Executable conventions for the corrected CRR finite-analogue probe v2.

This is a discovery convention, not a continuous CRR convention.  It retains
the v1 row identifiers, sizes, variants, master seed, and thresholds, while
making every formerly verbal construction and every random-word consumption
rule executable.  Floating-point proxy arithmetic is deliberately separated
from the dual-precision outcome checks in the runner.
"""
from __future__ import annotations

from fractions import Fraction


MASTER_SEED = 0x43525255424F4C44
MASK64 = (1 << 64) - 1
SPLITMIX64_GAMMA = 0x9E3779B97F4A7C15
SPLITMIX64_MUL1 = 0xBF58476D1CE4E5B9
SPLITMIX64_MUL2 = 0x94D049BB133111EB

N_VALUES = (256, 512, 1024, 2048)
REPLICATES = (0, 1)
FAMILY_ORDER = (
    "F1-phase-rounded-frame",
    "F2-macrocell-resonant-layers",
    "F3-near-product-rational-packet",
    "F4-quadratic-modular-chirp",
    "F5-symmetric-positive-trace-spectral",
)
FAMILY_VARIANTS = {
    "F1-phase-rounded-frame": (
        {"id": "V1", "phase_denominator": 8},
        {"id": "V2", "phase_denominator": 12},
        {"id": "V3", "phase_denominator": 16},
        {"id": "V4", "phase_denominator": 24},
    ),
    "F2-macrocell-resonant-layers": (
        {"id": "V1", "macrocells": 2, "phase_denominator": 8},
        {"id": "V2", "macrocells": 3, "phase_denominator": 12},
        {"id": "V3", "macrocells": 4, "phase_denominator": 16},
        {"id": "V4", "macrocells": 6, "phase_denominator": 24},
    ),
    "F3-near-product-rational-packet": (
        {"id": "V1", "packet_denominator": 2, "phase_denominator": 8},
        {"id": "V2", "packet_denominator": 3, "phase_denominator": 12},
        {"id": "V3", "packet_denominator": 5, "phase_denominator": 20},
        {"id": "V4", "packet_denominator": 7, "phase_denominator": 28},
    ),
    "F4-quadratic-modular-chirp": (
        {"id": "V1", "prime_modulus": 257},
        {"id": "V2", "prime_modulus": 263},
        {"id": "V3", "prime_modulus": 269},
        {"id": "V4", "prime_modulus": 271},
    ),
    "F5-symmetric-positive-trace-spectral": (
        {"id": "V1", "spectral_rank": 2, "phase_denominator": 8},
        {"id": "V2", "spectral_rank": 3, "phase_denominator": 12},
        {"id": "V3", "spectral_rank": 4, "phase_denominator": 16},
        {"id": "V4", "spectral_rank": 5, "phase_denominator": 20},
    ),
}

MUTATIONS_PER_ROW = 128
PROXY_QUADRATURE_NODES = 16
FINAL_QUADRATURE_NODES = 32
PROXY_CUBIC_MODE = 8
FINAL_CUBIC_MODE = 12
WALL_SECONDS = 55 * 60
RSS_BYTES = 1 << 30
MARGIN = Fraction(1, 20)
PROXY_INCREMENT = Fraction(1, 1 << 40)


class SplitMix64:
    """Reference unsigned-64 SplitMix64, with one output per ``next`` call."""

    def __init__(self, seed: int) -> None:
        self.state = seed & MASK64

    def next_u64(self) -> int:
        self.state = (self.state + SPLITMIX64_GAMMA) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * SPLITMIX64_MUL1) & MASK64
        z = ((z ^ (z >> 27)) * SPLITMIX64_MUL2) & MASK64
        return (z ^ (z >> 31)) & MASK64


def nth_root_floor(value: int, degree: int) -> int:
    low, high = 0, 1
    while high**degree <= value:
        high *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if mid**degree <= value:
            low = mid
        else:
            high = mid
    return low


def floor_power(n: int, numerator: int, denominator: int) -> int:
    return nth_root_floor(n**numerator, denominator)


def scales(n: int) -> dict[str, int]:
    return {
        "H": floor_power(n, 6, 5),
        "R": floor_power(n, 4, 5),
        "Q": floor_power(n, 2, 5),
        "V": floor_power(n, 7, 10),
        "rational_height": floor_power(n, 3, 5),
        "cubic": floor_power(n, 18, 5),
    }


def expected_scale_rows() -> dict[int, dict[str, int]]:
    result = {n: scales(n) for n in N_VALUES}
    expected = {
        256: {"H": 776, "R": 84, "Q": 9, "V": 48, "rational_height": 27, "cubic": 467373274},
        512: {"H": 1782, "R": 147, "Q": 12, "V": 78, "rational_height": 42, "cubic": 5667243323},
        1024: {"H": 4096, "R": 256, "Q": 16, "V": 128, "rational_height": 64, "cubic": 68719476736},
        2048: {"H": 9410, "R": 445, "Q": 21, "V": 207, "rational_height": 97, "cubic": 833273994645},
    }
    if result != expected:
        raise RuntimeError("v2 scale rounding mismatch")
    return result


def scheduled_rows() -> list[dict[str, object]]:
    stream = SplitMix64(MASTER_SEED)
    rows: list[dict[str, object]] = []
    number = 0
    for n in N_VALUES:
        for family in FAMILY_ORDER:
            for variant in FAMILY_VARIANTS[family]:
                for replicate in REPLICATES:
                    rows.append({
                        "row_number": number,
                        "id": f"N{n}-{family}-{variant['id']}-R{replicate}",
                        "N": n,
                        "family": family,
                        "variant": dict(variant),
                        "replicate": replicate,
                        "row_seed": f"0x{stream.next_u64():016X}",
                    })
                    number += 1
    if len(rows) != 160 or len({str(row["id"]) for row in rows}) != 160:
        raise RuntimeError("v2 schedule must be the 160 unique v1 rows")
    return rows


CONSTRUCTION_CONTRACT = {
    "stream_rule": "All listed initialization and mutation requests consume exactly one next_u64 word, in stated order; collision scans consume no word.",
    "repair": "insert(start): test start,start+1,... modulo H; insert first unused residue; after H failed tests return INIT_INVALID.",
    "F1": "For j=0,...,R-1, let a=floor(j*H/R), J=floor(H/(8R)), u=next_u64, and insert a+(u mod (2J+1))-J modulo H.",
    "F2": "For j, c=j mod k, q=floor(j/k), r_c=floor((R+k-1-c)/k), A=floor(cH/k), B=floor((c+1)H/k), h=B-A, J=floor(h/(8r_c)); consume u and insert A+floor(qh/r_c)+(u mod (2J+1))-J modulo H.",
    "F3": "For j, ell=j mod d, q=floor(j/d), r_ell=floor((R+d-1-ell)/d), J=floor(H/(16R)); consume u and insert floor(qH/r_ell)+floor(ell H/d)+(u mod (2J+1))-J modulo H.",
    "F4": "For each of R points consume u and insert u mod H.",
    "F5": "For pair q=0,...,floor(R/2)-1 consume u, set a=1+((u mod floor((H-1)/2))*rank mod floor((H-1)/2)), insert a then H-a. If R is odd, finally insert 0 without consuming a word.",
    "phase_rounding": "For non-chirp families S_n=sum_{t in W} exp(-2*pi*i*n*t/H). If S_n=0 choose phase index 0; otherwise choose the least k in {0,...,K-1} minimizing |S_n/|S_n|-exp(2*pi*i*k/K)|, and set b_n=exp(2*pi*i*k/K). This is recomputed after every proposed W. For F4 b_n=exp(2*pi*i*(n^2+n)/p).",
    "mutation": "At each of exactly 128 proposals consume u_remove, remove sorted(W)[u_remove mod R]; consume u_insert and collision-repair u_insert mod H in W\\{removed}; recompute coefficients and the fixed proxy score; accept only if new_score-current_score >= 2^-40.",
    "proxy_score": "min(LV/lv_cut, min(E/e_low,e_high/E), mu_16/mu_cut, C_8/c_cut), with score=-infinity if C_8<=0 or a component is nonfinite; lv_cut,e_low,e_high,mu_cut,c_cut are the unchanged final numerical thresholds with mu_16 substituted for mu_32.",
    "precision": "Mutation proxies use deterministic NumPy 1.26.4 binary64/complex128 only. Final outcome checks use mpmath 1.2.1 at 256 and 384 bits for the first failed complex diagnostic, or for every complex diagnostic of a binary64 provisional hit. Binary64 is only a screen; a row never receives NO_RETAINED_HIT until a dual-precision outcome diagnostic falls strictly on the failing side of its threshold.",
    "energy": "Maintain ordered modular pair-sum counts exactly. On x->y, remove (x,x) once and (x,z),(z,x) twice for z in W\\{x}; then add (y,y) once and (y,z),(z,y) twice for z in W\\{x}. Update sum_s count[s]^2 exactly.",
    "cubic": "For modes m in {-M,...,-1,1,...,M}, set G_ab=sum_{t in W} exp(2*pi*i*(b-a)t/H), A=diag(w)G with w_m=1-|m|/(M+1). Compute tr((A-MI)^3) and multiply by N^3. This equals tr(B_M^3) for the prescribed zero-diagonal B_M.",
}


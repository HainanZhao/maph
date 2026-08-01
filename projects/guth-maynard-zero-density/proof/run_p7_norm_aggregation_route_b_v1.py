#!/usr/bin/env python3
"""Route B: symbolic local-factor and epsilon-bookkeeping proof for P7-1.

Unlike Route A, this route uses the local prime splitting descriptions and
explicit generators.  It does not enumerate ray-class multiplication tables
and it does not read Route A or the preregistration's conjectured values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_norm_aggregation_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-norm-aggregation-route-b-v1.json"
SELF = Path(__file__).resolve()


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gaussian_multiply(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def gaussian_power(z: tuple[int, int], exponent: int) -> tuple[int, int]:
    answer = (1, 0)
    for _ in range(exponent):
        answer = gaussian_multiply(answer, z)
    return answer


def chi_minus_four(value: int) -> int:
    if value % 2 == 0:
        return 0
    return 1 if value % 4 == 1 else -1


def divisor_local_sum(prime: int, exponent: int) -> int:
    return sum(chi_minus_four(prime) ** power for power in range(exponent + 1))


def ideal_local_count(prime: int, exponent: int) -> int:
    """Exact count from the three splitting types in Z[i]."""
    if prime == 2:  # (2)=(1+i)^2: exactly one ideal of each norm 2^e.
        return 1
    if prime % 4 == 1:  # p=ppbar: p^e has e+1 ideal exponent allocations.
        return exponent + 1
    # p remains prime with norm p^2, hence only even exponents occur.
    return 1 if exponent % 2 == 0 else 0


def source_integrity() -> dict[str, object]:
    rows: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(digest(path) == row["sha256"], f"pinned source hash mismatch: {label}")
        rows[label] = {"path": row["path"], "sha256": row["sha256"]}
    zaman = (ROOT / C.SOURCES["zaman_tex"]["path"]).read_text(encoding="utf-8")
    gm = (ROOT / C.SOURCES["guth_maynard_tex"]["path"]).read_text(encoding="utf-8")
    require("The \\emph{conductor}" in zaman and "maximal integral ideal" in zaman, "pinned exact-conductor definition unavailable")
    require("R\\le T^{o(1)}" in gm and "N^{18/5}V^{-4}" in gm and "TN^{12/5}V^{-4}" in gm, "pinned GM Theorem 1.1 text unavailable")
    require("we may assume $N<T$" in gm, "pinned GM nontrivial reduction unavailable")
    require("by the divisor bound" in gm, "pinned GM divisor-bound convention unavailable")
    return rows


def ray_class_hand_calculation() -> dict[str, object]:
    pi = (1, 1)
    pi4 = gaussian_power(pi, 4)
    require(pi4 == (-4, 0), "(1+i)^4 identity failed")
    # F_9^* has order 8 and its mu_4 subgroup has order 4.  For pi^e,
    # |(O/pi^e)^*|=2^(e-1); the image of mu_4 has sizes 1,2,4,4.
    pi_data = []
    for e, mu_image_size in zip(range(1, 5), (1, 2, 4, 4), strict=True):
        unit_count = 2 ** (e - 1)
        require(unit_count % mu_image_size == 0, "invalid mu_4 image count")
        pi_data.append({"e": e, "unit_count": unit_count, "mu4_image_count": mu_image_size, "quotient_count": unit_count // mu_image_size})
    require([row["quotient_count"] for row in pi_data] == [1, 1, 1, 2], "pi-power quotient formula failed")
    plus_mod_3 = (1, 1)  # 4+i = 1+i mod (3)
    minus_mod_3 = (1, -1)  # 4-i = 1-i mod (3)
    require(gaussian_power(plus_mod_3, 4) == (-4, 0), "(1+i)^4 calculation failed")
    require(gaussian_power(minus_mod_3, 4) == (-4, 0), "(1-i)^4 calculation failed")
    # -4 is -1 modulo 3. In F_9^*/mu_4 (order two), this is the nonidentity
    # quotient class, so its unique nontrivial quotient character is -1.
    mod_3_values = {"4+i": -1, "4-i": -1}
    # 4+i=i and 4-i=-i mod (4)=(pi^4); both lie in the image of mu_4.
    mod_pi4_values = {"4+i": 1, "4-i": 1}
    return {
        "status": "PROVED",
        "class_number_one_reduction": "For h(Q(i))=1, a coprime ideal (alpha) is evaluated through alpha modulo f, modulo the generator ambiguity mu_4.",
        "mod_3": {
            "unit_count": 8,
            "mu4_image_count": 4,
            "quotient_count": 2,
            "fourth_power_calculation": {"(1+i)^4": "-4=-1 mod (3)", "(1-i)^4": "-4=-1 mod (3)"},
            "values": mod_3_values,
            "exact_conductor": "The only proper divisor of (3) is (1); its ray quotient is trivial.",
        },
        "pi_power": {
            "formula": "|(O/(1+i)^e)^*|=2^(e-1), with |image(mu_4)|=1,2,4,4 for e=1,2,3,4.",
            "rows": pi_data,
            "exact_conductor": "The nontrivial e=4 quotient character cannot factor through e<4 because all those quotients are trivial.",
        },
        "mod_pi4": {"congruences": {"4+i": "i mod (4)", "4-i": "-i mod (4)"}, "values": mod_pi4_values},
        "aggregated_values": {"A_chi_3(17)": sum(mod_3_values.values()), "A_chi_pi4(17)": sum(mod_pi4_values.values())},
    }


def norm_aggregation_proof() -> dict[str, object]:
    checked_rows = []
    for prime in (2, 3, 5):
        for exponent in range(0, 9):
            lhs = ideal_local_count(prime, exponent)
            rhs = divisor_local_sum(prime, exponent)
            require(lhs == rhs, f"local norm identity failed at p={prime}, e={exponent}")
        checked_rows.append({"prime": prime, "splitting": "ramified" if prime == 2 else ("inert" if prime % 4 == 3 else "split"), "exponents_checked": "0..8"})
    return {
        "status": "PROVED",
        "identity": "a_Q(i)(n)=sum_{d|n} chi_-4(d)",
        "derivation": [
            "Both sides are multiplicative by unique ideal factorization and divisor convolution.",
            "p=2: one ideal of norm 2^e and sum_{j=0}^e chi_-4(2)^j=1.",
            "p=1 mod 4: p=ppbar, so e+1 ideals of norm p^e and sum_{j=0}^e 1=e+1.",
            "p=3 mod 4: p is a prime ideal of norm p^2, so there is one ideal for even e and none for odd e; sum_{j=0}^e(-1)^j has exactly that value.",
        ],
        "inequality": "0<=a_Q(i)(n)<=tau(n), because chi_-4(d) is in {-1,0,1} and the local formulas are nonnegative.",
        "finite_local_crosscheck": checked_rows,
    }


def normalization_bookkeeping() -> dict[str, object]:
    # The theorem statement has threshold powers 2,4,4.  The exact
    # substitution F_chi=D_N F_tilde is recorded term-by-term.
    powers = list(C.GM_THEOREM_1_1["threshold_powers"])
    require(powers == [2, 4, 4], "frozen GM threshold powers changed")
    return {
        "status": "PROVED_CONDITIONAL_ON_LENGTH_HEIGHT_RELATION",
        "stated_estimate": C.GM_THEOREM_1_1,
        "normalization": "D_N=max_{N<n<=2N} tau(n); b_n=A_chi(n)/D_N has |b_n|<=1 and F_chi=D_N F_b.",
        "exact_threshold_substitution": "V becomes V/D_N, yielding multipliers D_N^2, D_N^4, D_N^4 on the three Theorem-1.1 terms.",
        "epsilon_lemma": "For each delta>0, D_N<<_delta N^delta. If N<=T^C for fixed C, then D_N^4<<_{delta,C}T^(4C delta)=T^o(1); choose delta after the desired o(1) allowance. Hence all three multipliers are absorbed into the existing T^o(1).",
        "precise_outcome": "EXPONENT_HARMLESS_IN_THE_POLYNOMIAL_LENGTH_HEIGHT_REGIME",
        "gm_proof_regime": "The pinned proof explicitly reduces the nontrivial use of Theorem 1.1 to N<T, which is covered with C=1.",
        "unconditional_limit": "NOT_ESTABLISHED for an arbitrary two-parameter use of the displayed theorem with no relation between N and T: N^o(1) need not be T^o(1).",
        "separate_family_cost": "Even in N<=T^C this only normalizes each fixed chi polynomial. It does not supply a common coefficient vector or pay the cost of summing over chi.",
    }


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    ray = ray_class_hand_calculation()
    norm = norm_aggregation_proof()
    normalize = normalization_bookkeeping()
    require(ray["aggregated_values"] == {"A_chi_3(17)": -2, "A_chi_pi4(17)": 2}, "hand witness calculation failed")
    return {
        "artifact_id": "p7-norm-aggregation-route-b-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "claim_boundary": "Exact ray-character hand calculation, norm identity, and conditional epsilon bookkeeping only; no Hecke-family large-value or density theorem follows.",
        "route": "B: local splitting, explicit generator, and threshold-homogeneity derivation",
        "source_integrity": source_integrity(),
        "ray_character_calculation": ray,
        "norm_aggregation": norm,
        "normalization": normalize,
        "type_mismatch": {"status": "PROVED", "statement": "The two fixed-character A_chi differ at n=17. A theorem whose input is one coefficient vector b_n shared across all samples cannot be invoked verbatim on their joint (chi,t) sample collection.", "non_no_go": "This does not exclude a character-aware, ideal-indexed, or separately summed theorem with a separately proved family accounting."},
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/run_p7_norm_aggregation_route_b_v1.py --write", "check_command": "python3 proof/run_p7_norm_aggregation_route_b_v1.py --check"},
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    started = time.monotonic_ns()
    data = render(report())
    elapsed = time.monotonic_ns() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "route B exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "route B exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed Route B artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "Route B artifact mismatch; issue a correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)

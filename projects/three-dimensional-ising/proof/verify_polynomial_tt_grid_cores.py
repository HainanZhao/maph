#!/usr/bin/env python3
"""Direct checkerboard local-core replay for the polynomial TT theorem.

The first route contracts mask-carrier supercores obtained from one global
cochain gauge.  The independent route enumerates every linear character with
the spin-slice transfer and applies the exact quadratic Walsh transform.
No TT factorization of the final tensor is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_arbitrary_width_frontier import _case  # noqa: E402
from proof.verify_lane_b_universal_canonical_ranks import _canonical_reindex  # noqa: E402
from proof.verify_lane_b_width_scaling import _edge_payload, _f_values_from_walsh  # noqa: E402
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
    universal_embedding_genus,
)


PRIMES = (1_000_000_007, 1_000_000_009)
CASES = ((6, 3), (7, 3), (4, 4))
REFERENCE_SOURCE = ROOT / "proof" / "lane_b_direct_core_reference.cpp"


def _compile(directory: Path, prime: int) -> tuple[Path, str]:
    executable = directory / f"direct-core-reference-{prime}"
    command = [
        "g++",
        "-O3",
        "-std=c++17",
        "-fopenmp",
        f"-DMODULUS={prime}",
        str(REFERENCE_SOURCE),
        "-o",
        str(executable),
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    version = subprocess.run(
        ["g++", "--version"], text=True, capture_output=True, check=True
    ).stdout.splitlines()[0]
    if result.stderr:
        raise AssertionError(result.stderr)
    return executable, version


def _reference_values(
    executable: Path, prime: int, n: int, w: int, evaluation: int
) -> tuple[list[int], str]:
    genus = universal_embedding_genus(n, w)
    rotation = universal_checkerboard_rotation(n, w)
    edge_text, labels, intersection = _edge_payload(n, w, rotation, genus)
    vertices, edges = cubic_box((n, w, w))
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    result = subprocess.run(
        [str(executable)],
        input=f"{n} {w} {2 * genus} {len(edges)} {evaluation}\n{edge_text}\n",
        text=True,
        capture_output=True,
        check=True,
        env=environment,
        timeout=1800,
    )
    raw_g = [int(value) for value in result.stdout.splitlines()]
    raw_f = _f_values_from_walsh(raw_g, intersection, prime)
    structural = _case(w, n)["length_rows"][-1]
    canonical, _ = _canonical_reindex(raw_f, structural)
    inverse_spin_scale = pow(pow(2, len(vertices), prime), prime - 2, prime)
    canonical = [value * inverse_spin_scale % prime for value in canonical]
    return canonical, hashlib.sha256(
        json.dumps(labels, separators=(",", ":")).encode()
    ).hexdigest()


def _full_potential(pinned: int) -> int:
    """Insert the pinned zero at transverse vertex zero."""
    return pinned << 1


def _atomic_labels(n: int, w: int, row: dict[str, object]):
    _, edges = cubic_box((n, w, w))
    dimension = int(row["homology_bits"])
    supports = [
        {
            tuple(map(tuple, pair))
            for pair in row["atomic_coordinate_edge_support"][str(bit)]
        }
        for bit in range(dimension)
    ]
    labels = [
        sum(((edge.u, edge.v) in supports[bit]) << bit for bit in range(dimension))
        for edge in edges
    ]
    return edges, labels


def _weight(prime: int, evaluation: int, layer: int, m: int, left: int, right: int, axis: int) -> int:
    edge_hash = ((layer * m + left) * m + right) * 3 + axis
    return 2 + ((edge_hash + 1) * 104729 + evaluation * 13007) % (prime - 3)


def _kernel_scaled(lambda_state: int, mu_state: int) -> int:
    total = 0
    la, lb = lambda_state & 1, (lambda_state >> 1) & 1
    ma, mb = mu_state & 1, (mu_state >> 1) & 1
    for x in (0, 1):
        for y in (0, 1):
            exponent = (x * y) ^ ((la ^ ma) * x) ^ ((lb ^ mb) * y)
            total += -1 if exponent else 1
    if total not in (-2, 2):
        raise AssertionError("one-handle Gauss kernel lost magnitude two")
    return total // 2


GAUSS = tuple(
    tuple(_kernel_scaled(lam, mu) for mu in range(4)) for lam in range(4)
)


class DirectCoreCircuit:
    def __init__(self, n: int, w: int, prime: int, evaluation: int):
        self.n = n
        self.w = w
        self.m = w * w
        self.prime = prime
        self.evaluation = evaluation
        self.row = _case(w, n)["length_rows"][-1]
        self.genus = int(self.row["genus"])
        self.dimension = 2 * self.genus
        self.edges, self.labels = _atomic_labels(n, w, self.row)
        if any(self.row["quadratic_affine_correction"]):
            raise AssertionError("exercised atomic basis has a nonzero affine correction")

        self.transverse = [[] for _ in range(n)]
        self.connectors = [[] for _ in range(n - 1)]
        for edge_index, (edge, label) in enumerate(zip(self.edges, self.labels)):
            axis = next(i for i in range(3) if edge.u[i] != edge.v[i])
            left = self.w * edge.u[1] + edge.u[2]
            right = self.w * edge.v[1] + edge.v[2]
            item = (edge_index, edge, label, axis, left, right)
            (self.connectors if axis == 0 else self.transverse)[edge.u[0]].append(item)
        if any(label for layer in self.connectors for _, _, label, _, _, _ in layer):
            raise AssertionError("connector homology label is nonzero")

        audits = self.row["atomic_layers"]
        nonexact = [set(item["nonexact_bits"]) for item in audits]
        exact = [
            {int(bit): int(potential) for bit, potential in item["exact_mode_potentials"].items()}
            for item in audits
        ]
        self.group_of_bit = {}
        self.handles_by_group = {layer: [] for layer in range(n - 1)}
        for handle in range(self.genus):
            a_bit = 2 * handle
            layers = [layer for layer in range(n) if a_bit in nonexact[layer]]
            if not layers:
                raise AssertionError("a handle has no nonexact atomic layer")
            group = min(layers)
            self.group_of_bit[a_bit] = group
            self.group_of_bit[a_bit + 1] = group
            self.handles_by_group[group].append(handle)
        if any(not handles for handles in self.handles_by_group.values()):
            raise AssertionError("the exercised strip has an empty slab-handle group")

        pinned_potentials = [[0] * self.dimension for _ in range(n)]
        for bit in range(self.dimension):
            for layer in range(n):
                if bit in exact[layer]:
                    pinned_potentials[layer][bit] = exact[layer][bit]
            exceptional = [layer for layer in range(n) if bit in nonexact[layer]]
            if exceptional:
                before = next(
                    (
                        exact[layer][bit]
                        for layer in range(exceptional[0] - 1, -1, -1)
                        if bit in exact[layer]
                    ),
                    0,
                )
                after = next(
                    (
                        exact[layer][bit]
                        for layer in range(exceptional[-1] + 1, n)
                        if bit in exact[layer]
                    ),
                    0,
                )
                for index, layer in enumerate(exceptional):
                    pinned_potentials[layer][bit] = (
                        before if index < len(exceptional) - 1 else after
                    )
        self.potentials = [
            [_full_potential(value) for value in layer] for layer in pinned_potentials
        ]

        self.layer_gates = [[] for _ in range(n)]
        for layer, items in enumerate(self.transverse):
            for _, _, raw_label, axis, left, right in items:
                residual = 0
                for bit in range(self.dimension):
                    potential = self.potentials[layer][bit]
                    coboundary = ((potential >> left) ^ (potential >> right)) & 1
                    if ((raw_label >> bit) & 1) ^ coboundary:
                        residual |= 1 << bit
                groups = {
                    self.group_of_bit[bit]
                    for bit in range(self.dimension)
                    if (residual >> bit) & 1
                }
                if len(groups) > 1:
                    raise AssertionError("one transverse gate mixes handle slabs")
                group = next(iter(groups)) if groups else None
                if group is not None and group not in (layer - 1, layer):
                    raise AssertionError("residual gate escaped its two-layer collar")
                flip = (1 << left) ^ (1 << right)
                weight = _weight(prime, evaluation, layer, self.m, left, right, axis)
                self.layer_gates[layer].append((flip, weight, residual, group))

        self.jump_terms = [[] for _ in range(n - 1)]
        for layer in range(n - 1):
            for bit in range(self.dimension):
                jump = self.potentials[layer][bit] ^ self.potentials[layer + 1][bit]
                if jump:
                    group = self.group_of_bit[bit]
                    if group != layer:
                        raise AssertionError("gauge jump escaped its handle slab")
                    self.jump_terms[layer].append((bit, jump))

        self.masks = np.array(
            [mask for mask in range(1 << self.m) if mask.bit_count() % 2 == 0],
            dtype=np.uint32,
        )
        self.state_index = {int(mask): index for index, mask in enumerate(self.masks)}
        self.zero_index = self.state_index[0]
        self.permutations = {}
        for layer in self.layer_gates:
            for flip, _, _, _ in layer:
                if flip not in self.permutations:
                    self.permutations[flip] = np.array(
                        [self.state_index[int(mask) ^ flip] for mask in self.masks],
                        dtype=np.int32,
                    )
        self.sign_cache = {}
        self.connector_diagonals = []
        for layer, items in enumerate(self.connectors):
            diagonal = np.ones(len(self.masks), dtype=np.uint64)
            for _, _, _, axis, left, right in items:
                if left != right:
                    raise AssertionError("longitudinal connector changed transverse label")
                weight = np.uint64(
                    _weight(prime, evaluation, layer, self.m, left, right, axis)
                )
                selected = ((self.masks >> left) & 1).astype(bool)
                diagonal[selected] = (diagonal[selected] * weight) % prime
            self.connector_diagonals.append(diagonal)

    def _sign(self, potential: int) -> np.ndarray:
        if potential not in self.sign_cache:
            self.sign_cache[potential] = np.array(
                [
                    self.prime - 1 if (int(mask) & potential).bit_count() & 1 else 1
                    for mask in self.masks
                ],
                dtype=np.uint64,
            )
        return self.sign_cache[potential]

    def _apply_gates(self, vector, gates, character: int):
        result = vector
        for flip, weight, label, _ in gates:
            coefficient = self.prime - weight if (character & label).bit_count() & 1 else weight
            result = (
                result
                + np.uint64(coefficient) * result[self.permutations[flip]]
            ) % self.prime
        return result

    def apply_character_block(self, vector, group: int, character: int):
        leading = [
            gate
            for gate in self.layer_gates[group]
            if gate[3] is None or gate[3] == group
        ]
        result = self._apply_gates(vector, leading, character)
        result = (result * self.connector_diagonals[group]) % self.prime
        jump = 0
        for bit, potential in self.jump_terms[group]:
            if (character >> bit) & 1:
                jump ^= potential
        if jump:
            result = (result * self._sign(jump)) % self.prime
        trailing = [
            gate for gate in self.layer_gates[group + 1] if gate[3] == group
        ]
        if group == self.n - 2:
            trailing += [
                gate for gate in self.layer_gates[group + 1] if gate[3] is None
            ]
        return self._apply_gates(result, trailing, character)

    def apply_f_core(self, vector, group: int, lambda_states: tuple[int, ...]):
        handles = self.handles_by_group[group]
        if len(handles) != len(lambda_states):
            raise AssertionError("physical group width changed")
        accumulated = np.zeros_like(vector)
        for packed_mu in range(1 << (2 * len(handles))):
            character = 0
            coefficient = 1
            for local, handle in enumerate(handles):
                mu_state = (packed_mu >> (2 * local)) & 3
                character |= mu_state << (2 * handle)
                coefficient *= GAUSS[lambda_states[local]][mu_state]
            transformed = self.apply_character_block(vector, group, character)
            if coefficient == 1:
                accumulated = (accumulated + transformed) % self.prime
            else:
                # Unsigned wraparound is modulo 2^64, not modulo p.
                accumulated = (
                    accumulated + (np.uint64(self.prime) - transformed)
                ) % self.prime
        inverse = pow(2, -len(handles), self.prime)
        return accumulated * np.uint64(inverse) % self.prime

    def evaluate(self, lambda_index: int) -> int:
        vector = np.zeros(len(self.masks), dtype=np.uint64)
        vector[self.zero_index] = 1
        for group in range(self.n - 1):
            states = tuple(
                (lambda_index >> (2 * handle)) & 3
                for handle in self.handles_by_group[group]
            )
            vector = self.apply_f_core(vector, group, states)
        return int(vector[self.zero_index])

    def convention_digest(self) -> str:
        payload = {
            "shape": [self.n, self.w, self.w],
            "groups": self.handles_by_group,
            "potentials": self.potentials,
            "jumps": self.jump_terms,
            "gates": [
                [[flip, weight, label, group] for flip, weight, label, group in layer]
                for layer in self.layer_gates
            ],
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()


def _selected_indices(dimension: int, all_values: bool) -> list[int]:
    if all_values:
        return list(range(1 << dimension))
    selected = {0}
    selected.update(1 << bit for bit in range(dimension))
    selected.update(3 << (2 * handle) for handle in range(dimension // 2))
    state = 0x6A09E667
    for _ in range(64):
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        selected.add(state & ((1 << dimension) - 1))
    return sorted(selected)


def verify(smoke: bool = False) -> dict[str, object]:
    started = time.perf_counter()
    rows = []
    compilers = {}
    with tempfile.TemporaryDirectory(prefix="lane-b-direct-core-") as temporary:
        primes = PRIMES[:1] if smoke else PRIMES
        cases = CASES[:1] if smoke else CASES
        evaluations = (0,) if smoke else (0, 1)
        for prime in primes:
            executable, compiler = _compile(Path(temporary), prime)
            compilers[str(prime)] = compiler
            for n, w in cases:
                for evaluation in evaluations:
                    reference, label_hash = _reference_values(
                        executable, prime, n, w, evaluation
                    )
                    circuit = DirectCoreCircuit(n, w, prime, evaluation)
                    indices = _selected_indices(
                        circuit.dimension,
                        all_values=smoke or (n, w) == (6, 3),
                    )
                    direct = [circuit.evaluate(index) for index in indices]
                    expected = [reference[index] for index in indices]
                    if direct != expected:
                        mismatch = next(
                            position
                            for position, pair in enumerate(zip(direct, expected))
                            if pair[0] != pair[1]
                        )
                        raise AssertionError(
                            "direct grid core mismatch: "
                            f"shape={(n,w,w)}, prime={prime}, evaluation={evaluation}, "
                            f"lambda={indices[mismatch]}, direct={direct[mismatch]}, "
                            f"reference={expected[mismatch]}"
                        )
                    rows.append(
                        {
                            "shape": [n, w, w],
                            "prime": prime,
                            "evaluation": evaluation,
                            "genus": circuit.genus,
                            "carrier": len(circuit.masks),
                            "group_handle_counts": [
                                len(circuit.handles_by_group[group])
                                for group in range(n - 1)
                            ],
                            "checked_spin_structures": len(indices),
                            "all_spin_structures": len(indices) == 1 << circuit.dimension,
                            "direct_core_matches_independent_reference": True,
                            "atomic_label_sha256": label_hash,
                            "core_convention_sha256": circuit.convention_digest(),
                        }
                    )
    return {
        "claim_status": "CERTIFIED_NUMERICAL direct polynomial-core firewall",
        "primes": list(primes),
        "compilers": compilers,
        "weight_rule": "2 + ((hash+1)*104729 + evaluation*13007) mod (p-3)",
        "gauss_kernel_scaled": GAUSS,
        "rows": rows,
        "construction": (
            "atomic cochains -> one transported layer gauge -> residual two-layer "
            "handle groups -> parity-mask convolution cores -> local quadratic "
            "Walsh/Gauss transform"
        ),
        "independence": (
            "Direct route uses even-mask convolution and local core actions. "
            "Reference route uses spin-slice transfer for every linear character "
            "followed by the global quadratic Walsh transform."
        ),
        "no_final_tensor_factorization": True,
        "runtime": {
            "implementation": platform.python_implementation(),
            "python": platform.python_version(),
            "numpy": np.__version__,
        },
        "wall_seconds": round(time.perf_counter() - started, 6),
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def render_latex(result: dict[str, object]) -> str:
    grouped = {}
    for row in result["rows"]:
        key = tuple(row["shape"])
        grouped.setdefault(key, row)
    lines = [
        r"\begin{table}[ht]",
        r"\centering",
        r"\caption{Direct denominator-free core firewall.  Each row agrees at",
        r"two nonuniform evaluations over both declared primes.}",
        r"\label{tab:polynomial-core-firewall}",
        r"\small",
        r"\begin{tabular}{@{}lrrrrl@{}}",
        r"\toprule",
        r"graph & genus & carrier & handle groups & sectors & result\\",
        r"\midrule",
    ]
    for shape, row in grouped.items():
        graph = f"$G_{{{shape[0]},{shape[1]}}}$"
        groups = ",".join(str(value) for value in row["group_handle_counts"])
        sectors = (
            f"all {row['checked_spin_structures']}"
            if row["all_spin_structures"]
            else str(row["checked_spin_structures"])
        )
        lines.append(
            f"{graph} & {row['genus']} & {row['carrier']} & "
            f"$({groups})$ & {sectors} & agree\\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--json-output")
    parser.add_argument("--tex-output")
    arguments = parser.parse_args()
    payload = verify(smoke=arguments.smoke)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.json_output:
        Path(arguments.json_output).write_text(encoded)
    else:
        print(encoded, end="")
    if arguments.tex_output:
        Path(arguments.tex_output).write_text(render_latex(payload))

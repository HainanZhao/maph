"""Exact Fourier bridge between zero-field spin slices and parity frontiers.

The cross-section has ``m`` vertices.  Spin configurations are represented by
bit masks modulo the all-one mask, using the representative whose bit zero is
zero.  Frontier masks have even Hamming parity.  These two ``2^(m-1)`` sets
are perfect duals under the dot product over GF(2).
"""

from __future__ import annotations

from itertools import product


def spin_representatives(m: int) -> tuple[int, ...]:
    if m < 1:
        raise ValueError("a slice must contain at least one spin")
    return tuple(mask << 1 for mask in range(1 << (m - 1)))


def even_masks(m: int) -> tuple[int, ...]:
    if m < 1:
        raise ValueError("a slice must contain at least one site")
    return tuple(mask for mask in range(1 << m) if mask.bit_count() % 2 == 0)


def walsh_pairing(m: int) -> tuple[tuple[int, ...], ...]:
    """Return H[s,x]=(-1)^(s dot x), with quotient/even ordering pinned."""
    spins = spin_representatives(m)
    parity = even_masks(m)
    return tuple(
        tuple(-1 if (spin & mask).bit_count() % 2 else 1 for mask in parity)
        for spin in spins
    )


def transverse_edges(w: int) -> tuple[tuple[int, int], ...]:
    """Lexicographically ordered edges of one free ``w x w`` slice."""
    if w < 1:
        raise ValueError("width must be positive")
    edges: list[tuple[int, int]] = []
    for y, z in product(range(w), repeat=2):
        u = w * y + z
        if y + 1 < w:
            edges.append((u, w * (y + 1) + z))
        if z + 1 < w:
            edges.append((u, w * y + z + 1))
    return tuple(edges)


def parity_transfer_mod(
    w: int,
    transverse_weights: tuple[int, ...],
    connector_weights: tuple[int, ...],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    """High-temperature transfer K[x,y]=B[x+y]C[y] over GF(prime)."""
    m = w * w
    edges = transverse_edges(w)
    if len(transverse_weights) != len(edges) or len(connector_weights) != m:
        raise ValueError("weight count mismatch")
    boundary = [0] * (1 << m)
    boundary[0] = 1
    for (u, v), weight in zip(edges, transverse_weights):
        flip = (1 << u) | (1 << v)
        updated = boundary[:]
        for mask, value in enumerate(boundary):
            if value:
                updated[mask ^ flip] = (updated[mask ^ flip] + value * weight) % prime
        boundary = updated
    connector = [1] * (1 << m)
    for mask in range(1 << m):
        value = 1
        for site, weight in enumerate(connector_weights):
            if mask >> site & 1:
                value = value * weight % prime
        connector[mask] = value
    parity = even_masks(m)
    return tuple(
        tuple(boundary[left ^ right] * connector[right] % prime for right in parity)
        for left in parity
    )


def quotient_spin_transfer_mod(
    w: int,
    transverse_weights: tuple[int, ...],
    connector_weights: tuple[int, ...],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    """Normalized conventional transfer on spins modulo global flip.

    Edge Boltzmann factors have been divided by their cosh factors.  For a
    quotient target ``[tau]`` the two representatives ``tau`` and ``-tau``
    are summed, so this is exactly the restriction of the full zero-field
    transfer to globally flip-even functions.
    """
    m = w * w
    edges = transverse_edges(w)
    if len(transverse_weights) != len(edges) or len(connector_weights) != m:
        raise ValueError("weight count mismatch")
    spins = spin_representatives(m)
    rows: list[tuple[int, ...]] = []
    for spin in spins:
        intra = 1
        for (u, v), weight in zip(edges, transverse_weights):
            sign = -1 if ((spin >> u) ^ (spin >> v)) & 1 else 1
            intra = intra * (1 + sign * weight) % prime
        row: list[int] = []
        for target in spins:
            plus = 1
            minus = 1
            for site, weight in enumerate(connector_weights):
                sign = -1 if ((spin >> site) ^ (target >> site)) & 1 else 1
                plus = plus * (1 + sign * weight) % prime
                minus = minus * (1 - sign * weight) % prime
            row.append(intra * (plus + minus) % prime)
        rows.append(tuple(row))
    return tuple(rows)


def matmul_mod(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matrix shape mismatch")
    columns = tuple(zip(*right))
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column)) % prime for column in columns)
        for row in left
    )


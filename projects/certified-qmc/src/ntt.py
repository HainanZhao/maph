"""Auditable radix-two number-theoretic transform."""

from __future__ import annotations

from typing import Sequence


def _validate_length(length: int, prime: int) -> None:
    if length < 1 or length & (length - 1):
        raise ValueError("transform length must be a positive power of two")
    if (prime - 1) % length:
        raise ValueError("transform length does not divide prime-1")


def radix2_ntt(
    values: Sequence[int],
    prime: int,
    primitive_root: int,
    *,
    inverse: bool = False,
) -> list[int]:
    """Return the forward or normalized inverse radix-two NTT."""

    length = len(values)
    _validate_length(length, prime)
    transformed = [value % prime for value in values]

    target = 0
    for source in range(1, length):
        bit = length >> 1
        while target & bit:
            target ^= bit
            bit >>= 1
        target ^= bit
        if source < target:
            transformed[source], transformed[target] = (
                transformed[target],
                transformed[source],
            )

    block = 2
    while block <= length:
        root = pow(primitive_root, (prime - 1) // block, prime)
        if inverse:
            root = pow(root, -1, prime)
        half = block // 2
        for start in range(0, length, block):
            twiddle = 1
            for offset in range(half):
                even = transformed[start + offset]
                odd = transformed[start + offset + half] * twiddle % prime
                transformed[start + offset] = (even + odd) % prime
                transformed[start + offset + half] = (even - odd) % prime
                twiddle = twiddle * root % prime
        block *= 2

    if inverse:
        inverse_length = pow(length, -1, prime)
        transformed = [
            value * inverse_length % prime for value in transformed
        ]
    return transformed


def direct_cyclic_convolution(
    left: Sequence[int],
    right: Sequence[int],
    prime: int,
) -> list[int]:
    if len(left) != len(right) or not left:
        raise ValueError("equal nonempty vectors are required")
    length = len(left)
    return [
        sum(
            left[index] * right[(output - index) % length]
            for index in range(length)
        ) % prime
        for output in range(length)
    ]


def ntt_cyclic_convolution(
    left: Sequence[int],
    right: Sequence[int],
    prime: int,
    primitive_root: int,
) -> list[int]:
    if len(left) != len(right) or not left:
        raise ValueError("equal nonempty vectors are required")
    left_hat = radix2_ntt(left, prime, primitive_root)
    right_hat = radix2_ntt(right, prime, primitive_root)
    product_hat = [
        x * y % prime for x, y in zip(left_hat, right_hat)
    ]
    return radix2_ntt(
        product_hat, prime, primitive_root, inverse=True
    )


def ntt_plus_correlation(
    left: Sequence[int],
    right: Sequence[int],
    prime: int,
    primitive_root: int,
) -> list[int]:
    """Return C[a]=sum_t left[t]*right[t+a] modulo prime."""

    if len(left) != len(right) or not left:
        raise ValueError("equal nonempty vectors are required")
    length = len(left)
    reversed_left = [0] * length
    for index, value in enumerate(left):
        reversed_left[-index % length] = value
    return ntt_cyclic_convolution(
        reversed_left, right, prime, primitive_root
    )

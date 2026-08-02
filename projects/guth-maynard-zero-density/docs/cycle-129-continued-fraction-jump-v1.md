# Cycle 129: every collision forces a large partial-quotient jump

Let `alpha=g^a` and let `p/q` be a reduced Cycle-92 collision label on
multiplicity scale `M`. Then

```text
|alpha-p/q| << 1/(KQ),             q << Q/M.       (1)
```

Consequently,

```text
2q^2|alpha-p/q| << Q/(KM^2).                       (2)
```

Writing `K=X^xi`, `M=X^mu`, the reciprocal of the right side has exponent

```text
xi+2mu-1/3 >= 16/25-1/3=23/75.                   (3)
```

Thus (2) is below one for sufficiently large `X`, uniformly throughout the
lower band. Legendre's elementary continued-fraction criterion proves that
`p/q` is a convergent of `alpha`.

Let `q_next` be the denominator of the next convergent. The standard
determinant proof for consecutive convergents gives

```text
|alpha-p/q| > 1/[q(q+q_next)].                    (4)
```

Combining (1) and (4),

```text
q_next > 1/(q|alpha-p/q|)-q >> KM.                (5)
```

The subtraction is harmless because its ratio to the first term is bounded
by `Q/(KM^2)`, already power-small by (3).

If `A_next` is the next partial quotient, then

```text
q_next=A_next q+q_previous.
```

Equations (1) and (5) therefore force

```text
A_next >> KM^2/Q.                                 (6)
```

The jump in (6) has exponent `xi+2mu-1/3`, uniformly at least `23/75`.
This proves the continued-fraction pattern seen in Cycle 128 and strengthens
it: collisions do not merely select convergents, but convergents followed by
a fixed-power denominator jump.

The exact remaining counting theorem is now:

```text
#{a: some convergent q<<Q/M of g^a has
      A_next>>KM^2/Q}
 << (Q/M)X^epsilon.                               (7)
```

After multiplication by `M`, (7) gives the required `QX^epsilon` collision
bound for that dyadic class. Exceptional violations of (7) retain their
mode, convergent, next denominator, partial quotient, and rational label for
the Cycle-125/126 recurrence inverse.

No averaged theorem (7), collision or simple-root closure, complete moment,
density gain, or interval gain is proved.

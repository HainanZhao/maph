# Cycle 130: broad continued-fraction cylinders close at volume scale

For a Cycle-129 multiplicity class define

```text
A0=KM^2/Q,
q0=sqrt(D/A0),
L=Q/M.                                             (1)
```

If a convergent `p/q` has next partial quotient at least a fixed multiple of
`A0`, its continued-fraction cylinder lies in an interval of length

```text
O(1/(A0q^2))                                      (2)
```

about `p/q`. On the fixed compact chart, consecutive mode targets `g^a` are
separated by `asymp 1/D`. Hence an interval `J` contains

```text
O(1+D|J|)                                         (3)
```

mode targets.

For each `q`, there are `O(q)` relevant numerators. Summing (3) with (2) over
`q<=q0` gives

```text
O(sum_(q<=q0)q + (D/A0)sum_(q<=q0)1/q)
 =O(q0^2+(D/A0)log q0)
 =O((D/A0)X^epsilon).                             (4)
```

After restoring collision multiplicity `M`, (4) becomes

```text
M D/A0 = DQ/(KM).                                 (5)
```

Its exponent is `14/15-xi-mu`, below the target `1/3` by

```text
xi+mu-3/5>=1/25.                                  (6)
```

The broad range is nonempty and genuinely partial throughout the registered
low branch. Its ceiling has exponent

```text
7/15-xi/2-mu >= 7/300,                            (7)
```

while the ratio between the full denominator ceiling and `q0` has exponent

```text
xi/2-2/15 >=14/75.                                (8)
```

Thus the only remaining low-multiplicity denominators lie in the narrow-
cylinder range

```text
sqrt(DQ/(KM^2)) < q << Q/M.                       (9)
```

Closure of (9) requires endpoint discrepancy or an inverse relation between
distinct narrow cylinders; it is not supplied by total cylinder measure.
No full low-multiplicity or simple-root closure, complete moment, density
gain, or interval gain is proved.

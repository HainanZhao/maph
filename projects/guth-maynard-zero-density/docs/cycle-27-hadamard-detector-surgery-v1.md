# Cycle 27: Hadamard detector surgery

## Claim boundary

`PROVED`: equal-mass prime blocks admit an exact dichotomy between a large
signed detector orthogonal to the original coefficient direction and
simultaneous aligned largeness on every block. This supplies the algebraic
E10 conservation lemma and routes its exceptional case into E7. No bound for
the multiblock synchronized branch, full density saving, or interval result
is proved.

## Orthogonal signed detectors

Let `J` be a power of two and partition the prime coordinates into blocks
whose restricted coefficient vectors `b_j` are orthogonal with
`||b_j||^2=A/J`. This can be done by equal-cardinality grouping for the prime
atom, where every coefficient has the same modulus. Let `H=(h_(ell,j))` be a
Sylvester Hadamard matrix whose first row is all `+1`, and put

```text
b^(ell)=sum_j h_(ell,j)b_j.
```

Hadamard orthogonality gives

```text
<b^(ell),b^(m)>=A delta_(ell,m).
```

Thus every nonzero Hadamard row produces a coefficient vector exactly
orthogonal to the original detector `b^(0)` while preserving its norm and
coefficient magnitudes.

For one phase row `x`, write

```text
z_j=<x,b_j>,   S_ell=<x,b^(ell)>=sum_j h_(ell,j)z_j.
```

Parseval and deletion of the all-plus row give the exact identities

```text
sum_ell |S_ell|^2=J sum_j |z_j|^2,
sum_(ell>=1)|S_ell|^2=J sum_j |z_j-S_0/J|^2.
```

## Surgery-or-synchronization dichotomy

Assume `|S_0|>=V`. If

```text
sum_(ell>=1)|S_ell|^2 >= V^2/(16J),
```

then some nontrivial signed detector satisfies

```text
|S_ell| >= V/(4 sqrt(J(J-1))) >= V/(4J).
```

This detector is exactly orthogonal to the original resonant direction. If
the displayed energy inequality fails, then

```text
sum_j |z_j-S_0/J|^2 < V^2/(16J^2).
```

After rotating so that `S_0` is positive, every block consequently obeys

```text
|z_j-S_0/J| < V/(4J),
Re z_j > 3V/(4J).
```

Hence every block is simultaneously large with a common phase. When
`J=X^o(1)`, neither conclusion loses a fixed power.

## Gate effect

`PROVED`: E10 complementary detection is now automatic on every row with
nontrivial block variance; only the low-variance rows remain resonant. Those
rows carry aligned large values on all `J` prime blocks and are passed to E7
phase-code rigidity or E9 differencing. The next analytic theorem should
bound a separated set possessing this simultaneous multiblock alignment, not
revisit generic detector colouring.

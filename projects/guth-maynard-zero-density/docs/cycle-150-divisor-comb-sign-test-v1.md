# Cycle 150: strict endpoint combs cannot cancel one another

## Claim boundary

`PROVED`: on the modulus selected by Cycle 149, every other strict positive
endpoint mode contributes nonnegatively up to a power-negligible Poisson
error.  Therefore the negative anti-aligner cannot be another strict endpoint
population.  It must have a quantitatively large component in the halo,
denominator boundary, a different coefficient-phase chart, or nonsmooth
payload.

The escape component is not excluded or bounded above.  No full second
moment, endpoint, complete moment, density gain, or interval gain is proved.

## The sampled divisor-comb test

For the retained endpoint denominator `h`, put

```text
w_h(k)=Q 1_(h|k),       K<=k<=2K.                 (1)
```

Split the exact Cycle-149 complement as

```text
R=P+H,                                             (2)
```

where `P` contains every other mode having:

- a reduced endpoint approximation of denominator at most `QX^(-delta)`;
- error at most the strict constant times `(KQ)^(-1)`;
- a positive interior coefficient chart; and
- the same smooth length-`Q` coefficient symbol.

The residual `H` is defined exactly as the complement of this class.

On the support of (1), write `k=h ell`.  For a mode of `P` with endpoint
denominator `h_b`, Cycle 148 gives two cases:

```text
h_b|h ell:     Re S_b(h ell)>=cQ,
h_b not|h ell: S_b(h ell)<<_J Q(Q/h_b)^(-J).      (3)
```

Since `h_b<=QX^(-delta)`, choose fixed `J` large enough to absorb all modes.
Summing (3) proves

```text
Re <P,w_h> >=-X^(-A)                              (4)
```

relative to every registered power-scale witness.  In particular, strict
positive endpoint combs reinforce rather than anti-align with one another.

## Forced escape correlation and norm

Suppose Cycle 149 gives

```text
Re <R,w_h><=-M.                                   (5)
```

Writing the negligible bound in (4) as `eta`, equations (2), (4), and (5)
give

```text
Re <H,w_h><=-(M-eta).                             (6)
```

Moreover,

```text
||w_h||_2 asy Q sqrt(K/h),                        (7)
```

so Cauchy--Schwarz forces

```text
||H||_2 >= (M-eta)/(Q sqrt(K/h)).                 (8)
```

With bounded endpoint weights, insertion of the Cycle-149 modulus witness
puts (8) at the one-ray scale

```text
||H||_2^2 >> KQ^2/N,       h~N,                   (9)
```

again a factor `Q/N` above one-mode diagonal energy `KQ`.

## Exhaustive scoped escape classes

Relative to the definition of `P`, every negative anti-aligner belongs to at
least one of:

1. `HALO`: endpoint error larger than the strict `c/(KQ)` core;
2. `BOUNDARY_DENOMINATOR`: reduced denominator within a fixed power of `Q`,
   where nonmultiple Poisson decay is no longer power-saving;
3. `PHASE_CHANGE`: coefficient phase leaves the positive chart; or
4. `NONSMOOTH_PAYLOAD`: the actual coefficient symbol was not transported
   into the smooth Poisson model.

This list is exhaustive only within the frozen smooth endpoint decomposition.
It is not a theorem that any class is small.

## Structural consequence

The lower-band problem has narrowed from arbitrary cross-endpoint
cancellation to four explicit anti-aligner classes, each carrying a
quantified negative divisor-comb correlation and the norm obligation (8).
The next step should attack `HALO` and `BOUNDARY_DENOMINATOR` together using
the exact core--halo kernel; coefficient-phase and nonsmooth payload remain a
separate bridge.

## Gate effect

The gate becomes `HALO_BOUNDARY_DIVISOR_COMB_ESTIMATE_OPEN`.

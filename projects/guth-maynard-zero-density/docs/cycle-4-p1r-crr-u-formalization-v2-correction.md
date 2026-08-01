# Cycle 4 P1R-CRR-U formalization v2 correction

## Claim boundary and correction

`OBSERVED`: hostile audit v1 rejected formalization v1.  Version 1 remains
immutable and `CONTAINED_FAIL`.  This version corrects only its slack
bookkeeping and phase label; it does not prove CRR-U, construct a witness,
improve zero density or short intervals, establish method saturation, or
authorize a computational search.

The v1 witness class is deliberately retained rather than narrowed to exact
constant-factor bands.  For integer `v>=3`, let

```text
delta=delta(v)=1/sqrt(log v).
```

All expressions below of the form `a+b*delta` are exact exponents of `v`,
not asymptotic abbreviations.  Their constant terms are the critical central
exponents, and their delta coefficients record the admitted subpower slack.

## Preserved witness definition

The functions, Fourier sign, scales, Base(v), RationalMass(v), and
PositiveCubic(v) are exactly those in v1, except that their consequences are
now stated with the correct slack.  One common pair `(b,W)` must still satisfy
all three blocks.  In particular,

```text
L=v^10,
v^(8-delta)<=|W|<=v^(8+delta),
|D_v(t)|>=v^(7-delta),
v^(20-delta)<=E(W)<=v^(20+delta).
```

The source parameter corresponding to the admitted pointwise threshold is
therefore

```text
sigma_v=7/10-delta/10,
```

not exactly `7/10` at finite `v`.

## Corrected exact source-bound bookkeeping

`PROVED`: direct substitution of `sigma_v` and the upper cardinality edge
`8+delta` into the pinned Guth--Maynard upper bounds yields:

```text
large-values upper rows:
  6+2*delta, 8+4*delta, 8+4*delta;

energy upper rows:
  20+5*delta, 20+(37/8)*delta, 20+5*delta;

four-term S3 upper rows:
  36+(3/2)*delta, 36+3*delta,
  36+3*delta, 36+(45/16)*delta.
```

The range check remains `L=H^(5/6)>=H^(3/4)`.  Each row has the same
constant term as the earlier critical tie, but none is promoted as an exact
finite-`v` tie.

`PROVED`: the RationalMass(v) lower predicate gives

```text
integral f >= v^(8-3*delta),
integral f^2 >= v^(20-5*delta),
```

for `f=|Rtilde_W|^2` (with an optional fixed compact cutoff equal to one on
the rational net).  After inserting `M=v^2`, its two induced affine lower
scales are `28-6*delta` and `28-5*delta`.  In contrast, the source moment
upper bounds together with the upper Base bands give affine upper scales
`28+2*delta` and `28+delta`.  Thus the rational configuration is
leading-exponent compatible but no exact finite-`v` equality or contradiction
is asserted.

The arbitrary explicit `psi1,psi2` pair is not claimed to be the existential
pair selected in Guth--Maynard Proposition `prpstn:S3Expansion`; therefore
the smoothed clause of their Lemma `RL4` is not invoked literally.  Instead,
put `A=integral psi1>0` and `F=Rtilde_W^2`.  Direct Fubini and weighted
Cauchy--Schwarz give

```text
integral F=A*integral psi2*|R_W|^2,
integral F^2<=A^2*integral psi2^2*|R_W|^4.
```

The published raw-`R` `L2`/`L4` arguments apply to the fixed compact support
of `psi2`, giving `integral F << |W|` and
`integral F^2 lessapprox E(W)`.  This fresh two-line reduction, rather than an
unverified identification of bump pairs, supplies the upper moment rows.

`PROVED`: because `delta(v)->0`, the constant terms recover the central
lists `[6,8,8]`, `[20,20,20]`, `[36,36,36,36]`, rational moments
`[8,20]`, and affine scales `[28,28]`.  This is a limit statement about
exponent bookkeeping, not a common-family construction or sharpness proof.

## Corrected phase identity

For real `w` and

```text
hat(f)(xi)=integral f(u)exp(-2*pi*i*xi*u)du,
```

one has

```text
conjugate(hat(h_a)(mL))=hat(h_(-a))(-mL).
```

Expanding `I_m`, reversing `t2` and `t3`, and commuting the three scalar
factors gives the exact labeled identity

```text
conjugate(I_(m1,m2,m3))=I_(-m3,-m2,-m1).
```

The map `(m1,m2,m3)->(-m3,-m2,-m1)` is an involutive bijection of the
all-nonzero-coordinate lattice.  Absolute convergence therefore permits
reindexing and proves that the aggregate `S3_signed` is real.  No individual
summand is asserted to be nonnegative.

## Gate and authorized work

CRR-U remains `CONJECTURED`:

```text
there exists v0 such that no common-pair witness exists for integer v>=v0.
```

An unbounded witness sequence falsifies it; a finite witness does not.
Formalization v2 is analytic-only: row cap `0`, no RNG, no candidate rows,
and no certification margin.  Discovery remains prohibited.  A later search
requires a new preregistration freezing all families, ranges, resources,
failed-row rules, seeds, and rigorous retention margins.

The mathematical obligations remain the Base hypotheses, both energy bounds,
rational mass, cubic convergence/reality/sign/size, all slack uniformity, and
independent proof routes.  The displayed compatible upper and lower exponent
bands alone prove neither compatibility nor incompatibility.

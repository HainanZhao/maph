# Cycle 6 actual-log spectral probe v1: preregistration

## Claim boundary

`CONJECTURED`: this is a bounded discovery experiment designed to test the
new capped leading-eigenvector/minimum-value construction mechanism.  It is
not a CRR witness test: it uses the literal exponent relations at `v=2`, far
below the `v>=8` geometry regime, and replaces continuous smoothing by a
three-node bounded-jitter quadrature.  A retained row is only `OBSERVED`; its
floating-point complex diagnostics are `RECOGNIZED`.  No outcome proves or
refutes AFARI, FARI, CRR-U, a density estimate, or a short-interval result.

Unlike the earlier finite additive-group probe, every row uses:

```text
D_b(t)=sum_(L<n<2L) w(n/L)b_n n^(it),
R_W((r/s)exp(theta/H)),
```

with literal reduced Farey pairs, literal plateau-ray counts, and one common
pair `(b,W)` per row.

## Frozen finite scales and labels

```text
v=2, H=4096, L=1024, R=256, Q=16,
central value V=v^7=128, raw Farey amplitude v^6=64.
```

The coefficient support is the exact integer set `L<n<2L`, with the frozen
smooth CRR weight.  The Farey shell is

```text
gcd(r,s)=1, Q<=r,s<2Q, 3/4<=r/s<=5/4,
theta in {-3,0,3},
K_(r,s)={k:6L/5<=rk,sk<=9L/5}.
```

The discrete actual-Farey score is exactly

```text
A_disc(W)=sum_(r,s,theta) #K_(r,s)
          |R_W((r/s)exp(theta/H))|^2.
```

It is the labelled cross-Gram sum at the frozen theta nodes by the inherited
identity `C_theta(sk,rk)=R_W((r/s)exp(theta/H))`.  It is *not* a substitute
for `RationalMass(v)` or the averaged integral `A_v(W)`.

## Three deterministic rows

No RNG is used.  First construct the literal Farey feature matrix `U` whose
columns are `sqrt(#K_(r,s))*x^(it)` at the frozen labels.  A 32-step
positive-semidefinite power iteration on `U*U`, started from the normalized
all-ones vector, produces a Farey spectral score on every `0<=t<H`.
Selection takes the sixteen score leaders in each of sixteen equal
macrocells, with gap at least two.  This creates the initial common set.

For a fixed `W`, form its actual Dirichlet matrix and calculate a numerical
top left singular vector.  Its capped phase lift is `b_n=x_n/|x_n|`.
The row-reweighted minimum-value iteration then repeats sixteen times:

```text
z_t=phase((M_W b)_t),
p_t proportional to 1/max(|(M_W b)_t|,2^(-40)),
b <- phase(M_W^*(p z)).
```

For a fixed `p,z`, this coordinate update cannot decrease the corresponding
weighted linear phase functional.  Because `p` changes between iterations,
the protocol makes no global monotonicity claim.

The sole rows, in order, are:

1. `F0-farey-leading-phase`: initial `W`, capped top-eigenvector phase only.
2. `F1-farey-leading-minimum`: initial `W`, then sixteen row-reweighted
   phase updates.
3. `F2-joint-reselection-minimum`: two outer rounds of the preceding
   minimum-value update followed by a fresh stratified selector using the
   fixed equal-weight sum of normalized Farey and `|D_b(t)|` scores; then the
   final sixteen phase updates.

Every row reports its final same-pair coefficient cap, exact tolerance-one
energy, minimum row value, Farey score, and the `rho`/`phi` leading-phase
diagnostics.  It never transfers a coefficient or a set from another row.

## Retention and resources

The protocol records all three rows exactly once.  A row receives
`OBSERVED_JOINT_PROXY_HIT` iff all following pre-result diagnostic gates hold:

```text
max_n |b_n|<=1+2^(-40),
min_t |D_b(t)|>=128,
R^4/(4H)<=E_1(W)<=4R^4/H,
at least 1/8 of frozen (r,s,theta) labels have |R_W|>=64,
the leading-phase sufficient-certificate lower root is at least 128.
```

Otherwise it receives `NO_RETAINED_HIT` and retains every gate value.  A
miss is not a negative statement about the continuous construction.  The
wall cap is 600 seconds and RSS cap is 1 GiB; a cap retains the active row as
`RESOURCE_CAP` and later rows as `GLOBAL_CAP_UNREACHED`, without retry or
parameter change.

The runtime is pinned to CPython 3.12.3, NumPy 1.26.4, non-optimized mode.
All numerical diagnostics are binary64/complex128 and are `RECOGNIZED`, not
interval certificates.  Exact energy and integer ray labels are separately
recorded as exact arithmetic.

## Replay boundary

The preregistration builder seals only this protocol.  The runner, after
this artifact exists, executes it once and writes a distinct discovery
artifact.  Its `--check` recomputes semantic fields but does not reinterpret a
row or change any budget, threshold, label, or selection rule.

```sh
python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v1.py --write
python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v1.py --check
python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --write
```

# Cycle 6 CRR actual-log/Farey RFDI outlier surgery v2 correction

## Correction record and claim boundary

`PROVED`: this is a versioned replay correction, not a rewrite of v1. The v1
artifact remains byte-for-byte preserved:

```text
cycle-6-crr-rfdi-outlier-surgery-v1.json
SHA-256 0bd2843123957ed045b1feae389467030066f572f65914032955fc4cb90bc351.
```

After that artifact was sealed, its convention, document, and builder were
edited to clarify (i) that the normalized pinned bumps give
`0<=psi1,psi2<=1`, and (ii) that the deletion failure applies in particular
to every fixed `ell+r+2s<2` budget. Those post-seal edits changed the v1
input hashes, so v1 replay correctly rejects its current inputs. No v1
artifact bytes were changed. This v2 artifact independently pins the
post-mutation v1 ledger and its own document, convention, builder, and tests.

`PROVED`: v2 re-seals the same conditional actual-log/Farey outlier-surgery
theorem below. `CONJECTURED`: the required core is not constructed. Thus
neither v1 nor v2 refutes RFDI, proves a full Base/RationalMass/PositiveCubic
common witness, proves the capped Base value condition after surgery, or
proves AFARI/FARI/CFARI, a cubic estimate, a density or short-interval gain,
a saturation theorem, or an L-function result.

## Conditional actual-row surgery theorem

Use the frozen scales

```text
H=v^12, L=v^10, R=v^8, Q=v^4,
delta(v)=1/sqrt(log v),
M_A(t,n)=w(n/L)n^(it), G_A=M_A M_A^*.
```

Fix `0<g<=1`, `epsilon>0`, and fixed nonnegative `ell,r,s` with
`ell+r+2s<2`. Suppose a core `A` exists with `|A|=R-1` and:

```text
A subset [0,H/4] is H^(1/100)-separated;
v^(20-delta)<=E(A)<=v^(20+delta)-(4R-3);
lambda_1(G_A)=Lambda,
lambda_2(G_A)<=(1-g)Lambda,
Lambda>=v^(12-ell*delta),
S_L+sqrt(Lambda*S_L)<=gLambda/2.                         (1)
```

Here `S_L=sum_(L<n<2L)w(n/L)^2<=L`. Assume also that on a frozen rational
set `E` of measure at least `v^(-4-delta)`, the *same* RationalMass smoothing

```text
F_A(u)=H integral psi1(H(u-u'))psi2(u')|R_A(u')|^2du'
```

satisfies

```text
F_A(u)>=(1+epsilon)v^(12-2delta).                        (2)
```

This is a conditional core hypothesis. Its existence is not claimed.

### `PROVED`: preservation on one common actual set

Let `I=[3H/4,H]`. For every `tau in I`, the pair-sum classes
`A+A`, `tau+A=A+tau`, and `{2tau}` are mutually farther than one apart.
Consequently the ordered tolerance-one energy is exactly

```text
E(A union {tau})=E(A)+4|A|+1=E(A)+4R-3.                  (3)
```

Thus the interior core band in (1) gives the frozen energy band after adding
the actual row; separation and cardinality are immediate.

The pinned normalized bump formulas give `0<=psi1,psi2<=1`, while
`supp(psi1) subset [-1,1]`. Hence

```text
J(u)=H integral psi1(H(u-u'))psi2(u')du'<=2,
F_(A union {tau})(u)>=F_A(u)-2sqrt(2F_A(u)).             (4)
```

If `v^(12-2delta)>=max(2,8(1+epsilon)/epsilon^2)`, (2) and (4) show that
the same `E` establishes frozen RationalMass for the enlarged `W`.

The Farey object is also unchanged in kind:

```text
(K_F)_(t,s)=sum_(a in F_Q) integral_(-3)^3
              (a exp(theta/H))^(i(t-s))dtheta,
C_theta(sk,rk)=R_W((r/s)exp(theta/H)).                  (5)
```

This is one common actual `W=A union {tau}` throughout. No generic Gram
model, replacement set, rational-cell choice, or post-selection jitter is
introduced.

### `PROVED`: actual-log selection and small deletion coverage

Let `u_A` be a unit top eigenvector of `G_A` and let
`x=M_A^*u_A/sqrt(Lambda)`. Directly from the actual rows,

```text
u_A^*G_(A,tau)=sqrt(Lambda) D_c(tau),
D_c(tau)=sum_(L<n<2L) conjugate(x_n)w(n/L)n^(-i tau),
sum|c_n|^2<=1.                                          (6)
```

The elementary integral and harmonic estimates give

```text
(1/|I|) integral_I |D_c(tau)|^2dtau
 <= C_v:=1+32L(1+log L)/H.                               (7)
```

Choose `tau in I` with `|D_c(tau)|^2<=C_v`. At `v>=64`,
`log v<=sqrt(v)` and `L/H=v^(-2)` give `C_v<=2`.

Writing the enlarged actual Gram matrix in the `u_A`-plus-complement block
form, (1) implies that its complement block has norm at most
`Lambda-gLambda/2`. Therefore every unit top eigenvector `u_W` obeys

```text
|u_W(tau)|^2<=4C_v/(g^2Lambda).
```

The prior exact actual-log row-deletion inequality then gives

```text
DelCov(W)<=mu_top(W)<=4RC_v/(g^2Lambda)
        <=8g^(-2)v^(-4+ell delta(v)).                    (8)
```

For any fixed `g,ell,r,s` with `ell+r+2s<2`, the last expression is below
`v^(-2s delta(v))` for all sufficiently large `v`. Hence the enlarged actual
`W` violates the deletion half of `RFDI_(s,kappa)` for every fixed `kappa`.

## Exact implication and open route

`PROVED`, conditional on (1)--(2): scalar set conditions that survive the
surgery—separation, cardinality, energy, RationalMass, the actual logarithmic
matrix lower-eigenvalue scale, and actual Farey labels—do not force the
row-deletion RFDI lower bound. A successful RFDI proof must use genuinely
all-row log/Farey structure, exclude such isolated cores, or exploit the
non-hereditary common-coefficient/pointwise part of Base.

`CONJECTURED`: whether a core satisfying (1)--(2) exists. Showing that it
cannot exist would be a new structural incompatibility theorem, not a
refutation of this conditional surgery lemma.

## Replay

```sh
python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v2.py --write
python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v2.py --check
python3 -m unittest tests/test_cycle_6_crr_rfdi_outlier_surgery_v2.py
```

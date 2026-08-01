# Cycle 6 CRR CFARI phase-equivalence reduction v1

## Claim boundary

`PROVED`: on the frozen CRR Base class, the coefficient phase factor in
CFARI has the two-sided power-scale enclosure

```text
v^(20-4 delta(v)) <= a^* G_W a
                 <= C v^(20+delta(v)) (1+log(2L)).       (1)
```

Here `C` is absolute for the fixed smooth weight.  Consequently, at the
level of any fixed power saving, `CFARI_eta` and the averaged actual-Farey
target `AFARI_eta` are equivalent: each implies the other with (for example)
half of the saving.  The coefficient-phase product is therefore not a new,
strictly stronger power-scale obstruction than AFARI.

`PROVED`: the exact four-linear expansion of the CFARI product factorizes as
a tensor product before an additional mixed estimate is supplied.  The
Schur/Hadamard product gives a valid diagonal mixed kernel, but it does not
by itself bound that tensor-product norm.

`CONJECTURED`: AFARI, CFARI, and the local fourth-moment saving stated below
remain open.  This note neither proves nor refutes any of them, CRR-U, a
common Base-plus-RationalMass witness, a positive cubic estimate, a density
gain, a short-interval theorem, a method-saturation theorem, or an L-function
extension.  It is a reduction/no-go for treating the phase factor as an
independent fixed-power source of saving.

## Frozen objects

Use the CRR-v2 scales

```text
H=v^12,  L=v^10,  Q=v^4,  R=v^8,
delta(v)=1/sqrt(log v),
```

and the actual reduced Farey kernel from Cycle 6:

```text
(K_F)_(t,t')=
  sum_((r,s) in F_Q) integral_(-3)^3
  ((r/s) exp(theta/H))^(i(t-t')) dtheta,
Mcal_v(W)=1^*K_F 1.
```

The labelled plateau-ray comparison is

```text
(L/(20Q)) Mcal_v(W) <= A_v(W) <= (2L/Q) Mcal_v(W).       (2)
```

For a common Base pair `(b,W)`, put

```text
M_W(t,n)=w(n/L)n^(it),
G_W=M_W M_W^*,
D_v=M_W b,
a_t=D_v(t)/|D_v(t)|.
```

The Base pointwise condition makes every `a_t` defined.  It also gives the
phase-Rayleigh lower bound already sealed in the preceding coefficient-Farey
reduction:

```text
a^*G_W a >= v^(20-4 delta(v)).                           (3)
```

Define, for fixed positive `eta`,

```text
AFARI_eta: A_v(W) <= v^(26-eta)

CFARI_eta: (a^*G_W a) Mcal_v(W) <= v^(40-eta).
```

The quantifiers are the existing ones: all sufficiently large `v`, every
Base-admissible common pair `(b,W)`, and the actual reduced labels in `F_Q`.
No replacement of `log(r/s)` by a generic alias or an additive rational
phase occurs below.

## `PROVED`: sampled mean-value upper bound for the phase factor

The classical Dirichlet-polynomial mean-value estimate, in its standard
coefficient-ℓ2 form, says that for `c_n` supported on `L<n<2L`,

```text
integral_J |sum_n c_n n^(iu)|^2 du
 <= C_0 (|J|+L) sum_n |c_n|^2.                           (4)
```

The relevant primary-source anchor is Guth--Maynard,
`LargevaluesDirichlet17.tex`: their introduction records the simple
orthogonality estimate at lines 217--225, and their matrix discussion at
lines 320--333 explicitly identifies the mean-value bound
`||M_W|| << T^(1/2)` in the same Dirichlet matrix setup.  The following
short sampling argument checks the translation to our frozen `M_W` and
retains a harmless logarithm.

Let `f(u)=sum_n c_n n^(iu)` and let `I_t=[t-1/2,t+1/2]`.  Base separation is
at least `H^(1/100)>1`, so the `I_t` are disjoint.  The fundamental theorem
of calculus, averaged over `I_t`, gives

```text
|f(t)|^2 <= integral_(I_t)|f(u)|^2du
            + integral_(I_t)|(|f(u)|^2)'|du.
```

Summing and applying Cauchy--Schwarz on
`J=[-1/2,H+1/2]` gives

```text
sum_(t in W)|f(t)|^2
 <= integral_J |f|^2 + 2 (integral_J|f|^2)^(1/2)
                         (integral_J|f'|^2)^(1/2).
```

Apply (4) to `f` and to `f'`, whose coefficients are `c_n log n`.  Since
`log n<=log(2L)` on the support,

```text
sum_(t in W)|f(t)|^2
 <= C_1 (H+L)(1+log(2L)) sum_n|c_n|^2.                   (5)
```

This is an operator-norm statement, valid for arbitrary complex `c`, not
only for the Base coefficient vector.  Inserting the fixed weight
`0<=w<=1` in `c_n` therefore proves

```text
||M_W||_op^2 <= C_1(H+L)(1+log(2L)).                     (6)
```

For the Base phase, `||a||_2^2=|W|<=v^(8+delta(v))` and `H>L`; hence

```text
a^*G_Wa <= 2C_1 v^(20+delta(v))(1+log(2L)),              (7)
```

which with (3) proves (1).  The upper bound uses no RationalMass, energy,
or cubic predicate.  The lower bound uses the same `b`, same `W`, and phase
as CFARI.  Since

```text
delta(v) log v=sqrt(log v),
log log(2L)=o(log v),
```

the factor on the right of (7) is `v^(20+o(1))` in the only sense used by
the fixed-power statements below.

## `PROVED`: CFARI and AFARI are fixed-power equivalent

First, (2) gives the elementary conversion

```text
AFARI_eta  =>  Mcal_v(W) <= 20 v^(20-eta),               (8)
Mcal_v(W) <= v^(20-eta)  =>  A_v(W) <= 2v^(26-eta).      (9)
```

If `CFARI_eta` holds, divide by (3):

```text
Mcal_v(W) <= v^(20-eta+4delta(v)).                       (10)
```

For sufficiently large `v`, this and (9), including its fixed factor two,
give `AFARI_(eta/2)`.

Conversely, if `AFARI_eta` holds, insert (8) into (7):

```text
(a^*G_Wa)Mcal_v(W)
 <= 40C_1(1+log(2L))v^(40-eta+delta(v)).                 (11)
```

For sufficiently large `v`, the subpower factor in (11) is at most
`v^(eta/2)`.  This is `CFARI_(eta/2)`.

Thus the two existential fixed-saving assertions are equivalent:

```text
(exists eta>0 CFARI_eta)  <=>  (exists eta>0 AFARI_eta). (12)
```

The implication retains all actual Farey labels through (2).  It does not
say that a proof must look scalar; it says that any eventual CFARI proof is
also, quantitatively, an AFARI proof, and vice versa.  In particular, the
phase lift cannot be advertised as an additional power-scale gate unless it
supplies a genuinely new way to establish the same restricted Farey saving.

## Exact tensor and Schur identities

Let `Omega=F_Q x [-3,3]` with counting measure in the first coordinate and
Lebesgue measure in the second, and set

```text
xi_(r,s,theta)=(r/s) exp(theta/H).
```

Define the actual-Farey analysis operator

```text
(F_W x)(r,s,theta)=sum_(t in W) x_t xi_(r,s,theta)^(-it).
```

Then `F_W^*F_W=K_F` (up to the harmless conjugate convention) and exactly

```text
Mcal_v(W)=||F_W 1||_2^2,
a^*G_Wa=||M_W^*a||_2^2,

(a^*G_Wa) Mcal_v(W)
 = ||(M_W^*a) tensor (F_W 1)||_2^2.                      (13)
```

Expanding (13) is a four-row/four-frequency sum, but its `(t_1,t_2)` and
`(s_1,s_2)` pairs are independent:

```text
sum_(n,(r,s),theta) w(n/L)^2
  [sum_(t1,t2) a_t1 conjugate(a_t2) n^(-i(t1-t2))]
  [sum_(s1,s2) xi^(i(s1-s2))].                           (14)
```

The condition that `a` is the phase of `M_W b` concerns only the first
bracket.  Thus (14) has no automatic diagonal reduction from that condition.

There is nevertheless an exact labelled Schur product:

```text
(G_W circ K_F)_(t,t')
 = sum_(n,(r,s),theta) w(n/L)^2
   (n xi_(r,s,theta))^(i(t-t')).                         (15)
```

It is positive semidefinite because it is the Gram kernel of the product
frequencies `n*xi`.  Equation (15) is a legitimate candidate for a future
mixed trace or restricted large-sieve argument.  `PROVED`: it is not equal
to the tensor product in (13); it retains only the diagonal row label.
Therefore no Schur-product identity alone turns (15) into the fixed-power
upper bound in CFARI.  A new inequality relating the tensor and diagonal
objects would be a substantive analytic input, not an algebraic consequence
of Base.

## The least currently isolated extra energy condition

Cycle 6 already isolated the actual-Farey local fourth-moment target

```text
F4F_zeta:
  integral_(U_v) |R_W(u)|^4 du <= v^(20-zeta)
```

for fixed `zeta>0` and all Base-admissible `W`.  Within the existing
Cauchy/actual-Farey route, this is the least non-tautological extra condition
currently identified: the exact Jacobian and window measure give

```text
Mcal_v(W) <= 8 Q H^(1/2)
                (integral_(U_v)|R_W(u)|^4du)^(1/2)
             <= 8 v^(20-zeta/2).                        (16)
```

Combining (7), (16), and subpower absorption gives `CFARI_(zeta/3)` for
sufficiently large `v`.  Conversely, RationalMass forces a local fourth
moment at central exponent `20-o(1)`, so an `F4F_zeta` saving would exclude
RationalMass in the required way.

This is not claimed to be a logically weakest possible hypothesis.  It is
the weakest presently isolated energy/Farey input in this Cauchy chain.  The
frozen PositiveCubic predicate supplies no proven relation to the Base phase
`a` or to (15); using it to improve CFARI requires a new explicit mixed-trace
bridge.

## Literature boundary: classical Farey large-sieve spectra

`PROVED` as a source-scope comparison: Boca--Radziwill,
*Limiting distribution of eigenvalues in the large sieve matrix*,
arXiv:1609.05843, Introduction (read 2026-08-01), studies the additive
matrix `e(n a/q)` on the complete Farey set `q<=Q`, with integer coefficient
index `n<=N` in the regime `N asymp Q^2`.  It proves convergence of
normalized eigenvalue moments.  Ramaré's 2007 paper studies the same
additive Farey form and notes that its uniform point weights are essential.

`OBSERVED`: our kernel has `xi^(it)=exp(i t log(r/s)+...)`, arbitrary real
rows `W subset [0,H]` with `H=Q^3`, and bounded logarithmic jitter.  It is
not the additive Farey matrix under the hypotheses of those results; their
moment theorem supplies neither a bound for the all-ones direction of
`K_F` nor a joint estimate with `G_W` and the Base phase.  It can motivate a
new log-Farey moment calculation, but is not imported as a theorem here.

## Consequence for CRR-U and falsifiers

`PROVED`: this reduction does not advance the truth status of CRR-U.  It
eliminates only the prospect that the displayed CFARI product is an
independent power-scale refinement of AFARI.  A proof of either target would
still imply CRR-U through the sealed averaged-jitter reduction.

This note would be refuted by a failure of the sampled mean-value estimate,
the Base phase lower bound, either labeled ray comparison in (2), or any
identity in (13)--(15).  An AFARI proof immediately produces CFARI by (11);
a CFARI proof immediately produces AFARI by (10).  A common asymptotic
Base-plus-RationalMass family refutes both covering fixed-saving targets.

## Replay

```sh
python3 proof/build_cycle_6_crr_cafari_phase_equivalence_v1.py --write
python3 proof/build_cycle_6_crr_cafari_phase_equivalence_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_cafari_phase_equivalence_v1.py
```

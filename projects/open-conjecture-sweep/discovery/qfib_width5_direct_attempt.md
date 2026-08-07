# Width-five q-Fibonomial direct attempt

Opened: 2026-08-07 UTC, after W0 closed.

Status at opening: candidate lemmas below are **CONJECTURED** until tested and
proved. This note records their pre-test form.

## W1.1 — Paper A kernel extracted from the manuscript

Paper A fixes `a=F_(m+1)`, `b=F_(m+2)` and writes the width-four polynomial
as

\[
W_{m,4}(q)=\frac{[a]_q[b]_q[a+b]_q[a+2b]_q}{[2]_q[3]_q}.
\]

The manuscript uses BCK polynomiality and nonnegativity plus q-reciprocity to
deduce that this quotient is a symmetric polynomial of degree
`3a+4b-7`. If `c_t` are its coefficients, symmetry reduces unimodality to
`c_t-c_(t-1)>=0` through the midpoint.

It then defines

\[
p_{123}(t)=[q^t]\frac1{(1-q)(1-q^2)(1-q^3)},
\]

with `p(t)=0` for negative `t`, and obtains the exact midpoint formula

\[
c_t-c_{t-1}=p(t)-p(t-a)-p(t-b)+p(t-(2a+b)).
\]

The required inputs separate as follows.

Part-set agnostic:

1. polynomiality, nonnegative coefficients, reciprocity, and midpoint
   reduction;
2. `(1-q)W` as a numerator inclusion--exclusion against one restricted-
   partition kernel;
3. cancellation of equal subset shifts before estimating;
4. `p(t)=0` for negative arguments and splitting at the surviving shifts;
5. monotonicity of a kernel containing part 1, via the injection that adds
   one part of size 1;
6. lower bounds for positive translates and upper bounds for negative
   translates;
7. exact treatment of the finite range below a uniform threshold.

Specific to parts `(1,2,3)` and width four:

1. the period-six quadratic formula for `p_123`;
2. its error interval of width `11/12`;
3. the four surviving shifts and their order below the midpoint;
4. the resulting concave quadratic and linear lower envelopes;
5. the threshold `a>=34`, equivalent to `m>=8` in the proof.

No bracket-cancellation injectivity is used. The only injection is the
coefficientwise proof that `p_123(t)` is nondecreasing.

## W1.2 — width-five candidate lemmas, frozen before tests

Put

\[
a=F_{m+1},\quad b=F_{m+2},\quad
(A_1,\ldots,A_5)=(a,b,a+b,a+2b,2a+3b),
\]

and let

\[
p(t)=[q^t]\frac1{(1-q)(1-q^2)(1-q^3)(1-q^5)},
\qquad p(t)=0\quad(t<0).
\]

### Candidate L1 — exact kernel quasipolynomial

For every `t>=0`,

\[
p(t)=\frac{t^3}{180}+\frac{11t^2}{120}+\frac{9t}{20}+\rho_{t\bmod30},
\]

where `rho_r` depends only on `r mod 30` and satisfies

\[
\frac{91}{360}\le\rho_r\le1.
\]

### Candidate L2 — six-translate midpoint identity

If `W_(m,5)(q)=sum c_t q^t`, its degree is `5a+7b-12`; for every `t` at or
below its midpoint,

\[
\begin{aligned}
c_t-c_{t-1}={}&p(t)-p(t-a)-p(t-b)+p(t-(2a+b))\\
&+p(t-(a+3b))-p(t-(2a+3b)).
\end{aligned}
\]

### Candidate L3 — uniform worst-error envelope

For every `m>=20`, split the midpoint interval at

```text
a, b, 2a+b, a+3b, 2a+3b.
```

On each interval, replace every positive occurrence of `p(x)` by

```text
x^3/180 + 11*x^2/120 + 9*x/20 + 91/360
```

and every negative occurrence by the same cubic plus `1`. The resulting
piecewise polynomial lower envelope is nonnegative throughout the interval.

### Candidate L4 — finite remainder

For `1<=m<=19`, every exact midpoint difference in Candidate L2 is
nonnegative.

## Falsifiers

- L1: any residue or exact partition count disagreeing with the formula or
  bounds;
- L2: any direct quotient coefficient difference disagreeing with the six
  translates;
- L3: a negative value of the frozen worst-error envelope for any
  `20<=m<=240`, any residue modulo 30, and any interval;
- L4: a negative exact midpoint difference for `1<=m<=19`.

An indispensable failed candidate is discarded. A repair gets at most the
pre-registered two-agent-day-equivalent effort before this method is killed.

## W1.2 test outcome

All four frozen candidates passed:

```text
{"L1_rho_max": "1", "L1_rho_min": "91/360", "L2_direct_quotient_rows": 8, "L2_symbolic_rows": 240, "L3_envelope_intervals": 1326, "L3_minimum": "91/360", "L3_minimum_location": 0, "L3_minimum_m": 20, "L4_cases": 19, "L4_minimum": 0, "status": "PASS"}
```

Replay: `python3 experiments/qfib_width5_candidate_lemmas.py`.

## W1.3 proof outcome

**PROVED.** In fact, Candidate L3 holds already for `m>=8`, where `a>=34`;
only `m=1,...,7` are needed as exact finite cases.

Write

\[
Q(x)=\frac{x^3}{180}+\frac{11x^2}{120}+\frac{9x}{20}.
\]

Candidate L1 gives `Q(x)+91/360 <= p(x) <= Q(x)+1`. On each interval in
Candidate L3, form `H` by using the lower error for positive translates and
the upper error for negative translates. Then the exact difference `g`
satisfies `g>=H`. Put `d=b-a>=1`. Straight differentiation gives the
following minima; every displayed numerator is `360` times the stated lower
bound.

| interval | behavior of `H` | lower-bound numerator |
| --- | --- | --- |
| `[0,a)` | increasing | `91` |
| `[a,b)` | increasing | `2a^3+33a^2+162a-269` |
| `[b,2a+b)` | increasing | `2a^3+6a^2d+33a^2+6ad^2+66ad+162a-629` |
| `[2a+b,a+3b)` | concave; right endpoint is smaller | `22a^3+30a^2d-33a^2+6ad^2-66ad-162a-538` |
| `[a+3b,2a+3b)` | decreasing | `3(2ab(a+b-11)-149)` |
| `[2a+3b,T]` | decreasing | `3(2ab-269)` |

For the third interval, `H'` is a concave quadratic and is positive at both
endpoints when `a>=34` and `b>a`; hence `H` is increasing. For the fourth,
`H` is concave. For the fifth, `H'` is convex and negative at both endpoints,
so `H` decreases. On the last interval `360H'=-12ab`; evaluating at the
continuous midpoint `(5a+7b-12)/2` gives the final lower bound, and the
integer midpoint can only be larger. All displayed quantities are positive
for `a>=34,d>=1`.

For `m=1,...,7`, exact symbolic evaluation gives minimum midpoint differences

```text
m:       1  2  3  4  5  6  7
minimum: 0  0  0  1  1  1  1
```

Symmetry therefore proves width-five q-Fibonomial unimodality for every
`m>=1`. W1 reaches Outcome A.

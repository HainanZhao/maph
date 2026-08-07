# Width-four q-Fibonomial unimodality

**Claim: `PROVED`.** For every integer `m >= 1`,

\[
W_m(q)=\left[\!\begin{matrix}m+4\\4\end{matrix}\!\right]_{\mathcal F}
=\frac{[F_{m+1}]_q[F_{m+2}]_q[F_{m+3}]_q[F_{m+4}]_q}{[2]_q[3]_q}
\]

is unimodal. This proves topic 3 of `GOAL.md`. The proof below is algebraic;
the small exact calculation is only the explicitly listed finite base range.

## Difference reduction

Set `a=F_(m+1)` and `b=F_(m+2)`. The four numerator lengths are

\[
a,\quad b,\quad a+b,\quad a+2b.
\]

The q-Fibonomial is a polynomial with nonnegative integer coefficients by the
path-domino tiling theorem of Bergeron--Ceballos--K\"ustner (as recalled in
Theorem 2.3 of Connelly--Ito--Martinez--Shevchenko--Yang). It is symmetric:
this also follows directly by replacing `q` by `q^{-1}` in the displayed
quotient. Its degree is

\[
D=3a+4b-7.
\]

It therefore suffices to prove that the coefficients of `(1-q)W_m(q)` are
nonnegative through `T=floor(D/2)`.

Let

\[
p(t)=[q^t]\frac1{(1-q)(1-q^2)(1-q^3)}
=\begin{cases}
\left\lfloor\dfrac{t^2+6t+12}{12}\right\rfloor,&t\ge0,\\
0,&t<0.
\end{cases}
\tag{1}
\]

The first equality counts solutions of `x+2y+3z=t`; the displayed closed
form is the standard period-six evaluation (and is directly checked by the
six possible residues of `t`). Since

\[
(1-q)W_m(q)=
\frac{(1-q^a)(1-q^b)(1-q^{a+b})(1-q^{a+2b})}
     {(1-q)(1-q^2)(1-q^3)},
\]

inclusion-exclusion gives, for `0 <= t <= T`,

\[
g(t):=[q^t](1-q)W_m(q)
=p(t)-p(t-a)-p(t-b)+p(t-(2a+b)).
\tag{2}
\]

Here is the cancellation in (2). Every triple shift is at least
`a+b+(a+b)=2a+2b>T`. Among pair shifts, `a+b` cancels the singleton
`a+b`, and `b+(a+b)=a+2b` cancels that singleton. The pair shifts
`a+(a+2b)=2a+2b`, `b+(a+2b)`, and `(a+b)+(a+2b)` exceed `T`; the only
possible remaining pair shift is `a+(a+b)=2a+b`.

## Uniform positivity for `m >= 8`

For `t >= 0`, (1) implies

\[
\frac{t^2+6t+1}{12}\le p(t)\le
\frac{t^2+6t+12}{12}.
\tag{3}
\]

For `0 <= t < a`, (2) gives `g(t)=p(t)>0`; for `a <= t < b`, it gives
`g(t)=p(t)-p(t-a)>=0` because `p` is nondecreasing.

For `b <= t < 2a+b`, the last term in (2) vanishes. By (3),

\[
12g(t)\ge K(t):=-t^2+(2a+2b-6)t-a^2-b^2+6a+6b-23.
\tag{4}
\]

`K` is concave. On `[b,2a+b-1]` its lower endpoint bound is

\[
K(b)=a(2b-a+6)-23,
\]

and its other endpoint is strictly larger than

\[
K(2a+b)=a(2b-a-6)-23.
\]

When `m>=8`, `a>=F_9=34` and `b>a`, so both displayed quantities are
strictly positive. Thus `g(t)>=0` in this range.

Finally, for `2a+b <= t <= T`, applying both sides of (3) to (2) yields

\[
12g(t)\ge L(t):=-2at+3a^2+4ab-6a-22.
\tag{5}
\]

The right side decreases with `t`. Since

\[
t\le T\le\frac{3a+4b-7}{2},
\]

equation (5) gives `12g(t)>=a-22>0` for `a>=34`. This completes every
case `m>=8`.

## The seven finite cases

For `m=1,...,7`, substitution into the exact formula (2), over the full
integer interval `0<=t<=floor(D/2)`, gives the following minima:

| `m` | `(a,b)` | `T` | `min g(t)` |
| --- | --- | ---: | ---: |
| 1 | `(1,2)` | 2 | 0 |
| 2 | `(2,3)` | 5 | 0 |
| 3 | `(3,5)` | 11 | 0 |
| 4 | `(5,8)` | 20 | 0 |
| 5 | `(8,13)` | 34 | 1 |
| 6 | `(13,21)` | 58 | 1 |
| 7 | `(21,34)` | 96 | 1 |

`proof/qfib_width4_unimodality_proof.py` evaluates exactly these finite
instances of (2). Consequently `g(t)>=0` from degree zero to the midpoint
for every `m>=1`; symmetry gives unimodality of `W_m(q)`.

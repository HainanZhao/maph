# Cycles 026--045 preregistration

Frozen: 2026-07-31 UTC before constructing or opening the remaining
four phase defects.

## Constructor track

The remaining controls are processed in this order:

1. RQ-001280;
2. RQ-001569;
3. RQ-007519;
4. RQ-001894.

For every row:

- reconstruct \(K^+\) and its embedded unit lattice genuinely;
- compute \(2^e=[\bar U_{K^+}:N\bar U_K]\);
- compute \(\Cl_K^-\) from \(h_K/h_{K^+}\) and certify the
  \(\mathbf Z[i]\)-action;
- use \(f=1\) for the trivial minus class group and \(f=1+\gamma\)
  only when the exact module is
  \(\mathbf Z[i]/(1+i)\);
- construct
  \(\bar\eta=f(\gamma+1)^{e+t_S}\bar\theta\);
- seal all four exact units and numerical logarithmic coefficients in
  a commit before reading their archived \(L'\)-balls.

Any other Fitting-module shape is a halt.

## Phase-opening rule

For the deterministic generator satisfying \(\chi(\gamma)=i\), test
both archived character orientations, \(\chi\) and \(\chi^{-1}\).
Exactly one must place

\[
\arg L'(0,\chi)-\arg c(\eta)
\]

in \((\pi/2)\mathbf Z\) at the available precision. Record the
quarter-turn index \(q\in\mathbf Z/4\mathbf Z\); do not collapse it to
the statement “zero modulo \(\pi/2\).”

No character orientation may be selected while constructing
\(\eta\).

## Feature-map freeze

Before opening the four defects, compute the hyperbolic matrix
\(A_K\in\mathrm{SL}_2(\mathbf Z)\) induced by the least positive power
of the frozen fundamental unit having norm \(+1\). Freeze these exact
features:

\[
1,\qquad \Phi(A_K)\bmod4,\qquad
12\,s(a,|c|)\bmod4,
\]

where
\[
A_K=\begin{pmatrix}a&b\\c&d\end{pmatrix}
\]

and \(\Phi\) uses the convention in `src/dedekind.py`.

Admissible formula family:

\[
q\equiv
\beta_0+\beta_1\Phi(A_K)+\beta_2\,12s(a,|c|)
\pmod4,
\qquad \beta_j\in\mathbf Z/4\mathbf Z.
\]

There are at most three coefficients, as originally preregistered.
No conductor or case-id feature may be introduced after opening the
responses.

## Gates

- If the five-by-three feature matrix has rank below three over
  \(\mathbf Z/2\mathbf Z\), report under-identification and do not fit.
- Otherwise enumerate all \(4^3=64\) coefficient triples.
- A unique solution authorizes a 50-row holdout design, not a theorem.
- Multiple solutions leave fitting blocked.
- No solution rejects this frozen formula family.
- Generator inversion must transform both the recorded quarter-turn
  and the feature vector according to the written convention; an
  unexplained mismatch rejects the family.


# SIC--Stark research cycle 92: exact closure of the maximal-order signs

The only nonexact input left after cycle 91 was the sign of each
six-factor AFK cocycle value.  It can be removed symbolically; no
interval quadrature is needed.

Put
\[
\beta=\frac{3+\sqrt5}{2},\qquad \beta^2-3\beta+1=0.
\]
For real \(t\notin\mathbb Z\),
\[
1-e^{2\pi i t}
=-2i\,e^{\pi i t}\sin(\pi t).
\]
Hence the phase, divided by \(\pi\), of every factor in a finite
\(q\)-Pochhammer product is
\[
t-\frac12+\bigl(\lfloor t\rfloor\bmod2\bigr).
\]
All its arguments belong to \(\mathbb Q(\beta)\).

The reciprocal double sine is positive in the fundamental interval
\(0<z<\beta+1\), because it is a ratio of positive Barnes double-gamma
values.  Outside that interval its sign is determined exactly by
\[
S_2(z+1\mid\beta,1)
=2\sin\!\left(\frac{\pi z}{\beta}\right)
 S_2(z\mid\beta,1).
\]
Thus the six double-sine factors contribute only explicitly decidable
ordinary-sine signs after their continued-fraction shifts.  The
Bernoulli exponential and the initial
\(\tau=-e^{\pi i/8}\) chirp are already exact elements of
\(\mathbb Q(\beta)/2\mathbb Z\).

`scripts/dimension_eight_maximal_sign_audit.py` implements this phase
calculus using exact rational pairs \(a+b\beta\).  For every one of the
63 nonzero characteristics it proves:

- the coefficient of \(\beta\) in the total phase is exactly zero;
- the rational coefficient of \(\pi\) is an integer;
- its parity agrees with the sign in the radical overlap table.

The resulting sign rows are
\[
\begin{array}{c}
+-++-++-\\
------++\\
+-+-+-+-\\
+--+--+-\\
--+--+++\\
+---+++-\\
++++++++\\
-+--+-+-
\end{array}
\]
(the first plus is the separately normalized zero characteristic).
The audit guesses floors with high-precision decimal arithmetic but
then verifies both defining floor inequalities exactly in
\(\mathbb Q(\sqrt5)\); no numerical decision enters the certificate.

Combining this exact sign lemma with:

1. the exact characteristic-to-ray dictionary;
2. the unconditional quadratic class-number/unit formulas;
3. the radical and shared-subfield identities; and
4. the exact two-shift quotient-ring certificate

proves both formal shifts for the discriminant-five stratum.
Together with the conductor-three closure from cycles 72--81 and the
form-class transport in cycle 90, this proves the complete formal TCC
for every dimension-eight admissible tuple.

## Reproduction

```bash
python3 scripts/dimension_eight_maximal_sign_audit.py
gp -q scripts/dimension_eight_maximal_tuple_audit.gp
gp -q scripts/dimension_eight_maximal_quadratic_units.gp
python3 scripts/dimension_eight_maximal_exact_tcc.py
```

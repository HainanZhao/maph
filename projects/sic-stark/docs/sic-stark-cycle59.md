# SIC--Stark research cycle 59: theorem schema and the d=8 orientation sieve

## Outcome

The reusable proof architecture from dimensions \(4,5,7\) has been
separated into six gates:

\[
\begin{array}{c}
\text{AFK/Kopp convention and conductor bridge}\\
\Downarrow\\
\text{powered algebraicity in a labeled ray field}\\
\Downarrow\\
\text{certified analytic-to-algebraic root identification}\\
\Downarrow\\
\text{Artin labels and phase/sign packet}\\
\Downarrow\\
\text{exact finite Weyl reconstruction}\\
\Downarrow\\
\text{both formal TCC shifts.}
\end{array}
\]

This changes the project ranking.  Dimension seven is now a closed
control, not the next candidate.  Dimension eight is the next exact
finite-TCC target, while dimension six remains the cleanest target for
a genuinely new analytic algebraicity theorem.

## Cross-dimensional gate table

\[
\begin{array}{c|c|c|c|c}
d&\text{character theorem}&\text{analytic bridge}
 &\text{exact packet}&\text{status}\\ \hline
4&\text{quadratic/class-number}&\checkmark&\checkmark&\text{closed}\\
5&\text{Shintani index two}&\checkmark&\checkmark&\text{closed}\\
6&\text{primitive order six}&\text{one scalar open}
 &\text{conditional exact}&\text{analytic boundary}\\
7&\text{Shintani index two}&\checkmark&\checkmark&\text{closed}\\
8&\text{quadratic plus cyclic quartic}&\text{two phases open}
 &\text{orientation selected numerically}&\text{finite target}
\end{array}
\]

The distinction between dimensions six and eight is important:

- \(d=6\) is mathematically smaller, but its remaining scalar is outside
  all presently applicable unconditional theorem families.
- \(d=8\) has two quartic phases, but the associated fields, units,
  regulator indices, ramification, Euler factors, and absolute values
  are already unconditional.  It therefore offers more exact finite
  work before a new analytic theorem is required.

## Discrete quartic orientation sieve

Roblot's cyclic-quartic theorem leaves the complex logarithmic
resolvents unoriented.  For each of the two quartic conjugate pairs, the
natural unit candidates admit eight discrete presentations:

\[
 z,\ iz,\ -z,\ -iz,\quad
 \bar z,\ i\bar z,\ -\bar z,\ -i\bar z.
\]

The script
`scripts/dimension_eight_orientation_sieve.gp` propagates all
\(8^2=64\) pairs through the convention-matched three-factor
conductor-lowering formula.  For each pair it produces the real
log-square values of all \(48\) primitive characteristics.

The Python companion inserts the \(15\) unaffected lower-conductor
values, reconstructs both \(8\times8\) Weyl matrices, and tests trace,
idempotency, and rank-two minors.  At threshold \(10^{-6}\):

\[
\boxed{\text{exactly one of the 64 discrete orientation pairs passes.}}
\]

The selected pair is the original PARI/Kopp orientation \((0,0)\), with
maximum numerical residual

\[
4.84\cdot10^{-11}.
\]

The second-best orientation has residual greater than \(0.43\), so the
separation is not numerical noise.

## Logical limitation

This sieve is not an unconditional analytic phase proof.

Roblot's theorem proves equality of absolute values of complex
resolvents.  Absolute-value equality alone does not prove that the
analytic resolvent differs from a selected unit resolvent by one of the
eight discrete Gaussian/conjugation operations; an arbitrary point on
the same circle is not excluded.

The result proves something narrower and still useful:

> Among the natural exact unit orientations supplied by the two
> cyclic-quartic fields, the finite TCC equations select a unique pair.

Consequently the exact algebraic packet should be built using this pair.
The remaining analytic theorem must then identify the two Shintani
resolvents with those selected oriented unit resolvents.

## Primitive squared-overlap field collapse

The \(48\) primitive characteristics form \(16\) Zauner orbits.  Their
baseline log-square values give the reciprocal relative polynomial

\[
\begin{aligned}
P_8(X)={}&X^{16}-(32+56\phi)X^{15}
 +(1668+2696\phi)X^{14}\\
&-(43656+70632\phi)X^{13}
 +(670940+1085616\phi)X^{12}\\
&-(6222872+10068808\phi)X^{11}
 +(34239444+55400584\phi)X^{10}\\
&-(104864752+169674744\phi)X^9
 +(158055290+255738816\phi)X^8+\cdots+1,
\end{aligned}
\]

where \(\phi=(1+\sqrt5)/2\), and the omitted coefficients are determined
by reciprocity.

The numerical coefficient recognition residuals are below
\(10^{-180}\).  After installing the recognized coefficients exactly:

\[
\deg_{\mathbf Q} P_8=32,
\]

the absolute polynomial is irreducible, and exact `nfisisom` identifies
its field with the one-place ray-\(24\) class field.

This is the dimension-eight analogue of the field collapse that unlocked
dimension seven.  The recognition step is not yet a proof of the
special-value identities; it supplies the exact candidate field and
polynomial for Sturm isolation, Artin labeling, and height rigidity.

The Sturm step is now also complete.  The absolute polynomial has
exactly \(16\) real roots, and disjoint rational intervals of width
\(10^{-6}\) isolate one root for every primitive Zauner representative.
The remaining \(16\) absolute conjugates form eight complex pairs, in
agreement with the signature of the one-place ray field.

## Exact Artin labels

The isolated roots are now labeled by the ray group rather than merely
matched as an unordered set.  The script
`scripts/dimension_eight_artin_labels.gp` fixes the positive embedding
of \(\phi\), isolates the distinguished \((0,1)\) root, and computes all
\(16\) automorphisms of the degree-\(32\) absolute field.  Local
Frobenius calculations identify ray generators at

\[
\mathfrak p_{31},\qquad \mathfrak p_{59},\qquad \mathfrak p_{71},
\]

with ray logs

\[
(1,0,0),\qquad(0,1,0),\qquad(0,0,1)
\]

in \(C_4\times C_2\times C_2\).  Acting with these generators sends the
distinguished root bijectively onto the \(16\) isolated characteristic
windows.  Hence every primitive squared overlap now has an exact Artin
label.

The Frobenius exponent is the norm of the prime ideal of
\(\mathbf Q(\sqrt5)\), not always the underlying rational prime.  This
matters for inert primes, whose exponent is \(p^2\); the certificate
uses split primes for the displayed generators and implements the
prime-ideal norm generally.

## One signed-overlap field

The primitive roots do not require sixteen independent square-root
extensions.  Let \(H\) be the degree-\(32\) ray field generated by the
distinguished primitive squared overlap \(h\).  Exact unit arithmetic
shows

\[
\frac{\sigma(h)}{h}\in H^{\times 2}
\qquad
(\sigma\in\operatorname{Gal}(H/K)).
\]

All sixteen square identities are verified directly.  On the other
hand, \(P_8(X^2)\) is irreducible: it has relative degree \(32\) over
\(K\) and absolute degree \(64\).  Therefore \(h\) is not already a
square in \(H\), but

\[
F=H(\sqrt h)
\]

contains every signed primitive overlap.

The four nontrivial lower-conductor absolute values are the real roots
of

\[
X^8-8X^7+12X^6+8X^5-22X^4
 +8X^3+12X^2-8X+1.
\]

This polynomial is irreducible, has exactly four real roots, and its
degree-eight field has four exact embeddings into \(F\).  Thus all
\(63\) nonexceptional overlap entries, including the \(15\)
lower-conductor entries, lie in the same degree-\(64\) field.

## Exact finite dimension-eight TCC

Composing \(F\) with the Weyl phase field
\(\mathbf Q(\zeta_{16})\) gives four convention choices because their
intersection has degree four.  The positive real cyclotomic embedding
selects a unique compatible component \(N\), with

\[
[N:\mathbf Q]=128.
\]

The script `scripts/dimension_eight_exact_tcc.gp` installs all \(64\)
overlaps in \(N\), fixes every primitive sign by the AFK phase, inserts
the four isolated lower-conductor roots, and reconstructs both formal
shifts.  Exact arithmetic gives, for each shift,

\[
\operatorname{Tr}\Pi=1,\qquad
\Pi^2=\Pi,\qquad
\text{all } \binom82^2=784 \text{ rank-two minors vanish}.
\]

Hence the selected algebraic packet satisfies both dimension-eight
finite TCC equations exactly.  This is a genuine finite-algebra
closure, not a floating-point residual.

It is not yet the unconditional analytic dimension-eight theorem.  The
recognized algebraic roots still have to be identified rigorously with
the convention-matched Shintani cocycle values.  In particular, the two
oriented cyclic-quartic identities remain outside Roblot's
absolute-value theorem.  The exact certificate proves that no further
finite obstruction remains once those analytic identifications are
made.

## Even-dimensional wrap phase

The second shift is now reconstructed correctly.  With

\[
 D_{p,q}=\tau^{pq}X^pZ^q,\qquad \tau=-e^{\pi i/8},
\]

complex conjugation gives

\[
 \overline{D_{p,q}}=\tau^{-pq}X^pZ^{-q}.
\]

For \(q\ne0\), replacing \(-q\) by its standard representative \(8-q\)
changes the displacement phase by

\[
 \tau^{8p}=(-1)^p.
\]

Thus the determinant-\(-1\) reconstruction must multiply the
\((p,q)\)-coefficient by \((-1)^p\) when \(q\ne0\).  With this wrap
factor, the selected packet gives the same \(4.84\cdot10^{-11}\)
maximum residual for both formal shifts.  The earlier \(0.2\)-scale
failure came exactly from omitting this factor.

## Recommended next round

1. Build the rigorous analytic/height bridge, leaving only the two
   genuinely oriented quartic identities if current theorems still stop
   at absolute values.
2. Certify the degree-eight lower-conductor root identifications with
   the same Arb/height method used in dimensions five and seven.
3. Turn the numerical coefficient recognition of \(P_8\) into a height
   rigidity lemma over \(\mathbf Q(\sqrt5)\).

In parallel, dimension six should be treated as a standalone analytic
theorem project:

\[
\exp(D_0/2)=x_{\mathrm{alg}}
\quad\text{for }K=\mathbf Q(\sqrt{21}),\ \mathfrak f=(6)\infty_1.
\]

That theorem would be more conceptually important, but the d=8 finite
closure is presently the more executable research step.

## Reproduction

```bash
python3 scripts/analyze_dimension_eight_orientation_sieve.py
gp -q scripts/dimension_eight_overlap_polynomial.gp
gp -q scripts/dimension_eight_root_isolation.gp
gp -q scripts/dimension_eight_artin_labels.gp
gp -q scripts/dimension_eight_square_root_lift.gp
gp -q scripts/dimension_eight_exact_tcc.gp
python3 -m unittest tests.test_higher_dimension_sieve
```

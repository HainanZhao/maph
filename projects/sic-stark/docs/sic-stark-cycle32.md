# SIC--Stark research cycle 32: the cyclic-limit route reopens

Date: 2026-07-27

> **Superseded warning.**  Cycle 33 found that Sections 4--5 below apply
> Kopp's rational Jacobi formula at excluded zero cyclic factors.  The
> resulting fractional exponents cannot be orders of a meromorphic
> characteristic cocycle.  The scalar identity-class approximation in
> Sections 1--3 remains valid, but the proposed full-table
> renormalization and tropical test do not.

## Outcome

The remaining dimension-six identity is still not proved, but this cycle
found a better attack and eliminated a plausible shortcut.

First, the primitive Hecke \(L\)-function cannot be transported to an
imaginary quadratic field by the Katayama--Kida coincidence theorem.
The normal closure of the one-infinite-place ray field is the
both-infinite-place ray field.  PARI/GP identifies its Galois group as

\[
 \operatorname{Gal}(N/\mathbb Q)
 \simeq \operatorname{SmallGroup}(24,8)
 \simeq C_3\rtimes D_4.
\]

The faithful quotient seen by the primitive order-six character is
\(D_6\), whose commutator has order \(3\).  It is therefore not isoclinic
to the Heisenberg group

\[
 \operatorname{He}_2\simeq D_4,
\]

whose commutator has order \(2\).  By Katayama--Kida's criterion, there is
no second quadratic induction producing the same faithful Artin
character.  The classical imaginary-quadratic/elliptic-unit proof of
Shintani's theorem is unavailable for an intrinsic reason, not merely
because a convenient field has not yet been found.

Second, Yalkinoglu's 2025 cyclic-quantum-dilogarithm formula supplies a
new route that was absent from the earlier pentagon audit.  It does not
replace the irrational real-multiplication parameter by a root of unity.
Instead, it approaches the real-multiplication fixed point through a
canonical sequence of rational points and expresses the limiting
Shintani factor as a limit of finite cyclic dilogarithms.

For dimension six this specializes exceptionally cleanly.

## 1. Exact rational geodesic

Put

\[
 \beta=\frac{5+\sqrt{21}}2,\qquad
 L=\begin{pmatrix}5&-1\\1&0\end{pmatrix},\qquad
 A=L^3.
\]

Define integers

\[
 T_0=2,\qquad T_1=5,\qquad
 T_{n+1}=5T_n-T_{n-1},
\]

and rational points

\[
 t_n=\frac{T_{n-1}}{T_n}.
\]

Then \(t_n\to\beta^{-1}\), and direct use of the recurrence gives

\[
 L\cdot t_n=t_{n-1},\qquad
 \boxed{A\cdot t_{n+3}=t_n}.
\]

Thus the same matrix \(A\) that defines the Shintani--Faddeev cocycle
transports consecutive points separated by the modulus-six unit order.
This is a structural bridge between a finite root-of-unity object and
the absolute value of the irrational identity-class RM value.

## 2. Cyclic dilogarithm specialization

For a reduced fraction \(m/n\), define

\[
 \log\left|D_{m/n}(1/6)\right|
 =
 \sum_{k=1}^{n-1}
 \frac{k}{n}
 \log\left|
 1-\exp\left(2\pi i(k+1/6)\frac mn\right)
 \right|.
\]

The totally positive unit \(\beta\) has order

\[
 g((6))=3
\]

modulo the rational principal ideal \((6)\).  Yalkinoglu's formula
therefore specializes to

\[
 X_1((6))
 =
 \lim_{n\to\infty}
 \left|
 \frac{D_{t_n}(1/6)}
      {D_{t_{n+3}}(1/6)}
 \right|.
\]

In the present conventions the limit is the Kopp/Shintani reciprocal
of the positive primitive overlap:

\[
 X_1((6))=x^{-1},
\qquad
 x=2.212885291\ldots.
\]

The executable specialization gives:

\[
\begin{array}{c|r|r|c|c}
n&T_n&T_{n+3}&\text{cyclic approximation}&
 |\text{approximation}-x^{-1}|\\ \hline
1&5&527&0.457273381462421&5.38\cdot10^{-3}\\
2&23&2525&0.452464881836621&5.66\cdot10^{-4}\\
3&110&12098&0.451923403040466&2.47\cdot10^{-5}\\
5&2525&277727&0.451898753468986&4.69\cdot10^{-8}\\
6&12098&1330670&0.451898708435006&1.82\cdot10^{-9}
\end{array}
\]

This is independent evidence for the convention and positive-root
selection.  It is not evidence for the missing complex orientation:
Yalkinoglu's announced formulas are stated with absolute values.  The
rational geodesic selects the identity-class scalar invariant, but the
absolute value still discards the oriented order-six character component.

## 3. Why this is not yet a proof

Every cyclic approximant is algebraic, lying in a Kummer extension of a
cyclotomic field.  A convergent sequence of algebraic numbers can,
however, have an arbitrary transcendental limit.  The cyclic formula by
itself proves neither that the limit lies in the ray field nor that it
satisfies the degree-twelve primitive polynomial.

The 2025 paper is also explicitly an announcement; it states that a full
account with complete proofs will appear separately.  Even after its
limit formula is accepted, the algebraicity step remains the substance
of the Stark--Shintani conjecture.

The earlier rejection of a direct cyclic pentagon remains correct:
\(\exp(\pi i\beta)\) is not a root of unity.  What changes here is the
availability of a sequence of genuine root-of-unity problems
\(t_n\), tied together exactly by \(A\), whose limit is the desired RM
value.

## 4. The full finite table has a new boundary obstruction

The strongest possible finite-level statement would define, for every
characteristic
\(\boldsymbol r\in(1/6)\mathbb Z^2/\mathbb Z^2\), the rational cocycle
value

\[
 \nu_{\boldsymbol r}^{(n)}
 =
 \Phi_{\boldsymbol r}\,
 \operatorname{shin}_{A}^{\boldsymbol r}(t_{n+3}),
 \qquad A\cdot t_{n+3}=t_n,
\]

The technical obstruction is explicit: Kopp's published rational formula
is stated for the Jacobi cocycle away from its branch locus, while the
level-six characteristics can make individual cyclic factors vanish.
The numerator and denominator zeros can be combined exactly by assigning
a common regulator to the Jacobi argument.  The resulting regulator
order does not always vanish.

For the first four rational steps, the numbers of singular nonzero
characteristics are respectively

\[
 4,\quad 5,\quad 5,\quad 5.
\]

For example, at

\[
 t_5=\frac{527}{2525},
\]

the five diagonal characteristics

\[
 (1,1),(2,2),(3,3),(4,4),(5,5)\pmod6
\]

have nonzero rational-boundary orders.  Thus the naive full cyclic table
does not exist as a table of finite nonzero values at a fixed rational
boundary point.  This agrees with Kopp's warning that the characteristic
formula is subtler because cyclic factors can vanish.

Consequently, an exact finite-level TCC identity for the unrenormalized
table is not the right statement.  The remaining finite problem is to
determine whether there is a canonical characteristic-dependent
renormalization

\[
 \widehat\nu_{\boldsymbol r}^{(n)}
 =
 \lim_{\delta\to0^+}
 \delta^{-v_n(\boldsymbol r)}
 \Phi_{\boldsymbol r}
 \operatorname{shin}_{A}^{\boldsymbol r}(t_{n+3}+i\delta)
\]

whose leading coefficients satisfy a balanced convolution identity, or
whether the TCC defect only vanishes after the subsequent limit
\(n\to\infty\).

This suggests a tropical first test: for every TCC summand, compare

\[
 v_n(\boldsymbol q)+v_n(\boldsymbol q-\boldsymbol p).
\]

If the smallest order is unique for some
\(\boldsymbol p\), no leading-coefficient cancellation is possible.  If
the minimum is always attained in balanced phase-paired sets, a cyclic
pentagon or telescoping identity remains plausible.

The executable audit now performs this test.  Its first four results are:

\[
\begin{array}{c|c|c}
n&\text{number of singular characteristics}&
\text{nonzero shifts with a unique minimum}\\ \hline
1&4&(2,2),(4,4)\\
2&5&\varnothing\\
3&5&\varnothing\\
4&5&\varnothing
\end{array}
\]

At the second and third steps the minimum multiplicity is \(26\) for
thirty shifts and \(30\) for five shifts; the zero shift has multiplicity
\(31\).  Thus those two steps pass the necessary tropical cancellation
gate very strongly.  The first step fails it for two nonzero shifts.  At
the fourth step only the zero shift has a unique minimum, caused by a
single polar characteristic, so its normalization must be changed before
the trace equation can survive.

This does not prove a leading-coefficient identity.  It does identify the
right subsequences for the next calculation: start with the second and
third congruence classes of the Chebyshev recurrence, where every
convolution equation has enough equal-order terms to permit phase
cancellation.

## 5. Recommendation

Do not return first to regulator magnitudes or to a general wild-sextic
Stark theorem.  They discard precisely the orientation needed here.

Instead:

1. retain the two Chebyshev subsequences that pass the tropical gate;
2. derive their nonzero leading coefficients with branches and AFK
   phases retained;
3. evaluate the resulting thirty-six finite convolution sums exactly;
4. search for a cyclic pentagon or telescoping identity only if those
   sums exhibit exact cancellation.

This route is still ambitious, but it is narrower than proving the full
rank-one Stark conjecture.  It attacks the SIC identity directly and
uses a new finite approximation that preserves the hyperbolic
orientation.

## Reproducibility

- `scripts/dimension_six_normal_closure.gp`
- `scripts/explore_dimension_six_cyclic_dilog.py`
- `scripts/dimension_six_shintani_cycle.py`
- `scripts/verify_dimension_six_ray_bridge.py`

## Primary sources

- Y. Katayama and M. Kida, *Coincidence of \(L\)-functions*,
  Acta Arith. 204 (2022), 369--385.
- B. Yalkinoglu, *Shintani's invariant via cyclic quantum
  dilogarithm*, arXiv:2508.18320 (2025).
- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units
  from \(q\)-Pochhammer ratios*, arXiv:2411.06763.

# P7-1 norm aggregation over \(\mathbb Q(i)\): executed gate v1

## Outcome and boundary

`PROVED`: the preselected \(Q=8\) witness is correct.  The finite ray-class
quotients after division by \(\mu_4\) both have order two; their nontrivial
characters have exact conductors \((3)\) and \((1+i)^4\), respectively; and

\[
17=(4+i)(4-i),\qquad
A_{\chi_{(3)}}(17)=-2,\qquad A_{\chi_{(1+i)^4}}(17)=2.
\]

`PROVED`: for all \(n\geq1\),

\[
a_{\mathbb Q(i)}(n)=\#\{\mathfrak a\subset\mathbb Z[i]:N\mathfrak a=n\}
=\sum_{d\mid n}\chi_{-4}(d)\leq\tau(n).
\]

`PROVED_CONDITIONAL_ON_LENGTH_HEIGHT_RELATION`: normalizing a fixed norm
coefficient vector by \(D_N=\max_{N<n\leq2N}\tau(n)\) is exponent-harmless
for the exact Guth--Maynard Theorem 1.1 form when \(N\leq T^C\) for a fixed
\(C\).  In particular this covers the source proof's nontrivial reduction
\(N<T\).  It is not established for an unrestricted two-parameter use of a
bound with only a \(T^{o(1)}\) loss, because \(N^{o(1)}\) need not be
\(T^{o(1)}\) without a relation between \(N\) and \(T\).

This is not a Hecke-family large-value theorem, a zero-density estimate, or a
prime-ideal short-interval theorem.  It does not turn a fixed-polynomial
estimate into an estimate for joint \((\chi,t)\) samples.

## Algebraic calculation

Zaman's pinned source defines the finite ray class group as
\(I(\mathfrak f)/P_{\mathfrak f}\), its conductor as the maximal modulus from
which a character is induced, and the ideal Euler product (TeX §1,
lines 101--110; §2.1, lines 298--309).  Since \(\mathbb Z[i]\) has class
number one and no real places, the finite quotients here are

\[
\operatorname{Cl}(\mathfrak f)
\cong(\mathbb Z[i]/\mathfrak f)^*/\operatorname{image}(\mu_4).
\]

For \((3)\), the residue field is \(\mathbb F_9\), so its unit group has
order eight and the unit-image \(\mu_4\) has order four.  The quotient has
order two.  In it,

\[
(4\pm i)^4\equiv(1\pm i)^4=-4\equiv-1\pmod{3},
\]

which is the nonidentity quotient class; hence the unique nontrivial quotient
character takes both values as \(-1\).  It cannot factor through the only
proper modulus \((1)\).

Let \(\pi=1+i\).  For \(e=1,2,3,4\), the unit group of
\(\mathbb Z[i]/\pi^e\) has sizes \(1,2,4,8\), while the image of \(\mu_4\)
has sizes \(1,2,4,4\).  The quotient sizes are therefore \(1,1,1,2\).
Thus its nontrivial order-two character at \(e=4\) has exact conductor
\(\pi^4\).  Since \(\pi^4=-4\),

\[
4+i\equiv i,\qquad4-i\equiv-i\pmod{\pi^4};
\]

both are in the unit image and both character values are \(+1\).

Two independent routes record this calculation: exact multiplication tables
of the finite residue quotients, and the local cardinality/generator derivation.
They are reconciled in the versioned gate artifact.  Route B v1 used
parenthesized coefficient labels whereas Route A used the canonical underscore
labels; a separate versioned label-only correction records the explicit
bijection before reconciliation.  No numerical or algebraic claim changed.

## Norm aggregation and normalization

The norm-count identity is local at rational primes.  At \(2\) there is one
ideal of each norm \(2^e\); at split \(p\equiv1\pmod4\) there are \(e+1\)
ideals of norm \(p^e\); and at inert \(p\equiv3\pmod4\) there is one exactly
when \(e\) is even.  These agree respectively with
\(\sum_{j\leq e}0^j\), \(\sum_{j\leq e}1\), and
\(\sum_{j\leq e}(-1)^j\).  Multiplicativity proves the formula above.

The pinned Guth--Maynard source, Theorem 1.1 (TeX lines 62--79), states for
one \(1\)-bounded coefficient sequence the three terms with threshold powers
\(V^{-2},V^{-4},V^{-4}\).  For a fixed \(\chi\), put
\(b_n=A_\chi(n)/D_N\).  The original threshold \(V\) becomes \(V/D_N\), so
the three terms acquire precisely \(D_N^2,D_N^4,D_N^4\).  The standard divisor
bound gives \(D_N\ll_\delta N^\delta\); if \(N\leq T^C\), choosing \(\delta\)
after the desired epsilon absorbs the largest \(D_N^4\) into \(T^{o(1)}\).

The source itself reduces its nontrivial use to \(N<T\) (TeX lines 447--457),
so the normalization has no exponent cost in that stated regime.  This says
nothing about summing the fixed-character estimates over a conductor family.

## Type boundary

The unequal values at \(n=17\) prove that the two norm-collapsed coefficient
vectors are not one common vector.  Therefore a theorem whose hypothesis is a
single \((b_n)\) shared by every sample point cannot be imported verbatim to a
joint collection indexed by \((\chi,t)\).  This is `PASS_TYPE_MISMATCH`, not
a no-go result: an ideal-indexed or character-aware large-value theorem, or a
separate-in-\(\chi\) application with a proved family-size cost, remains open.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/run_p7_norm_aggregation_route_a_v1.py --check
python3 proof/run_p7_norm_aggregation_route_b_v1.py --check
python3 proof/correct_p7_norm_aggregation_route_b_v2.py --check
python3 proof/reconcile_p7_norm_aggregation_v1.py --check
python3 -m unittest tests/test_p7_norm_aggregation_v1.py -v
```

The reconciliation artifact pins the source, convention, route, document, and
test hashes.  Both route contracts cap wall time strictly below 60 seconds and
peak resident memory strictly below 256 MiB.

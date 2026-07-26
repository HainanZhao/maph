# T3e challenge audit: extension and failed elementary proof routes

Date: 2026-07-26

This note deliberately treats Conjecture T3e as a target to falsify, not
as an assumption.  Recall that the relevant monic polynomial is

\[
Q_a(b)=(a!)^2 C_{a,b}
\]

for even \(a\), while for odd \(a\) the two proved linear factors are
removed:

\[
R_a(b)=\frac{Q_a(b)}{(b+1)(b-2a)}.
\]

The question tested here is whether \(Q_a\) (even \(a\)) or \(R_a\)
(odd \(a\)) is irreducible over \(\mathbb Q\).

## Result: rigorous extension through \(a=59\)

No counterexample was found.  The existing certificate range
\(a\leq38\) extends rigorously to every \(39\leq a\leq59\).  The new
finite-field certificates are:

```text
39: 167
40: 487
41: 359
42: 2539
43: 431
44: 647
45: 593
46: 163
47: 127
48: 139
49: 1559
50: 929
51: 397
52: 491
53: 1493
54: 911
55: 241
56: 353
57: 433
58: 1013
59: 1009
```

An entry `a: p` means that the relevant residual polynomial is
irreducible in \(\mathbb F_p[b]\).  Since it is monic over
\(\mathbb Z\), Gauss's lemma proves irreducibility over
\(\mathbb Q\).

The certificates were found by increasing-prime search.  For
\(a=39,40,41\), the search and proof both used the existing
standard-library Rabin implementation.  For \(42\leq a\leq59\), SymPy
1.14.0 was used only as a faster search filter; every positive result
was then independently rerun through the standard-library Rabin test.
Thus SymPy is not part of the final certificate.

The sum of the individually printed row runtimes for \(a=39,\ldots,59\)
was 862.846 seconds on the current machine.  This excludes time spent
on an unfinished \(a=60\) search, which was stopped without drawing a
conclusion.  Expensive rows included \(a=53\) (104.876 s), \(a=54\)
(88.872 s), and \(a=58\) (83.832 s).  Runtime varies mainly with how
far the first successful prime lies into the prime list, so this is
not a clean asymptotic benchmark.

A structural explanation for the size of the primes is immediate.
The constant term is \((\pm)(2a)!\) for even \(a\), and
\((2a-1)!\) for the odd residual.  Every prime at or below the
corresponding factorial bound makes the reduction have zero constant
term and hence a factor \(b\).  Therefore a finite-field
irreducibility certificate must use \(p>2a\) (for \(a\geq2\)).
There is no evidence here for a single fixed prime or an elementary
uniform choice \(p=p(a)\).

The exploratory reproducer is
`scripts/search_reflection_irreducibility_certificates.py`.  Its
default path uses only the standard library.  The faster optional
search is, for example:

```text
/Users/hainan/miniconda3/bin/python3 \
  scripts/search_reflection_irreducibility_certificates.py \
  --min-a 42 --max-a 50 --prime-limit 20000 \
  --search-backend sympy
```

Failure to find a certificate under a prime limit does **not** imply
reducibility.  Only a reported and verified positive pair has
mathematical content.

## Challenge to the proposed Newton-polygon route

The most elementary versions of the Newton-polygon idea show no
traction:

1. For every \(2\leq a\leq60\), and for every prime that can divide
   the unshifted constant term, the residual polynomial fails the
   primitive one-segment Dumas criterion.
2. Consequently ordinary unshifted Eisenstein also fails throughout
   that range.
3. A bounded shift search found no primitive one-segment case for
   \(2\leq a\leq25\), integer shifts \(|c|\leq2a\), and primes
   \(p\leq4a+10\), applied to \(f(b+c)\).

These checks are reproduced by:

```text
python3 scripts/diagnose_reflection_newton.py
```

The unshifted prime search is exhaustive because its constant term is
a factorial.  The shifted search is explicitly not exhaustive: a
shifted constant \(f(c)\) can have prime factors above the tested
bound.

This does not rule out a subtler Newton-polygon proof using several
primes, several edges, or exclusion of possible factor degrees.
It does rule against presenting “apply Eisenstein after an obvious
shift” or “find one primitive Newton edge” as a plausible near-term
uniform proof without a new structural observation.

## Assessment

The evidence for T3e is stronger—exactly certified through \(a=59\)—
but the proof-route evidence is weaker.  Certificate primes are
irregular, necessarily grow beyond \(2a\), and the elementary
Newton/Eisenstein patterns tested above are absent.  T3e should remain
a conjectural strengthening, not the main dependency of the physical
zero theorem.  A robust thesis strategy is:

- retain T3e as an algebraic observation and computationally certified
  conjecture;
- seek a direct proof of the weaker integral-root statement T3 using
  divisibility, sign, or reciprocity;
- revisit Newton polygons only after deriving coefficient-valuation
  structure capable of excluding all possible factor-degree
  partitions.


# Census-paper preregistration amendment v2: Artin-orbit factor

Frozen: 2026-07-31 UTC, after the trace recurrence passed the
dimension-eight two-character anchor and before extracting unit data
from any four-character Q row.

## Preserved correction

Amendment v1 correctly proves that trace descent constructs the full
formal sign orbit of the denominator-cleared unit factors.  Its
statement that \(q=1\) makes this automatically the packet orbit is
valid only when the supported-character sign map is surjective onto
all formal sign patterns.

For the 57 frozen Q rows with ray group \(C_2^3\), there are four
supported quadratic characters but only eight Artin classes.  Their
sign vectors satisfy a character relation, so the 16 formal sign
patterns split into two parity cosets.  The raw trace polynomial is an
ambient orbit polynomial, not yet the eight-value packet polynomial.
Amendment v1 and its dimension-eight certificate remain unchanged;
this versioned correction controls the general corpus.

## Exact orbit gate

For every Q row:

1. enumerate the exact image of
   \(A\mapsto(\chi(A))_{\chi(R)=-1}\);
2. record its cardinality and all multiplicative sign relations;
3. synthesize the full formal sign-orbit polynomial from traces;
4. factor it exactly over \(K\) whenever the Artin image is a proper
   subset of the formal sign cube;
5. match a factor to the exact Artin image using the identity-class
   unit product and the frozen class action;
6. apply the denominator-\(q\) lift from amendment v1;
7. require exact reciprocity, squarefreeness, irreducibility, and full
   orbit cardinality before using “minimal polynomial.”

Neither coefficient sign patterns nor a numerical packet value alone
may select the Artin factor in the proper-image case.

## Frozen anchor

RQ-000089 is the first Q row in stable RQ order with four supported
quadratic characters.  It is frozen as the first proper-Artin-image
anchor before its relative units, traces, exponents, or polynomial
factors are inspected.

The anchor passes only if:

- the exact character image has eight of the sixteen sign patterns;
- the four-character relation is printed explicitly;
- the ambient trace polynomial factors over \(K\) into the required
  Artin cosets;
- the identity-class exact unit product selects one factor without
  analytic target data;
- the selected packet orbit has the exact expected cardinality.

Failure preserves the memory-saving ambient recurrence but blocks its
promotion to a corpus packet-polynomial algorithm.

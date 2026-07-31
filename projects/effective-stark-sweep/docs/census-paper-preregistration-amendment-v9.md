# Census-paper preregistration amendment v9: deduplicated sextic screening

Frozen: 2026-07-31 UTC, after the sequential run had attempted 119 of
764 kernels and recorded ten 600-second timeouts, before extracting the
primitive-field key population.

The sequential route is preserved at
`artifacts/roblot-sextic-population-sequential-partial-v0.json`, SHA-256
`2618e6376ee4169d4b9ec65ed5ce2436fa6da22c42f918e6215874b5138188dc`.
Its mathematical method remains valid, but repeating full degree-12
`bnfinit(P,1)` plus `bnfcertify` for every occurrence is superseded as
the population implementation.

The optimized route has two exact stages.

1. For every frozen kernel, compute the primitive conductor, transported
   primitive character, primitive kernel HNF, and row-local A3 and
   \(S=S(H/K)\) predicates without constructing the sextic field.  The
   primitive-field key is the tuple consisting of the base radicand,
   primitive conductor, primitive ray cyclic invariants, and primitive
   kernel HNF.  The route-stage cap is 60 seconds and 2 GiB per kernel.
2. Group identical keys.  For a key having at least one occurrence that
   passes the row-local A3 and \(S\)-equality gates, construct and certify
   its degree-12 absolute field exactly once.  Propagate only the
   field-invariant A1, A2, class-number, and ramification-above-3 results
   to matching occurrences.  The field-stage cap remains 600 seconds
   and 2 GiB per distinct key.

An already completed sequential certificate may seed a field key only
after the new route reproduces the same base, primitive conductor, and
primitive kernel HNF.  A sequential timeout never propagates a negative
result.  If every occurrence of a key already fails A3 or
\(S=S(H/K)\), Theorem 7.1 is exactly nonapplicable and no field
construction is required; untested field-level gates are recorded as
`NOT_NEEDED_AFTER_EXACT_LOCAL_FAILURE`.

Any route-stage failure or still-hard distinct field key remains
explicitly incomplete.  No kernel is dropped, and eligibility remains
prior-work coverage rather than a new Stark identity.

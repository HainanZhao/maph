# Cycle 11: exact SAT encoding and certificate boundary

Fix a base tuple `v`, parameters `(k,p,c)` with `gcd(p,c)=1`, and
`q=pc`.  For each coordinate `i` and digit `d` in `{0,...,c-1}`, let
`x(i,d)` mean that the lifted speed `v_i+pd` is selected.  The CNF contains
one at-least-one clause and every pairwise at-most-one clause for each
coordinate, so exactly one digit is selected.

For every time `a` in `Z/qZ`, the CNF contains the clause consisting of all
`x(i,d)` whose lifted speed is bad at `a`, namely

```
(k+1) min(a(v_i+pd) mod q, q-a(v_i+pd) mod q) < q.
```

Thus all time clauses hold exactly when the selected bad masks cover all of
`Z/qZ`, equivalently when there is no denominator-`q` witness.

For every prime `r` dividing `c` and coordinate `i`, an auxiliary variable
`y(r,i)` is equivalent to the disjunction of the selected digits for which
`r` divides `v_i+pd`.  The forward clauses are `not x(i,d) or y(r,i)` for
each such digit, and the reverse clause is `not y(r,i)` or their disjunction.
Because exactly one digit is selected, the equivalence is exact.  For every
subset of `k-1` coordinates the CNF has the clause containing the negations
of their `y(r,i)` variables.  These clauses say that at most `k-2` selected
speeds are divisible by `r`.

Definition 2.1's gcd condition holds after omitting a coordinate exactly when
some prime divisor `r` of `c` divides each of the other `k-1` speeds.
Consequently the cardinality clauses fail exactly in the gcd-proper cases.
Together, the CNF is satisfiable if and only if this base has an improper
first lift in the frozen fiber.

A SAT result is accepted only after an independent parser extracts one digit
per coordinate, directly recomputes all denominator-`q` times and every
omission gcd, and checks every emitted CNF clause.  An UNSAT result is accepted
only when the pinned `drat-trim` checker validates CaDiCaL's DRAT proof against
the exact emitted DIMACS file and the checker reports `VERIFIED`.  A timeout,
resource stop, malformed output, missing model, or failed proof is `CAP` or
`ERROR`, never SAT or UNSAT.

The H11 and p47 controls test the full encoding pipeline on finite instances
whose expected exclusions were established independently in Cycle 8.  Results
on the fixed 100 p199 bases concern only those first-lift fibers; they do not
establish `F_1(13,199,14)=empty`, `J(13,199)=empty`, or `LRC(13)`.

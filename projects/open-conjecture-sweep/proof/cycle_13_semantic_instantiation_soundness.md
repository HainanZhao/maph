# Cycle 13: typed semantic core instantiation

The source is the certified 293-clause Cycle-12 subcore.  Its variables have
three fixed types: a choice variable `x(i,s)`, a divisibility variable
`y(2,i)`, or a divisibility variable `y(7,i)`.  Here `s` is the selected
speed modulo 14, rather than its base-dependent lift digit.  Each choice also
has the intrinsic divisor color

```
(2 divides s, 7 divides s).
```

A permitted semantic substitution consists of a permutation `pi` of the
thirteen coordinate blocks and, independently for every source coordinate
`i`, a bijection `sigma_i` of the fourteen residue choices which preserves
the divisor color.  It maps

```
x(i,s)   -> x(pi(i), sigma_i(s)),
y(r,i)   -> y(r,pi(i))
```

and preserves literal signs and clause multiplicities.  Unlike Cycle 12,
choices with the same divisor role may be exchanged.  Their bad-time coverage
roles are not assumed equal: the target's actual time clauses decide whether
the completed substitution is valid.

The exact instantiation checker applies a proposed substitution to every
literal of every source-core clause and requires the resulting clause
multiset to occur in the target CNF.  Therefore an accepted image is an exact
copy of a certified unsatisfiable subformula.  The target CNF is then
unsatisfiable, and Cycle 11's encoding theorem excludes an improper first lift
for that named target base.

Colored incidence signatures, clause roles, refinement, and backtracking are
search devices only.  They may remove a candidate image only when the
corresponding already-complete mapped clause is absent, or when a Hall test is
proved necessary for extending the partial typed bijections.  A statistical
role match, incomplete substitution, timeout, or search cap proves nothing.
Every `MATCH` must carry the full coordinate and within-coordinate bijections
and pass a separate literal-level clause-multiset containment replay.

For the frozen row-76 subcore, the permitted generalization collapses.  Its
196 negative choice-pair clauses map to other exactly-one clauses which every
target contains.  Its 84 `not x or y(2)` clauses map to other exact y-channel
clauses because divisor color is preserved.  Its single twelve-coordinate
negative-y clause maps to another target cardinality clause.  Each of the
remaining twelve positive choice clauses intersects any divisor-color class
either in the entire class or not at all, so every `sigma_i` fixes that clause
setwise.  Clause multiplicities are preserved by the bijections.

Consequently, for any fixed coordinate permutation, a typed substitution
embeds this core if and only if the identity residue substitution embeds it.
Cycle 12 exhaustively found no such coordinate embedding in the frozen 20
validation and 100 external targets.  The typed family therefore has no image
in those targets without running the formally larger search.

This theorem concerns only the frozen substitution family and named target
CNFs.  It does not state that the chosen subcore is canonical, that every
semantic or interpolant map has this form, or that the full retained set,
`J(13,199)`, or `LRC(13)` is closed.

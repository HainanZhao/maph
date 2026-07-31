# Cycle 118 — B5-022 label-aware Euler deletion

Let the exact canonical ray map from target to source send the target
generator to the source generator to the power `c`, with `c=1` or
`c=5` modulo six.  A target label `a` therefore maps to source label
`ca`.  For distinct added primes with source logs `l_i`, Euler deletion
and rank-one vanishing give

\[
 X_{m'}(a)=\prod_J X_m(ca-\sum_{j\in J}l_j)^{(-1)^{|J|}}.
\]

The exact `bnrmap` records identity and sign-label preservation, and
records `c` explicitly.  Thus `Mat(5)` is a label conversion, not an
identity-labelled shortcut.  Positivity is preserved because all source
packet entries are positive at the fixed split embedding.

This applies only to the five source-coprime B5-022 targets selected
by Cycle 117; it excludes the two targets that enlarge the source prime.

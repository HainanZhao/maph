# Cycle 12: exact embedding-search completeness

After lifted-residue normalization, a permitted map is determined by a
permutation of the thirteen coordinate blocks.  The search maintains a partial
injective map.  For each source coordinate it first removes a target coordinate
from the domain only when a one-coordinate core clause would map to a clause
absent from the target.  Such a clause must be present under every valid full
embedding, so this domain filter is necessary.

The depth-first search chooses each source coordinate once and tries every
unused member of its filtered domain.  Hence, absent a cap, it visits every
coordinate permutation which could satisfy the unary conditions.  It prunes a
partial map only when a core clause whose complete coordinate support has
already been assigned maps to a clause absent from the target.  That condition
is also necessary for every extension.

Exactly-one and gcd-channel clauses whose normalized forms occur universally
were removed only from the hot-path pruning loop.  Removing a pruning test can
enlarge the search but cannot eliminate a valid map.  At every complete map,
the checker maps the entire certified core, including all universal clauses,
and requires multiset containment in the target CNF.  It also checks that the
coordinate image is a permutation.

Therefore `MATCH` supplies an explicitly rechecked clause embedding, while
`NO_MATCH` after uncapped exhaustion proves that no map in the frozen family
exists.  `CAP` makes no claim.  The 100 source-to-self controls exercise the
positive path; each returned map passes the same full containment check.

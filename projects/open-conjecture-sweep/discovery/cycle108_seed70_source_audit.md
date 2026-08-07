# C108 n=70 seed source audit

**`PROVED` source-replay fact.** Epoch AI published a dedicated n=70
constructor on 31 July 2026 at
`https://epoch.ai/files/open-problems/ramsey-book-graphs-70.py`, with a
five-page derivation. It uses \(q=139\equiv3\pmod8\), two quadratic-character
sequences on the square subgroup of \(\mathbb F_{139}^\times\), and a
six-block Seidel matrix of order 278. The derivation proves row sum \(-1\)
and off-diagonal square entries in \(\{0,-4\}\).

The local replay `proof/cycle108_seed70.py` is the direct source transcription
and independently checks symmetry, signs, row sums, the full integer square,
and graph/common-neighbour maxima. It replaces C108's obsolete absence claim:
the previous source audit only checked Wesley's q=1 mod 4 theorem, not this
later q=3 mod 8 construction.

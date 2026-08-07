# Oracle C109 selection: inversion-warped quadratic-character incidence

**`CONJECTURED` planning decision.** The human-selected F001 asymmetric
book-Ramsey target remains fixed; Oracle selects this cycle and method only.

The prior C103--C107 routes enforced structured Seidel equalities. C109 tests
the actual asymmetric local book caps in a nonlinear, two-layer finite-field
state without a free graph census.

For \(V=\mathbb F_q\times\{0,1\}\), \(n=(q+1)/2\), choose nonsquares
\(a_0,a_1,c\), and arbitrary \(t,z\in\mathbb F_q\). Red same-layer edges
in layer \(i\) satisfy \(\chi((x-y)^2-a_i)=1\); a red cross edge satisfies
\[
 \chi((\iota(x+t)+z-y)^2-c)=1,\qquad
 \iota(0)=0,\quad\iota(u)=u^{-1}\ (u\ne0).
\]
The invariant is the complete ordered red/blue common-neighbour slack profile.
The direct bitset verifier requires every red edge to have at most
\((q-3)/2\) red common neighbours and every blue edge at most
\((q-1)/2\) blue common neighbours.

**Exact gate:** exhaust all \(3^3\cdot7^2=1323\) states at \(q=7\). Only
if a hit occurs, exhaust all \(11^3\cdot23^2=704099\) states at \(q=23\).
No RNG, subset census, or second family.

**Caps:** at most four workers, 30 aggregate wall-minutes, 2 GiB aggregate
memory, and 512 MiB output. **Falsifier:** zero q=7 hits, a profile/direct
verification mismatch, or any claimed hit failing direct checks. **Stop:**
zero q=7 hits closes only this family; q=7-only hits stop without enlargement;
both hits are a candidate mechanism only.

**Exclusion map:** C103 has fixed character blocks; C104--C106 are dihedral
Cayley states; C107 has a fixed Paley cross kernel; C108 needs an absent seed.
C109 instead has a nonlinear inversion-warped cross kernel and checks the
asymmetric inequalities directly.

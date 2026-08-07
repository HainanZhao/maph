# Oracle post-result packet: C103 one-reflection boundary

## Recommendation

**`PROVED`:** rely on
`artifacts/cycle-103-b103-book-ramsey-reflection-boundary-correction-v2.json`,
which supersedes v1's replay packaging, for the C103 one-reflection boundary.
The active book-Ramsey problem remains open. The next bounded design question
is the minimal two-orbit dihedral Cayley group-ring constructor, not a further
six-block modification.

## Question the question → question that critique → brainstorm

The immediate question was whether all (2^{25}) signed/reflected templates
fail at (q=7). **`PROVED`:** all 222 row-sum survivors and 14,208 full
Seidel checks have no hit under two exact evaluators. Treating another local
six-block alteration as progress would be misleading: C101 already rules out
the sign-only placement, and C103 rules out its six independent right-inversion
choices. Conversely, those failures do not rule out group-based constructions
outside that placement. Serious alternatives were: (i) a two-orbit dihedral
Cayley constructor; (ii) a recursive switching/two-lift transition, rejected
for lacking a size-compatible transition; and (iii) another twist/free block,
rejected as a duplicate near-variant.

## Exclusion map

| Prior record | Former question and outcome | Delta required now |
| --- | --- | --- |
| `cycle-101-b101-book-ramsey-character-sign-rigidity-v1` | Fixed 19-sign six-block completion; no (q=7) hit. | A global group-convolution state, not sign retuning. |
| `cycle-103-b103-book-ramsey-reflection-boundary-correction-v2` | Same placement plus six (R)-bits; no (q=7) hit. | A nonabelian Cayley connection set, not another local reflection/twist. |
| `cycle-102-b102-hadamard-quartic-boundary-v1` | Quartic-character PAF completion; no triple. | Different target; inactive by the active-problem discipline. |

## Bounded next design question

**`CONJECTURED`:** Let (G_q=D_{2q}=\langle r,s:r^q=s^2=1,
srs=r^{-1}\rangle) for (q=7,23). Test the 16 inverse-closed connection
sets using one bit for all nonidentity rotations and three reflection bits for
(sr^x) according as (x=0\), \(\chi(x)=1\), or \(\chi(x)=-1\). The
invariant is the group-ring convolution (1_D*1_D(g)), independently checked
against exact adjacency common-neighbor counts and translated to the frozen
book/Seidel thresholds. First enumerate 16 (q=7) rows; only hits proceed to
(q=23). A no-hit closes this minimal Cayley class only. Cap: one worker, 32
template-control rows, 60 seconds, 64 MiB RAM, 1 MiB disk. No arbitrary
reflection subsets, character-polynomial search, larger group census, or
six-block repair.

# Cycle 24 idea selection scratch

The new question must be structurally distinct from Cycle 23: changing the
width-four partition or taking another LP reweighting is not enough.

Candidate A — **CRT Fourier-class dual (chosen).**  On
\(G=\mathbb Z_{199}\times\mathbb Z_{14}\), use the tensor product of the
two Ramanujan character algebras: the \(\alpha=0\)/\(\alpha\ne0\) classes
on \(\mathbb Z_{199}\), and the four \(\gcd(\beta,14)\) classes on
\(\mathbb Z_{14}\).  This is an eight-dimensional, integer-valued
low-degree Fourier space that preserves the coupled CRT predicate while
testing correlations that pair savings cannot encode.  First establish the
exact transform/class convention and seek a direct-CNF capacity or global
cover obstruction from a normalized nonnegative class weight.

Candidate B — heterogeneous width five.  A \(5+4+4\) or \(5+3+3+2\)
capacity LP may see more interactions, but it still extends the same block
capacity family and has a rapidly growing option set.  It is rejected now:
a compact performance control and a reason to prefer one partition family
are required before spending a cycle on it.

Candidate C — direct primal assignment.  A full allowed-digit selection that
covers every time would be a decisive falsifier only after its exact
equivalence to an improper lift (including the gcd witness) is established.
Without that semantic bridge, a cover of one weighted support refutes only a
dual candidate.  It is rejected as currently framed.

Questioning the choice: the eight CRT classes may be too coarse and collapse
to a non-discriminating invariant.  A failure would not discredit individual
characters, higher Fourier degree, width five, or a semantic primal model.
It is chosen because its convention and its small exact state space can be
falsified cheaply, while it directly exploits the proved two-diagonal CRT
interface instead of revisiting pairwise partition scoring.

Chosen decision question: **does a normalized nonnegative weight in the
frozen eight-class CRT/Ramanujan space give a direct exact deficit for at
least one of the 60 named leaves under a preregistered full-cover upper-bound
or a specified safe block-capacity relaxation?**

Main rejected alternative: width-five heterogeneous capacity LP.

Falsifier: an exact convention/control mismatch, a direct-CNF mismatch, or
exhaustive failure of the preregistered finite class family to achieve a
strict direct integer margin.  No floating recognition or class score is a
certificate.

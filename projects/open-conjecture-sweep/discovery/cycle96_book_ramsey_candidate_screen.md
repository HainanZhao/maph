# C96 candidate screen: book-Ramsey construction

This is a candidate-selection packet, not an attack preregistration. It
authorizes no executable search.

## Source-defined lead

`OBSERVED` from Epoch AI's current primary problem page and its source
summary: for the triangular book `B_n`, Rousseau--Sheehan give
`R(B_{n-1}, B_n) <= 4n-1`, and the lower bound is known for an infinite
family and all `n <= 21`. The requested object is an explicit graph on
`4n-2` vertices avoiding `B_{n-1}` whose complement avoids `B_n`.
The page also reports subsequent AI constructions through `n=56` and a
published-format construction at `n=70`; those updates reduce novelty of
an isolated numerical instance but do not supply the requested all-`n`
algorithm.

Primary problem source: <https://epoch.ai/frontiermath/open-problems/ramsey-book-graphs>.
The underlying literature includes Wesley, *Lower Bounds for Book Ramsey
Numbers*, arXiv:2410.03625, and Rousseau--Sheehan (1978). The exact
`n=70` construction is independently available as
<https://epoch.ai/files/open-problems/ramsey-book-graphs-70.py>.

The reported AI-generated family and instances are `OBSERVED` benchmark
updates, not accepted theorems here; any reuse requires an independent proof
and overlap audit.

## Question and adversarial questioning

Question: can a source-compatible algebraic/block-circulant mechanism be
extended to one first unresolved parameter with a proof-grade graph witness,
or can the smallest unresolved parameter be certified impossible under a
frozen construction family?

Question the questioning: this target may be attractive merely because its
verifier is easy and its graph encoding is familiar. A single witness would
be a finite result, not the stated all-(n) theorem, and the benchmark's AI
progress may already cover the easiest arithmetic instances. Conversely,
choosing `n=57` solely because it follows the reported `n <= 56` range
would be a scale-driven census unless the current status and a construction
family are frozen first.

Hidden question: what invariant distinguishes the successful Paley/
2-block-circulant constructions from the unexplained exceptional values, and
can that invariant yield an algorithm rather than another lookup table?

## Alternatives screened

* Large Steiner systems have an exact finite output but the source problem
  asks for some unspecified parameters (n,q,r); no smallest unresolved
  parameter or canonical verifier target is supplied.
* Arithmetic Kakeya has a finite-object formulation, but its first useful
  object is not a smallest unresolved instance and the requested advance is a
  new general bound, not a bounded exact certificate.
* Nivat (|F|=6), stretched LR, finite-cyclic Fuglede, and Kakeya residuals
  are already excluded in `cycle96_portfolio_no_selection.md` for lacking a
  bounded state/falsifier/stop.

## Candidate gate if Oracle selects it

State: a frozen (n), graph on (4n-2) vertices, and adjacency-string
encoding. Invariant: no edge has (n-1) common neighbors in (G), and no
edge has (n) common neighbors in (overline G). Exact verifier: enumerate
common-neighbor counts for every edge and its complement; independently
replay the string parser and both graph constructions. Falsifier: one edge
meeting the forbidden threshold. Stop: a certified witness is sealed as a
finite boundary; an exhaustive failure of the frozen algebraic family ends
that method only. No unrestricted graph census or claim about all (n).

The strongest flaw is that this gate may reproduce already-known AI-generated
instances without a reusable mechanism. Expected information gain is higher
for a general algebraic invariant than for another isolated (n), so Oracle
must choose the family and (n) jointly or return `NO_SELECTION`.

## Oracle outcome

Oracle reconstructed the C80--C95 history and returned `NO_SELECTION`.
The candidate remains a preserved lead, not an authorized attack: a current
uncovered parameter and a new finite algebraic family must be source-cleared
first.

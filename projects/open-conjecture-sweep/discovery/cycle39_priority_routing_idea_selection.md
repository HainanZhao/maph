# Cycle 39 idea selection: root-free priority routing

## Candidate engines

1. **Full priority/fallback section span.** For fallback coordinate (r), a
   deterministic first-cover rule matters to an (r)-blocker only through the
   subset (P) of coordinates preceding (r). Enumerate all (2^{12})
   predecessor subsets for each of 13 fallbacks. Their signed linear span is a
   root-free 53,248-column routing space whose sections satisfy totality and
   exclusivity pointwise and annihilate every blocker away from their fallback.
2. **Ad hoc corrections to the thirteen Cycle 38 roots.** Add a few routing
   variables only at the recorded first violated pairs.
3. **Arbitrary independent routing probabilities.** Give every complete time
   type a probability vector over current covering coordinates and route times
   independently.
4. **General degree-three ownership pseudoexpectation.** Introduce all labeled
   ownership moments through degree three and solve the resulting linear
   system.

## Question the questions

Correcting thirteen witnesses is post-result fitting: it can cancel the first
rows while missing the structural reason later rows fail. It is rejected.

Independent routing probabilities look symmetric but make rank-two blocker
moments quadratic in the routing variables, obscuring both exact infeasibility
certificates and what the state space actually preserves. A general degree-
three pseudoexpectation is principled but its labeled pair-moment space is too
large for the smallest falsifiable prototype.

The full priority-section span is the sharp linear intermediate question.
Cycle 38 used only the empty-predecessor section for each fallback. For a fixed
fallback, every deterministic priority order projects to exactly one
predecessor subset, and the coordinates after the fallback cannot affect
fallback ownership. Thus the (2^{12}) columns are complete for the moment
vectors of all priority orders with that fallback, not a sample of orders.
Signed mixtures permit cancellation while preserving pointwise ownership in
every column.

Questioning that framing again: this still privileges priority sections and a
single fallback per section. A nonlocal correlated routing law need not lie in
their span. Therefore infeasibility is only a no-go for this exact linear
routing family. Feasibility at rank two is only a candidate and must survive
all rank-one, rank-two, and rank-three blockers.

## Choice and falsifier

Choose the full priority/fallback section span. Use exact subset-product
transforms to evaluate all 4,096 predecessor columns without looping over
orders. Solve by exact CEGAR: a rational candidate from selected blocker rows,
then complete label-preserving separation over the complete global-type
quotient. Preserve an integer left-null witness if rank-two feasibility fails.

The branch is falsified by any mismatch between a predecessor-subset moment
and direct signed-support enumeration, any off-fallback blocker that does not
vanish pointwise, any omitted complete type or multiplicity, or any exact
candidate/certificate that fails direct substitution.

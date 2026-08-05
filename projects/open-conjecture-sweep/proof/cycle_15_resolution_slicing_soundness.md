# Cycle 15: resolution-dependency slicing boundary

The pinned `drat-trim -L` replay validates the selected DRAT proof and emits
ASCII LRAT additions with antecedent hints.  Every positive antecedent ID must
precede its derived clause.  Starting from the final empty clause and following
those hints therefore gives the exact input dependency support of that LRAT
derivation.  This support is a proof property, not necessarily a minimal
unsatisfiable subset.

Attach a super-sink after every reached input clause and orient dependency
edges from the final empty clause toward antecedents.  If a strict derived node
dominates the super-sink, every path beginning through each immediate child of
the empty clause must reach that node.  Propagating one exact bit per immediate
child down the acyclic ID order is therefore a necessary dominator test.  In
the frozen graph, no derived node receives all child bits, so no strict derived
dominator exists.  This argument does not classify unions or communities of
resolution branches.

Backward distance and antecedent frequency are selection scores only.  A
prefix has no proof status until its emitted CNF is independently solved.  A
SAT row is accepted only after the complete model is preserved and directly
evaluated against every clause; an UNSAT row would require a fresh DRAT proof
checked against that exact subset.  Thus the six SAT results refute only the
six frozen candidates, not all at-most-500-clause source subsets.

# Cycle 48 idea selection: Möbius tensor and cube repair

## Brainstorm

1. **Möbius tensor plus cube repair.**  Glue the three prescribed pair
   transports by an explicit inclusion--exclusion tensor.  Its defects are
   coefficients on forbidden owner triples.  Repair them with signed
   (2\times2\times2) cube moves, the local kernel generators of all three
   pair-marginal maps.  Orient repairs by a frozen defect order and study the
   critical diamonds.
2. **Rewrite the existing sparse Gaussian solver.**  Extract its pivot trace,
   name pivots as rewrite rules, and prove the trace terminates.
3. **Arithmetic/CRT cokernel.**  Define lift maps between the p199 affine
   section and the next prime-product ownership space, then test whether the
   canonical section lies in their image.
4. **Broader global-section census.**  Generate more connected patches and
   repeat Cycle 47.

The companion proposed a canonical-face rewrite/confluence theorem and
deferred the arithmetic lift until its preservation laws are proved.  The
primary proposal sharpens that suggestion to (1): begin from a closed formula
and use the Markov-kernel cubes as the only corrections.

## Decision questions and adversarial comparison

- For (1): does every forbidden coefficient in the explicit Möbius tensor
  admit a support-local cube repair, and do overlapping repairs join?  The
  initial tensor and every move have short generic proofs.  A failure produces
  a small exact structural countermodel, while success yields a formula rather
  than another existence solve.
- For (2): does the RREF trace define a terminating rule?  Yes almost by
  definition, but this merely renames elimination and has little explanatory
  value.  Reject as the main engine.
- For (3): does arithmetic lifting detect a missing obstruction?  Potentially,
  but non-image has no force until the lift is proved necessary and preserves
  ownership, blocker, and face data.  Defer.
- For (4): does the canonical rule keep filling?  Cycle 47 already gives a
  dense unseen positive patch.  More rows would improve prevalence estimates,
  not explain the mechanism.  Reject.

## Question the questioning

Why confluence rather than mere termination?  A deterministic repair order
already gives one tensor, and two allowed tensors may legitimately differ by
an all-allowed cube on which no defect rewrite acts.  Literal confluence can
therefore be false without harming existence.  The cycle must separate three
claims: repair existence, termination of a fixed orientation, and
order-independence.  A nonjoinable diamond refutes only the third unless it
also blocks every oriented repair.

Why is the cube mechanism new rather than Gaussian elimination in disguise?
The starting tensor is a closed Möbius formula, each cube is a universal
three-marginal kernel identity, and the proposed termination measure depends
only on forbidden support.  No pivot may inspect the desired canonical tensor
or a prior fill.  If repair selection needs arbitrary matrix rank or
post-result free-variable choices, the mechanism has collapsed back to (2)
and fails its advance condition.

Why should cubes suffice with structural zeros?  They generate the kernel on
a full Cartesian product, but deletions can disconnect the corresponding
fiber graph.  This is precisely the discriminating question.  An unrepaired
defect or disconnected repair fiber is a headline structural no-go, not an
implementation failure.

Could a bounded critical-pair check prove a universal statement?  Only for the
finite frozen structural rule system whose state patterns are completely
enumerated.  A hash holdout tests generalization but does not convert that
finite result into all p199 triples.

## Choice

Choose (1).  The main rejected alternative is (2), because a renamed pivot
trace solves the old computational problem without exposing a new invariant.

Advance: prove the Möbius marginal identity and cube-kernel theorem, then
either derive a terminating support-local repair constructor on the frozen
structural pattern universe or isolate the smallest exact obstruction.  Treat
confluence as a separately classified strengthening.

Falsifier: the lexicographically smallest frozen face state with a nonzero
forbidden Möbius coefficient but no admissible cube-repair path, or the
smallest critical diamond whose branches cannot be joined under the frozen
rules.  The latter refutes order-independence but not deterministic repair.

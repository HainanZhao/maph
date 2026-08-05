# C77 coherent continuation: idea selection

## Question

After the finite packet and the already-known classical slice, what is the
most discriminating next question about coherent compatible three-qubit states
with \(Q\ne I/2\)?

## Question the questioning

The obvious question—whether a larger random search finds a violation—can
confuse a failure to sample with evidence for the conjecture.  The converse
bias is also dangerous: the strong conjecture is false, but its known example
uses incompatible marginals, so importing it can destroy the very constraint
that defines C77.  A reduction of a qubit \(Q\) to \(I/2\) is attractive only
if it demonstrably preserves one-global-state compatibility and the relevant
two-body support; neither is automatic.

## Candidate mechanisms

1. **Compatibility-preserving qubit reduction.**  Try to lift the known
   \(Q\to I/2\) expansion through a reset-to-\(|0\rangle\) channel on one
   global state.  Falsifier: the induced subset-dependent mixture cannot be
   realized as marginals of one state, or it necessarily introduces support
   outside \(AB,AC,BC\).
2. **Exact coherent countermodel packet.**  Search a deterministic packet of
   dense complex integer-amplitude pure states and rational \(q\)'s, then
   certify only a strict candidate by exact characteristic-polynomial/root
   isolation.  Falsifier: a certified positive Ky Fan margin; a null packet
   is only `OBSERVED`.
3. **Perturbative active-face analysis.**  Derive a symbolic first/second
   variation at \(Q=I/2\) using the three-qubit marginal constraints.  A
   positive admissible directional coefficient gives a local countermodel;
   otherwise it may yield a rigidity lemma.  Falsifier: an active face with a
   verified positive coefficient.

## Selection

Choose mechanism 2 first: it has a decisive exact falsifier and tests the
coherent degrees of freedom that mechanisms 1 and the classical overlap leave
untouched.  It is not an enlarged version of the previous real low-support
packet: the state space is dense complex rational projectors.  Mechanism 1 is
the main rejected alternative and must be revisited if this packet is null;
mechanism 3 requires a nontrivial spectral-stratification setup and follows
only if a candidate shape or active face makes it discriminating.

# Cycles 063--070 preregistration: Roblot phase clarification

Frozen: 2026-07-31 UTC, before the new five-control replay and before
constructing a census population.

## Objective and claim boundary

This is a clarification branch, not a revival of the rejected
Dedekind/squared-multiplier formula.

1. Audit whether the five archived phase comparisons used any
   information from the analytic target to choose a weak-unit
   representative, character orientation, or Artin label.
2. Prove the exact relation between a Roblot weak solution and a true
   quartic Stark unit.
3. If a genuinely reconstructed Roblot-eligible quartic census
   population and a rigorous weak-unit coefficient evaluator are
   available, screen it for certified failures of quarter-turn
   quantization.

Positive ball overlap is not proof of equality. A census row may be
reported only as `CONSISTENT_WITH_QUANTIZATION` unless an independent
proved Stark identification closes it. A rectangular complex ball
disjoint from all four quarter-turns is a
`CANDIDATE_COUNTEREXAMPLE`; it halts the branch and must be rerun at
twice the precision through an independent code path before any
counterexample claim.

## Cycle allocation

- 063: circularity/provenance audit.
- 064: five-control replay under a data-independent gauge, if the
  provenance audit authorizes it.
- 065--066: lemma pair and source mapping.
- 067: freeze the census population from genuine census records;
  no proxy-derived eligibility is allowed.
- 068--070: rigorous phase-defect screen, subject to the population and
  evaluator gates.

## Frozen conventions

- \(G=\langle\gamma\rangle\simeq C_4\), with
  \(\chi(\gamma)=i\).
- For a weak unit \(\eta\),
  \(c_\chi(\eta)=\frac12\sum_{g\in G}\chi(g)
  \log|\eta^g|_w\), matching Roblot's Theorem 6.1 convention.
- The dominant-embedding gauge uses only the four logarithms of the
  independently constructed weak unit. It may not inspect \(L'\), a
  certified Stark packet, or a phase residual.
- If a proved Stark unit \(\epsilon\) and a weak solution satisfy
  \(\bar\eta=h\bar\epsilon\) for a trivial group-ring unit \(h\), the
  predicted ratio is recorded with the convention
  \(c_\chi(h\bar\epsilon)=\chi(h)c_\chi(\bar\epsilon)\); hence
  \(L'(0,\chi)/c_\chi(\eta)=\chi(h)^{-1}\).

## Gates and stop conditions

| Gate | Pass condition | Failure action |
|---|---|---|
| Circularity | representative, orientation, and labels all trace to data sealed before the analytic target was opened | preserve finding; do not call the old five-ratio replay independent |
| Control replay | all five ratios use only the frozen gauge and independently sourced orientation | mismatch halts theorem-to-data validation |
| Lemma | hypotheses and both implications follow from Roblot Thm. 6.1 plus the rank-one Stark formula, with conventions checked | narrow or reject statement |
| Population | every row is genuinely reconstructed and exactly satisfies (A1)--(A3); list and source hashes frozen before phase evaluation | no census |
| Rigorous evaluator | both \(L'\) and weak-unit coefficient are Arb balls from exact inputs; precision and tool versions recorded | no census |
| Counterexample | one row is disjoint from all \(\mu_4\)-rotations | immediate halt, doubled precision, independent rerun |

## Resource cap

The census screen is capped at one node-hour per row and five cycles in
this branch. Missing population metadata or missing rigorous weak-unit
construction is a scientific/tooling boundary, not authorization to
substitute floating point or proxy predicates.

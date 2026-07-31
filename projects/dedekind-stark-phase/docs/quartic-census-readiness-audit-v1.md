# Quartic phase-defect census readiness audit

Recorded: 2026-07-31 UTC.

## Verdict

`BLOCKED_BEFORE_TARGET_OPENING`.

The proposed Arb-rigorous phase-defect census was not run. Two
preregistered inputs do not yet exist at proof grade.

## Population gate

The census paper has a genuine, support-first higher-order stratum of
2,704 rows. Its execution plan lists “Roblot coverage” as a future
column of the higher-order taxonomy. The Effective-Stark master plan
marks construction of the H-eligibility columns as `READY`, not
`BANKED`.

Consequently there is currently no frozen set that can honestly be
called “the census paper's Roblot-eligible quartic H-rows.” The 881
Engine-C-eligible rows are not a substitute: Engine C is a descent
through imaginary-quadratic bases, whereas Roblot's (A1)--(A3) concern
the original cyclic-quartic extension over the totally real base.

The population gate therefore fails without opening a phase target.

## Rigorous-evaluator gate

The five existing Roblot constructors certify the algebraic unit and
unit-lattice data exactly, but record the logarithmic Fourier
coefficient as a high-precision point evaluation. The phase project's
own tag is `NUMERICAL_FROM_EXACT_UNIT`.

The archived \(L'\)-targets are rigorous complex balls. The weak-unit
side is not. No independent script in this project currently:

1. isolates every relevant real embedding by Arb balls;
2. evaluates every algebraic-unit logarithm as a certified ball;
3. forms \(c_\chi(\eta)\) with outward rounding;
4. proves separation from, or overlap with, each of the four rotated
   \(L'\)-balls.

The evaluator gate therefore also fails.

## Implication of the clarification lemma

Even after both gates are built, the census is a falsification screen,
not a proof campaign:

- certified separation from all four rotations would refute the
  quartic rank-one Stark conjecture for that row and triggers immediate
  escalation;
- overlap with one rotation is only certified numerical consistency;
- exact quantization in an uncertified row is equivalent to the
  conjecture and cannot be promoted from finite-radius overlap.

## Minimal reopening sequence

1. In the census project, genuinely construct the quartic quotient
   field for every relevant H-row and check (A1)--(A3) exactly.
2. Freeze the resulting case/character list and hashes before
   evaluating phases.
3. Implement and anchor a rigorous algebraic-unit logarithm evaluator
   on the five controls.
4. Reconstruct the real-quartic/analytic character orientation from
   exact Artin transport, also before opening \(L'\).
5. Only then run the counterexample screen.

No floating-point pre-screen is authorized to delete rows or define
the proof-grade population.

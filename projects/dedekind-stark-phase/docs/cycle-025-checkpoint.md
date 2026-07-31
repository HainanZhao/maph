# Cycle 025 checkpoint: bounded continuation gate

Banked: 2026-07-30 UTC.

## Verdict

**CONTINUE.** The five-cycle gate passed.

All five original cyclic-quartic controls genuinely satisfy Roblot's
(A1)--(A3). RQ-000129 was selected by the frozen cost rule. Its
Roblot weak solution was constructed from the exact minus-unit module,
the genuine embedded \(K^+\)-unit lattice, and the trivial minus class
group without reading an \(L'\)-value, packet polynomial, or Engine-C
unit.

After the corrected constructor was sealed, the analytic record was
opened. With the sealed convention \(\chi(\gamma)=i\), the archived
analytic record corresponds to \(\chi^{-1}\), and the comparison gives

\[
c(\eta)=i\,\overline{L'(0,\chi^{-1})}
\]

to the full available precision. Equivalently, the phase defect is
zero modulo \(\pi/2\). Both component differences lie inside the
certified rectangular \(L'\)-ball.

This is the first legitimate independent calibration point for the
Dedekind--Rademacher phase project.

## Preserved failed seal

The initial sealed constructor returned \(e=2\) and missed the analytic
magnitude by \(\sqrt2\). It had substituted
\((\bar U_K)^{\gamma^2}\) for the embedded
\(\bar U_{K^+}\). These are not equal here. The corrected exact
calculation gives

\[
[\bar U_{K^+}:N\bar U_K]=2,\qquad e=1.
\]

The failed v1 artifact remains in the ledger. No theorem or conjecture
tag was issued from it.

## Five-cycle ledger

| Cycle | Result | Status |
|---:|---|---|
| 021 | Roblot Theorem 6.1 translated to an executable unit-lattice formula | BANKED |
| 022 | Genuine (A1)--(A3) screen of all five original quartic fields | 5/5 PASS |
| 023 | First independent constructor sealed | PRESERVED_FAILURE |
| 024 | Proxy isolated; genuine \(K^+\) norm index and corrected constructor sealed | PASS |
| 025 | Inverse-character convention aligned; independent phase defect opened | PASS |

## Claim boundary

- Exact field, unit-lattice, norm-index, and algebraic-unit statements:
  `VERIFIED_EXACT`.
- The logarithmic Roblot coefficient: high-precision `NUMERICAL`.
- The \(L'\)-value: certified rectangular ball inherited from the
  Effective Stark archive.
- The phase-law relation at this one point: `NUMERICAL_PHASE_MATCH`.
- No Dedekind-sum formula has been fitted or promoted.

## Recommendation

Continue for a second bounded block:

1. construct the independent coefficients for the remaining four
   controls, with RQ-001280 next because its class group is also
   trivial;
2. freeze the admissible Dedekind--Rademacher feature map before
   opening their phase defects;
3. require route/generator inversion invariance;
4. stop if the five-point feature matrix has rank below the frozen
   coefficient count or if any independently opened defect violates
   the proposed congruence class.

The fifty-row holdout remains premature.


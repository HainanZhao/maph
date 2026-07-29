# SIC--Stark research cycle 160: Paper-II referee correction

Date: 2026-07-29

## Gate reopening

The dimension-seven publication gate was reopened after a referee
identified that admissibility permits two form conductors. The prior
Cycle-158 replay was arithmetically valid for its packet but its scope
inference was not: covariance transports only within a fixed
discriminant.

The exact new scope audit
`scripts/dimension_seven_admissible_strata.gp` proves:

```text
D7_F1=2
D7_FORM_CONDUCTORS=[1, 2]
D7_DISCRIMINANTS=[8, 32]
D7_Q8=[1, -4, 2]
D7_Q32=[1, -6, 1]
D7_WIDE_CLASS_NUMBER_8=1
D7_WIDE_CLASS_NUMBER_32=1
D7_CERTIFIED_STRATUM_DISCRIMINANT=32
D7_OPEN_STRATUM_DISCRIMINANT=8
```

## Forensic result

The existing exact certificate is the conductor-two, discriminant-32
calculation, not the discriminant-8 calculation:

- `dimension_seven_phase_audit.py` uses
  \(Q_{7,2}=\langle1,-6,1\rangle\), conductor \(2\), and stabilizer
  \(\left(\begin{smallmatrix}204&-35\\35&-6\end{smallmatrix}\right)\);
- the analytic fixed point is \(3+2\sqrt2\);
- the determinant-two map sends the auxiliary reduced maximal-order
  point \(2+\sqrt2\) to that fixed point;
- the degree-48 exact reconstruction verifies both formal shifts and
  all \(441\) minors for this discriminant-32 tuple.

The manuscript had displayed the auxiliary maximal-order point and
lowered stabilizer without displaying the certified form and tuple
stabilizer. It then incorrectly described wide-class transport within
discriminant 32 as transport over all dimension-seven forms.

## Resolution

Paper II is rescoped rather than starting a new analytic packet during
the publication cycle:

- dimension seven: theorem proved for every admissible form of
  discriminant \(32\);
- dimension seven, discriminant \(8\): explicit open target;
- dimension eight: both discriminants \(5\) and \(45\), unchanged.

A direct substitution of \(2+\sqrt2\) into the existing
discriminant-32 packet formula was also run as a `NUMERICAL`
diagnostic and did not produce an idempotent reconstruction. This is
not a negative theorem about discriminant 8; it confirms only that the
existing packet cannot be relabeled as a proof of that stratum.

Cycle 158 is therefore superseded only in its universal scope verdict.
Its discriminant-32 exact replay remains valid.

## Referee regressions repaired

Paper II now includes:

- both dimension-seven conductors, discriminants, and representative
  forms;
- the certified form \(Q_{7,2}\), its fixed point, tuple stabilizer,
  lowering stabilizer, and exact phase;
- the complete 32-divisor table for the safe exponent \(16128\), plus
  its generated HNF transcript;
- the full reciprocal degree-16 packet polynomial, its
  \(2,2,12\) factorization, all Sturm intervals, and exact
  Artin/Frobenius labels;
- the raw Arb error
  \(\epsilon_{\log}\le5.86\cdot10^{-11}\), not only its powered form;
- the \(\Q(\sqrt{-6})\) modulus
  \(\mathfrak p_2^3\mathfrak p_3\mathfrak p_5\) underlying cyclic
  coordinates \([8,4]\);
- the explicit \(|S_M|=4\ge3\) hypothesis for Stark's global-unit
  clause;
- the script certifying \(e=|\mu(E_b)|=2\);
- a citation to companion Paper I;
- platform, runtime, memory, archive, and Zenodo-status text.

`tests/test_paper_ii_referee_regressions.py` locks these manuscript
features against future deletion.

## Publication status

The corrected source and PDF compile without warnings. The Paper-II
archive passes all 16 clean-extraction tests, builds byte-identically
twice, and verifies its self-checksum manifest. The standalone arXiv
source archive also compiles twice after clean extraction.

The mathematical publication hold is cleared at the corrected scope.
External Zenodo and arXiv account actions remain pending; no DOI or
submission predates this gate.

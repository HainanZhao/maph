# Cycle 183 preregistration: intercept-cleared primitive ray boxes

## Question

Can the `X^(21/25-o(1))` Cycle-181 common-intercept stable packet be converted
to a populated, coefficient-preserving inverse object rather than merely a
line partition? The proposed engine clears the common intercept, factors the
stable cross determinant through primitive rays, and performs one frozen
dyadic selection on the *complete stable rectangle state*.

## Frozen state

- Fix a Cycle-181 packet `rho=p/v`, reduced, and use every Cycle-182 full
  fibre line `j=(A/U)h+p/v` with `U=v*u`, `gcd(A,U)=1`, `N>=2`, and its
  base height residue. Retain the actual labels, all physical rows, residuals,
  slope determinant, and stable product shell.
- Retain the inherited actual-exponential chart `1<=ell<=c*Delta` with fixed
  `0<c<1` (Cycle 177). Thus the positive label gap satisfies `r<Delta`, which
  is the frozen cap for its dyadic field.
- A stable rectangle chooses labels `ell!=m`, a pair separation of `r`, and
  two line-step multipliers `k,q>=1`. Its physical gaps and numerator gaps
  are

  ```text
  d=k*U,  a=k*A,       e=q*V,  b=q*B.
  ```

  Freeze `D=e*a-d*b`, `K0=(4C/pi)HDelta/X`, and
  `r*k*q*U*V>=K0`. No aggregate pair count may replace `k,q` or its two
  physical pairs.
- Freeze dyadic ranges for the seven positive integer parameters
  `(N_ell,N_m,U,V,k,q,r)`. The number of admissible boxes is bounded before
  selection by

  ```text
  B_box = b_R^4 * b_H^2 * b_Delta,
  b_R=bit_length(2R), b_H=bit_length(H), b_Delta=bit_length(Delta).
  ```

  Here `bit_length(M)` is the number of base-two ranges meeting positive
  integers at most `M`. A failed box remains an empty row, not a deleted
  candidate.

## Proposed engine

Writing `U=v*u` and `V=v*w`, the intercept-clearing coordinates are

```text
t=h/u,       J=v*j-p=A*t,
s=h'/w,      K=v*j'-p=B*s.                                 (1)
```

Thus each fibre becomes an integral ray segment with one residue class
modulo `v`. Freeze the primitive cross-ray determinant

```text
F=w*A-u*B,
D=k*q*v*F.                                                  (2)
```

The engine must prove `F!=0`, retain its two-sided stable comparison with
`r*U*V/(v*Delta)`, and derive the row-sensitive near-orbit bounds

```text
||U*alpha_ell|| <= 2C/((N_ell-1)X),
||V*alpha_m|| <= 2C/((N_m-1)X).                             (3)
```

for every rectangle side. If a critical stable packet has mass `W`, the
frozen dyadic partition must exhibit one full ray box of mass at least
`W/B_box`, where `B_box` is the preregistered logarithmic box count.

## Advance and failure rules

Advance only if the following are proved.

1. (1)--(3), including the exact factorization `D=k*q*v*F`, are valid with
   all physical and coefficient fields retained.
2. The stable box selection gives an actual populated primitive-ray
   exponential near-orbit class from any critical packet; it may not select
   parameters after observing a box population.
3. The result is explicitly scoped as a nonrational **candidate saturation
   class**, not an in-packet upper bound, recurrence, density gain, or
   interval result.

Falsifiers are a legal packet row with `u` not dividing `h`, failure of (2),
`F=0` at distinct labels, loss of a pair multiplier/residual/stable shell, or
a stable rectangle missing from the frozen dyadic partition.

## Amendment log

- 2026-08-02: initial preregistration. The transformed coordinates,
  determinant family, seven dyadic fields, and population rule are frozen
  before replay construction.
- 2026-08-02: made the already stated product of logarithmic bin counts
  explicit as `B_box=b_R^4*b_H^2*b_Delta` before final replay. The earlier
  toy identity check is exploratory only; the sealed selection uses this
  formula.
- 2026-08-02: stated the inherited `0<c<1` label chart explicitly, so the
  `bit_length(Delta)` label-gap cap is tied to the frozen actual scale rather
  than an implicit convention. Earlier toy replay remains exploratory.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 183,
  "parameters": {
    "actual_label_chart": {
      "kind": "symbolic",
      "value": "1 <= ell <= c*Delta with fixed 0<c<1; r<Delta",
      "rationale": "inherits the actual positive-exponential chart and bounds the seventh dyadic field"
    },
    "light_fibre_cap": {
      "kind": "expression",
      "value": "N_ell,N_m,k,q <= 2R",
      "rationale": "Cycle-178 light branch and complete C182 fibre segments"
    },
    "stable_product": {
      "kind": "expression",
      "value": "r*k*q*U*V >= (4C/pi)*H*Delta/X",
      "rationale": "retains the C180 stable branch without scalarization"
    },
    "dyadic_box_cap": {
      "kind": "expression",
      "value": "B_box=bit_length(2R)^4*bit_length(H)^2*bit_length(Delta)",
      "rationale": "seven frozen fields (N_ell,N_m,U,V,k,q,r)"
    }
  },
  "resource_caps": {
    "numerical_search": {
      "kind": "integer",
      "value": 0,
      "rationale": "only exact rational replay fixtures; no parameter search may select a ray box"
    },
    "formula_family": {
      "kind": "text",
      "value": "intercept-cleared rays and the primitive determinant F=wA-uB only",
      "rationale": "prevents an unregistered substitute census"
    }
  },
  "formula_families": [
    "v*j-p=A*(h/u) with U=v*u",
    "D=k*q*v*(w*A-u*B)",
    "seven-field dyadic ray box selection"
  ],
  "selection_rule": [
    "assign every stable rectangle all seven dyadic fields before grouping",
    "select a maximum-count box with the deterministic lexicographic tie break"
  ],
  "failure_rule": [
    "record an unclassified stable rectangle or an exceeded B_box as failure",
    "do not promote a box after a post-result cap or formula-family change"
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T13:30:37Z",
    "git_head": "7f0f50dfc209d9ec3d73e6cfff9a5fcea11465e3",
    "git_state": "C183 and generic preflight pilot files untracked; prior toy checks are exploratory; this manifest freezes the certified replay boundary"
  },
  "input_paths": [
    "artifacts/cycle-180-cross-label-pair-determinant-v1.json",
    "artifacts/cycle-181-common-intercept-packet-v1.json",
    "artifacts/cycle-182-fibre-line-rigidity-v1.json"
  ]
}
-->

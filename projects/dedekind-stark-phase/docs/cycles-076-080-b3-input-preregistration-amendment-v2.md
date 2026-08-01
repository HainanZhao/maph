# B3 input preregistration amendment v2: exact field gate

Frozen: 2026-07-31 UTC, after the full-`bnfcertify` pilot and before
any population row is promoted.

## Preserved resource finding

The first 800-kernel segment used `bnfinit(P,1)` and `bnfcertify` on
every absolute degree-eight field and its real quartic subfield.  This
is stronger than A1--A3 require because it proves class-group and unit
data that never enter an eligibility predicate.  It produced 799 exact
screens, including 45 A3 failures, and one contained PARI
`bnrclassfield` segmentation fault.

The next two \(D=91\) kernels each spent more than ten minutes in this
irrelevant class/unit certification layer.  The monolithic first run
and the attempted continuation are preserved as operational failures.

## Corrected uniform exact gate

The final population replay must use one uniform field-only gate:

- retain certified `bnfinit`/`bnfcertify` for the real quadratic base,
  because its ray class group constructs the extension;
- construct the absolute degree-eight polynomial exactly and require
  `polisirreducible(P)=1`;
- use exact `nfinit` data for degree, signature, and automorphisms in
  A1;
- construct the unique totally real quartic subfield exactly and use
  `nfinit` for its degree and signature in A2;
- use the exact ray-character local criterion frozen in amendment v1
  for A3.

No class number, regulator, or unit group of the degree-eight or
quartic field appears in A1--A3.  Omitting their class/unit
certification therefore removes an irrelevant computation; it does
not weaken any eligibility predicate.

The 800-row stronger pilot remains evidence and a cross-check, but the
final population artifact must rerun all 2,245 kernels through this
uniform field-only path.  Tool failures and resource failures remain
explicit rows.


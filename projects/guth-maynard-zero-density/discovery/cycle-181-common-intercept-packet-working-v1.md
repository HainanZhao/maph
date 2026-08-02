# Cycle 181 working ledger: common-intercept packets

## Frozen question

Use the Cycle-180 complete stable rectangle state to test whether the common
fixed `beta` exactifies a new four-row intercept invariant. See the linked
preregistration for the frozen formulas and advance criteria.

## Working derivation (CONJECTURED until sealed)

For a left pair put `delta=a-d alpha_ell` and
`eta=j1+beta-h1 alpha_ell`. Then

```text
q+d beta = d eta-h1 delta.
```

Since the first row may have height `2H`, this gives
`|q+d beta|<=5 C H/X`; applying this at both labels suggests
`I=e q-d q'` is an integer bounded by `10 C H^2/X`, so it should vanish at
the frozen cutoff. If valid, `q/d=q'/e` is a common rational intercept.

## Candidate engine and falsifier

The engine is a rational-intercept packet decomposition of the *complete*
stable rectangle census. Its decisive falsifier is an exact admissible
four-row test vector satisfying the residual bounds but with nonzero `I`.
The code prototype must exercise both a nonzero-beta packet and the
denominator/divisibility route; no floating-point recognition closes this
claim.

## Log

- 2026-08-02: opened from C180. No result promoted.
- 2026-08-02: corrected the height constant before replay construction;
  retained the same formula family and exactification mechanism.
- 2026-08-02: the first exact toy fixture used `x=1000`, which violates the
  frozen `10 C H^2/x<1` cutoff at `H=20`. Raised only the fixture scale to
  `x=100000`; this is a test setup correction, not a mathematical failure.

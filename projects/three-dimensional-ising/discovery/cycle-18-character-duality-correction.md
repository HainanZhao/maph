# Cycle 18 — character-duality correction

## Decision question

Does the arbitrary-width internal-cut proof use the cochain extracting the
coefficient multiplied by `lambda_b`, and does that cochain remain
frontier-determined after the triangular symplectic correction?

## Questioning the question

For `h=sum_i(x_i a_i+y_i b_i)`, the symplectic pairing forces

    x_i=<h,b_i>,   y_i=<h,a_i>.

Hence `lambda_a` uses `PD(b_i)` and `lambda_b` uses `PD(a_i)`.  A proof about
the exposed longitude `b_i` proves locality of the wrong character.

## Exclusion map

- Former claim: the exposed longitude cocycle proves H3.
- Falsifier: on the one-handle class `a_i`, `PD(b_i)(a_i)=1` while the
  `b_i` coefficient is zero.
- Claim-boundary delta: the published written proof of the arbitrary-width
  internal bond is withdrawn until the meridian-dual proof and its transport
  firewall close.  Pair-cut results and finite exact rank certificates are
  not falsified by this coordinate mismatch.

## Selected mechanism and acceptance rule

Use the pushed-off exposed meridian in the planar cut collar.  Its cellular
intersection cochain differs from `PD(a_i)` only by a collar coboundary and,
as a proper arc in the disk collar, equals `delta s_i`.  Under
`b_j=tilde b_j+sum_k U_kj a_k`, Poincare duality gives

    alpha_j=tilde alpha_j+sum_k U_kj beta_k,
    beta_j=tilde beta_j.

Accept only if the manuscript proves the push-off statement, the exact GF(2)
firewall verifies the crossed character table and column indexing, the
finite canonical internal ranks replay, and the denominator-free core replay
still agrees with the independent reference.

## Falsifier

Any relative cycle on the exposed side with zero frontier trace and nonzero
`PD(a_i)` evaluation, or any triangular correction that changes `beta_i`,
invalidates the repaired H3 proof.

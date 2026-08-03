# Cycle 221 / B058 preregistration: forced tilde-sector inversion correction

Cycles 219--220 leave exactly two sign choices that match the raw negative-`k`
state in `tau`, `u`, and `tilde-tau`; their sole product-coordinate defect is
`tilde-u` negation. This block derives the one Pochhammer ratio forced by that
defect and tests the resulting, newly proposed extension without fitting.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":221,
  "parameters":{
    "frozen_survivors":{"kind":"expression","value":"Freeze M_+=(p,k,r,s)=(-5,24,115,24), raw M_-=-M_+, and exactly the two Cycle-219 tau/u sign survivors (a,b,c,d)=(sigma,-1,sigma,-sigma), sigma in {+1,-1}. For each, freeze the exact coordinate consequence tau_+=tau_-, u_+=u_-, tilde-tau_+=tilde-tau_-, and tilde-u_+=-tilde-u_-.","rationale":"The correction may repair only the observed single sector defect; no broader sign family is reopened."},
    "forced_correction":{"kind":"expression","value":"With z=exp(2*pi*i*tilde-u_-) and qtilde=exp(2*pi*i*tilde-tau_-), freeze C(z;qtilde)=(qtilde*z;qtilde)_infinity/(qtilde*z^(-1);qtilde)_infinity. Define the only candidate H_sigma=C(z;qtilde)*Gamma_{M_+}(sigma*mu,-m;sigma*omega1,-sigma*omega2). No additional scalar, Z multiplier, B_2,2 counterterm, theta factor, shift, swap, branch, or label correction is permitted.","rationale":"The numerator ratio is forced by equality of the two unnormalized product sectors after tilde-u inversion; all other correction freedom is excluded."},
    "identity_tests":{"kind":"expression","value":"Derive C(z)C(z^(-1))=1 and its exact transformations under the source omega1/r and omega2/-1 shifts. Then test: product-sector equality at both sigma values; simultaneous-sign involutivity; normalized reflection; both normalized shifts (38)--(39); and source factorization identities (16)--(17), retaining every residual ordinary-gamma factor. A failed identity contains this sole correction construction.","rationale":"A forced product match is not an extension unless the frozen source identities survive."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only if the explicit H_sigma satisfies every listed test with source normalization unchanged. If an identity is undefined because the source supplies no signed-matrix counterpart, record the exact missing interface and do not treat formal product equality as a Gamma_M extension. Do not claim a general signed-k extension, packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"This is a constructed bridge attempt with a narrow, falsifiable acceptance condition."}
  },
  "resource_caps":{"sign_survivors":{"kind":"integer","value":2,"rationale":"Exactly the two sealed tau/u survivors."},"product_coordinates":{"kind":"integer","value":4,"rationale":"tau, u, tilde-tau, tilde-u."},"functional_identity_families":{"kind":"integer","value":5,"rationale":"Involutivity, reflection, two shifts, and factorization."},"wall_seconds":{"kind":"integer","value":240,"rationale":"Exact symbolic Pochhammer/theta algebra only."},"floating_point":{"kind":"not_applicable","justification":"All comparisons are formal product identities and exact coefficient algebra.","rationale":"No numerical Gamma_M evaluation is admissible."}},
  "formula_families":["Sarkissian--Spiridonov equations (3), (5)--(8), (16)--(17), normalized reflection (33), shifts (38)--(39)","q-Pochhammer inversion and Jacobi theta product","Cycle-219 tau/u survivors","Cycle-220 reflection reduction"],
  "selection_rule":["Derive C from the frozen tilde-product ratio before testing any identity.","Use both and only the two sealed tau/u survivors.","Preserve every residual factor and mark a missing signed-matrix law as a failed extension requirement, not as a scalar convention."],
  "failure_rule":["Do not fit a scalar, alter Z(m), add a B_2,2 counterterm, change branch, add a second theta/Pochhammer factor, shift, swap, or relabel after an identity fails.","Do not declare unnormalized product equality to be a normalized Gamma_M extension.","Do not infer any packet, AFK, fusion, Stark, or TCC consequence."],
  "pre_execution":{"timestamp_utc":"2026-08-03T07:18:00Z","git_head":"adef381ad13a02d254788a20723b86aacf7fb0d8","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-220-b057-normalized-reflection-v1.json","proof/verify_cycle_220_normalized_reflection.py","proof/verify_cycle_219_signed_k_extension.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->

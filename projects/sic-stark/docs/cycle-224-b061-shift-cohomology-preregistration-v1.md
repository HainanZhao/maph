# Cycle 224 / B061 preregistration: joint signed-shift cohomology

Cycle 223 leaves a universal second-shift residual. This block solves the
two-generator shift-cocycle problem and then applies that uniquely determined
cochain to the same live signed-product construction.

Amendment — 2026-08-03: companion review determined that reflection,
involutivity, and factorization are dependent acceptance tests of this already
authorized construction, not a new cycle. No cochain family, residual, or
passing criterion has been broadened.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":224,
  "parameters":{
    "frozen_shift_lattice":{"kind":"expression","value":"Freeze the raw signed shift actions T1:(mu,m)->(mu+omega1,m-115) and T2:(mu,m)->(mu+omega2,m-1), acting on u=tilde-u_- by T1:u->u-24 and T2:u->u-tilde-tau. Freeze the Cycle-223 residuals rho1=1 and rho2=exp(-pi*i*tilde-tau) required to cancel the old first/second shift defects.","rationale":"The two commuting translations and their residuals are fully determined by the sealed explicit-product audit."},
    "cochain_family":{"kind":"expression","value":"Use only D_a(u)=exp(pi*i*a*u), with a an exact scalar independent of mu,m,omega1,omega2. Require D_a(T1 u)/D_a(u)=rho1 and D_a(T2 u)/D_a(u)=rho2 as meromorphic identities. Quotient only by factors invariant under both T1 and T2; do not admit arbitrary theta, Pochhammer, polynomial, or fitted factors.","rationale":"This is the minimal argument-dependent exponential family capable of carrying the observed half-period residual."},
    "integrability_and_boundary":{"kind":"expression","value":"Check T1*T2=T2*T1 on the full cochain ratios, solve a exactly, and record uniqueness modulo joint invariants. If and only if this shift system closes, compose that exact D_a with the frozen Cycle-223 product and test the full raw reflection argument/label map, double-sign involutivity, and both factorization identities (16)--(17), retaining every ordinary-gamma residual factor.","rationale":"Commutator integrability is a necessary precondition; the dependent acceptance tests decide whether the single live construction is an extension."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only if the unique minimal cochain satisfies both shifts and the commutator and the combined product then satisfies reflection, involutivity, and both factorization identities. It is a new construction, not a source-derived signed Gamma_M law. A failed dependent test contains this full construction. Do not claim a packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"Shift closure is necessary but not sufficient for the program gate."}
  },
  "resource_caps":{"shift_generators":{"kind":"integer","value":2,"rationale":"The two normalized source shifts."},"commutator_cells":{"kind":"integer","value":1,"rationale":"One fundamental T1/T2 square."},"cochain_parameters":{"kind":"integer","value":1,"rationale":"Minimal exponential exponent a."},"dependent_identity_families":{"kind":"integer","value":3,"rationale":"Reflection, involutivity, and the paired factorization family."},"wall_seconds":{"kind":"integer","value":240,"rationale":"Exact symbolic lattice and product identity algebra."},"floating_point":{"kind":"not_applicable","justification":"All equations are symbolic exponent identities.","rationale":"No numerical Gamma_M evaluation is admissible."}},
  "formula_families":["Sarkissian--Spiridonov normalized reflection (33), shifts (38)--(39), and factorization identities (16)--(17)","Cycle-223 exact residual multipliers","Multiplicative cohomology of the commuting two-shift lattice","Minimal exponential cochain"],
  "selection_rule":["Use exactly the two frozen shifts and residuals.","Solve the exponential coefficient before considering any larger cochain family.","Record uniqueness only modulo jointly shift-invariant factors.","Apply only the resulting D_a, without alteration, to the frozen Cycle-223 product for the dependent acceptance tests."],
  "failure_rule":["Do not add a theta/Pochhammer, polynomial, branch, scalar, or label factor after solving the minimal equations.","Do not call a cochain source-derived or use it to infer packet statements before the dependent reflection/factorization tests pass.","Do not infer any AFK, fusion, Stark, or TCC consequence."],
  "pre_execution":{"timestamp_utc":"2026-08-03T07:58:00Z","git_head":"2988fc65c865d0ac6d5a06079413b318b9ee1e70","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-223-b060-explicit-signed-product-v1.json","proof/verify_cycle_223_explicit_signed_product.py","proof/verify_cycle_222_z_label_cocycle.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->

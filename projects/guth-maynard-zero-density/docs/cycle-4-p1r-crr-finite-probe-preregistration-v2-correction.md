# Cycle 4 P1R-CRR finite-analogue probe preregistration v2 correction

## Claim boundary and disposition of v1

`OBSERVED`: the v1 preregistration is immutable but **not executable as
written**.  It leaves the initial maps called “jittered frame,” “bounded
jitter,” “uniform distinct stream,” and the spectral construction unspecified;
it also gives no phase denominator for F2, F3, or F5, no exact proxy formula,
and an infeasible literal reading of “every complex quantity” during all
20,480 mutations.  Thus v1 is `CONTAINED_UNEXECUTABLE`, not an executed
search and not evidence about CRR compatibility.

This v2 correction retains the exact 160 row identifiers, row order, master
seed, SplitMix64 seed words, `N,H,R,Q,V` scales, variants, thresholds,
128-proposal budget, 16/32 Farey orders, 8/12 cubic modes, 5% margins,
55-minute aggregate cap, 1-GiB RSS cap, and all-miss interpretation.  It
only supplies the missing deterministic execution conventions.  No result was
consulted in choosing them.  The correction proves no continuous CRR claim,
no extremizer, no saturation theorem, no density improvement, and no
short-interval consequence.

Every finite retained configuration remains `OBSERVED`; complex outcome
values are `RECOGNIZED`, never certified numerical enclosures.  A miss,
resource cap, or recognition failure does not imply a universal negative.
No hostile audit is initiated during this research-stage discovery run.

## Exact v2 execution conventions

`PROVED` (as a definition):
[the v2 conventions module](../conventions/crr_finite_analogue_probe_v2.py)
is the source of truth for the following fully specified rules.  It must be
hash-pinned in the sealed artifact and the runner must reject a mismatch.

- The five row families retain their v1 names and parameters.  Their missing
  phase counts are now fixed without adding variants: F2 uses `4*macrocells`,
  F3 uses `4*packet_denominator`, and F5 uses `4*spectral_rank`.  Hence their
  phase counts are respectively `(8,12,16,24)`, `(8,12,20,28)`, and
  `(8,12,16,20)`.
- F1 takes the `j`th lattice frame point `floor(jH/R)` and a one-word jitter
  in `[-floor(H/(8R)),floor(H/(8R))]`.  F2 sends `j mod k` to macrocell `k`,
  uses the within-cell rational frame and jitter radius `floor(h/(8r_c))`.
  F3 uses lane `j mod d`, base
  `floor(qH/r_lane)+floor(lane*H/d)`, and radius `floor(H/(16R))`.  F4 uses
  one uniform stream residue per requested member.  F5 uses one stream word
  per inverse pair, maps it through multiplication by the listed rank modulo
  `floor((H-1)/2)`, inserts the residue and then its additive inverse, and
  appends `0` when `R` is odd.
- In every case, inserting residue `a` scans `a,a+1,...` cyclically and takes
  the first unused residue; a scan uses no new random word.  An all-group
  scan is `INIT_INVALID`.  The exact number and order of stream consumptions
  is in `CONSTRUCTION_CONTRACT`.
- For non-chirp families, every coefficient is the least-index nearest of the
  stated equally spaced unit phases to the normalized Fourier sum
  `sum_{t in W} exp(-2*pi*i*n*t/H)`; a zero sum selects phase one.  F4 is the
  stated quadratic chirp.  Coefficients are rebuilt from the current same
  `W` after every proposal.
- A proposal consumes one word for the index in sorted `W`, removes it, then
  consumes one word for a collision-repaired insertion.  Exactly 128 are
  attempted, and the strictly frozen score is
  `min(LV/lv_cut,min(E/e_low,e_high/E),mu16/mu_cut,C8/c_cut)`, with score
  `-infinity` for a nonfinite quantity or nonpositive `C8`.  It is accepted
  precisely when its rise is at least `2^-40`.

The runner computes energy by exact ordered pair-sum counts.  For the cubic it
uses the finite-rank identity
`tr(B_M^3)=tr((A-MI)^3)`, where
`A=U diag(w) U*`, `U_{t,m}=exp(2*pi*i*m*t/H)`,
`m in {+-1,...,+-M}`, and `w_m=1-|m|/(M+1)`.  This is an algebraic speed-up,
not a change of `B_M` or its signed proxy.

## Precision correction

The 16-node/mode-8 mutation score is expressly a deterministic NumPy 1.26.4
binary64/complex128 proxy.  It is not a final complex calculation and is
reported only as a mutation aid.  Final binary64 diagnostics score every row;
then mpmath 1.2.1 re-evaluates at 256 and 384 bits the first failing complex
diagnostic, or all complex diagnostics of a provisional binary64 hit.  A
complex outcome is accepted as a failure only when both precisions lie
strictly on the failing side of the unchanged threshold.  Otherwise it is
`RECOGNITION_RADIUS` (or `REPLAY_MISMATCH` on replay divergence).  The
recognition ball is centred at the 384-bit value with the v1 empirical radius;
it remains a stability screen, not interval arithmetic.

This correction makes the high-precision requirement target outcome-bearing
diagnostics rather than every one of the 20,480 exploratory proxy calls.  It
preserves the original final scientific thresholds while making the aggregate
cap meaningful.

## Resource and retention rule

The runner checks elapsed monotonic time and current process RSS before every
row and proposal.  At 55 minutes or 1 GiB it records the active row as
`RESOURCE_CAP` and every remaining row exactly once as `GLOBAL_CAP_UNREACHED`.
No resume, rerun, row reordering, threshold change, or post-result family
selection is allowed.  Otherwise every scheduled row is retained exactly
once as `RETAINED_HIT`, `NO_RETAINED_HIT`, or an existing frozen failure code.

The runner, sealed artifact, concise results note, and tests are separate
post-seal files.  They must not alter v1 or v2 preregistration files.


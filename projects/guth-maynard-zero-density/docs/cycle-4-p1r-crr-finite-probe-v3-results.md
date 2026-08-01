# Cycle 4 P1R-CRR finite-analogue probe v3: results

## Claim boundary

`OBSERVED`: all 160 pre-registered finite rows completed.  This is evidence
only about the v3 finite surrogate and its five frozen construction families.
It proves neither CRR compatibility nor incompatibility, no extremizer or
saturation theorem, no zero-density improvement, and no short-interval
consequence.  In particular, this all-miss table is **not** a universal
negative statement.

Complex final values are `RECOGNIZED`, not certified numerical enclosures.
No hostile audit was initiated; paper-stage promotion remains the appropriate
place for that review.

## Outcome

`OBSERVED`: the exact 160-row schedule was retained once per row, with
`160 NO_RETAINED_HIT`, `0 RETAINED_HIT`, and no resource or recognition-cap
row.  Each row completed all 128 prescribed proposals.  The aggregate run
took 713.816 seconds and reported peak RSS 564,809,728 bytes, below the
sealed 3,300-second and 1,073,741,824-byte caps.

`RECOGNIZED`: in every row, both `C8` and `C12` were positive and the `C12`
size threshold passed at 256 and 384 bits; the failure was uniformly the
frozen mode-agreement condition.  The relative `|C8-C12|` discrepancy ranged
from 0.1731800247 to 0.4241937834, exceeding the required 0.05 in every row.
The dual-precision evaluations agreed on that failure.  This localizes the
finite-model miss to the low-mode cubic-proxy stability screen, not to a
nonpositive cubic trace or its magnitude cutoff.

This is a lead for analytic construction work, not a no-go result: the proxy
may be sensitive to modes 8 versus 12 in a way the continuous CRR cubic term
is not.  Any change to that screen requires a new preregistration rather than
a rerun or reinterpretation of these rows.

## Corrections retained

`OBSERVED`: v1 remains `CONTAINED_UNEXECUTABLE` because it lacked executable
family/phase/proxy/precision rules.  V2 remains `CONTAINED_UNEXECUTED` because
the low-rank cubic trace did not explicitly prohibit the wrong `2M`-dimensional
diagonal shift.  V3 states and uses the ambient identity

```text
tr(B_M^3)=tr((DG)^3)-3M tr((DG)^2)+3M^2 tr(DG)-R M^3.
```

The first v3 launch then failed before row 0 on a wrapper frozen-hash-key bug;
its standalone record confirms zero RNG draws and zero scheduled rows.  The
post-seal runner correction was regression-tested before the successful v3
launch.  These are protocol corrections, not research outcomes.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v3.py --check
python3 discovery/run_cycle_4_p1r_crr_finite_probe_v3.py --check
python3 -m unittest tests.test_cycle_4_p1r_crr_finite_probe_v3
```

The full retained rows, final sets, binary diagnostics, and dual-precision
cubic outcomes are in
`discovery/cycle-4-p1r-crr-finite-probe-v3.json`.


# Cycle 161 preregistration: phase-aligned four-cycle or labelled star refinement

Date frozen: 2026-08-02 UTC.

Freeze a Cycle-160 cell of effective multiplicity `X^(1/75-o(1))`, split it
into 24 half-open subcells of width `1/(24K)` and 12 coefficient-phase sectors
of width `pi/6`. Retain ordered `u!=v` edges
`r=(u,v)`, `delta_r=z_u-z_v`, `b_r=a_u conjugate(a_v)`, and all atom, anchor,
denominator, tail, orientation, and coefficient labels. Freeze the star
threshold `tau_*=X^(-1/300)` and an error budget below `1/600`.

In one retained subcell/sector write `x_r=|b_r|`, `L=sum_r x_r`, and
`D_x=sum_(r: x endpoint of r)x_r`.

Required dichotomy:

1. If `max_x D_x<tau_*L`, then all but `O(tau_*L^2)` weighted ordered
   edge-pair mass is disjoint. For every disjoint pair, the frozen geometry
   gives `|delta_r-delta_s|<=1/(24K)` and phase difference at most `pi/6`, so
   for `K<=k<=2K`,
   `Re(b_r conjugate(b_s)e(k(delta_r-delta_s)))>=|b_rb_s|/2`.
2. Otherwise a labelled hub has `D_x>=tau_*L`. Its effective neighbor degree
   must be at least `X^(1/300-o(1))`; preserve the common-anchor near-translate
   fan without calling it a rational web.

Only a fixed-proportion coefficient-weighted positive-real disjoint mass or
the stated labelled hub advances the gate. Unweighted counts or coefficient-
free edge families do not.

The persistent companion `/root/guth_maynard_session_mentor` fixed this
criterion and was reactivated under its stable identity on 2026-08-02 UTC.
The required liveness rehearsal then succeeded: after it had completed, the
same identity acknowledged the frozen Cycle-160 scope correction and required
that Cycle 161 retain actual coefficient mass and every label. The primary
adopts that guardrail. The uncommitted pre-seal Cycle-160 output may therefore
be rebuilt from the corrected sources; a committed output would instead need
a versioned correction artifact.

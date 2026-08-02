# Cycle 163 preregistration: star wrap-fiber dichotomy

Date frozen: 2026-08-02 UTC.

For every Cycle-162 consistently oriented labelled star `s`, freeze its hub
`u_s`, difference-cell centre `theta_s`, and the unique half-open integer
wrap `m_v` for each leaf satisfying

```text
z_(u_s)-z_v=theta_s+m_v+O(K^(-1)).
```

Retain all `(d,q,c0)`, coefficient, phase-sector, orientation, atom, and cell
labels. Freeze compact support `z_v asymp Q`, the logarithmic Lipschitz
constant, tie handling, and all `o(1)` slack below `1/1200`.

With `x_v=|b_(u_s,v)|`, set

```text
D_s=sum_v x_v, E_s=sum_vx_v^2,
D_(s,m)=sum_(m_v=m)x_v, E_(s,m)=sum_(m_v=m)x_v^2,
R_s=D_s^2/E_s,
R_wrap=D_s^2/sum_mD_(s,m)^2,
R_fiber=sum_mD_(s,m)^2/sum_mE_(s,m).
```

Prove the exact factorization `R_s=R_wrap R_fiber`. Given the Cycle-162
lower bound `R_s>=X^(1/300-o(1))`, freeze threshold `X^(1/600)`. Either
`R_wrap>=X^(1/600-o(1))`, yielding an explicit weighted integer-wrap
complexity inverse, or `R_fiber>=X^(1/600-o(1))`. In the latter case retain
common-wrap squared edge mass and prove for leaves in one fiber

```text
|log(q_v/q_w)+2pi(d_v-d_w)/D| << 1/(KQ),
```

as a labelled logarithmic rational web. A row violating the factor dichotomy
or the fixed-wrap relation is the falsifier. No density, moment, or interval
claim is permitted.

## Companion checkpoint

The persistent companion `/root/guth_maynard_session_mentor` was live-checked
and reactivated under its stable identity on 2026-08-02 UTC. It selected the
star family because the common hub reduces the pullback to one integer-wrap
variable before four-variable curvature analysis. The primary adopts this
target and preserves the four-cycle arm as an explicit alternative.

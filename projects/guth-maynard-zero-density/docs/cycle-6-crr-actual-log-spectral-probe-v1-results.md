# Cycle 6 actual-log spectral probe v1: results

## Outcome

`OBSERVED`: all three V2-preregistered bounded rows completed under the
600-second and 1-GiB caps.  Each retained `NO_RETAINED_HIT`.  This is not a
negative result about the continuous CRR problem, AFARI, FARI, or the
phase-lift gate.  It tests only the frozen `v=2` actual-log surrogate with
three jitter nodes and does not evaluate `RationalMass(v)` smoothing.

`RECOGNIZED`: the reported complex matrix diagnostics use pinned
NumPy binary64/complex128.  Exact ordered tolerance-one energies and the
integer Farey/ray labels are recomputed from the retained finite sets, but no
floating quantity is a certified enclosure.

The immutable result artifact is
`discovery/cycle-6-crr-actual-log-spectral-probe-v1.json`, SHA-256
`0cab222fe49623263fb953ee0d7e863d339774172df5d4843fe40707376a853d`.
The semantic replay passed after recomputation.

## Row-level diagnostics

| Row | final min `|D_b|/128` | energy / `(R^4/H)` | active Farey labels / 285 | leading `rho` | leading `phi` |
|---|---:|---:|---:|---:|---:|
| F0 capped leading phase | `5.01e-8` | `4.57245` | `8` | `0.58714` | `5.83e-8` |
| F1 inverse-row minimum updates | `0.06848` | `4.57245` | `8` | `0.58714` | `5.83e-8` |
| F2 joint reselect + minimum updates | `0.06075` | `4.44326` | `12` | `0.58730` | `4.15e-5` |

`OBSERVED`: the inverse-row phase updates substantially lifted this surrogate's
minimum from the bare leading-phase value, while the capped leading
eigenvector itself was very non-flat across its selected rows.  This is a
bounded mechanism diagnostic, not an asymptotic exponent statement.  The
finite leading `rho` values were moderate, whereas `phi` was the dominant
loss; that matches the analytic phase-lift decomposition but does not prove
that the same behavior persists at frozen asymptotic scales.

`OBSERVED`: the fixed joint reselection improved the discrete Farey activity
from `8/285` to `12/285`, still short of the preregistered `1/8` proxy gate.
Both selected energy values were slightly above the predeclared upper
central-proxy boundary `4R^4/H`.  These finite misses are retained as
diagnostics only.

For F1/F2, every fixed-`p` coordinate update passed its specified local
linear-functional check.  The row minima were not globally monotone because
the inverse row weights changed between iterations, exactly as preregistered.

## What this changes

`PROVED`: the separate phase-lift theorem remains the operative analytic
gate:

```text
Gamma(W)=max_z min_p ||M_W^*(p z)||_1,
Gamma(W)^2 >= lambda*N*rho*phi^2/|W|.
```

The finite run does not change its hypotheses, strict
`ell+r+2s<2` closure condition, or status.  It does establish a reproducible
actual-label implementation for future, separately preregistered exploration.
The next mathematical task is still an asymptotic inverse theorem or a common
actual-Farey set that controls the adversarial `p` and row-flatness `phi`.

## Replay

```sh
python3 discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py --check
python3 discovery/run_cycle_6_crr_actual_log_spectral_probe_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_actual_log_spectral_probe_v1.py
```

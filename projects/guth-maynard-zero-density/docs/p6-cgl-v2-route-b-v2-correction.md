# P6 CGL-v2 Route B v2 correction: exact margin check

## Outcome and claim boundary

`PROVED`: Route B v1 recorded the correct displayed comparison
\(7/3-30/13=1/39\), but its replay checked the unrelated true identity
`7 * 13 - 30 == 61`. This v2 correction preserves the sealed v1 files and
checks the required cleared-denominator identity
`7 * 13 - 30 * 3 == 1`, together with the other stated exact comparisons.

This correction changes neither the 46 source-trace rows nor their
`OPEN_ANALYTIC_INPUT` disposition. It does not validate or repair the
Chen--Gupta--Li preprint and proves no new zero-density or short-interval
result.

## Replay

```sh
python3 proof/p6_cgl_v2_route_b_v2_correction.py --check
python3 -m unittest tests/test_p6_cgl_v2_route_b_v2_correction.py -v
```

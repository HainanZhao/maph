# P6 CGL-v2 Route A: literal source-order reconstruction

## Outcome and claim boundary

`OBSERVED`: Route A has traced every canonical registry row in the sealed
46-row Chen--Gupta--Li v2 audit, including both `L12` character-subdivision
subchecks. The result is `OPEN_ANALYTIC_INPUT`, not a validation or repair of
the preprint. CGL v2 remains a three-author arXiv preprint and prior work.

`PROVED`, conditional on the displayed CGL terms: the exact `q1=q` comparison
has first base `q^(7/3)T^2` (whose normalized exponent is at most `7/3`), and
the remaining coefficients `9/4`, `(10-sqrt(10))/3`, and `30/13`; each is at
most `7/3`, with margins `1/3`, `1/12`, `(sqrt(10)-3)/3`, and `1/39`.
This algebra does not close the theorem because its detector and
primitive-to-all inputs remain open.

## Preserved open inputs

- `S06_EXTERNAL_INPUTS`: the reached external theorem hypotheses have not all
  been read and checked.
- `Z03_TAIL_X_RANGE`: the source uses `T -> infinity` with `X` polynomial in
  `T`, but later chooses `X=(qT)^epsilon` and calls `T=1` worst. This route
  does not add `q<=T^C` or alter the logarithm.
- `Z05`/`Z06`: the primitive-to-all transfer needs Euler-factor zero comparison,
  conductor partitioning, and domination of the `q1`-sensitive terms.
- `F08_T_SMOOTH_UNDEFINED`: the pinned TeX uses `T`-smooth without defining it.

The machine-readable per-row hypotheses, locators, formulae, ranges, tags,
and dispositions are in `artifacts/p6-cgl-v2-route-a-v1.json`.

## Replay

```sh
python3 proof/reconstruct_p6_cgl_v2_route_a_v1.py --check
python3 -m unittest tests/test_p6_cgl_v2_route_a_v1.py -v
```

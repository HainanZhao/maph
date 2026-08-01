# P7-3 common ideal cubic v3 test correction

`OBSERVED`: P7-3 v2's integer replay artifact is correct, but its new unit
test searched for the literal phrase `remains open` in a list that instead
contains `the open coloured primitive cubic estimate`. This is a test-label
defect only.

`OBSERVED`: v3 verifies the corrected integer values \(34,34,62\) and the
semantic open-estimate boundary. It changes no mathematical claim, source
pin, or gate status. V1 and v2 remain immutable.

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_common_ideal_cubic_v3_test_correction.py --check
python3 -m unittest tests/test_p7_common_ideal_cubic_v3_test_correction.py -v
```

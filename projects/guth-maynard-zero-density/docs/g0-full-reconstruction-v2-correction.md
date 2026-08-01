# G0 full reconstruction v2 correction

Claim boundary: `PROVED` corrected G0 gate adjudication only, conditional on
the selected published analytic theorems. No new theorem or improved exponent
is claimed.

A hostile post-certificate review found that v1 was premature:

- its resource gate timed the four Cycle-2 routes but omitted the two
  independent Cycle-1 routes required by the Cycle-1 preregistration;
- it did not explicitly connect the official formula/proof bytes to the MIT
  DSpace item's authoritative `Publication` classification; and
- it did not assert a proof-runtime version, although performance metadata
  happened to record Python 3.12.3.

V2 preserves v1 and corrects all three defects. Two read-only Cycle-1 replay
wrappers now reproduce Route A and Route B separately. The six-route resource
gate measures those two plus the four Cycle-2 routes; every row exits zero
strictly below 60 seconds and 262144 KiB. Published-source v5 verifies that
the exact official Theorem 1/proof occurs in an issued, archived,
discoverable, nonwithdrawn MIT DSpace `Publication` (a learning object; no
journal or peer-review claim). The authoritative replay asserts CPython
3.12.3 through a hashed convention module before invoking any subordinate
checker.

`PROVED`: corrected **G0 PASS**, with no remaining frozen blocker. V1 must not
be cited as the final authority; v2 supersedes it.

```sh
python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v2.py --check
```

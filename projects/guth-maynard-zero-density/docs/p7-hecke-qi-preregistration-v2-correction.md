# P7 \(\mathbb Q(i)\) preregistration v2 status correction

## Outcome and boundary

`OBSERVED`: P7 v1 remains immutable and replays unchanged. It selected the
finite-order primitive ray-class family over fixed \(\mathbb Q(i)\), pinned
the three primary sources, and froze the six transfer gates. Its preselected
repeated-norm witness, however, was a material algebraic input without an
explicit epistemic tag. This status-only v2 correction labels that input
`CONJECTURED` until `P7-1-NORM-AGGREGATION` independently checks the ray-class
quotients, exact conductors, and character evaluations.

No family, conductor shell, endpoint convention, source pin, gate identifier,
pass/fail rule, resource cap, or non-promotion boundary changes. In
particular, v2 still proves no Hecke zero-density theorem, no Guth--Maynard
transfer, and no prime-ideal short-interval theorem. It neither starts a
theorem search nor a hostile audit.

## Corrected witness status

The frozen prospective witness is still

\[
 Q=8,\quad \mathfrak f_3=(3),\quad
 \mathfrak f_4=(1+i)^4,\quad 17=(4+i)(4-i),
\]

with expected aggregated coefficients \(-2\) and \(+2\). These values are
now `CONJECTURED`, not `PROVED`, until the gate's exact calculation validates
the two order-two quotient descriptions and their conductor minimality. A
successful verification would establish only the direct-import type mismatch;
it would not rule out a character-aware large-value theorem.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_hecke_qi_preregistration_v1.py --check
python3 proof/build_p7_hecke_qi_preregistration_v2.py --check
python3 -m unittest \
  tests/test_p7_hecke_qi_preregistration_v1.py \
  tests/test_p7_hecke_qi_preregistration_v2.py -v
```

V2 records hashes for its conventions, document, builder, and tests, and
anchors the exact immutable v1 artifact hash.

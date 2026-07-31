# Results companion v1.4 correction layer

## Claim boundary

This deterministic layer does not rewrite the published v1.3
companion. It contains that immutable archive byte-for-byte and adds:

1. the `PROVED` Engine-C Fourier/\(\sigma^{+r}\) convention correction
   already used by v1.3;
2. the later `CONTAINED_ORIENTATION_CIRCULARITY` record withdrawing the
   claim that the five-control replay had a data-independent choice
   between \(\chi\) and \(\chi^{-1}\);
3. the `PROVED` clarification that, in each of the five certified
   quartic Stark cases satisfying Roblot's (A1)--(A3), the weak/Stark
   ratio lies in \(\mu_4\);
4. the `PROVED` RQ-000013 Engine-A certificate with
   \(E_\chi=I_\chi=2\) and
   \(X_{[0]}=u^2,\ X_{[1]}=u^{-2}\).

The fully oriented numerical five-control replay remains withdrawn.
The retained numerical statement is only that exactly one of the two
conjugate character orientations has a quarter-turn match in each
case. The five certified-case \(\mu_4\) corollaries follow instead
from Roblot's uniqueness theorem and the independently proved Stark
packets.

The PARI `bnrL1` comparison in the RQ-000013 record is `OBSERVED` and
quarantined; it is not part of that exact proof.

## Replay

From the extracted archive root:

```bash
python3 projects/effective-stark-sweep/scripts/verify_results_companion_v14.py .
```

The verifier checks the outer manifest, the immutable v1.3 archive
hash and its internal manifest, both correction records, all five
Roblot (A1)--(A3) rows, and the exact RQ-000013 GP replay.

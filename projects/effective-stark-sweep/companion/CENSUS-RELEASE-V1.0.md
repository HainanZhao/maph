# Effective Stark census release v1.0

Public DOI: <https://doi.org/10.5281/zenodo.21729947>

This archive supports the paper's corrected selected-modulus census boundary. It does not claim a full isomorphism-class quotient, label all higher-order packet roots, or turn the 220 open Engine-B member rows into proved transports.

The deleted-prime cover criterion is `PROVED`; its exhaustive 1,560-row census corollary is an exact finite check. The rejected four-support nondegeneracy statement is `REFUTED` by the preserved exact counterexample.

From the extracted archive root, run:

```sh
python3 proof/audit_q_euler_deleted_prime_cover.py
python3 scripts/audit_census_referee_revision.py
python3 scripts/audit_census_paper.py
python3 scripts/verify_census_companion_v1.py --tree .
```

The build was made under Python 3.11 and PARI/GP 2.15.4. `MANIFEST.sha256` is the byte-level file inventory.

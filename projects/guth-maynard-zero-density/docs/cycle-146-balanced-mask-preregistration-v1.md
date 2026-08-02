# Cycle 146 preregistration: balanced high-pass mask

Date frozen: 2026-08-02 UTC.

Return to the exact Cycle-87 periodic pair kernel

```text
Psi_K(t)=sum_k U(k/K)e(kt)=K sum_m hat U(K(m-t)).
```

Keep its nonzero Fourier label `k` and the fact `U(0)=0`.  Prove the exact
mean-zero identity.  State the Gram-feature identity under the additional
standard choice `U>=0`, which Cycle 87 did not itself freeze, and quantify
what is inserted by replacing the kernel with a nonnegative collision
majorant.

For a deterministic partition of oriented coefficient pairs into arithmetic
cells, derive a signed pigeonhole statement for the real cell contributions.
The extracted cell must retain `k`, both coefficient endpoints, their
correlation product, phase residual, rational centers, orientations, and
tails.  Record the exact cost in the number of cells; do not suppress it as
`X^epsilon` unless proved.

Success is a coefficient-preserving signed inverse contract or a proof that
the current arithmetic partition has unaffordable entropy.  No cell estimate,
paired norm, complete moment, density gain, or interval theorem is implied.

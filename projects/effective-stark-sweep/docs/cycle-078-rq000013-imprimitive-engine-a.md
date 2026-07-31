# Cycle 078 — certified nonzero imprimitive Engine-A row

Recorded: 31 July 2026 UTC.

## Outcome and claim boundary

`PROVED`: the preregistered row RQ-000013 satisfies the uniform
Engine-A theorem with exact imprimitive factor \(E_\chi=2\), exact
relative index \(I_\chi=2\), and Artin-labelled packet
\[
X_{[0]}=u^2,\qquad X_{[1]}=u^{-2}.
\]

This closes the program's requested imprimitive branch.  It does not
complete the 1,560-row Q corpus or the preregistered independent
50-row Arb audit.

The PARI `bnrL1` point-value agreement is `OBSERVED` and quarantined.
It is not used to prove the identity.

## Exact route

- \(K=\mathbb Q(\sqrt2)\), finite modulus HNF
  \(\left(\begin{smallmatrix}14&6\\0&2\end{smallmatrix}\right)\),
  norm \(28\);
- ray group \(C_2\), sign class \([1]\), unique odd quadratic
  character;
- primitive conductor HNF
  \(\left(\begin{smallmatrix}7&3\\0&1\end{smallmatrix}\right)\);
- one omitted norm-two prime, with primitive character value \(-1\),
  hence \(E_\chi=2\);
- quartic field \(t^4+2t^2-7\), signature \((2,1)\), discriminant
  \(-448\), class number \(1\), and `bnfcertify=1`;
- exact norm map \((1,-1)\), primitive kernel \((1,1)^T\), embedded
  base-unit vector \((1,-1)^T\), and determinant index \(I_\chi=2\);
- oriented unit \(u=(t^2-2t+3)/4\), tied to the selected embedding by
  exact rational Sturm isolation;
- exact nontrivial Artin action \(t\mapsto-t\), \(u\mapsto u^{-1}\).

Substitution in the uniform theorem gives
\(L'_{\mathfrak m}(0,\chi)=2\log u\).  Since \(|G|=2\), Fourier
inversion gives the displayed packet identity.

## Evidence and replay

- certificate:
  `artifacts/rq000013-engine-a-imprimitive-certificate-v1.json`;
- transcript:
  `artifacts/rq000013-engine-a-imprimitive-certificate-v1.transcript`;
- exact replay:
  `python3 scripts/certify_rq000013_engine_a.py --check`;
- staged results-paper addendum:
  `paper/effective-stark-results-supplement-rq000013-addendum.tex`;
- census manuscript surface:
  `paper/effective-stark-sweep-draft.md`.

The initial replay under PARI/GP 2.15.4 took 0.06 seconds wall time and
18,176 KiB peak resident memory.  The already-published Zenodo v1.3
files were not modified; publishing this addendum requires an
explicitly authorized new Zenodo version.

## Gate change

The single-row imprimitive certificate is `BANKED`.  The Q-corpus gate
remains open, and the independent 50-row Arb audit remains blocked on
completion of that corpus.  No external publication or correspondence
action was taken in this cycle.

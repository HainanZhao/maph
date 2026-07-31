# Constructor correction preregistration

Frozen: 2026-07-30 UTC after the failed v1 magnitude check and before
the corrected constructor is run.

## Preserved failure

The v1 sealed constructor used

\[
(\bar U_K)^{\gamma^2}
\]

as a proxy for the embedded group \(\bar U_{K^+}\) when computing
\[
2^e=[\bar U_{K^+}:N_{K/K^+}\bar U_K].
\]
For RQ-000129 the proxy returned index \(4\), hence \(e=2\). After the
seal was committed, opening the analytic record gave a magnitude ratio
of exactly \(\sqrt2\), so the comparison gate failed.

The failed artifact remains immutable as
`artifacts/roblot-quartic-gate-sealed-v1.json`.

## Correction

Construct \(K^+\) as the unique totally real quartic subfield, certify
its unit group independently, embed each fundamental unit into \(K\)
using `nfisincl`, and compute the norm-image index inside that genuine
embedded lattice.

The pre-run exact lattice calculation predicts

\[
[\bar U_{K^+}:N\bar U_K]=2,\qquad e=1.
\]

No analytic \(L'\)-value or Engine-C unit is an input to the corrected
constructor. The already opened magnitude is used only after the new
unit and coefficient are sealed.

## Acceptance

The corrected run must:

1. certify both absolute unit groups with `bnfcertify`;
2. exhibit the embedded \(K^+\)-unit lattice and norm-coordinate
   matrix;
3. obtain index \(2\) without numerical recognition;
4. construct the exact anti-unit using Roblot's formula with \(e=1\);
5. reproduce its output byte-for-byte on a second run;
6. agree in magnitude with the previously opened \(L'\)-ball.


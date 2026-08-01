# P1R-FS final hostile promotion audit v1 — PASS

Claim boundary: `OBSERVED` audit of the narrow fixed-splice promotion only. It does not prove an actual zero-density lower bound, saturation of the Guth--Maynard method, a new density/short-interval theorem, or anything about CRR.

The audit independently rederives the strict-left supremum over the reals. For every real (0<\eta<30/13), the positive threshold

\[
H_\eta=\frac{169\eta}{300-130\eta}
\]

and (h=\min\{1/10,H_\eta/2\}) give (0<h<H_\eta), hence

\[
\frac{300h}{169+130h}<\eta,
\qquad
I(7/10-h)>30/13-\eta.
\]

Together with (I(\sigma)<30/13) on the strict left branch, this proves the real supremum. The retained left image is contained in every splice with an extended-real right branch (J), so (sup F_J=\max\{30/13,\sup J\}\ge30/13), including the (\pm\infty) cases.

The final package is hash-pinned: both route scripts/artifacts/docs/tests, reconciliation, sealed v4 authorization/audit, Huxley source, and classical ledger. Normal replay, `-O`, `-OO`, overwrite, source/input tamper, self tamper, source range/log-factor scope, route independence, and all 11 package tests pass.

Replay:

```text
python3 proof/audit_p1r_fs_final_v1.py --check artifacts/p1r-fs-final-hostile-audit-v1.json
```

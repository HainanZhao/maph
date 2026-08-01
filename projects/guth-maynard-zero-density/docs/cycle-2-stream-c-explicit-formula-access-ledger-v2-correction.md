# Cycle 2 — Stream C explicit-formula access ledger v2

Claim boundary: `PROVED` for the source-license and theorem/convention audit
below; this closes the archival source node only. It does not reprove the
Guth--Maynard density theorem or claim a new prime-interval exponent. V1 and
the Route-A adjudication remain preserved.

## Correction to the archival gate

`PROVED`: MIT OpenCourseWare describes itself as an online publication of
course materials and licenses its materials under CC BY-NC-SA 4.0. The license
expressly permits copying and redistribution subject to attribution,
noncommercial use, and share-alike. No course-specific exception was visible
in the inspected course landing page or calendar.

`PROVED`: the official MIT OCW course handle is `1721.1/101679` for K. S.
Kedlaya's 18.785 *Analytic Number Theory* (Spring 2007). Its official indexed
path identifies `contents/lecture-notes/errorbounds.pdf`; the course calendar
links the matching proof unit `von-mangoldt.pdf`. The author-hosted course PDFs
were frozen byte-for-byte as replay copies:

- `kedlaya-2007-errorbounds-author.pdf`, SHA-256
  `375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d`.
- `kedlaya-2007-von-mangoldt-author.pdf`, SHA-256
  `43cbe51ee69fe552078d90d0c21b165456f3ad67ad64c83df71b9cce3d56ae05`.

`PROVED`: Theorem 1 in the first unit states, for every \(x\ge2\) and
\(T>0\), the half-weighted explicit formula truncated by \(|\Im\rho|<T\),
with remainder

\[
 O\!\left(\frac{x\log^2(xT)}T+
 (\log x)\min\{1,x/(T\langle x\rangle)\}\right).
\]

`PROVED`: the proof unit supplies the missing convention: every zero residue
is counted with multiplicity. It reaches “We are done!”, so this is a proof
unit rather than an unproved course assertion.

`OBSERVED`: direct DSpace retrieval returned 405/403 in this run. That is a
retrieval-replay limitation, not a license/provenance exception: the official
handle and indexed filename establish provenance, while the matching
author-hosted course files provide local byte replay.

## Formula transfer

`PROVED`: apply the theorem at
\(u=\lceil x\rceil-1\) and \(v=\lfloor x+y\rfloor\). The half weights
give exactly the desired integer sum over \([x,x+y]\), up to
\(O(\log x)\), and \(v-u=y+O(1)\). At integer endpoints the distance to a
different prime power is at least one. For \(2\le T\le x\), the two
remainders and endpoint terms are \(O(x\log^3x/T)\).

`PROVED`: the source's \(|\gamma|<T\) and Guth--Maynard's printed
\(|\rho|\le T\) differ only in boundary sets contained in unit strips around
\(\pm T\). The pinned multiplicity-inclusive Riemann--von Mangoldt count
from HSW plus Bui--Heath-Brown gives \(O(\log T)\) such zeros; their endpoint
contribution is \(O(x\log T/T)\), absorbed by the stated error.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/check_cycle_2_stream_c_explicit_formula_sources_v2.py
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_explicit_formula_sources_v2.py
```

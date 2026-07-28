# SIC--Stark research cycle 113: the exact cyclic parameter ledger

Date: 2026-07-28

## Outcome

For a rational geodesic point \(\tau=m/n\), the factor belonging to the
level-six characteristic \((a,b)\) is

\[
 z_j=
 \exp\!\left(
 \frac{2\pi i}{6n}(bm-an+6jm)
 \right).
\]

Thus every factor lies in one common \(6n\)-th-root system, at the exact
node

\[
 k_{a,b,j}=bm-an+6jm\pmod{6n}.
\]

The initial nodes

\[
 k_{a,b}=bm-an\pmod{6n}
\]

are distinct for all \(36\) characteristics once \(n>6\).  This gives a
complete symbolic parameter ledger for the rational-boundary table; no
floating-point recognition is involved.

## Central characters

Raising the initial node to the \(n\)-th power gives

\[
 z_{a,b}^{\,n}=\zeta_6^{\,bm-an}.
\]

The \(36\) characteristics therefore split into six central sectors, each
containing six nodes.  Since \(A\equiv I\pmod6\), the source point
\((m,n)\) and target point \(A(m,n)=(m',n')\) assign the same central
sector to every characteristic.

## Reproduction

```bash
python3 scripts/dimension_six_cyclic_parameter_ledger.py
```

# Cycle 164: oriented conductor-lowered ray-monoid section

## Outcome

`PROVED`: on the frozen 36 characteristics for (K=\mathbb Q(\sqrt{21})),
the convention-pinned conductor-lowering construction gives a total
least-exponent section into the one arithmetic-Frobenius-oriented source
(C_6). All 18 fixed-full-modulus rows recover their direct ray logarithms;
the retained anchors are `(3,5) -> g^1` and `(3,4) -> g^2`.

This advances the state-space subgate only. It does not prove the missing
additive coefficient-to-logarithm operation, AFK compatibility, a Stark
identity, fusion continuity, or dimension-six TCC.

## Exact construction and checks

For each frozen characteristic, the positive representative is
\(\gamma=b\beta-p^*\). Let
\(c=(6)+(\gamma)\), \(\mathfrak m_{a,b}=(6)/c\), and
\(\mathfrak a_{a,b}=(\gamma)/c\), with the selected real place retained.
The natural projection from the full ray group is evaluated on the fixed
generator \(g=[(4\beta+1)]\). The section value is the least
\(e\in\{0,\ldots,5\}\) whose projected (g^e) equals
\([\mathfrak a_{a,b}]\). This rule was frozen before any row output.

| Exact check | Result |
|---|---:|
| Source ray structure and generator coordinate | `C6`, `g -> 1` |
| Characteristics enumerated | 36 |
| Full-modulus/direct-log recovery rows | 18 |
| Lowered-modulus rows with a source-image label | 18 |
| Total rows in the projected-source image | 36 |
| `(3,5)`, `(3,4)` section exponents | `1`, `2` |

The section-exponent histogram is `0:14, 1:10, 2:3, 3:3, 4:3, 5:3`.
The principal exact replay took 0.06 seconds and 14,592 KiB peak RSS on
CPython 3.12.3 with PARI/GP 2.15.4.

## Claim boundary and decision

The finite calculation proves only the stated ideal/ray-class construction.
The least-exponent rule is a deterministic set-theoretic section; it supplies
neither an operation on additive spectral coefficients nor a compatibility
law with an AFK cocycle. Any claim that it closes the interface or TCC is
withheld.

The session companion `/root/decision_companion_2` recommends sealing this
limited result and then attacking an outcome-blind additive-to-logarithmic
operation class on the now-defined section. That recommendation is adopted.
Its stated falsifier is replay disagreement, a nonfunctorial projection,
failed anchor/direct-log recovery, or any promotion beyond the frozen finite
state space.

## Next authorized action

Cycle 165 / `B003` must preregister an outcome-blind additive-to-logarithmic
operation class on this section and seek either exact compatibility or an
exact falsifier of that named class. It must not repackage the finite labels
as an AFK interface without defining and checking the operation.

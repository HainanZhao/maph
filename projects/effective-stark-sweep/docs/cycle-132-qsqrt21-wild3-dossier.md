# Cycle 132 — \(\mathbb Q(\sqrt{21})\) wild-3 dossier

## Decision

**PROVED (method boundary).** RQ-000692 is a sharply localized failure
of the wild-ramification hypothesis in Roblot's sextic index formula.
It is the primary arithmetic target after the portable deleted-prime
theorem: extending an appropriate sextic Stark/index mechanism across
this wild local configuration would address a named census wall.

**PROVED (structural convergence).** The local dimension-6 companion
uses exactly (G=\operatorname{Cl}_{(6)\infty_2}(\mathbb Q(\sqrt{21}))
\simeq C_6), with its primitive character sending the stated generator
to \(\zeta_6\). Its degree-12 ray polynomial is the substitution
\(P_{\rm SIC}(X)=P_{\rm census}(-X)\), so the two records name the
same ray field under the explicit generator change (X\mapsto-X\).

This does not prove that an extension of Roblot's theorem would by
itself establish the TCC bridge. The remaining dimension-6 statement
is an oriented primitive order-six (L'_S)-to-regulator identity;
the companion paper makes its TCC consequence conditional on its
separate MFC6 analytic conjecture.

## Frozen object and exact local failure

The frozen row is RQ-000692:

| invariant | exact value |
|---|---|
| base field | \(K=\mathbb Q(\sqrt{21})\) |
| finite modulus | HNF \(\left[\begin{smallmatrix}6&0\\0&6\end{smallmatrix}\right]\), norm \(36\) |
| one-place ray group | \(C_6\), sign log \(3\) |
| Fourier support | orders \((2,6)\), three supported characters |
| Shintani / derived-subgroup index | \(6\) |
| primitive sextic ray field | degree 12 over \(\mathbb Q\), signature \((6,3)\), class number \(1\) |
| prime above \(3\) | local row \((e_K,f_K,e_H,f_H,e_{H/K})=(2,1,12,1,6)\) |

Thus the relative ramification index is \(6\), divisible by \(3\).
Roblot Theorem 7.1's no-wild-prime-above-3 hypothesis fails. The other
audited gates pass: A1, A2, A3, equality of the relevant local sets,
and \(3\nmid h_H\). This is a theorem-hypothesis failure only, not an
impossibility or non-algebraicity result.

The field is independently pinned in the sextic field inventory by
the polynomial

\[
x^{12}-3x^{11}-6x^{10}+16x^9+3x^8+27x^6+3x^4+16x^3-6x^2-3x+1.
\]

The companion's polynomial is
\(X^{12}+3X^{11}-6X^{10}-16X^9+3X^8+27X^6+3X^4-16X^3-6X^2+3X+1\),
which is exactly the displayed census polynomial evaluated at \(-X\).
Its pinned Fourier audit independently reproduces the ray group
\([6]\), retains the imprimitive order-six factors with ratio one,
and identifies the same primitive Fourier component. These are
**PROVED** structural identifications; its floating point residual is
only a quarantined numerical check of the outstanding oriented identity.

## Controls and research use

The frozen sextic screen has 764 primitive character/inverse-character
kernels, 407 primitive-field keys, and 259 kernels (206 rows) for
which Roblot 7.1 applies. They are the appropriate exact control
population for a proposed wild-3 modification; they should be used to
verify that any revised formula specializes to the existing tame
formula. They are controls for the index-formula mechanism, not
evidence that a proposed TCC/SIC identification is correct.

RQ-002057 over \(\mathbb Q(\sqrt{57})\) is a useful *negative
comparison*: it has order-six support and a ramified 3-power conductor,
but is reachable by the different Shintani packet route while it too
fails Roblot's wild-3 hypothesis. It prevents the false inference that
order six or a ramified 3-power conductor alone explains the wall.

The new all-order deleted-prime theorem does not decide RQ-000692:
the order-six primitive characters have no deleted finite primes and
the quadratic character's only deleted prime has value \(-1\). That
removes a cheap Euler-degeneracy explanation from the target.

## Next falsifiable action

The shared object is now exactly identified. The next falsifiable
mathematical action is to formulate a wild-local replacement for the
Roblot 7.1 hypothesis and prove that it supplies the **oriented**
primitive order-six regulator equality, not merely an absolute-value
or unoriented index statement. Failure to retain this orientation would
not close the companion's bridge theorem.

## Evidence

- `artifacts/census-h-taxonomy-v2.json` (row RQ-000692)
- `artifacts/roblot-sextic-population-v1.json` (exact A1--A3 and
  class-number gate)
- `artifacts/roblot-sextic-field-inventory-v1.json` (field polynomial
  and local ramification row)
- `artifacts/roblot-sextic-route-inventory-v1.json` (control population)
- `artifacts/h-all-order-deleted-prime-cover-audit-v1.json` (Euler
  criterion control)
- `/root/projects/maph/projects/sic-stark/paper/sic-stark-dimension-six-boundary-fusion.tex`
  (same ray group and bridge target)
- `/root/projects/maph/projects/sic-stark/scripts/dimension_six_primitive_fourier_audit.gp`
  (independent ray/Fourier audit)

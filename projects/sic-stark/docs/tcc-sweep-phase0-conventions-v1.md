# Phase-0 convention dossier: 2-elementary TCC sweep

**Status:** `G0_FAIL_CONTAINED`
**Date:** 2026-08-01 UTC
**Claim boundary:** this dossier closes the planned maximal-order,
tuple-only scan design negatively. It does not determine the order-ray
support for all AFK forms, and it makes no TCC claim.

## Headline result

**PROVED (source check):** AFK's unconditional squared normalized-overlap
formula is indexed by a class in the imprimitive ray-class monoid
\(\operatorname{Clt}_{d\infty_2}(\mathcal O_f)\), where \(f\) is the
conductor of the admissible form. Consequently the proposed Phase-1 test
on only \((K,d)\), using the maximal-order group
\(\operatorname{Cl}_{(d)\infty_2}(\mathcal O_K)\), is not a theorem for
the full admissible AFK family.

This is a correction to the proposed premise, not evidence that a
2-elementary stratum is absent.

## Primary-source record

The primary source is Appleby--Flammia--Kopp, *A Constructive Approach to
Zauner's Conjecture via the Stark Conjectures*, arXiv:2501.03970v2,
2025-03-17. The downloaded source archive has SHA-256
`bc742b19594b5842d1edc343d9b48616273e8225c76910f7d758722cf6761519`;
the PDF has SHA-256
`d469d975f14501d7593fcd9160c1175026a9159eff2d0b2dbb57d58831a42443`.

- **PROVED (AFK Definitions 1.21--1.24; source labels
  `dfn:admissiblePair`, `dfn:sequenceofconductors`, `dfn:fjrjmdjm`,
  `def:admissibleform`):** an admissible tuple is
  \((d,r,Q)\sim(K,j,m,Q)\), with \(d=d_{j,m}\),
  \(r=r_{j,m}\), and form conductor \(f\mid f_j\).
- **PROVED (AFK theorem `thm:nupnumpeq1`, equation `eq:nusquared`):** for
  \(\boldsymbol p\ne0\), the square of the normalized AFK overlap is
  \(\exp(n Z'_{d\infty_2}(0,\mathfrak A))\), with
  \(\mathfrak A\in\operatorname{Clt}_{d\infty_2}(\mathcal O_f)\).
- **PROVED (AFK Definition `dfn:orderConductorf`):**
  \(\mathcal O_1=\mathcal O_K\), but AFK explicitly permits \(f>1\).
  Their example after `def:admissibleform` has
  \(Q'=\langle5,-20,4\rangle\) of conductor 8, admissible at
  \((K,j,m)=(\mathbb Q(\sqrt5),3,1)\) and \(d=19\).

The one-place label is \(\infty_2\), not an unlabelled real place. For
the conductor-one PARI controls the increasing root is selected by `[1,0]`:
it sends \(\sqrt5\) and \(\sqrt3\) to their negative values.

## Consequence for the planned predicate

For any finite abelian group \(G\) and residue/sign class \(R\), the
Fourier support of the Kopp difference \(1-R\) consists exactly of the
characters \(\chi\) with \(\chi(R)\ne1\). Thus a full-quadratic
predicate must be evaluated in the *actual AFK order ray object* and must
also account for the imprimitive Euler factors used by Engine A.

The provisional condition
\[\operatorname{exp}(G/\langle R\rangle)\le2\quad\text{and}\quad R\notin G^2\]
was never proved here and cannot be used as the Phase-1 classifier. In
particular, neither the D4/D5 maximal-order controls nor an isomorphism at
one conductor implies the assertion for every \(f\mid f_j\).

## Exact conductor-one controls

Run:

```sh
python3 projects/sic-stark/proof/verify_tcc_sweep_phase0_calibrations.py
```

The resulting artifact is
`projects/sic-stark/artifacts/tcc-sweep-phase0-calibrations-v1.json`.

- **PROVED:** D4, \(K=\mathbb Q(\sqrt5)\), \(f=1\), modulus
  \((4)\infty_2\), has one-place ray group \(C_2\), nontrivial sign
  class, and its sole supported character has order two.
- **PROVED:** D5, \(K=\mathbb Q(\sqrt3)\), \(f=1\), modulus
  \((5)\infty_2\), has one-place ray group \(C_8\), sign class \(g^4\),
  and support character orders \(8,8,8,8\). Its quadratic character is
  killed by \(1-R\).

These controls agree with the published D4 certificate and the exact D5
character-support certificate. They falsify no theorem; they establish
that the adapter's sign and embedding convention is coherent at conductor
one.

## Gate outcome and successor action

**G0 outcome: `FAIL`.** The old Phase-1 universe is not authorized. No
maximal-order `bnrinit` scan may be labelled a sweep of every admissible
AFK tuple.

## Existing canonical-family no-go (separate scope)

**PROVED (existing exact route, not a proof for all AFK tuples):**
`docs/sic-stark-cycle29.md` and
`scripts/analyze_canonical_order_character_obstruction.py` establish that
for the canonical order family
\[\mathcal O_d=\mathbb Z[\beta_d],\qquad
  \beta_d^2-(d-1)\beta_d+1=0,\qquad d\ge5,\]
the local one-place order-ray kernel has exponent greater than two and
the nontrivial Kopp sign class forces a nonquadratic character into the
principal packet. The script's independent exact finite audit for
\(5\le d\le40\) passes in this run.

This rules out an all-quadratic continuation in the canonical
dimension-one/rank-one order family above four. It does **not** imply the
same conclusion for every AFK \((K,j,m,Q)\): the AFK dimension grid has
noncanonical \(m\)-branches and forms of every allowed conductor.
Treating the canonical result as a full-family boundary statement would
be a scope error.

## Successor-universe feasibility map

**OBSERVED (exact integer enumeration, no support verdict):**
`discovery/enumerate_tcc_sweep_afk_tuple_skeleton.py` enumerates the AFK
pair/triple skeleton through \(d=1024\). It finds 1,063 admissible
\((d,r)\) rows: 1,021 canonical rank-one rows and 42 noncanonical rows,
across 981 fundamental discriminants. Their allowed form-conductor lists
contain 2,187 tuple/conductor strata, with largest \(f_j=377\). The
hash-recorded output is
`discovery/tcc-sweep-afk-tuple-skeleton-d1024-v1.json`.

This is sufficient evidence that a corrected finite universe can be
specified. It is not an all-form census: each conductor stratum still
requires an exact enumeration of primitive indefinite form classes and
an order-ray/monoid support computation.

**OBSERVED (exact maximal-order group layer, still not a packet
certificate):** all 42 noncanonical AFK pair/triple rows in this range
have the conductor-one stratum \(f=1\). The PARI group-layer replay in
`discovery/screen_tcc_sweep_conductor_one_group_layer.py` finds zero
full-quadratic rows among them: every \(1-R\) support contains a
character of order greater than two. Its output is
`discovery/tcc-sweep-conductor-one-group-layer-d1024-v1.json`.

This discharges neither the 21 noncanonical positive-conductor strata
nor the form-class enumeration. It is a negative filter for the
conductor-one slice only.

**RECOGNIZED (exact finite group computation; not yet a packet proof):**
the completed local order-ray screen has 2,187 tuple/conductor rows. In
2,184 rows it exhibits a local quotient element of order greater than two
while the sign class is nontrivial, forcing a nonquadratic character in
the group-theoretic \(1-R\) support. The three rows without such a local
witness are \((d,r,f)=(4,1,1),(8,1,1),(12,1,1)\). Direct PARI maximal
order checks give respectively \(C_2\), \(C_2^2\), and \(C_2^3\) with
nontrivial sign class. Thus D12 over \(\mathbb Q(\sqrt{13})\), modulus
\((12)\infty_2\), is the sole new full-quadratic *group-layer* candidate
in this finite skeleton; D8 is an existing proved control.

The exact output is
`discovery/tcc-sweep-nonmaximal-local-kernel-d1024-v1.json`. This result
still needs a proof-grade successor replay and an AFK order-ray/monoid
coverage theorem before it can become G1.

**Preregistration correction:** the 2,187-row screen was exploratory: its
universe and resource rule were not frozen before the output was opened.
Accordingly the D12 selection is `EXPLORATORY`, not a preregistered hit.
The output may guide a separately registered proof attempt, but it cannot
support the plan's bounded G1 boundary statement or a post-hoc claim of
scan completeness.

## Exploratory D12 Engine-A packet

**EXPLORATORY (exact shared-pipeline replay):** applying the banked
Engine-A construction to the D12 conductor-one modulus produces one-place
ray group \(C_2^3\), sign log \((0,1,1)\), four quadratic group-support
characters, and two nonzero imprimitive-Euler character contributions.
Their exact trace descent gives
\[
 X^4-(4y+6)X^3+(13y+17)X^2-(4y+6)X+1,
 \qquad y^2-y-3=0,
\]
with absolute resultant
\[
 X^8-16X^7+59X^6-54X^5+29X^4-54X^3+59X^2-16X+1.
\]
The replay is
`discovery/certify_tcc_sweep_d12_engine_a_exploratory.py` and its artifact
is `discovery/tcc-sweep-d12-engine-a-packet-exploratory-v1.json`.

This opens no analytic AFK value and has not checked any
characteristic-to-ray, multiplier, sign-table, or minor condition. It is
therefore not evidence for formal TCC beyond identifying a concrete
exploratory bridge target.

## D12 fixed-full-ray shortcut audit

**OBSERVED (exact integer arithmetic, shortcut contained):** the
all-characteristic bridge cannot simply take ray logs in the one fixed
full modulus \((12)\infty_2\).  With
\(y^2-y-3=0\), \(\beta=4+3y\), and the positive lift
\(\widetilde p\), one has
\[
 N(q\beta-\widetilde p)
 =\widetilde p^2-11\widetilde p q+q^2.
\]
Among the 143 nonzero D12 characteristics, 71 of these norms have a
nontrivial common divisor with 12.  The corresponding ideals are not
eligible for a full-modulus ray-class label.  (The lift inequality is
decided by the exact square test
\((11q-2\widetilde p)^2>117q^2\), not by floating point.)

The replay
`discovery/audit_tcc_sweep_d12_fixed_ray_shortcut.py` writes
`discovery/tcc-sweep-d12-fixed-ray-shortcut-audit-v1.json`.  This is not
a failure of the D12 candidate itself: it is a failure of the proposed
fixed-ray shortcut.  A valid D12 bridge would need a
characteristic-dependent conductor-lowering theorem, plus compatible
multiplier and AFK labels, before it can use any ray logs.

**EXPLORATORY (exact conductor-lowering ledger):** the requisite
maximal-order lowering is available from Kopp, arXiv:2411.06763,
Proposition `prop:changemodzeta`: for a principal representative
\(\gamma=q\beta-\widetilde p\), put
\(\mathfrak d=(12)+(\gamma)\), then reduce to
\((12)/\mathfrak d\) and \((\gamma)/\mathfrak d\).  The exact PARI
replay `discovery/audit_tcc_sweep_d12_conductor_lowering.py` supplies a
ray group, sign log, and ideal log for every nonzero D12 characteristic.
It finds 72 full-modulus rows and 71 lowered rows; reduced finite modulus
norms occur with counts
\[
144:72,\quad36:18,\quad16:36,\quad9:6,\quad4:9,\quad1:2.
\]
The output is `discovery/tcc-sweep-d12-conductor-lowering-v1.json`.
This is a valid arithmetic input to an eventual D12 bridge, but it has
not compared the AFK phase, derived signs, or checked TCC minors.

**EXPLORATORY (exact multiplier ledger):** for
\(Q=\langle1,-3,-1\rangle\), the D12 Zauner stabilizer is
\[
 L_z=\begin{pmatrix}10&3\\3&1\end{pmatrix},\qquad
 A_t=L_z^3=\begin{pmatrix}1189&360\\360&109\end{pmatrix}.
\]
The exact Dedekind-sum calculation gives Rademacher invariant zero.
Kopp's theta-character formula and AFK's phase-square formula then agree
for every nonzero characteristic: both have multiplier exponent
\(-Q(p,q)/4\pmod1\).  The 143-row replay is
`discovery/audit_tcc_sweep_d12_multiplier_ledger.py`, with output
`discovery/tcc-sweep-d12-multiplier-ledger-v1.json`.

It independently closes only the multiplier sub-ledger.  In particular,
it is not an AFK-to-lowered-ray identification or a signed TCC
reconstruction.

**EXPLORATORY (lowered Engine-A packets):** the six scalar reduced
moduli in the lowering ledger are exactly \((1),(2),(3),(4),(6),(12)\).
The shared exact Engine-A replay has now synthesized each corresponding
packet: the one-place ray groups are respectively
\[
1,\quad1,\quad C_2,\quad C_2,\quad C_2,\quad C_2^3,
\]
with relative packet degrees \(1,1,2,2,2,4\).  The replay
`discovery/certify_tcc_sweep_d12_lowered_engine_a_packets.py` writes
`discovery/tcc-sweep-d12-lowered-engine-a-packets-v1.json` and is chained
to the lowering ledger hash.  These packets make the remaining D12
problem a label/sign/reconstruction problem; they do not solve it.

**Next authorized action:** create a versioned successor design with an
exact order-ray/monoid implementation, a finite enumeration of admissible
form classes and conductors for each \((K,j,m)\), and a proof that its
support classifier agrees with the AFK indexing object. It must state
separately whether it scans all forms or only the conductor-one subfamily.
The latter would be a narrower theorem, not a substitute for the stated
objective.

## D12-C1 correction

The first exploratory D12 lowering branch is superseded.  It used the
stabilizer eigenunit \((11+3\sqrt{13})/2\) in place of the AFK/Kopp
fixed point \(\rho=(3+\sqrt{13})/2\).  Therefore its shortcut count,
six-modulus lowering ledger, and dependent packet output are not valid
ray-label evidence.  The correction record is
`docs/tcc-sweep-d12-correction-v1.md`; the replacement outputs are
`discovery/tcc-sweep-d12-conductor-lowering-corrected-v2.json` and
`discovery/tcc-sweep-d12-lowered-engine-a-packets-corrected-v2.json`.
They are `EXPLORATORY` and make no TCC claim.

## Falsification record

The former tuple-only premise would be restored only by a proved,
label-preserving equivalence from every relevant
\(\operatorname{Clt}_{d\infty_2}(\mathcal O_f)\) support object to the
same maximal-order quotient, uniform in every allowed \(f\mid f_j\).
No such theorem was found in AFK, and AFK's displayed use of
\(\mathcal O_f\) is direct contrary evidence.

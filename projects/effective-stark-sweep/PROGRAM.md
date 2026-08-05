# Effective-Stark master plan

**Role:** authoritative project map and execution ledger  
**Last reconciled:** 2026-07-31 UTC
**Prior checkpoint:** `c5fa6657db302f8f180bf3e1b435ac83dc5b1be3`  
**Historical evidence:** `docs/cycle-*.md`, `artifacts/*.json`, and preserved
failed transcripts

This file is the single current plan for the Effective-Stark project.
Cycle notes record what happened; they do not override this file.
When an old note and this plan disagree, the newer certified artifact
named here controls. A mathematical claim still requires its own
certificate: this plan records state but is not evidence for a theorem.

## How to maintain this file

At the beginning and end of every research block:

1. update the status and evidence link of each affected item;
2. move newly discovered obligations into the dependency graph before
   starting downstream work;
3. record failures and supersessions rather than deleting them;
4. distinguish `ELIGIBLE` screening results from case-level `PROVED`
   packets;
5. commit this file with the corresponding scripts, artifacts, and
   manuscript changes.

Allowed plan states are:

- `BANKED`: proved or replay-certified, with named evidence;
- `ACTIVE`: work currently authorized;
- `READY`: unblocked but not started;
- `BLOCKED`: a named predecessor is incomplete;
- `QUARANTINED`: a prior claim or route cannot be used;
- `DEFERRED`: deliberately outside the current execution block;
- `HUMAN`: requires referee, correspondence, or publication authority.

The mathematical tags remain separate:
`VERIFIED`, `ENCLOSED`, `NUMERICAL`, and `CONJECTURAL`.

## Project objective

The project has two complementary mathematical products:

1. **Effective theorems and selected instances:** reusable proofs for
   unconditional one-place archimedean Stark packets over real
   quadratic fields.
2. **Certified census and frontier map:** a genuine-provenance
   classification of the frozen 8,200 representatives, followed by
   case-level identification where claimed and a structural analysis
   of the reachable and obstructed zones.

The project is not complete merely because routing is complete.
For every occurrence, the following levels must be kept distinct:

```text
genuine W1 predicate
        |
        v
engine eligibility / FRONTIER classification
        |
        v
W2 algebraicity data and closure reconstruction
        |
        v
W3 packet identification and Artin labeling
        |
        v
occurrence transport
        |
        v
case-level PROVED corpus entry
```

## Current snapshot

| Track | State | Current fact | Controlling evidence / file |
|---|---|---|---|
| Results paper | `PUBLISHED` | v1.5 is public at DOI 10.5281/zenodo.21713178; the integrated 19-page main paper sorts first and is the default preview | `paper/effective-stark-results.tex`, `artifacts/zenodo-results-publication-v6.json` |
| Results v1.4 correction | `BANKED` | The withdrawn-orientation correction, Tangedal--Young page correction, and RQ-000013 addendum are published and publicly verified | `artifacts/zenodo-results-publication-v5.json`, `docs/cycle-082-results-v1.4-publication.md` |
| Results v1.5 integration | `BANKED` | Public v1.5 merges RQ-000013 into the 19-page main paper, omits the standalone addendum at deposit root, and verifies `effective-stark-results-00-main-paper.pdf` as the default preview | `artifacts/zenodo-results-publication-v6.json`, `docs/cycle-084-results-v1.5-publication.md` |
| Results-paper audit | `BANKED` | Versioned full A/B/C audit and extracted companion replay pass, including exact Engine-A degeneracy and the sigma-positive Engine-C re-audit | `artifacts/results-paper-referee-audit-v4.json`, `artifacts/engine-c-fourier-convention-correction-v3.json` |
| Genuine routing census v5 | `BANKED` | 8,200/8,200 genuine screens; proxy recovery complete | `artifacts/full-census-yield-declaration-v5.json` |
| Census-paper range | `BANKED_CORRECTED_BOUNDARY` | Amendment v18 preserves all 8,200 rows and defines them as finite-ideal conjugacy orbits followed by the pinned \(\infty_2\) choice; they are not the full orbit set of all pointed one-place moduli | `data/census-paper-preregistration-amendment-v18.json`, `artifacts/census-paper-referee-revision-v1.json` |
| Census-paper Layer 0 | `BANKED` | Clean PARI enumeration reproduced the backbone; support-first split is T/Q/H = 3,936/1,560/2,704 | `artifacts/census-paper-layer0-reconciliation-v1.json` |
| Census packet synthesis | `BANKED` | Compositum-free trace descent, the RQ-000245 proper-image gate, and all 1,560 exact Q-row packet polynomials pass; the corpus hash-chain root is `7c04242b1d4c11293af96f83f4915dbed25f6125c60d82965e533df5c9d81855` | `artifacts/census-q-packet-corpus-audit-v1.json`, `docs/cycle-087-census-q-packet-corpus.md` |
| Quadratic Euler-degeneracy theorem | `BANKED` | The deleted-prime cover criterion proves that a quadratic-support packet is one exactly when every supported character has a deleted prime of primitive-character value +1.  It classifies all 346 frozen rows with zero errors.  The apparent four-support obstruction is refuted exactly at norm 252 over Q(sqrt(7)) | `artifacts/q-euler-deleted-prime-cover-theorem-v1.json`, `docs/cycle-128-q-euler-deleted-prime-cover-theorem.md` |
| All-order deleted-prime implication | `BANKED` | The one-way all-order Euler-factor cover theorem is proved.  Exact H local features find 64 fully covered rows among 2,704; it has no higher-order converse, and it does not settle RQ-000692 | `docs/cycle-131-all-order-deleted-prime-cover-theorem.md`, `artifacts/h-all-order-deleted-prime-cover-audit-v1.json` |
| Q(sqrt(21)) wild-3 target | `BANKED_SHARED_OBJECT_DOSSIER` | RQ-000692's exact local row has relative ramification index 6 above 3, while every other registered Roblot gate passes. The dimension-6 companion uses the same (C_6) ray group and ray field (its polynomial is the census polynomial at (-X)); the oriented analytic bridge remains open | `docs/cycle-132-qsqrt21-wild3-dossier.md` |
| Census coefficient-height cap | `BANKED` | The height predictor observed 89 digits, the frozen cap is 256 digits, and the exact corpus maximum is 62 digits | `artifacts/census-packet-height-calibration-v1.json`, `artifacts/census-q-packet-corpus-audit-v1.json` |
| Census H taxonomy | `ACTIVE_COMPLETION` | The 2,704-row H matrix and per-order frontier are assembled.  V2 corrects its displayed index provenance; five legacy quartic kernels remain incomplete while a separately preregistered completion run is active | `artifacts/census-h-taxonomy-v2.json`, `docs/cycle-092-h-taxonomy-index-provenance-correction.md`, `docs/cycle-093-quartic-completion-preregistration.md` |
| Worked imprimitive Engine-A row | `BANKED` | RQ-000013 has exact \(E_\chi=2\), \(I_\chi=2\), and packet \(X_{[0]}=u^2,\ X_{[1]}=u^{-2}\) | `artifacts/rq000013-engine-a-imprimitive-certificate-v1.json` |
| Census manuscript | `BANKED_LOCAL_V1_1_CORRECTION` | Published v1.0 remains immutable; the nine-page local v1.1 candidate clarifies the orbit-count display, Theorem 3 condition labels and nonvanishing input, the finite-corpus route partition, and the 309+73 sextic certificate split.  All audits and 175 tests pass | `paper/effective-stark-census.tex`, `artifacts/census-paper-referee-correction-v3.json`, `docs/cycle-130-census-referee-feedback-correction.md` |
| Census Zenodo release | `PUBLISHED_AND_PUBLICLY_VERIFIED` | Version 1.0 is public at DOI `10.5281/zenodo.21729947`; all three downloads match frozen hashes and the main paper is the default preview | `docs/cycle-129-census-zenodo-publication.md`, `artifacts/zenodo-census-publication-v1.json` |
| Census v1.1 referee correction | `BANKED_LOCAL_CORRECTION` | Five post-publication comments are closed locally without changing a theorem or count; a future public correction requires a new Zenodo version | `docs/cycle-130-census-referee-feedback-correction.md`, `artifacts/census-paper-referee-correction-v3.json` |
| Engine-B occurrence transport | `ACTIVE_COMPLETION` | Twenty-two exact noncanonical transports are sealed. Of the former 220 open members, the corrected screen gave 116 direct-coprime-route obstructions and 104 source-or-proof-open; ten certified-source directions now close, leaving 210 open | `artifacts/engine-b-transport-ledger-v5.json`, `artifacts/corrected-direct-source-transports-v1.json` |
| W4 census analysis | `BANKED_WITH_SCOPE_GATES` | All five preregistered descriptive slices are replayed: the 51-closure certified safe-exponent scope and the 1,560-row Q family corpus are exact; the v5 tower slice correctly reports zero completed transports and infers no recurrence | `artifacts/w4-genuine-index-distribution-v1.json`, `artifacts/w4-frontier-norm-v1.json`, `artifacts/w4-completion-v1.json` |
| DST / Cohen--Roblot comparison | `BANKED_FOR_FOUR_OBJECT_CONTROLS` | Primary-source theorem boundaries are read and four exact Hilbert/ray controls give three containments and one noncontainment; a row-level theorem-hypothesis map remains open | `docs/prior-art-overlap-table-v3.md`, `docs/cycle-105-prior-art-object-controls.md` |
| Public certificate archive | `PUBLISHED` | DOI-bearing companion v17 published; SHA-256 `e2a945edaddcec32e3aad10e67f8b960af0bc304b07ba5503ab7be62384b9506` | `artifacts/zenodo-results-publication-v5.json` |
| v1.5 certificate archive | `PUBLISHED` | Deterministic companion v18 SHA-256 `4a6d4417610215278d7be7788e2ae7845ee2c75ec5b22690c47b717c15e5b024` is public and extracted-replay verified | `artifacts/zenodo-results-publication-v6.json` |
| Zenodo / arXiv | `ZENODO_DONE` | Results v1.5 is published and publicly checksum-verified; arXiv remains a separate human action | DOI `10.5281/zenodo.21713178` |

### Genuine census v5 routing counts

These are screening/routing counts, not 2,673 already identified
nontrivial packet theorems.

| Verdict | Occurrences | Meaning |
|---|---:|---|
| `PROVED_TRIVIAL` | 3,899 | Exact empty-support identities |
| Engine A eligible | 1,560 | Governed by the uniform quadratic theorem |
| Engine B eligible | 232 | 88 distinct normal closures |
| Engine C eligible | 881 | 447 packet fields; 1,361 packet occurrences |
| `FRONTIER` | 1,628 | Named genuine obstruction |

FRONTIER taxonomy: 1,088 index, 502 exponent-cap, 31 unit-congruence,
five tool, and two real-place failures. The genuine norm-quartile
frontier shares are 8.42%, 19.53%, 24.58%, and 28.53%. These statistics
are banked at the routing-census level; their mathematical
interpretation belongs to W4.

The Engine-A row count is a routing count.  A subsequent exact
imprimitive-Euler audit found 672 zero Euler products among 2,232
supported quadratic character occurrences, affecting 603 rows; in
346 rows every supported derivative vanishes and the explicit product
is empty, so \(X_A=1\).  Before the census paper prints packet counts,
W4 must distinguish routing support from effective derivative support.

For the census paper, v5's routing labels are not the structural
trichotomy. A support-first audit found 3,936 empty-support rows:
3,899 labeled `PROVED_TRIVIAL` in v5 and 37 mislabeled `FRONTIER`
because the old declaration applied `EXPONENT_CAP` before the
empty-support theorem. The paper-level split is therefore
T/Q/H = 3,936/1,560/2,704, with the higher-order stratum cross-tabulating
as 232 B-eligible, 881 C-eligible, and 1,591 frontier. The v5 artifact
is preserved as historical routing evidence; the correction is banked
in `artifacts/census-paper-layer0-reconciliation-v1.json`.

## Banked theorem inventory

The current results manuscript contains the following mathematical
content. This list is a scope ledger, not a substitute for the paper.

1. `BANKED` — uniform Engine-A quadratic-support theorem and explicit
   positive-unit product.
2. `BANKED` — first unconditional order-six packet,
   \(\mathbb Q(\sqrt7),\mathfrak p_7\infty_2\), with margin \(>5688\).
3. `BANKED` — order-six replication over \(\mathbb Q(\sqrt{14})\),
   margin \(>7315\).
4. `BANKED` — ramified-prime-3 order-six neighbor RQ-002057 over
   \(\mathbb Q(\sqrt{57})\).
5. `BANKED` — first selected order-ten packet RQ-001107 over
   \(\mathbb Q(\sqrt{33})\).
6. `BANKED` — eight selected Engine-B packets in total, including
   RQ-000458 through Engine B.
7. `BANKED` — cyclic-quartic CM norm bridge under explicit
   \(C_4\), reinduction, Stark-unit, divisibility, and
   normal-closure hypotheses.
8. `BANKED` — five selected Engine-C packets: the
   \(\mathbb Q(\sqrt{35})\) mixed-class-number case, three corrected
   primitive \(e=6\) packets, and the natural \(e=8\)
   \(\mathbb Q(\sqrt6)\) route.
9. `BANKED` — absolutely-abelian no-go lemma.
10. `BANKED` — Shintani-index parity lemma, checked against 446 genuine
    odd-index cases.
11. `BANKED_WITH_OPEN_ORBIT_GATE` — compositum-free Engine-A
    packet-power synthesis:
    norm-one traces remain in \(K\), the exact resultant recurrence
    doubles the ambient formal sign orbit without constructing the
    compositum, and a separate denominator-lift gate is mandatory when
    the Fourier exponents have common denominator \(q>1\).  The
    dimension-eight \(q=2\) lift is exact, reciprocal, and irreducible
    over \(K\).  For \(C_2^3\), four supported characters have only
    eight Artin sign patterns.  RQ-000089 was preserved as a failed
    anchor choice because one factor vanishes; RQ-000245 must close
    the exact Artin-factor gate before corpus promotion.

### Quarantined or narrowed claims

- `QUARANTINED` — the \(\mathbb Q(\sqrt6)\), \(e=12\)
  auxiliary-prime route is only a cross-check until individual prime
  ideals, local characters, finite valuations, and residual
  \(S\)-unit ambiguity are closed.
- `QUARANTINED` — RQ-000458's Engine-C calculation is a normalization
  diagnostic. Its theorem claim rests on Engine B.
- `QUARANTINED` — the original \(e=6\) large polynomials were powered
  representatives, not primitive packets. The corrected primitive
  polynomials and six-route replay are in
  `artifacts/engine-c-e6-primitive-packet-correction-v1.json`.
- `QUARANTINED` — all proxy-derived index laws and pre-v5 census
  statistics. They remain process evidence only.

## Dependency map

```text
RESULTS PAPER
  complete mathematical revision
    -> fresh human referee round
      -> public certificate archive
        -> DOI / arXiv publication

CENSUS PAPER
  genuine routing census v5 [done]
    -> support-first T/Q/H reconciliation [done]
      -> Q exact corpus + H taxonomy
        -> W4 structural analysis
  regenerate v5 Engine-B transport scope
    -> close occurrence transport
      -> transported occurrence PROVED claims
  DST / Cohen--Roblot overlap comparison ------------+
  revise existing Markdown draft --------------------+
                                                       v
                                     journal LaTeX + tables + appendix
                                                       |
                                                       v
                                             full referee round
                                                       |
                                                       v
                                           corpus DOI / publication

THEORY
  effective Engine-B theorem
    -> obstruction theorem
  cyclic-quartic CM bridge [banked]
    -> auxiliary-prime independence
    -> higher-order CM descent
  occurrence transport
    -> conductor/norm-coherence theorem
```

## Immediate execution queue

Work in this order unless a newly discovered mathematical failure
changes a dependency.

### M0 — Keep the map truthful

- [x] Create the master plan.
- [ ] Reconcile the stale `README.md` narrative with census v5 and the
      full-paper freeze.
- [ ] At every checkpoint, update this plan before writing the status
      report.

### P1 — Referee the results paper

State: `ACTIVE`

- [x] Restore the complete three-engine manuscript.
- [x] Correct the primitive \(e=6\) CM packets.
- [x] Narrow the two unsupported proof routes.
- [x] Pass deterministic build and full internal audit.
- [x] Repair the powered-only notation in the all-embeddings
      height-rigidity lemma.
- [x] Add the hypothesis \(j(E)=E\), \(j|_k\ne1\), before defining
      the CM fixed field and norm.
- [x] Map the Shintani transfer proposition to the source's exact
      definitions, pages, equations, and propositions.
- [x] Replace the survey-bounded priority assertion by “we are
      unaware,” with the public search perimeter promised in the
      supplement.
- [x] Build and locally freeze the companion archive with minimal
      per-theorem verifiers, expected outputs, hashes, proof flags,
      runtimes, and memory.
- [x] Remove the superseded three-page CM gap-ledger manuscript and
      PDF so it cannot be mistaken for a second paper.
- [x] Correct the abstract to the proved \(e=2,6,8\) CM routes and
      state the five order-six rows without an ambiguous partial count.
- [x] Replace every manual equation tag by `label`/`eqref` numbering.
- [x] Freeze the Fourier, inverse-transform, Artin-action, and quartic
      generator conventions and reference them from Engines A and C.
- [x] Close the zero-radius nonsplit-place pairing in the height lemma
      and cite Voutier's main theorem with its degree range.
- [x] Audit the Engine-A zero-Euler-factor degeneracies exactly and add
      the result to the written theorem discussion and companion.
- [x] Add the explicit Theorem 2 completion marker and close all
      bibliography citation gaps.
- [x] Replace the priority language by the non-load-bearing statement
      that the authors are not aware of previous unconditional
      one-place packets at support order ten; cite the program's prior
      order-six and order-eight results explicitly.
- [x] Correct the Engine-C Fourier sign to
      \(L'_S(0,\psi)=-(4/e)(\ell_1+i\ell_\sigma)\) and the packet
      action to \(N_{E/E^+}(\sigma^r u)^{-1}\), matching the exact
      positive-power bridge loop; preserve the superseded record and
      bank an exact convention-correction audit.
- [x] Restate Shintani's three operational hypotheses in the paper.
- [x] Enlarge the main theorem tables, move exact HNFs to a readable
      appendix, and move the complete record map, interval replay, and
      Engine-A queue statistics to a separate supplement.
- [x] Deposit the companion archive under a public immutable
      identifier and put that identifier in the manuscript.
- [x] Preserve the later five-control direct/inverse circularity
      finding and build a deterministic v1.4 correction layer.
- [x] Audit Track A2 against the immutable v1.3 source: retain the
      historical back-reference, companion-paper anchor citations, and
      Tate/Arakawa/Roblot scope paragraph; correct Tangedal--Young
      pages 1022--1045 to 1045--1061.
- [x] Replace legacy auditors that rewrote v1 records with versioned
      Engine-C v2 and full-referee v3 successor artifacts.
- [x] Reserve the v1.4 DOI without publishing: draft 21712478,
      DOI 10.5281/zenodo.21712478.
- [x] Insert the DOI into all release-facing sources and metadata;
      independently rebuild all PDFs and deterministic companion v17.
- [x] Upload metadata and exactly seven files to the unsubmitted draft;
      verify requested metadata fields, remote MD5 checksums, byte
      counts, and local SHA-256 values.
- [x] Obtain immediate explicit publication approval and publish the
      correction layer.
- [x] Merge the RQ-000013 addendum into the v1.5 main paper, preserve
      the historical standalone addendum inside nested companion v17,
      and omit it from the new deposit root.
- [x] Name the v1.5 main upload so it sorts first, then verify from the
      authenticated draft record that it is Zenodo's default preview.
- [x] Build and extracted-replay deterministic companion v18; upload
      and checksum-verify the exact five-file v1.5 inventory.
- [x] Publish and publicly verify v1.5 DOI
      10.5281/zenodo.21713178.
- [ ] Conduct a new Papers-I/II-style referee pass over every displayed
      theorem, polynomial, exponent, height margin, and citation.
- [ ] Resolve every resulting mathematical issue.
- [x] Build a public, hash-manifested certificate archive.
- [x] Rebuild the exact manuscript version against that archive.
- [x] Obtain human authorization before Zenodo publication.
- [ ] Obtain human authorization before arXiv submission.

Definition of done: referee report closed; paper and public artifact
cross-reference one another; DOI exists; uploaded source and PDF match
the frozen hashes.

### P2 — Finish the census paper

State: `ACTIVE`

- [x] Freeze the existing maximal-order range and the RQ registry:
      squarefree radicands \(2\le D\le200\), integral-ideal norm at
      most 100, finite ideals deduplicated under field conjugation and
      then paired with the pinned \(\infty_2\) place.
- [x] Issue the Cycle-127 range-description amendment: the 8,200 rows
      are a canonical selected-modulus census, not the full quotient of
      all pointed one-place moduli.  Do not change the frozen RQ rows.
- [x] Correct the manuscript's false empty-support/trivial-packet
      biconditional: empty support is sufficient, while 346 nonempty-Q
      rows also evaluate to the value-one packet through Euler zeros.
- [x] Replace the complete-H wording by the exact boundary: 2,699 rows
      have complete registered-mechanism status and five quartic rows
      remain tool-incomplete.
- [x] Preserve the historical degree-32 exact-resultant cap and freeze
      the deterministic 50-row independent analytic audit.
- [x] Supersede the compositum-degree cap by a versioned trace-descent
      amendment without rewriting the original preregistration.
- [x] Prove the trace recurrence for denominator-cleared packet powers
      and pass the dimension-eight \(q=2\) positive-factor lift.
- [x] Preserve RQ-000089's failed proper-image anchor selection: one
      of its four supported terms has zero Euler product.
- [x] Close the proper-Artin-image factor gate on the corrected
      four-effective-character anchor RQ-000245.
- [x] Calibrate the \(\sum_\chi L'(0,\chi)\) coefficient-height
      predictor and freeze a numeric height cap before the full
      Q-stratum polynomial run.
- [x] Rerun the PARI ideal enumeration and reproduce the 121 fields,
      13,939 raw ideals, and 8,200 representatives exactly.
- [x] Reconcile the structural T/Q/H split. Correct the 37
      empty-support rows that v5 routed to `FRONTIER`; preserve v5
      rather than rewriting history.
- [x] Reconcile the Q-stratum counts: 1,560 rows, 2,232 supported
      quadratic characters, 912 quartic fields, 672 zero Euler
      products, 603 affected rows, and 346 all-vanishing rows.
- [x] Build the row-level exact Q corpus under the uniform theorem:
      all 1,560 rows pass, with a verified hash-chain root
      `7c04242b1d4c11293af96f83f4915dbed25f6125c60d82965e533df5c9d81855`.
- [x] Preselect RQ-000013 as the first one-character, one-removed-prime,
      nonzero imprimitive branch, hence the worked \(E_\chi=2\) row.
- [x] Complete and print RQ-000013's exact unit/index calculation;
      share its certificate with the census draft and a versioned,
      locally staged results-paper supplement addendum. The published
      v1.3 files remain immutable pending authorization for a new version.
- [x] Run the preregistered independent 50-row Arb audit: the 192-bit
      initial pass preserved a radius failure at RQ-006617; the
      unchanged route passes all 50 rows and 101 Artin sign rows at
      384 bits.
- [x] Build the support-order/Engine-B/Engine-C/Roblot/resolution
      matrix for all 2,704 H rows.
- [x] Extract the minimal unresolved row at every support order and
      the minimal all-mechanisms-fail row, led by the
      \(\mathbb Q(\sqrt{21})\) wall.
- [ ] Complete the five legacy quartic kernels under Cycle 093's
      preregistered completion protocol.  The existing PARI 2.15.4
      segmentation-fault records remain historical evidence; a new PARI
      version or exact construction route is a separately labelled route,
      never a silent replacement.
- [x] Derive a new v5 occurrence-transport manifest from 232 Engine-B
      eligible rows and 88 closures. Reconcile it explicitly against
      the obsolete 195-row/51-closure ledger; do not silently reuse the
      old count of 187 pending transports.
- [ ] Certify member-modulus identity, ray-class map, orientation, and
      packet transport for every occurrence claimed at case level.
- [ ] Seal the transport ledger before calling any transported
      occurrence case-level `PROVED`. Structural T/Q/H counts and
      mechanism eligibility do not wait on transport.
- [x] Run W4 in the preregistered order:
  1. Shintani-index distribution;
  2. FRONTIER share versus conductor norm;
  3. safe-exponent growth;
  4. packet-polynomial families;
  5. tower and norm-compatibility signals.
- [x] Tag pattern discovery as `CONJECTURAL` until an exact theorem is
      proved.
- [x] Characterize the 346 quadratic-support value-one rows from exact
      deleted-prime local data under Cycle 128; preserve every failed
      coarse simplification and promote only a bound-independent
      Euler-factor theorem.
- [x] Complete the primary-source theorem boundary and the
      preregistered four-control DST / Cohen--Roblot object table.
- [ ] Run any future row-level theorem-hypothesis comparison as a
      separately preregistered project; the four object controls do not
      supply it.
- [ ] Decide the paper's exact claim boundary: routing census,
      fully identified subcorpus, and unresolved eligible queue must be
      printed separately.
- [ ] Convert `paper/effective-stark-sweep-draft.md` into a standalone
      LaTeX manuscript and PDF.
- [ ] Include the v1--v5 correction history and R-13 provenance audit
      in an appendix, compressed in the mathematical narrative.
- [ ] Run a full referee and replay round.

Definition of done: every population number has genuine provenance;
every occurrence called proved has transport; W4 is reproducible;
the prior-art comparison is explicit; the paper has a compiled,
audited PDF.

### P3 — Corpus release

State: `BLOCKED` on P2

- [ ] One machine-readable record per frozen representative.
- [ ] Separate routing verdict, proof engine, W2/W3 state, transport
      state, and mathematical tag.
- [ ] One-command replay for a sample from each engine and obstruction.
- [ ] SHA manifest and immutable DOI.

## Highest-value theorem program

These directions are ranked by reusable mathematical value, not by the
number of additional computed examples.

### T1 — Effective Engine-B theorem

Priority: **1**  
State: `READY`

Goal: prove a reusable theorem of the following form.

> If a one-place real-quadratic ray field satisfies explicit
> unit-congruence, real-place, and index-two hypotheses, then an
> explicitly computable exponent \(m\) makes every relevant
> \(X_A^m\) algebraic in the stated ray field. Given certified
> all-conjugate analytic enclosures below a computable height threshold,
> the Artin-labeled packet is uniquely determined, and the procedure
> terminates as precision increases.

Required subresults:

- [ ] Translate the exact Shintani hypotheses and theorem numbers into
      modern ray-class notation without relying on case scripts.
- [ ] Define \(H\), the transfer conductor, every divisor datum, the
      class-number/root-of-unity factors, \(n(S_{\mathfrak d})\), and
      the safe exponent.
- [ ] Give a closed formula or terminating exact algorithm for \(m\).
- [ ] Prove the ray-field containment and Artin transport for
      \(X_A^m\).
- [ ] Give an a priori degree bound for the comparison quotient.
- [ ] State exactly which archimedean conjugates the evaluator must
      enclose.
- [ ] Prove the all-embeddings height-rigidity lemma, including the
      degree-one and degree-two fallbacks.
- [ ] Prove termination once the exact algebraic candidate is
      separated and analytic radii tend to zero.
- [ ] Replay all selected Engine-B cases as corollaries, not as
      independent theorem substitutes.

Current leverage: the results paper already contains a Shintani
transfer proposition and a height-rigidity lemma. The missing research
step is to make their hypotheses, degree control, and termination
uniform enough that the cases become corollaries.

### T2 — Obstruction theorem

Priority: **2**  
State: `READY`, informed by T1

Goal: distinguish a genuine algebraicity obstruction from limitations
of the current effective algorithm.

Questions:

- [ ] Is index two sufficient once the exact local and
      unit-congruence hypotheses hold?
- [ ] Which wild-ramification predicate fails for
      \(\mathbb Q(\sqrt{21})\)?
- [ ] Can failure be predicted from ray-group and unit-image data
      without constructing the full transfer?
- [ ] Can an alternative imaginary quadratic base restore a transfer?
- [ ] Which FRONTIER classes mean “the theorem does not apply,” and
      which mean only “degree/precision exceeds the frozen cap”?

Target deliverable: a theorem or exact decision diagram separating
`MATHEMATICAL_OBSTRUCTION` from `EFFECTIVITY_FRONTIER`, with
\(\mathbb Q(\sqrt{21})\), RQ-002057, and the ramified-\(7\) pair as
controls.

### T3 — General CM-descent theorem

Priority: **3**  
State: `BANKED` for cyclic quartic; `READY` beyond that scope

The current paper proves the cyclic-quartic bridge only under explicit
hypotheses. Preserve that theorem and extend it carefully rather than
calling it “general-\(e\).”

The next theorem should expose:

- [x] \(\operatorname{Gal}(E/k)\simeq C_4\), generator, internal
      involution, and global complex conjugation;
- [x] exact linear reinduction and imprimitive local Euler factors;
- [x] Fourier normalization and primitive extraction in the anti-unit
      lattice;
- [x] root-of-unity invariance of the positive CM norm;
- [x] common-normal-closure Artin labeling;
- [ ] a character-by-character extension beyond cyclic quartic;
- [ ] precise scopes for support orders \(6,8,10,12\), without
      conflating support order with \(|\mu(E)|\);
- [ ] a general orbit-size and orientation theorem.

Any higher-order theorem must replay the corrected \(e=6\) routes and
the clean \(e=8\) route. The quarantined \(e=12\) calculation cannot
serve as a proof anchor until T4 closes its valuation problem.

### T4 — Auxiliary-prime independence

Priority: **4**  
State: `READY`

Goal: prove how enlarging \(S\) changes the Stark unit through exact
group-ring Euler factors and when the original torsion-invariant CM
norm can be recovered.

Required components:

- [ ] Treat prime ideals of \(k\), not only rational primes.
- [ ] Separate split, inert, and ramified auxiliary primes.
- [ ] State local character values and group-ring Euler factors.
- [ ] Track both archimedean logarithms and finite valuations.
- [ ] Give a unit-lattice divisibility criterion for primitive
      extraction.
- [ ] Prove uniqueness modulo torsion and exclude residual
      \(S\)-unit factors.
- [ ] Prove independence of the auxiliary prime under explicit
      hypotheses.
- [ ] Apply the theorem to the \(\mathbb Q(\sqrt6)\), \(e=12\) route;
      promote it only if every hypothesis passes.

### T5 — Conductor transport and norm coherence

Priority: **5**  
State: `READY` after P2 transport

Goal: replace computationally reported transport by a formal
distribution relation between packets at
\(\mathfrak f\) and \(\mathfrak f\mathfrak q\).

Questions and deliverables:

- [ ] Derive the exact Euler-factor relation between the two
      differenced zeta derivatives.
- [ ] Prove when packet polynomials persist under conductor
      enlargement.
- [ ] Explain the norm-32 to norm-64
      \(\mathbb Q(\sqrt{35})\) transport.
- [ ] Test exact norm compatibility across all transported v5
      occurrences.
- [ ] Separate genuine Euler-system-like relations from numerical
      pattern matching.

A positive corpus-wide pattern is `CONJECTURAL` until the exact
distribution identity and Artin-label compatibility are proved.

## Research scheduling

The next block should not start five theorem projects simultaneously.

1. Keep P1 in the human referee lane.
2. Close P2 transport and begin the prior-art comparison.
3. Start T1 as the primary theory project.
4. Use P2/W4 data to formulate T2 and T5 precisely.
5. Start T4 before extending T3 to any route that needs an auxiliary
   prime.

No additional isolated W3 case outranks T1 unless it is a necessary
control or counterexample for T1/T2.

## Recent execution ledger

| Cycle | Finding | Status | Evidence |
|---:|---|---|---|
| 078 | RQ-000013 closes the first preregistered nonzero imprimitive Engine-A branch with exact \(E_\chi=I_\chi=2\) and \(X_{[0]}=u^2,\ X_{[1]}=u^{-2}\); the `bnrL1` comparison remains quarantined | `BANKED`, `PROVED` | `docs/cycle-078-rq000013-imprimitive-engine-a.md`, `artifacts/rq000013-engine-a-imprimitive-certificate-v1.json` |
| 079 | Public v1.3 was found to predate the withdrawn oriented-replay correction; deterministic v1.4 layer built and extracted replay passed, but no DOI was reserved or published | `CONTAINED_CORRECTION`, `HUMAN` | `docs/cycle-079-results-v1.4-correction-staging.md`, `artifacts/results-paper-v1.4-publication-candidate-v1.json` |
| 080 | Exact comparison with immutable v1.3 found the requested wording already present but exposed the incorrect Tangedal--Young pages; the one-line correction, versioned auditors, full replay, and deterministic companion v16 are locally frozen | `CONTAINED_BIBLIOGRAPHIC_CORRECTION`, `HUMAN` | `docs/cycle-080-results-track-a2-correction.md`, `artifacts/results-paper-v1.4-publication-candidate-v2.json` |
| 081 | Zenodo draft 21712478 reserved DOI 10.5281/zenodo.21712478 without publication; the DOI-bearing main paper, supplement, RQ-000013 addendum, and companion v17 were independently rebuilt, replayed, uploaded as an exact seven-file inventory, and checksum-verified | `DOI_DRAFT_UPLOADED_VERIFIED_UNPUBLISHED`, `HUMAN` | `artifacts/zenodo-results-v1.4-draft-upload-verification-v1.json`, `artifacts/results-paper-v1.4-publication-candidate-v4.json` |
| 082 | After explicit human approval, results v1.4 was published at DOI 10.5281/zenodo.21712478; all seven public downloads match the frozen byte counts, MD5 checksums, and SHA-256 checksums | `PUBLISHED_AND_PUBLICLY_VERIFIED` | `docs/cycle-082-results-v1.4-publication.md`, `artifacts/zenodo-results-publication-v5.json` |
| 083 | RQ-000013 was merged into the deterministic 19-page v1.5 main paper; the standalone addendum is preserved only inside nested v17, the five-file draft is checksum-verified, and the lexically first main PDF is Zenodo's authenticated draft preview | `DOI_DRAFT_UPLOADED_VERIFIED_UNPUBLISHED`, `HUMAN` | `docs/cycle-083-results-v1.5-main-paper-integration.md`, `artifacts/zenodo-results-v1.5-draft-upload-verification-v1.json` |
| 084 | Under the standing Zenodo authorization, v1.5 was published at DOI 10.5281/zenodo.21713178; all five public downloads match bytes, MD5, and SHA-256, the concept latest endpoint resolves to v1.5, and the main paper is the public preview | `PUBLISHED_AND_PUBLICLY_VERIFIED` | `docs/cycle-084-results-v1.5-publication.md`, `artifacts/zenodo-results-publication-v6.json` |
| 085 | The degree-32 compositum cap was superseded by a preregistered trace-descent route.  Exact resultants now synthesize the sign orbit of denominator-cleared packet powers over \(K\); a heightened check corrected the direct-packet claim when \(q>1\).  The dimension-eight \(q=2\) positive reciprocal factor and its irreducible degree-eight absolute polynomial pass exactly; archived numerics are quarantined validation only | `BANKED`, `PROVED` recurrence and lift; `OBSERVED` numerical cross-check | `docs/census-paper-preregistration-amendment-v1.md`, `artifacts/census-packet-polynomial-synthesis-v1.json` |
| 086 | Heightened checks exposed two further necessary gates: formal sign patterns can exceed the Artin image, and the first four-support anchor RQ-000089 loses one factor to a zero Euler product.  The corrected preregistered anchor RQ-000245 certifies the four-character relation, eight-element Artin image, exact denominator-two lift, unique degree-eight factor over \(K\), and degree-sixteen absolute polynomial without opening an analytic target | `BANKED`, `PROVED`; failed anchor preserved | `docs/census-paper-preregistration-amendment-v2.md`, `docs/census-paper-preregistration-amendment-v3.md`, `artifacts/rq000245-packet-synthesis-v1.json` |
| 087 | The full 1,560-row height-only calibration observed a maximum 89-digit predictor and froze a 256-digit cap.  An initial unit-lattice square-root route timed out on RQ-001090 and RQ-001697 and was preserved; replacing only that implementation step by exact `nfeltissquare` reduced both rows from 300-second failures to about 0.1 seconds.  The clean hash-chained corpus then certified all 1,560 Q packet polynomials in 43.46 seconds, with degrees 1/2/4/8 occurring 346/930/242/42 times, denominators 1/2 occurring 1,491/69 times, and maximum exact coefficient-coordinate height 62 digits | `BANKED`, `PROVED` finite Q corpus; `OBSERVED` height calibration | `docs/cycle-087-census-q-packet-corpus.md`, `artifacts/census-packet-height-calibration-v1.json`, `artifacts/census-q-packet-corpus-audit-v1.json` |
| 088 | The deterministic 50-row analytic sample was frozen before values.  A genuinely separate regulator/class-number route, completed before opening corpus traces, passes 43 nonzero character comparisons and 101 Artin sign rows.  The 192-bit initial run's RQ-006617 radius failure is preserved; the unchanged route passes at 384 bits | `BANKED`, `CERTIFIED_NUMERICAL`; initial precision failure preserved | `docs/cycle-088-census-q-independent-arb-audit.md`, `artifacts/census-q-arb-audit-v1.json` |
| 089 | The sequential sextic screen's ten cap failures and timeout-cleanup defect were preserved and superseded by a preregistered primitive-field deduplication: 764 kernels collapse to 407 keys, 382 require a field certificate, and all receive exact applicability decisions.  Seventy-three candidate 3-divisible fields are rejected exactly by unramified cyclic cubic certificates.  The complete H taxonomy has 1,079 full Roblot weak-coverage rows and exact per-order frontier minima; five old quartic construction failures remain incomplete.  RQ-000692 over \(\mathbb Q(\sqrt{21})\) fails the sextic theorem through wild ramification above three | `BANKED`, `PROVED` sextic eligibility and 3-class obstructions; `OBSERVED` finite taxonomy | `docs/cycle-089-census-h-taxonomy.md`, `artifacts/roblot-sextic-population-v1.json`, `artifacts/census-h-taxonomy-v1.json` |
| 090 | The v5 Engine-B transport scope is frozen at 232 rows and 88 normal-closure groups.  It retains all 195 historical eligible and 159 historical pending IDs, adds 37 v5 IDs, and promotes no member.  Six legacy printed normal-closure polynomials differ from their v5 reconstruction and are preserved as a reconciliation gate rather than treated as an identity | `BANKED_SCOPE_ONLY`, `VERIFIED` population reconciliation | `docs/cycle-090-engine-b-v5-transport-scope.md`, `artifacts/engine-b-transport-manifest-v5.json` |
| 091 | The standalone census manuscript is written, checksum-manifested, visually inspected, compiled twice without warnings, and audited against the frozen evidence.  It states the exact T/Q/H census and H frontier while explicitly excluding uncompleted member transport and the five legacy quartic failures.  No submission or publication action occurred | `BANKED_LOCAL_MANUSCRIPT`, `PROVED` claims only where named artifacts supply exact evidence | `docs/cycle-091-census-manuscript-local-freeze.md`, `paper/effective-stark-census.tex`, `paper/effective-stark-census.pdf` |
| 092 | A referee-facing provenance correction supersedes the H-taxonomy display field: RQ-005298's legacy W1 index two is replaced by its genuine common-stable-modulus derived-subgroup order four.  Eligibility counts are unchanged; the manuscript must cite the successor before refreeze | `CORRECTION_ACTIVE`, `VERIFIED` index reconstruction | `docs/cycle-092-h-taxonomy-index-provenance-correction.md`, `artifacts/census-h-taxonomy-v2.json` |
| 093 | User-authorized completion protocol: allocate a three-hour exact rerun only to RQ-005298's previously deferred order-16 resolvent; do not spend time rerunning the four reproducible PARI 2.15.4 segmentation faults.  First reproduce those faults under a separately pinned newer PARI build or an explicitly recorded exact construction route, then run the same geometry predicates and independently cross-check any positive result | `ACTIVE`, no mathematical verdict | `docs/cycle-093-quartic-completion-preregistration.md` |
| 094 | User authorized one controlled fresh-process retry of the first legacy PARI 2.15.4 segmentation fault, RQ-002397 packet 2, concurrently with RQ-005298.  This is an exploratory reproducibility probe with a 1,200-second cap, not a change of mathematical verdict or an excuse to discard the old crash evidence | `ACTIVE`, no mathematical verdict | `docs/cycle-094-fresh-process-segfault-retry.md` |
| 095 | The Cycle-094 retry reproduced the PARI 2.15.4 segmentation fault in 0.017 seconds.  GP returned exit code zero despite the fatal diagnostic, exposing a status-parser defect; v1 is preserved and an explicit v2 correction records `TOOL_FAILURE_REPRODUCED` | `CORRECTION_ACTIVE`, no mathematical verdict | `docs/cycle-095-rq002397-parser-correction.md` |
| 096 | The RQ-005298 rerun reached 3.60 GiB resident memory after 57 minutes under its legacy 4 GB stack ceiling, with 11 GiB host memory available.  User authorized a resource-cap amendment: preserve and interrupt the partial run, then restart the identical exact calculation with a 10 GB stack ceiling | `ACTIVE`, no mathematical verdict | `docs/cycle-096-rq005298-memory-cap-amendment.md` |
| 097 | The preserved 4 GB run reached the exact order-16 subgroup-resolution stage and exhausted its stack after 58 minutes; GP again returned zero on user interrupt.  A versioned v2 correction marks it partial, and the 10 GB restart is active | `ACTIVE`, no mathematical verdict | `docs/cycle-097-rq005298-partial-run-correction.md` |
| 098 | W4's genuine index slice passes: the 8,200-row histogram reproduces exactly, with 2,426 index-one, 3,226 index-two, 2,548 higher-index records, and the registered 446 odd indices above two.  It is finite descriptive evidence only | `BANKED`, `OBSERVED_EXACT_FINITE_CENSUS` | `artifacts/w4-genuine-index-distribution-v1.json`, `docs/cycle-098-w4-index-distribution-preregistration.md` |
| 099 | W4's frontier/norm slice passes independently: the four v5 fractions 189/2245, 404/2069, 459/1867, and 576/2019 reproduce exactly and increase strictly within the frozen bins | `BANKED`, `OBSERVED_EXACT_FINITE_CENSUS` | `artifacts/w4-frontier-norm-v1.json`, `docs/cycle-099-w4-frontier-norm-preregistration.md` |
| 100 | W4 completion audit passes.  Exact W2 safe exponents over 51 closures range from 2,016 to 577,080,960; the Q packet-degree distribution is 346/930/242/42 in degrees 1/2/4/8; and the tower slice truthfully reports zero completed v5 transports and no recurrence inference.  The 51-closure exponent scope is not extrapolated to 88 v5 closures | `BANKED_WITH_SCOPE_GATES`, `OBSERVED_EXACT_FINITE_CENSUS` | `artifacts/w4-completion-v1.json`, `docs/cycle-100-w4-completion-scope.md` |
| 101 | The prior-art review opened the reachable primary texts before any scope claim: DST 2003 Theorems 2 and 4, and Roblot 2013 Theorems 5.5, 6.1, and 7.1.  Exact hypothesis alignment and Hilbert/ray object containment remain separate open checks | `ACTIVE`, literature boundary verified | `docs/prior-art-overlap-table-v2.md` |
| 102 | The first Cohen--Roblot object-level control passes: the degree-32 B5-079 normal closure has 11 quartic subfields, exactly one isomorphic to the Hilbert biquadratic field ℚ(√5,√7).  This is containment only, not a Stark-unit or packet comparison | `BANKED`, `PROVED_EXACT_SUBFIELD_TEST` | `artifacts/b5079-hilbert-ray-containment-v1.json`, `docs/cycle-102-hilbert-ray-containment-preregistration.md` |
| 103 | At user direction, the RQ-005298 10 GB run was intentionally stopped after 9,535.52 seconds at its 10 GB stack ceiling.  Its zero exit status is corrected versionedly to `PARTIAL_RESOURCE_CAP_RUN`; the quartic result has no mathematical verdict | `BANKED_PARTIAL`, no mathematical verdict | `artifacts/rq005298-extended-resolvent-stack10-v2.json` |
| 104 | Three further Cohen--Roblot Hilbert/ray containment controls are preregistered on frozen Engine-C selector fields for bases 42, 51, and 186.  Each records exact normal-closure subfields only; no unit or packet overlap is in scope | `ACTIVE`, no mathematical verdict | `docs/cycle-104-hilbert-ray-containment-tranche-preregistration.md` |
| 105 | The four exact Cohen--Roblot object controls are mixed: the selected ray normal closures contain the stated Hilbert field for bases 35, 42, and 186, but not for base 51.  This is field containment only, with no unit, packet, or row-level theorem-hypothesis claim | `BANKED`, `PROVED_EXACT_SUBFIELD_TEST` | `artifacts/b5079-hilbert-ray-containment-v1.json`, `artifacts/hilbert-ray-containment-tranche-v1.json`, `docs/prior-art-overlap-table-v3.md` |
| 106 | User-authorized Engine-B closure begins with the first noncanonical B5-015 member, RQ-000039.  The conductor, ray-class, orientation, and Artin-labelled packet gates are frozen before any target computation; shared normal closure is explicitly insufficient | `ACTIVE`, no mathematical verdict | `docs/cycle-106-engine-b-first-transport-preregistration.md` |
| 107 | RQ-000021 to RQ-000039 passes exact conductor and ray-class-map gates: the target adds the unique norm-two prime and the canonical C6 map is the identity on identity, generator, and sign labels.  The added prime has nontrivial odd-character Euler factors, so packet equality is not inferred | `BANKED_PARTIAL`, `PROVED_EXACT_TRANSPORT_GATES_1_2` | `artifacts/rq000039-engine-b-transport-gates-1-2-v1.json`, `docs/cycle-107-engine-b-first-transport-gates-1-2.md` |
| 108 | RQ-000039 is the first exact Engine-B noncanonical-member transport: Euler deletion and rank-one vanishing give the Artin-labelled quotient formula from RQ-000021; the exact ray map and positive quotient close the orientation gate | `BANKED`, `PROVED_EXACT_MEMBER_TRANSPORT` | `artifacts/rq000039-engine-b-transport-v1.json`, `docs/cycle-108-rq000039-engine-b-transport-proof.md` |
| 109 | A successor Engine-B ledger preserves v5 scope history and promotes exactly RQ-000039.  The exact census state is one completed and 231 open member transports | `BANKED`, `VERIFIED_ENGINE_B_TRANSPORT_LEDGER` | `artifacts/engine-b-transport-ledger-v1.json`, `docs/cycle-109-engine-b-first-member-ledger.md` |
| 110 | The next deterministic Engine-B target is preregistered: RQ-000190 to RQ-000195 in B5-025.  Exact conductor and ray-map gates precede any packet claim | `BANKED_PARTIAL`, exact structural gates pass; packet gate deferred to Cycle 111 | `docs/cycle-110-engine-b-second-transport-preregistration.md` |
| 111 | RQ-000195 passes the exact conductor/ray-map screen but its required independent RQ-000190 Arb source replay reaches the preregistered 600-second cap at low memory.  The target is not promoted and no method substitution is made | `BANKED_PARTIAL`, `RESOURCE_CAP_NO_PACKET_CLAIM` | `artifacts/rq000195-engine-b-transport-resource-cap-v1.json`, `docs/cycle-111-rq000195-source-replay-cap.md` |
| 112–115 | A frozen sealed-source reuse rule validates the RQ-000190 data, transcript, and program hashes without calling it a fresh Arb replay.  Fresh exact geometry then promotes four identity-labelled, source-coprime B5-025 targets by Euler deletion.  The empty-factor batch v1 is preserved and superseded by v2 | `BANKED`, `PROVED_EXACT_MEMBER_TRANSPORT_BATCH` | `artifacts/b5025-euler-deletion-transports-v2.json`, `artifacts/engine-b-transport-ledger-v2.json`, `docs/cycle-115-b5025-batch-transport-ledger.md` |
| 116–117 | B5-022 is frozen and its exact geometry screen passes for five source-coprime targets.  Three require the explicit `Mat(5)` generator-label conversion; the two source-prime enlargements are excluded | `BANKED_PARTIAL`, no packet promotion yet | `artifacts/b5022-transport-geometry-v1.json`, `docs/cycle-117-b5022-geometry-screen.md` |
| 118–119 | The sealed RQ-000419 source certificate is hash-validated and its five source-coprime B5-022 targets are promoted with exact `Mat(1)`/`Mat(5)` Artin-label conversion.  The ledger now has ten completed and 222 open transports | `BANKED`, `PROVED_EXACT_MEMBER_TRANSPORT_BATCH` | `artifacts/b5022-label-aware-transports-v1.json`, `artifacts/engine-b-transport-ledger-v3.json`, `docs/cycle-119-b5022-ledger-successor.md` |
| 120 | The sealed order-ten source RQ-001107 passes integrity validation.  Its complete B5-086 target screen has zero eligible Euler-deletion transports: each of the seven target quotients shares source prime 11.  This is an exact route exclusion, not a packet verdict | `BANKED_NO_GO`, `PROVED_EXACT_TRANSPORT_GEOMETRY` | `data/census-paper-preregistration-amendment-v15.json`, `artifacts/b5086-source-certificate-integrity-v1.json`, `artifacts/b5086-transport-geometry-v1.json`, `docs/cycle-120-b5086-reusable-source-preregistration.md` |
| 121 | The last two direct certified-source closures are screened under v16.  B5-021 has no integral source-to-target modulus quotient for either member; B5-033 has no integral source-to-target quotient for all three.  No unexamined direct certified-source reusable Euler-deletion batch remains | `BANKED_NO_GO`, `PROVED_EXACT_TRANSPORT_GEOMETRY` | `data/census-paper-preregistration-amendment-v16.json`, `artifacts/final-direct-source-coprime-screen-v1.json`, `docs/cycle-121-final-direct-source-coprime-screen.md` |
| 122 | Local census completion audit passed under the then-recorded identity-label screen, with ten exact members and 222 explicit unpromoted members.  Its direct-source exhaustion sentence is superseded by Cycle 123; its build/audit results otherwise remain valid | `SUPERSEDED_SCOPE`, exact transport claims unchanged | `docs/cycle-122-local-census-completion-audit.md`, `docs/cycle-123-b5025-label-aware-correction.md` |
| 123 | Cross-batch comparison corrects the transport-route scope: RQ-000221 and RQ-000228 passed every B5-025 gate except its pre-Cycle-118 identity-generator restriction, and have exact source-coprime `Mat(5)` maps.  They are candidates, not yet promoted; B5-025 source-prime exclusions remain preserved | `CORRECTION_ACTIVE`, no new packet verdict | `artifacts/b5025-transport-geometry-v1.json`, `docs/cycle-118-b5022-label-aware-transport-proof.md`, `docs/cycle-123-b5025-label-aware-correction.md` |
| 124–126 | The frozen B5-025 label-aware correction batch validates its sealed source, records exact prime-ray logs and `Mat(5)` Artin labels, and promotes RQ-000221 and RQ-000228.  The successor ledger has twelve completed and 220 explicit open transports; source-prime exclusions remain unpromoted | `BANKED`, `PROVED_EXACT_MEMBER_TRANSPORT_BATCH` | `data/census-paper-preregistration-amendment-v17.json`, `artifacts/b5025-label-aware-transports-v1.json`, `artifacts/engine-b-transport-ledger-v4.json`, `docs/cycle-126-b5025-label-aware-ledger-successor.md` |
| 127 | Referee review exposed and corrected three claim-boundary errors without changing a frozen row: the 8,200-row universe is the finite-ideal conjugacy quotient with pinned \(\infty_2\), empty support is sufficient but not necessary for the value-one packet, and only 2,699 of 2,704 H rows have complete registered-mechanism status.  The repaired seven-page manuscript prints the exact H cross-table, twelve transports, numerical bounds, proof sketches, and prior-theorem boundary.  Both manuscript audits and all 173 tests pass; publication remains contained for lack of a census-paper DOI | `BANKED_LOCAL_CORRECTION`, no census count changed | `data/census-paper-preregistration-amendment-v18.json`, `artifacts/census-paper-referee-revision-v1.json`, `docs/cycle-127-census-referee-revision.md` |
| 128 | The quadratic deleted-prime cover criterion is proved from the imprimitive Euler product, nonvanishing of the remaining rank-one factor, and exact Fourier inversion.  It classifies all 346 nonempty-support value-one rows with zero errors and permits a pre-regulator decision.  Coarse unlabeled patterns fail.  A preregistered expanded search refutes universal four-support nondegeneracy at norm 252 over \(\mathbb Q(\sqrt7)\).  The first proof replay also caught and contained a mutated-preregistration hash; restored and versioned v2 successors pass.  The revised eight-page paper and all 174 tests pass | `BANKED`, `PROVED_DELETED_PRIME_COVER`; four-support claim `REFUTED` | `artifacts/q-euler-deleted-prime-cover-theorem-v1.json`, `artifacts/census-paper-theorem-revision-v2.json`, `docs/cycle-128-q-euler-deleted-prime-cover-theorem.md` |
| 129 | Census paper v1.0 was published under the standing Zenodo authorization at DOI `10.5281/zenodo.21729947`.  The frozen three-file inventory is public; independent DOI-bearing PDF and companion builds are byte-identical, the fresh extracted replay passes, all 174 live tests pass, every public download matches local bytes/MD5/SHA-256, and Zenodo selects the lexically first main PDF as the default preview.  The initial PDF build without a frozen epoch failed byte identity and is preserved in the release candidate record; the corrected `SOURCE_DATE_EPOCH` build passes | `PUBLISHED_AND_PUBLICLY_VERIFIED`; theorem tags unchanged | `docs/cycle-129-census-zenodo-publication.md`, `artifacts/zenodo-census-publication-v1.json`, `artifacts/census-paper-release-candidate-v1.json` |
| 130 | Post-publication referee feedback produced a local v1.1 correction candidate.  The v1.0 orbit equation is visually correct but now prints extraction-safe `2461+5739=8200`; Theorem 3 uses (i)--(iv) and explicitly proves/cites relative-log nonvanishing; Table 2 states its disjointness is an exact finite-v5 assignment fact, not a universal mechanism theorem; and the sextic field-certificate population is printed as `382=309+73`, with `309=48+261`.  Two deterministic builds agree, affected pages are visually clean, all audits pass, and all 175 tests pass.  No Zenodo mutation occurred | `BANKED_LOCAL_V1_1_CORRECTION_CANDIDATE`; theorem tags and counts unchanged | `docs/cycle-130-census-referee-feedback-correction.md`, `artifacts/census-paper-referee-correction-v3.json` |
| 131 | The all-order deleted-prime cover implication is proved by the imprimitive Euler product, the odd-real-place trivial zero, and Fourier inversion: a value-one deleted Euler factor for every supported character forces the whole packet to one.  Exact GP phase exports cover all 2,704 H rows: 1,040 of 18,865 supported character occurrences and 64 whole rows satisfy the cover predicate.  RQ-000692 is uncovered (two sextic characters have no deleted primes; its quadratic character has value −1 at its sole deleted prime), so the criterion neither resolves nor weakens the wild-ramification target | `BANKED`; theorem `PROVED`, finite screen `OBSERVED` | `docs/cycle-131-all-order-deleted-prime-cover-theorem.md`, `artifacts/h-all-order-deleted-prime-cover-audit-v1.json`, `docs/cycle-131-export-implementation-correction-v1.md` |
| 132 | The Q(sqrt(21)) dossier localizes RQ-000692 exactly: its degree-12 ray field has local row `(2,1,12,1,6)` above 3, so the relative index 6 is wild while A1--A3 and the prime-to-three class-number gate pass. The dimension-6 companion's (C_6) ray group, modulus, primitive character, and degree-12 field agree exactly: its polynomial is the census polynomial at (-X). This proves the shared arithmetic object, but not the remaining oriented analytic bridge | `BANKED_SHARED_OBJECT_DOSSIER`; local boundary and structural convergence `PROVED`, oriented bridge `OPEN` | `docs/cycle-132-qsqrt21-wild3-dossier.md` |
| 133–134 | The global 88-closure directed geometry screen checks 1,012 exact source-target directions. It partitions the 220 unpromoted members into 116 with no direct coprime-deletion incoming route and 104 source-or-proof-open. It also corrects the B5-086/B5-021/B5-033 no-go artifacts: their nonintegral field models were paired with integral-basis HNFs, producing false exclusions; the corrected models expose ten eligible directions from sealed sources. No new packet is promoted before label-aware Euler and orientation proofs | `CORRECTION_ACTIVE`; geometry `PROVED`, packet claims unchanged | `artifacts/engine-b-global-coprime-geometry-audit-v1.json`, `docs/cycle-133-engine-b-global-geometry-preregistration.md`, `docs/cycle-134-engine-b-integral-basis-correction.md` |
| 135–136 | The ten corrected certified-source directions pass exact quotient factor, ray-log, generator-label, Euler-deletion, and orientation gates. They are promoted in ledger v5, raising exact Engine-B transports from 12 to 22 and reducing open members to 210 | `BANKED`; `PROVED_EXACT_MEMBER_TRANSPORT_BATCH` | `artifacts/corrected-direct-source-transports-v1.json`, `artifacts/engine-b-transport-ledger-v5.json`, `docs/cycle-136-corrected-direct-source-transport-proof.md` |

## Standing integrity rules

1. Every predicate has `GENUINE` or `PROXY` provenance.
2. No `VERIFIED_*` tag may rest on proxy data.
3. Thresholds and selection rules precede measurements.
4. Failed runs remain preserved.
5. A promoted theorem appears in the next checkpoint.
6. Exact route disagreements halt the affected track.
7. Eligibility is never reported as a proved packet.
8. A certificate supports a written proof; it does not replace one.
9. Zenodo publication uses the user's standing authorization after all
   release gates pass; arXiv submission remains a human action.
10. Any correction updates this plan, the relevant artifact, the
    manuscript, and the test suite in the same checkpoint.

## Recovery pointers

After a crash or context loss, inspect in this order:

1. `PROGRAM.md`;
2. `git status` and the latest commit;
3. `docs/status-2026-07-30.md`;
4. `artifacts/results-paper-full-freeze-v1.json`;
5. `artifacts/full-census-yield-declaration-v5.json`;
6. the active task's certificate and transcript;
7. the full test suite.

Primary manuscripts:

- results: `paper/effective-stark-results.tex`;
- census draft: `paper/effective-stark-sweep-draft.md`.

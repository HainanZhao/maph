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
| Results paper | `PUBLISHED` | v1.4 is public at DOI 10.5281/zenodo.21712478; all seven public downloads match the frozen local byte counts, MD5 checksums, and SHA-256 checksums | `paper/effective-stark-results.tex`, `artifacts/zenodo-results-publication-v5.json` |
| Results v1.4 correction | `BANKED` | The withdrawn-orientation correction, Tangedal--Young page correction, and RQ-000013 addendum are published and publicly verified | `artifacts/zenodo-results-publication-v5.json`, `docs/cycle-082-results-v1.4-publication.md` |
| Results v1.5 integration | `HUMAN` | Unpublished draft 21713178 merges RQ-000013 into the 19-page main paper, omits the standalone addendum at deposit root, and verifies `effective-stark-results-00-main-paper.pdf` as the default preview | `artifacts/zenodo-results-v1.5-draft-upload-verification-v1.json`, `docs/cycle-083-results-v1.5-main-paper-integration.md` |
| Results-paper audit | `BANKED` | Versioned full A/B/C audit and extracted companion replay pass, including exact Engine-A degeneracy and the sigma-positive Engine-C re-audit | `artifacts/results-paper-referee-audit-v4.json`, `artifacts/engine-c-fourier-convention-correction-v3.json` |
| Genuine routing census v5 | `BANKED` | 8,200/8,200 genuine screens; proxy recovery complete | `artifacts/full-census-yield-declaration-v5.json` |
| Census-paper range | `BANKED` | Existing maximal-order universe frozen: squarefree radicands 2--200, ideal norm at most 100, 8,200 conjugacy representatives | `data/census-paper-preregistration-v1.json` |
| Census-paper Layer 0 | `BANKED` | Clean PARI enumeration reproduced the backbone; support-first split is T/Q/H = 3,936/1,560/2,704 | `artifacts/census-paper-layer0-reconciliation-v1.json` |
| Worked imprimitive Engine-A row | `BANKED` | RQ-000013 has exact \(E_\chi=2\), \(I_\chi=2\), and packet \(X_{[0]}=u^2,\ X_{[1]}=u^{-2}\) | `artifacts/rq000013-engine-a-imprimitive-certificate-v1.json` |
| Census manuscript | `ACTIVE` | Execution plan and older Markdown research draft exist; no journal LaTeX/PDF yet | `docs/census-paper-execution-plan-v1.md`, `paper/effective-stark-sweep-draft.md` |
| Engine-B occurrence transport | `READY` | Gates case-level transported `PROVED` claims, not structural T/Q/H statistics; scope must be regenerated from v5 | `docs/cycle-070-genuine-census-v5.md` |
| W4 census analysis | `READY` | Support-first finite-range analysis may run; transported-case and safe-exponent claims remain gated separately | `artifacts/census-paper-layer0-reconciliation-v1.json` |
| DST / Cohen--Roblot comparison | `READY` | Initial perimeter table exists; case-by-case overlap comparison is incomplete | `docs/prior-art-overlap-table-v1.md` |
| Public certificate archive | `PUBLISHED` | DOI-bearing companion v17 published; SHA-256 `e2a945edaddcec32e3aad10e67f8b960af0bc304b07ba5503ab7be62384b9506` | `artifacts/zenodo-results-publication-v5.json` |
| v1.5 certificate archive | `HUMAN` | Deterministic companion v18 SHA-256 `4a6d4417610215278d7be7788e2ae7845ee2c75ec5b22690c47b717c15e5b024` is uploaded and extracted-replay verified but unpublished | `artifacts/results-paper-companion-local-freeze-v18.json` |
| Zenodo / arXiv | `HUMAN` | Results v1.4 remains public; checksum-verified v1.5 awaits immediate explicit approval at reserved DOI 10.5281/zenodo.21713178; arXiv remains a separate human action | `artifacts/results-paper-v1.5-publication-candidate-v1.json` |

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
- [ ] Obtain immediate explicit approval and publish v1.5 DOI
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
      most 100, conjugate one-place pairs identified.
- [x] Freeze the degree-32 exact-resultant cap and deterministic
      50-row independent analytic audit.
- [x] Rerun the PARI ideal enumeration and reproduce the 121 fields,
      13,939 raw ideals, and 8,200 representatives exactly.
- [x] Reconcile the structural T/Q/H split. Correct the 37
      empty-support rows that v5 routed to `FRONTIER`; preserve v5
      rather than rewriting history.
- [x] Reconcile the Q-stratum counts: 1,560 rows, 2,232 supported
      quadratic characters, 912 quartic fields, 672 zero Euler
      products, 603 affected rows, and 346 all-vanishing rows.
- [ ] Build the row-level exact Q corpus under the uniform theorem.
- [x] Preselect RQ-000013 as the first one-character, one-removed-prime,
      nonzero imprimitive branch, hence the worked \(E_\chi=2\) row.
- [x] Complete and print RQ-000013's exact unit/index calculation;
      share its certificate with the census draft and a versioned,
      locally staged results-paper supplement addendum. The published
      v1.3 files remain immutable pending authorization for a new version.
- [ ] Run the preregistered independent 50-row Arb audit.
- [ ] Build the support-order/Engine-B/Engine-C/Roblot/resolution
      matrix for all 2,704 H rows.
- [ ] Extract the minimal unresolved row at every support order and
      the minimal all-mechanisms-fail row, led by the
      \(\mathbb Q(\sqrt{21})\) wall.
- [ ] Derive a new v5 occurrence-transport manifest from 232 Engine-B
      eligible rows and 88 closures. Reconcile it explicitly against
      the obsolete 195-row/51-closure ledger; do not silently reuse the
      old count of 187 pending transports.
- [ ] Certify member-modulus identity, ray-class map, orientation, and
      packet transport for every occurrence claimed at case level.
- [ ] Seal the transport ledger before calling any transported
      occurrence case-level `PROVED`. Structural T/Q/H counts and
      mechanism eligibility do not wait on transport.
- [ ] Run W4 in the preregistered order:
  1. Shintani-index distribution;
  2. FRONTIER share versus conductor norm;
  3. safe-exponent growth;
  4. packet-polynomial families;
  5. tower and norm-compatibility signals.
- [ ] Tag pattern discovery as `CONJECTURAL` until an exact theorem is
      proved.
- [ ] Complete the DST / Cohen--Roblot / Dummit--Sands--Tangedal
      overlap table case by case.
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

## Standing integrity rules

1. Every predicate has `GENUINE` or `PROXY` provenance.
2. No `VERIFIED_*` tag may rest on proxy data.
3. Thresholds and selection rules precede measurements.
4. Failed runs remain preserved.
5. A promoted theorem appears in the next checkpoint.
6. Exact route disagreements halt the affected track.
7. Eligibility is never reported as a proved packet.
8. A certificate supports a written proof; it does not replace one.
9. Publication actions require explicit human authorization.
10. Any correction updates this plan, the relevant artifact, the
    manuscript, and the test suite in the same checkpoint.

## Recovery pointers

After a crash or context loss, inspect in this order:

1. `PLAN.md`;
2. `git status` and the latest commit;
3. `docs/status-2026-07-30.md`;
4. `artifacts/results-paper-full-freeze-v1.json`;
5. `artifacts/full-census-yield-declaration-v5.json`;
6. the active task's certificate and transcript;
7. the full test suite.

Primary manuscripts:

- results: `paper/effective-stark-results.tex`;
- census draft: `paper/effective-stark-sweep-draft.md`.

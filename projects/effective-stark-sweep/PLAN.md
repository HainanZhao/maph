# Effective-Stark master plan

**Role:** authoritative project map and execution ledger  
**Last reconciled:** 2026-07-30 UTC  
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
| Results paper | `PUBLISHED` | Deterministic 17-page paper plus 2-page supplement and companion v10 published at DOI 10.5281/zenodo.21703306 | `paper/effective-stark-results.tex`, `artifacts/zenodo-results-publication-v1.json` |
| Results-paper audit | `BANKED` | Full A/B/C audit and compact companion replay pass, including exact Engine-A degeneracy and Engine-C Fourier-convention audits | `artifacts/results-paper-full-referee-audit-v2.json` |
| Genuine routing census v5 | `BANKED` | 8,200/8,200 genuine screens; proxy recovery complete | `artifacts/full-census-yield-declaration-v5.json` |
| Census manuscript | `ACTIVE` | Substantial Markdown draft exists; no journal LaTeX/PDF yet | `paper/effective-stark-sweep-draft.md` |
| Engine-B occurrence transport | `READY` | Last formal W4 gate; current scope must be regenerated from v5 rather than copied from the obsolete 195-row ledger | `docs/cycle-070-genuine-census-v5.md` |
| W4 census analysis | `BLOCKED` | Opens after the v5 Engine-B transport ledger closes | this plan |
| DST / Cohen--Roblot comparison | `READY` | Initial perimeter table exists; case-by-case overlap comparison is incomplete | `docs/prior-art-overlap-table-v1.md` |
| Public certificate archive | `PUBLISHED` | Companion v10 published; SHA-256 `79536ad9be167b3a18b499cd59dfd092ad03b29b8399b94a93ae709eaee29fe1` | `artifacts/zenodo-results-publication-v1.json` |
| Zenodo / arXiv | `ZENODO_DONE` | Zenodo record published; arXiv remains a separate human action | DOI `10.5281/zenodo.21703306` |

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
    -> regenerate v5 Engine-B transport scope
      -> close occurrence transport
        -> W4 structural analysis
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

- [ ] Derive a new v5 occurrence-transport manifest from 232 Engine-B
      eligible rows and 88 closures. Reconcile it explicitly against
      the obsolete 195-row/51-closure ledger; do not silently reuse the
      old count of 187 pending transports.
- [ ] Certify member-modulus identity, ray-class map, orientation, and
      packet transport for every occurrence claimed at case level.
- [ ] Seal the transport ledger and open W4.
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

# Cycle 20 / B020 preregistration: CRT two-diagonal bad-time interface

## Decision question and idea selection

Does the exact bad-time predicate for a product modulus \(q=pc\) reduce to
two CRT diagonals, and does an implementation of that interface agree with
direct modular arithmetic on every ordered \((s,a)\) pair in the complete
H11, p47, and p199 control domains?

The primary proposed (i) proving and exhaustively checking a two-diagonal CRT
formula, (ii) compressing the Cycle-19 masks with CRT signatures immediately,
or (iii) changing to a Fourier cover bound.  Darwin independently recommended
testing the CRT interface before committing to a larger CRT engine.  We
questioned whether an exhaustive test was being asked to stand in for proof;
it is not—the elementary general theorem is frozen in the soundness note, and
the enumeration tests only the executable interface.  We selected the theorem
plus exhaustive controls because it is the cheapest falsifiable prerequisite
for any lift-aware prime-product closure.  The main rejected alternative is
immediate signature compression, whose failure would confound an interface
error with a search-design failure.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":20,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: prove/check the CRT two-diagonal formula, immediately compress Cycle-19 masks by CRT signatures, or seek a Fourier cover bound. Companion: test the CRT interface before a larger CRT engine. Choose the proved interface plus exhaustive controls; reject immediate compression because it would confound interface and engine failures.","rationale":"Select the smallest exact and discriminating prerequisite."},
    "theorem":{"kind":"expression","value":"For coprime positive p,c, q=pc, canonical x=x_p+p*j with 0<=x_p<p and 0<=j<c: c*min(x,q-x)<q iff j=0 or (j=c-1 and x_p!=0). From canonical residues x_p=x mod p and x_c=x mod c, j is the canonical residue p^{-1}(x_c-x_p) mod c.","rationale":"Exact two-diagonal CRT interface, including the strict boundary."},
    "control_domains":{"kind":"expression","value":"Exactly the ordered triples (p,c,q)=(11,4,44),(47,7,329),(199,14,2786), in that order. For each triple enumerate s=0..q-1, then a=0..q-1, for exactly q^2 comparisons.","rationale":"Complete small, published-baseline, and active-target modulus controls; no sampling."},
    "direct_predicate":{"kind":"expression","value":"x=(a*s) mod q in [0,q-1]; direct_bad is c*min(x,q-x)<q, evaluated in exact unsigned integer arithmetic.","rationale":"Canonical unfactorized oracle."},
    "crt_predicate":{"kind":"expression","value":"xp=((a mod p)*(s mod p)) mod p; xc=((a mod c)*(s mod c)) mod c; inv is the unique 0<=inv<c with p*inv=1 mod c; j=((xc-(xp mod c))*inv) mod c canonically in 0..c-1; crt_bad is j=0 or (j=c-1 and xp!=0).","rationale":"Uses only the two local product residues and preserves the strict boundary xp=0."},
    "comparison_count":{"kind":"integer","value":7871973,"rationale":"44^2+329^2+2786^2."},
    "selection":{"kind":"expression","value":"Retain per-domain counts of direct bad, CRT bad, mismatches, strict-boundary rows, plus SHA-256 of a canonical summary. Retain every mismatch with p,c,s,a,x,xp,xc,j and both predicates; do not stop after the first mismatch.","rationale":"No post-result row selection and full contrary evidence."},
    "advance_condition":{"kind":"expression","value":"The algebraic proof must pass an independent exact theorem checker and all 7,871,973 executable comparisons must agree. This advances only the bad-time representation to a later diagonal-coverage engine.","rationale":"Separates theorem closure from downstream global coverage."},
    "falsifier":{"kind":"expression","value":"Any non-coprime frozen pair, inverse failure, direct/CRT disagreement, count mismatch, malformed strict-boundary treatment, nondeterministic summary, or audit disagreement invalidates the executable interface. A flaw in the algebraic case split invalidates the general theorem.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"The theorem factorizes one bad-time predicate only. Agreement on finite controls is not proof of the theorem and neither result proves a global cover reduction, closes a p199 leaf, empties F_1 or J, or proves LRC(13).","rationale":"No promotion beyond the local interface."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "control_domains":{"kind":"integer","value":3,"rationale":"Exactly the three frozen complete domains."},
    "ordered_pair_comparisons":{"kind":"integer","value":7871973,"rationale":"Complete enumeration, not a sample."},
    "aggregate_wall_seconds":{"kind":"integer","value":600,"rationale":"Compilation, three complete domains, theorem audit, executable audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":1024,"rationale":"Streaming enumeration and small summaries only."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"One GiB is ample and remains below available space minus the mandatory five-GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"All domains, enumeration orders, formulas, and outputs are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical product residues","CRT reconstruction diagonal","strict lonely-runner bad-time threshold","complete ordered-pair enumeration"],
  "selection_rule":["Check all frozen pairs are coprime and compute their unique inverses.","Enumerate every ordered (s,a) pair in every frozen domain.","Compare the direct and local CRT predicates on every row.","Retain all disagreements and canonical aggregate counts.","Promote only after independent theorem and executable audits agree."],
  "failure_rule":["Any theorem-check failure contains the general claim.","Any executable mismatch contains the implementation claim and is retained.","A resource cap yields no agreement claim for an incomplete domain.","Finite agreement never promotes a global cover or LRC claim."],
  "pre_execution":{"timestamp_utc":"2026-08-03T23:31:08Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 19 is sealed before this distinct CRT-interface theorem.","filesystem_observation_bytes":{"size":206900281344,"used":41198157824,"available":165685346304,"reserved":5368709120,"maximum_temporary_cap":160316637184,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["artifacts/cycle-19-b019-lrc-symbolic-antichain-v1.json","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_20_crt_diagonal_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop the interface branch on any algebraic or executable disagreement.  If all
checks pass, ask Darwin to review the completed theorem and controls, propose
independent diagonal-coverage engines, and advise whether this material result
should seal before a genuinely distinct coverage question opens.

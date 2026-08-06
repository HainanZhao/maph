# GOAL.md

Revised 2026-08-07. Supersedes the previous version, whose goal was
"finish every research topic below." That goal is retired: it contained no
kill condition, which conflicts with the pre-registered-kill-criteria
discipline used everywhere else in this program, and it bound three topics of
very different tractability into a single completion target.

---

## Primary goal

**Complete every topic below by reaching Outcome A, B, or C under its stated
stop condition.**

Success is research closure: a proof or refutation, a self-contained
reduction, or a documented kill criterion. Publication, external uptake, and
outreach are not requirements of this goal.

Secondary goal: keep at most one topic in open-ended proof search at a time.

---

## Success ladder (applies to every topic)

- **Outcome A — resolved.** Proved or refuted, uniformly, replayable,
  written up.
- **Outcome B — reduced.** Reduced to a stated, self-contained, checkable
  sub-problem that a third party could attack without my scaffolding.
  *B is a terminal research outcome, not a failure.*
- **Outcome C — killed.** Kill criterion met. Record the obstruction and the
  reason in the ledger. Stop.

A topic exits the queue on A, B, or C. It does not exit on "still trying."

---

## Topic 3 — Width-four q-Fibonomial unimodality (n = 4, all m ≥ 1)

**Status: Outcome A. Proved, replayable, written.**

**Evidence:** self-contained proof, exact replay, and written research note
are complete.

---

## Topic 2 — q-analog Conjecture 5.4, case (k = 4, r = 4)

**Status: Outcome B in hand.** Reduced to a specific coefficient /
window-dominance inequality.

**This is the highest-return live target.** One inequality from A; plausible
shared machinery with Topic 3 (gap absorption in products of q-analogs);
it directly builds on Topic 3.

**Pre-registered kill criterion.** Review on **2026-10-31**. If the
window-dominance inequality is not proved by that date:

- Declare Outcome B final.
- Write the reduction as a short standalone note: statement of the
  inequality, proof that it implies (k = 4, r = 4), the computational
  evidence, and the obstruction encountered.
- Record Outcome B in the ledger and stop. Do not extend the date.

**Before resuming proof work:**

- [ ] Record whose Conjecture 5.4 this is, and what the (k = 4, r = 4) case
      is worth to that community. If the answer is "nothing to anyone but
      me," this topic moves to the same challenge Topic 1 is under.
- [ ] Test the inequality numerically at the boundary of the admissible
      range before investing in a proof.

---

## Topic 1 — Exact covering number C(23,6,2)

**Status: open. 20 ≤ C(23,6,2) ≤ 21. Schönheim gives the lower bound;
the open question is whether it is attained.**

**This topic is under challenge and must justify its slot.** Three strikes:

1. **The likely answer is the expensive direction.** If stochastic search has
   failed to find a 20-block cover, the answer is probably 21 — which
   requires exhaustive nonexistence over 20 six-subsets of a 23-set modulo
   S_23. Symmetry breaking at that scale is a research problem in itself,
   not a compute purchase.
2. **Zero synergy.** Different field, toolchain, and audience from Topics 2
   and 3. Nothing transfers in either direction.
3. **Lowest payoff.** Resolved, it updates a table entry. Topic 2 resolved
   yields a technique that generalizes.

**Bounded experiment, budget fixed before starting.** Written down now so it
cannot expand later:

- Compute budget: **[FILL IN core-hours]**, single allocation, no extension.
- Wall-clock cap: **[FILL IN]**.
- Stop conditions, whichever comes first:
  - a verified 20-block cover is found → Outcome A, record and close;
  - the symmetry-broken encoding is built and the DRAT proof is *projected*
    to exceed the budget by more than 10x → **Outcome C, cut the topic**;
  - budget exhausted → **Outcome C, cut the topic.**
- Deliverable on C: a one-page note recording the encoding, the symmetry
  breaking used, the observed scaling, and the projected cost. This closes
  the topic honestly instead of leaving it open indefinitely.

**If the budget line above is not filled in by 2026-09-15, cut the topic
without running the experiment.**

---

## Sequencing

1. Topic 3 is complete (Outcome A).
2. Topic 2 proof attempt, single-threaded, until 2026-10-31.
3. Topic 1 bounded experiment only after Topic 2 exits, and only if the
   budget was fixed on time.

Do not open a fourth topic while any of the above is unresolved.

---

## Standing disciplines (unchanged)

- Append-only ledger; every claim classified A / B / C at the time it is
  made.
- Independent verification of all arithmetic before any claim is written up.
- Kill criteria pre-registered in writing, with dates, before work begins.
- Phase-0 direct-attempt protocol before building any scaffolding.
- No result is "finished" until a third party could replay it from the
  archive without asking me a question.

---

## Out of scope for this file

The compatible spin-alignment note (three-qubit, pair-support, arbitrary Q)
is on a separate track and is not part of this goal.

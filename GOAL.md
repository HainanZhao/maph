# GOAL.md

Revised 2026-08-07. Supersedes the previous version, whose goal was
"finish every research topic below." That goal is retired: it contained no
kill condition, which conflicts with the pre-registered-kill-criteria
discipline used everywhere else in this program, and it bound three topics of
very different tractability into a single completion target.

---

## Primary goal

**Post one result that someone outside my own framework cites, reuses, or
corresponds about.**

This replaces "resolve N of 3." Rationale: the failure mode of the analytic
number theory work was not lack of proved statements — it was that the proved
statements were internal to a self-invented coordinate system with no
externally legible implication. Counting resolutions does not detect that
failure. External uptake does.

Secondary goal: keep at most one topic in open-ended proof search at a time.

---

## Success ladder (applies to every topic)

- **Outcome A — resolved.** Proved or refuted, uniformly, replayable,
  written up.
- **Outcome B — reduced.** Reduced to a stated, self-contained, checkable
  sub-problem that a third party could attack without my scaffolding.
  *B is a shippable contribution, not a failure.*
- **Outcome C — killed.** Kill criterion met. Record the obstruction and the
  reason in the ledger. Stop.

A topic exits the queue on A, B, or C. It does not exit on "still trying."

---

## Topic 3 — Width-four q-Fibonomial unimodality (n = 4, all m ≥ 1)

**Status: Outcome A. Proved, replayable, written.**

**Action: ship this month. Nothing is sequenced ahead of it.**

- [ ] Post to arXiv (math.CO) by **2026-08-31**
- [ ] Zenodo deposit, DOI recorded in the paper before posting
- [ ] Email Connelly / Martinez (UCLA) with the link on the day of posting
- [ ] Cite Bergeron–Ceballos–Küstner Conjecture 2.5 and
      arXiv:2605.12822 as the n ≤ 3 case explicitly

**Why the date is hard.** arXiv:2605.12822 (May 2026) resolved n ≤ 3 and
stated that its methods suggest further directions. Five authors at one
department are plausibly on n = 4 now. Crowding is the central strategic
constraint of this program; holding a finished, timing-sensitive result while
grinding an unrelated topic is precisely the failure that constraint names.

**Explicitly rejected option:** merging Topic 3 into a heavier joint paper
with Topic 2. The combined paper would be stronger, but the exposure window
on n = 4 does not support waiting. Ship 3 now; let 2 be the sequel that
cites it.

---

## Topic 2 — q-analog Conjecture 5.4, case (k = 4, r = 4)

**Status: Outcome B in hand.** Reduced to a specific coefficient /
window-dominance inequality.

**This is the highest-return live target.** One inequality from A; plausible
shared machinery with Topic 3 (gap absorption in products of q-analogs);
same audience; would cite Topic 3.

**Pre-registered kill criterion.** Review on **2026-10-31**. If the
window-dominance inequality is not proved by that date:

- Declare Outcome B final.
- Write the reduction as a short standalone note: statement of the
  inequality, proof that it implies (k = 4, r = 4), the computational
  evidence, and the obstruction encountered.
- Post it. Do not extend the date.

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
  - a verified 20-block cover is found → Outcome A, ship immediately;
  - the symmetry-broken encoding is built and the DRAT proof is *projected*
    to exceed the budget by more than 10x → **Outcome C, cut the topic**;
  - budget exhausted → **Outcome C, cut the topic.**
- Deliverable on C: a one-page note recording the encoding, the symmetry
  breaking used, the observed scaling, and the projected cost. Publishable
  as a negative computational result; more importantly, it closes the topic
  honestly instead of leaving it open indefinitely.

**If the budget line above is not filled in by 2026-09-15, cut the topic
without running the experiment.**

---

## Sequencing

1. Ship Topic 3 (by 2026-08-31).
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
is on a separate track but competes for the same shipping bandwidth. It has
referee-level fixes outstanding and a live crowding risk from Song–Chen. Do
not let it and Topic 3 queue behind each other; they are both short and both
timing-sensitive.

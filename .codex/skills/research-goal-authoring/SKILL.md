---
name: research-goal-authoring
description: Create or revise user-owned research GOAL.md files with explicit objectives, claim boundaries, evidence gates, permitted terminal outcomes, and stop conditions. Use when a user asks to add, rewrite, extract, or structure a research goal file from prior project goals, research plans, or a new investigation.
---

# Research Goal Authoring

Create a concise durable contract for a research campaign. A goal file states
what completion means; it is not a progress log, a speculative paper abstract,
or a substitute for the project `PROGRAM.md`.

## Preserve ownership and establish context

1. Create, edit, rename, or delete `GOAL.md` only with explicit user
   authorization. Ask before overwriting an existing user-owned goal file.
2. Read the repository-level research instructions, the project `PROGRAM.md`,
   and the smallest set of prior goal files relevant to the requested work.
3. Extract reusable structure, not unsupported conclusions: prior goals may
   supply gates, labels, replay discipline, and stop rules, but they do not
   prove the new project's claims.
4. State the starting evidence and its label. Do not turn a numerical pattern,
   a proposal, or an open-problem citation into a theorem.

## Write the goal

Use [the goal template](references/goal-template.md). Adapt it to the project;
delete sections that have no meaningful content rather than filling them with
boilerplate.

The resulting file must contain all of the following:

- a one-paragraph objective and a precise scope/model or object of study;
- an explicit claim boundary and non-goals;
- the current evidence and its epistemic label;
- a small number of independently falsifiable workstreams or gates;
- for every gate: an acceptance condition, a mechanism-level kill/escalation
  condition, and the next permissible action after either outcome;
- verification requirements distinguishing proof, certified computation, and
  exploratory observation;
- a reproducibility and failure-ledger rule; and
- terminal outcomes for the whole campaign, including what does *not* count as
  completion.

When the research may later produce an animation, app, or public demo, include
a separate demo gate. The demo must name its mathematical dependency and label
simulations as observations unless independently proved.

## Keep stop conditions useful

Distinguish a failed mechanism from a failed project. A counterexample or
no-go result can close one gate while supporting another route. Resource use,
an unfinished calculation, or a polished document is not a terminal outcome.

Permit the campaign to end only through a stated result, such as a complete
proof, a rigorously verified countermechanism, a controlled theorem with a
defined scope, or another outcome explicitly authorized by the user. State
which evidence is required for each.

## Final audit

Before handing off the file, check that:

1. every material claim has an allowed epistemic label;
2. no gate promises a result stronger than its evidence standard;
3. every symbol, model, and source-dependent premise used in a completion
   condition is defined;
4. a reader can distinguish the campaign objective, the next action, and the
   terminal condition; and
5. the goal does not claim to solve a broader open problem without a stated
   proof criterion.

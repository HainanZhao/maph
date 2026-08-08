# Cycle 12: symbolic encoder-incidence proof

## Decision question

Can the normal-island and opposite-cut boundary claims used by Lemma 6.1 be
derived by one width-parametric symbolic incidence engine, with no exceptional
edge silently fitted after finite-width inspection?

## Question the questioning

The manuscript already contains plausible closed-form tables, and the sealed
G1 replay checks the resulting ranks. Neither fact proves that the printed
boundary trichotomy is exhaustive for arbitrary width. The relevant invariant
is the cellular boundary of each declared face chain under the correct
five-layer rotation phase. A generator is useful only if its expected side is
defined from the face families and edge recurrences independently of the
brute-force face-dual side.

## Exclusion map

- Former question: do the recursive encoders have the required terminal and
  cotree ranks at tested widths?
- Outcome: exact replays answer yes through their frozen ranges, but finite
  widths do not prove the symbolic boundary decomposition.
- False route excluded: reflecting the normal encoder to obtain the right
  encoder. It is rank deficient and cannot justify the opposite phase.
- Current delta: normal and opposite encoders are separately fixed; what is
  missing is a human-readable, arbitrary-width cellular-boundary identity.

## Mechanisms considered

1. Hand-expand the existing tables. Rejected: it cannot detect transcription
   omissions and is the precise weakness under review.
2. Infer formulas from widths 4--8. Rejected as the proof route: periodic data
   may suggest a family but cannot establish it.
3. Selected mechanism: compute cellular boundaries from symbolic face-family
   constructors and compare them with independently constructed gauge,
   exceptional, and retained-edge families. Emit the resulting finite
   period-two table; use actual rotation-system face walks only as a firewall.

## Frozen input and conventions

- Graph block: `P_5 square P_W square P_W`, vertices `(x,y,z)`.
- Edge key: `(axis,x,y,z)` is the positive coordinate edge from `(x,y,z)`.
- Face key: `(fixed_axis,x,y,z)` is the unit square with that lower corner.
- Normal phase: global checkerboard layers `0,...,4`.
- Opposite phase: global checkerboard layers `1,...,5`, translated to local
  layers `0,...,4`.
- Width firewall: every integer `W=4,...,8`.
- No modular arithmetic enters the incidence identities; the two-prime rule is
  therefore inapplicable to the generator itself. Downstream rank replays over
  `1,000,000,007` and `1,000,000,009` remain mandatory.

## Smallest direct verifier

At each width, compare the abstract square-boundary calculation with boundary
edges obtained from the actual rotation-system face walks. Then classify every
edge against independently constructed `T_W^0`, `X_W^+/-`, and `P_W^-` sets.

## Acceptance criterion

The engine must:

1. derive exactly the printed normal `I_3`, conditional `I_5`, and `I_{2,r}`
   internal/gauge/exceptional families;
2. derive exactly the six opposite `C_W` crossing families;
3. find no unclassified incidence at widths 4--8;
4. emit deterministic LaTeX from the same structured payload;
5. pass an independent unit test that reconstructs boundaries from face walks;
6. preserve the existing arbitrary-width proof obligation: the manuscript
   must explain algebraically why interval interiors cancel and only endpoints
   survive.

## Kill/escalation criterion

Any edge outside the declared trichotomy, any phase mismatch, or any formula
that needs a width-specific repair beyond the already declared width-four
opposite base invalidates the current decomposition. Name the first offending
width, face family, and edge; return to the encoder recurrence instead of
patching the table.

## Resource stop

This is a deterministic linear-size incidence calculation. Stop if a width-8
row exceeds one minute or 1 GiB, because that would indicate an avoidable
implementation error rather than mathematical difficulty.

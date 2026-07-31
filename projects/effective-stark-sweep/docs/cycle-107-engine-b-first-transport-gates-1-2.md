# Cycle 107 — B5-015 transport gates 1–2

## Outcome

The first two preregistered transport gates for RQ-000021 to RQ-000039
pass exactly under PARI/GP 2.15.4.

- The target finite ideal equals the source finite ideal times
  `[[2,0],[0,1]]`, the unique prime ideal of norm two in
  Q(sqrt(2)).
- The canonical ray-class map from target modulus to source modulus is
  `[Mat(1),[6],[6]]`.  It sends the identity to `[0]`, the fixed
  generator to `[1]`, and the real sign class `[3]` to `[3]`.

This is `PROVED_EXACT_TRANSPORT_GATES_1_2`.  It proves the conductor
relation and Artin-index map, but does not yet identify the target
packet.

## Consequence for the remaining gates

The added prime has source ray-class log one.  Thus the odd characters
are altered by nontrivial local Euler factors; a direct equality of the
two packets would be unjustified.  The remaining task is to derive and
certify the Artin-labelled Euler-factor distribution relation, then
check the positive orientation it induces at the fixed split real
place.  No target packet is promoted by this record.

## Replay

```sh
python3 scripts/run_rq000039_transport_gates_1_2.py
```

Evidence: `artifacts/rq000039-engine-b-transport-gates-1-2-v1.json`.

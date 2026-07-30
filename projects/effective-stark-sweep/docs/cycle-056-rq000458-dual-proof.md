# Cycle 056 — RQ-000458 dual proof

Status: `DUAL_PROVED`.

The cost screen selected RQ-000458, over `Q(sqrt(14))` with finite
ideal HNF `[[12,0],[0,6]]`, because its shortest Engine-B route has
safe exponent 1152.

The alignment gate was exact. Both engines use the same modulus, the
same character pair `[1,1]`, `[3,1]`, and the same relative packet

```text
x^4-(20+6*y)*x^3+(138+36*y)*x^2-(20+6*y)*x+1.
```

Engine B then proved the packet through Shintani index two and height
rigidity. Engine C independently proved it through exact linear
reinduction to `Q(sqrt(-42))` and `Q(sqrt(-3))`, Stark 1980, an Arb
unit-lattice orientation, and exact normal-closure identities. The C
orientation recomputed its analytic target and did not read the B
certificate transcript.

All failed parser runs, the failed first CM norm convention, and the
interrupted broad bridge search are retained. The final case record is
`data/rq000458-dual-case-v1.json`.

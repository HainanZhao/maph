# Cycle 060 — Engine-C tranche 01 boundary

**Recorded:** 2026-07-30T05:50:38Z  
**Claim tag:** `VERIFIED_STAGING_ONLY`  
**Promotion:** `BLOCKED_MISSING_GENERIC_W3`

The smallest closure-batched member of the open \(e\in\{2,4\}\)
queue is packet field 1 in the polynomial-sorted exact inventory:

```text
x^8 + 10*x^6 + 14*x^4 - 20*x^2 + 4.
```

It has two occurrences over \(\mathbb Q(\sqrt{35})\):

| Case | Finite ideal HNF | Norm | Packet | Primitive conductor |
|---|---|---:|---:|---|
| `RQ-001280` | `[[8,4],[0,4]]` | 32 | 1 | `[[8,4],[0,4]] infinity_2` |
| `RQ-001297` | `[[8,0],[0,8]]` | 64 | 1 | `[[8,4],[0,4]] infinity_2` |

Both member blocks independently give source and primitive character
`[1,0]`, the same packet polynomial, and the same two linear
reinduction bases \(\mathbb Q(\sqrt{-10})\) and
\(\mathbb Q(\sqrt{-14})\). The exact closure-level \(e\) calculation
was replayed once and returned route pair \((2,2)\), exactly matching
the frozen inventory. Member-modulus identity and packet transport were
then checked separately.

The first wrapper replay is preserved as
`engine-c-w3-tranche-01-e-replay-failed-v0.transcript`. It supplied
the radicand \(35\) where the existing GP contract requires field
discriminant \(140\), and halted at the source-subgroup assertion. The
corrected replay succeeded without changing the underlying GP code.

## W3 boundary

This tranche does **not** promote either occurrence. Repository
inspection found no generic Engine-C W3 pipeline. The generic machinery
currently stops after exact field geometry and exact torsion order.
Three components remain case-specific:

1. a complete compatible CM ray-character table with an injective
   exact Dirichlet-coefficient signature;
2. a rigorous Arb analytic target and unique integral unit-orbit
   isolation;
3. Artin-labeled exact normal-closure identities mapping that orbit to
   each real member packet.

The existing RQ-000458 and Paper-II scripts demonstrate these steps for
their individual cases, but they are not parameterized over a census
record. Reusing their constants or treating the exact \(e\) replay as
W3 would cross the banked promotion boundary. Consequently tranche 01
is a truthful implementation map for the generic C bulk, with zero new
`VERIFIED` packets.

## Replay

```text
python3 scripts/stage_engine_c_w3_tranche_01.py --run
```

The resulting boundary record is
`artifacts/engine-c-w3-tranche-01-boundary-v1.json`, SHA-256
`529358b90decf0026a82d87d8db31afa28548897c61428999104fd69ce18c6e6`.
The successful exact-\(e\) transcript has SHA-256
`aed946310c1ba7b1699b2e4933a8e3d714b93ccade07eb91a7e637579a6bf0e4`;
the preserved failed wrapper run has SHA-256
`9a73dee3ad719af3be940166415a64bc613e958fe5f6535ab490d9d68b9da6b6`.

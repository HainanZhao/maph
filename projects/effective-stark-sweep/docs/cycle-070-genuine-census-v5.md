# Cycle 070 — genuine census v5

## Outcome

All three proxy-recovery tracks closed in this block:

1. 241/241 Engine-B rows were reconstructed at a common stable modulus.
2. 252/252 quartic rows reached complete Engine-C geometry.
3. 8,200/8,200 normal-closure indices were reconstructed genuinely.

No case-level theorem was retracted. RQ-007500 re-passed and the
historical 51-closure count was restored before the wider recovery.

## Engine-B correction

The 241-row result is:

| result | rows |
|---|---:|
| genuine Engine-B pass | 90 |
| index 4 | 74 |
| index 6 | 45 |
| index 8 | 24 |
| index 10 | 8 |

All 64 former proxy passes genuinely re-pass. Of the 177 withdrawn
proxy negatives, 26 are genuine B passes and 151 are genuine
index frontiers. Integration exposed 19 further genuine-index-two rows
formerly excluded by the proxy: eight exceed the frozen degree-40 cap,
while all 11 affordable rows pass two independent imaginary-base
reconstructions. Final Engine-B accounting is therefore 232
occurrences in 88 distinct normal closures.

## Engine-C correction

The catch-up adds 153 fully C-eligible rows. Ninety-five rows have no
passing packet, three are mixed pass/fail, and one is explicitly
`TOOL_BLOCKED`. Across the old and new populations there are 881
C-eligible rows, 1,361 packet occurrences, and 447 distinct packet
fields.

## Census v5

| verdict | occurrences |
|---|---:|
| `PROVED_TRIVIAL` | 3,899 |
| Engine A | 1,560 |
| Engine B | 232 |
| Engine C | 881 |
| `FRONTIER` | 1,628 |

The taxonomy is 1,088 `INDEX_GT_2`, 502 `EXPONENT_CAP`, 31
`UNIT_CONGRUENCE_FAIL`, five `TOOL_BLOCKED`, and two
`REAL_PLACE_SPLITTING_FAIL`.

The genuine norm-quartile shares are \(189/2245\), \(404/2069\),
\(459/1867\), and \(576/2019\), or 8.42%, 19.53%, 24.58%, and
28.53%. Strict monotonicity survives; the old proxy percentages are
superseded.

The genuine index ledger contains 446 odd indices above two, all on
empty-support trivial rows. There is no substantive odd-index
frontier. RQ-000172 (index three) was the halt control that established
this distinction.

## Estimate versus realization

The frozen recovery estimate was 10–16 overlapping research cycles.
The first direct-polynomial control exhibited a 20-minute heavy tail,
but the common-stable-modulus quotient removed the unnecessary
polynomial proof obligation from index screening. Once that theorem
path was frozen, tracks a–c completed in the same research block. This
is a methodological gain, not a threshold rewrite: the original
estimate and failed heavy-tail transcript remain banked.

## Gates

Census v5 is open and banked. W4 remains closed only on occurrence
transport for the B closure corpus. The results paper is unchanged:
every result it contains was already proxy-clean and cannot change
under the v5 correction.

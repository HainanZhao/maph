# Effective Stark Sweep dependency for the SIC--Stark program

## Published source and frozen identity

`PROVED`: *Effective Archimedean Stark Theorems over Real Quadratic
Fields: Quadratic Support, Shintani Transfer, and CM Descent*, version 1.5,
was published on 31 July 2026 at DOI
<https://doi.org/10.5281/zenodo.21713178>. The publication record reports a
publicly verified five-file inventory and gives SHA-256
`ed273d87b90dd2539a948b654ba3e6d98d211e276ccb87bc4684fd1d53caf7b9`
for the top-level TeX source.

Local publication record:

- `../effective-stark-sweep/artifacts/zenodo-results-publication-v6.json`
- SHA-256 `5781310423454cf877fc4656e55740e594c5e293a87035d04b42841f249f9d39`

## Theorems relevant to SIC--Stark

`PROVED`: the published paper supplies three distinct engines:

1. a uniform exact formula for quadratic Fourier support;
2. an index-two Shintani-transfer plus all-embeddings height-rigidity engine
   for selected higher-order packets; and
3. a cyclic-quartic Fourier-to-CM-norm theorem using Stark's proved
   imaginary-quadratic result.

`PROVED`: its selected higher-order theorem closes five order-six packets.
In particular, `RQ-000190` over `Q(sqrt(7))` closes at safe exponent `4032`,
showing that character order six is not itself the obstruction. `RQ-002057`
over `Q(sqrt(57))` has a ramified 3-power conductor and also closes by the
Shintani route, showing that order six plus a ramified 3-power conductor is
still not sufficient to explain the dimension-six wall.

`PROVED`: the paper's componentwise results identify positive one-place
invariants as Artin-labelled polynomial roots. Roblot's cyclic-sextic index
theorem, by contrast, supplies a weak statement up to complex absolute
values; it does not by itself identify every oriented Artin component needed
by the SIC--Stark bridge.

## Shared `Q(sqrt(21))` object

`PROVED`: the subsequent Effective Stark Sweep dossier identifies its
`RQ-000692` row with the dimension-six companion's exact ray object:

- base field `Q(sqrt(21))`;
- finite modulus `(6)`, norm `36`, with one real place;
- ray group `C_6`, support orders `(2,6)`, and Shintani/derived-subgroup
  index `6`;
- the same degree-12 ray field, with the two pinned polynomials related by
  `P_SIC(X)=P_census(-X)`;
- relative ramification index `6` above `3`.

`PROVED`: every other audited Roblot sextic gate passes, but the no-wild-prime
condition above `3` fails. This is a theorem-hypothesis boundary, not a proof
of nonalgebraicity or a no-go for dimension-six TCC.

Local dossier:

- `../effective-stark-sweep/docs/cycle-132-qsqrt21-wild3-dossier.md`
- SHA-256 `7b06bb0aefd1b4871c30dc2fd9146d1fd3fb9c6395ccff6146ceccf18ea33748`

## Consequence for the accelerated program

`CONJECTURED`: Phase 0 should treat a wild-local extension of the sextic
Stark/index mechanism as an independent arithmetic engine alongside the
analytic interface/fusion route. It must recover the **oriented** primitive
order-six regulator equality and the pinned ray labels; an absolute-value or
unoriented index statement is insufficient.

Even a successful wild-local theorem does not automatically prove TCC. It
must still connect to the operational coefficient-to-cocycle/ray-logarithm
interface and then pass the exact downstream multiplier/TCC replay. The
published sweep paper is therefore a source of proved controls and candidate
engines, not a substitute for the missing bridge.

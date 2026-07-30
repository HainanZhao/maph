# Cycle 058 — theorem and bulk gates

## Yield scope correction

The 8,200-row yield is unchanged:

- 3,899 trivial proved occurrences;
- 2,483 substantive theorem-route occurrences;
- 1,818 frontiers.

The substantive count is `1560 A + 195 B + 728 C`. At packet level,
the 728 fully C-eligible rows contain 1,163 packets and 393 packet
fields. The previously reported 1,255/430 figures include 92 passing
packets in 41 mixed-pass rows; those are valid geometry passes but not
members of the complete-case C bulk. The corrected v2 declaration has
SHA-256
`f2be4c87f28842aab96750eedf50b379200689cacc56c00f5041ae53901269a9`.

## Uniform Engine-A theorem

The theorem gate is `VERIFIED_THEOREM`. For a quadratic character
odd at the selected real place, the quadratic field has signature
`(2,1)`, and

```text
L'_m(0,chi)
 = E_chi * (h_L/h_K) * (w_K/w_L)
   * (2/I_chi) * log|u_chi|.
```

Here `E_chi` is the exact imprimitive Euler product and `I_chi` is the
determinant of the embedded base-unit vector with a primitive generator
of the exact norm kernel on free unit lattices. This replaces the
insufficient coordinate-gcd shortcut. Exact Fourier inversion and
denominator clearing give the packet power identity. The
dimension-four and both dimension-eight quadratic packets replay the
formula. A-bulk is now open over 1,560 occurrences, 2,232 supported
characters, and 912 distinct quartic fields.

## Engine-C e inventory

All 393 distinct eligible packet fields were reconstructed through
both imaginary-base routes. Every one of the 786 character fields
passes `bnfcertify`. Minimum-e distributions are:

| minimum e | fields | packet occurrences |
|---:|---:|---:|
| 2 | 227 | 404 |
| 4 | 90 | 292 |
| 6 | 75 | 457 |
| 8 | 1 | 10 |

Thus banked `e=2,4` lemmas cover 317/393 fields and 696/1,163 packet
occurrences. At complete-case level, 395 cases have every packet on an
`e=2,4` route and may enter C-bulk. The remaining 333 cases contain at
least one minimum `e>4` packet and remain blocked behind general-e
normalization and orientation.

The unique minimum-e=8 field is the Q(sqrt(6)) packet. It occurs ten
times and has the exact route pair `(8,12)`, over Q(sqrt(-2)) and
Q(sqrt(-3)). This strengthens the inherited Q(sqrt(6)) boundary:
obligations (b) and (c) must handle an eightfold primary orientation
and a twelvefold independent-route normalization. The exact inventory
has SHA-256
`a53be7591753b11fecdad2d96dca4479b99bbfaf732982fc1cf17dcf0ac5ef9b`.

## Closure-batched B plan

The 195 eligible B occurrences define 59 closures. Eight closures have
a banked representative; exactly 51 remain, containing 159
occurrences. There are also 28 unverified member occurrences sharing
the eight banked closures, so 187 occurrence identities remain.

The protocol is:

1. one two-route and divisor audit per closure;
2. one canonical W3 packet identification per closure;
3. exact member-modulus ray-class and orientation transport.

Closure equality alone never promotes a member occurrence. The frozen
plan hash is
`fb63cd8953423a7120330ff259a84edab2225dd0b72ef9eb54aff0b3dadfd114`.

## Remaining B/C overlaps

After the bulk plan freeze, all ten remaining overlap candidates passed
exact alignment: same modulus, ray classes, odd quartic character pair,
kernel, and relative/absolute packet field polynomials. They remain
`ALIGNED_NOT_DUAL_PROVED`; each still needs independent B and C W3
bundles. The alignment artifact hash is
`871667c5e2a6ec033afa85ea523c7abce40d3de5f0dbcb1000a87f83b2843318`.
Two parser failures are preserved before the successful run.

## W4 gate

W4 remains closed until A-bulk, B closure/member transport, and both
open and general-e C queues close. Its frozen analysis queue is: index
distribution, FRONTIER share versus norm, exponent growth, polynomial
families, and tower recurrences.

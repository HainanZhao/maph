# Census-paper preregistration amendment v7: Roblot sextic census

Frozen: 2026-07-31 UTC, after reading Roblot 2013, Theorem 7.1 and
freezing the order-six kernel inventory, before extracting any new
sextic field.

Population:

- 486 H rows with order-six support;
- 1,528 supported order-six characters;
- 764 character/inverse-character kernels;
- inventory SHA-256
  `3ce1d225e63e3a87c1402271c571a115280e0ee2a58b4aa8ffa14b4887fb7dfd`.

For each kernel, transport the character to its primitive conductor and
construct the exact cyclic sextic ray field \(H/K\).  Check:

1. relative degree six and the one-place signature \([6,3]\) over
   \(\mathbb Q\) (`A1`);
2. the index-two maximal totally real subfield, which follows here from
   the cyclic degree-six construction plus the checked signature
   (`A2`);
3. every finite prime in the row's \(S\) is ramified or has even
   Frobenius order in the cyclic quotient (`A3`);
4. no finite prime was added beyond the conductor, since Theorem 7.1
   requires \(S=S(H/K)\);
5. `bnfinit(P,1)` plus `bnfcertify`, and \(3\nmid h_H\);
6. exact relative ramification indices above 3, with none divisible by
   3.

Theorem 7.1 is marked applicable only when all six gates pass.  A
kernel failure is preserved and keeps that row's sextic status
incomplete.  Eligibility is prior-work coverage, not a new Stark
identity.

Resource caps: 600 seconds and 2 GiB address space per kernel.  No
method substitution or dropped kernel is authorized by a cap failure.

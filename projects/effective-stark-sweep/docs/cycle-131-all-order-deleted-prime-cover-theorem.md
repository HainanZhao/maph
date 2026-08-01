# Cycle 131 — all-order deleted-prime cover theorem

## Claim boundary

**PROVED.** Let (K) be a real quadratic field, let (mathfrak m)
be a one-place ray modulus, and write

[
 Z_{mathfrak m}(s,A)=zeta_{mathfrak m}(s,A)-zeta_{mathfrak m}(s,RA),
 qquad X_{mathfrak m}(A)=exp Z'_{mathfrak m}(0,A).
]

For each character in the Fourier support (chi(R)=-1), let
(chi^circ) be its primitive character and let
(mathcal D_chi) be the finite primes present in (mathfrak m) but
absent from its primitive conductor.  If every supported (chi) has
a (mathfrak pinmathcal D_chi) with
(chi^circ(mathfrak p)=1), then
(X_{mathfrak m}(A)=1) for every ray class (A).

The result is independent of the character orders.  It is only a
one-way criterion: it neither states a converse nor supplies a
nonvanishing result for an uncovered higher-order character.

## Proof

The imprimitive Euler product is

[
 L_{mathfrak m}(s,chi)=L(s,chi^circ)E_chi(s),
 qquad
 E_chi(s)=prod_{mathfrak pinmathcal D_chi}
 (1-chi^circ(mathfrak p)Nmathfrak p^{-s}).
]

Because (chi(R)=-1), the primitive Hecke character has the odd
real-place infinity type.  Its completed Hecke (L)-function has the
corresponding gamma factor, so the functional equation gives the
trivial (rank-one) zero (L(0,chi^circ)=0).  This is the same
parity-zero input used in the exact Euler-deletion transport proofs;
it does not invoke a Stark-unit nonvanishing statement.

If (chi^circ(mathfrak p)=1) for a deleted prime, then its Euler
factor is (1-Nmathfrak p^{-s}).  Thus (E_chi(0)=0), and ordinary
differentiation gives

[
 L'_{mathfrak m}(0,chi)=L'(0,chi^circ)E_chi(0)
 +L(0,chi^circ)E'_chi(0)=0.
]

Fourier inversion for the differenced partial zeta function is

[
 Z'_{mathfrak m}(0,A)=
 {2\over |\operatorname{Cl}_{mathfrak m}(K)|}
 sum_{\chi(R)=-1}\overline{\chi(A)}L'_{mathfrak m}(0,\chi).
]

All summands vanish under the cover hypothesis, hence
(Z'_{mathfrak m}(0,A)=0) and (X_{mathfrak m}(A)=1).

## Exact finite corollary

The frozen H-stratum audit in
`proof/audit_h_all_order_deleted_prime_cover.py` replays the local
phases exactly from PARI/GP and identifies 64 fully covered rows among
2,704.  This finite count is **OBSERVED**, not a proof of any
converse.  RQ-000692 is uncovered: its two order-six characters have
no deleted finite primes, and its order-two character's only deleted
prime has primitive phase (1/2), hence value (-1), not one.

## Falsification condition

The theorem would fail if a supported primitive character did not have
the stated parity zero, if a listed deleted prime were ramified in its
primitive conductor, or if an exact phase denominator of one did not
mean character value one.  The exporter and replay audit check the
last two finite conditions; the first is the standard one-place
functional-equation parity calculation above.

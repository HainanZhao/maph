# Census-paper preregistration amendment v10: quotient class-group gate

Frozen: 2026-07-31 UTC, after a 60-second stage profile isolated full
`bnfcertify(bnf,0)` as the hard-field bottleneck, before applying the
quotient certificate to any population field.

The Roblot Theorem 7.1 gate needs only \(3\nmid h_H\); this census does
not use units or principal-ideal generators from the sextic field.
PARI's documented `bnfcertify(bnf,1)` proves that the actual class group
is a quotient of the group computed by `bnfinit`.  Therefore, when the
computed class-group order is prime to 3 and the quotient certificate
returns 1, the actual class-group order is rigorously prime to 3.  This
is sufficient for the theorem hypothesis.

The optimized field screen will still use `bnfinit(P,1)`.  It will then:

1. require `bnfcertify(bnf,1)=1`;
2. if the computed order is prime to 3, mark the theorem's class-number
   gate proved by the quotient argument and do not run the stronger
   full-unit certificate;
3. if the computed order is divisible by 3, run full
   `bnfcertify(bnf,0)` before deciding the gate.

This is a scoped supersession of the stronger procedural phrase
“`bnfinit(P,1)+bnfcertify` everywhere” for the sextic prior-work
eligibility census only.  It does not certify the displayed unit system
or regulator and must never be reused as such.  Every selected packet
identity and every field from which units are used retains the full
certificate requirement.

The 60-second profile of field key
`31570b7ac61b18dd001845e42db811b89347e61efb60ad1378c70a91bdec453e`
completed class-field construction, relative initialization, absolute
polynomial reduction, and `bnfinit`; its last completed marker was
`ABSOLUTE_BNFINIT`, isolating full `bnfcertify` as the timeout stage.

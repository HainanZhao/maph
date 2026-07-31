# Census-paper preregistration amendment v12: v5 Engine-B transport

Frozen: 2026-07-31 UTC, after the genuine v5 normal-closure
reconstruction and before building any member-transport certificate.

The population is exactly 232 v5 Engine-B rows in 88 exact normal
closures.  The historical W2 ledger contained 159 pending member IDs
in 59 closures; all 159 remain in v5.  All 195 historical Engine-B
eligible IDs remain, and v5 adds 37 further eligible IDs.  Thus 73 v5
rows lie outside the old pending-member list: 36 historical
direct/banked cases plus the 37 new v5 eligibility IDs.

The first deliverable is a manifest only.  It groups rows by their
already certified normal-closure polynomial and names a deterministic
canonical member (least finite norm, then RQ id).  It records no
member-level Stark identity.

For a member to acquire a transported case-level claim, all of these
exact obligations must pass:

1. finite-modulus identity or an exact conductor relation;
2. the ray-class map with identity and sign-class labels;
3. agreement of the positive orientation at the frozen split real
   place; and
4. an Artin-labelled packet distribution relation or direct packet
   equality.

Each member has a 600-second and 2-GiB cap.  A cap failure or a failed
obligation remains explicit and does not remove the member or promote
its closure.  Closure membership, mechanism eligibility, and a
banked representative are not member transport.

# Cycle 106 — first Engine-B member-transport certificate

The user has authorized work to close the Engine-B occurrence gap.  The
first target is frozen as the smallest noncanonical member in a closure
whose canonical member already has a direct packet certificate:

| source representative | target member | closure | base | source modulus | target modulus |
|---|---|---|---|---|---|
| RQ-000021 | RQ-000039 | B5-015 | Q(sqrt(2)) | `[[7,0],[0,7]]`, norm 49 | `[[14,0],[0,7]]`, norm 98 |

The shared degree-24 normal-closure polynomial, both genuine
derived-subgroup orders, and both one-place ray cyclic structures are
frozen inputs from the v5 records.  The target is a conductor-enlarged
one-place modulus; it is not promoted merely because the two normal
closures agree.

The proof route has four mandatory exact gates from amendment v12:

1. prove the ideal/conductor relation, including the prime ideal added
   in passing from norm 49 to norm 98;
2. construct the ray-class map and prove its identity and real-sign
   labels;
3. prove that the positive orientation at the chosen split real place
   is preserved; and
4. prove an Artin-labelled packet distribution relation, or certify the
   target packet directly and prove exact equality to that relation.

Exploratory `bnrL1` values may guide candidate selection, but they are
labelled `RECOGNIZED` and cannot close any gate.  The exact per-member
cap remains 600 seconds and 2 GiB.  A failed gate, timeout, or
counterexample is recorded as a visible target outcome; it does not
change the B5-015 membership or promote any other row.

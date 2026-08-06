# C86 source audit: chain conditions and optimal elements

`PROVED` from Cory H. Colbert, *Chain Conditions and Optimal Elements in
Generalized Union-Closed Families of Sets*,
[arXiv:2412.18740v3](https://arxiv.org/abs/2412.18740v3), Theorem 3.17:
every union-closed family of dimension at most two has an abundant element.
The source defines dimension as maximum chain length, so C86's "height four"
means dimension exactly three.

`PROVED` from the same source, Example 3.19: the dimension-three family
\[
\{\varnothing,\{2\},\{3\},\{1,2\},\{1,3\},\{2,3\},
\{1,2,3\}\}
\]
has an optimal element \(1\) that is not abundant.  It is a mandatory
negative control for any statement claiming every optimal element works.

`PROVED` from the same source, Example 3.20: a dimension-three union-closed
family on \([5]\) has every element optimal and abundant, while for each
\(x\) some set without \(x\) has no immediate \(x\)-cover.  It is a
mandatory control that distinguishes the proposed all-inclusion graph from
the source's immediate-cover graph.

`OBSERVED` from the current bounded literature screen: the cited arXiv v3
abstract proves the chain-at-most-three result and does not claim the
dimension-three case.  The OpenAI mathematics announcements inspected in
this run concern the planar unit-distance result, not union-closed families.
This bounded audit is not proof that no other result exists.

## Claim boundary

No source attributes the all-inclusion Hall transport statement to Colbert or
establishes it.  C86 treats it as `CONJECTURED` and tests only its frozen
finite gate.

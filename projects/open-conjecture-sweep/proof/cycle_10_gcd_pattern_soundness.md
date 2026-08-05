# Cycle 10: gcd-pattern state

At multiplier `c=14`, Definition 2.1's gcd condition is true precisely when,
after omitting some coordinate, the other twelve lifted speeds share a factor
2 or 7. Equivalently a lift can be improper only if its selected digits obey
`N_2<12` and `N_7<12`, where `N_r` counts lifted speeds divisible by `r`.

The search state records assigned digits, their covered lifted-time mask, and
these two counts. A branch that already has `N_2>=12` or `N_7>=12` contains no
improper lift and can be discarded. Conversely no other branch is discarded
merely from its pattern label. Any later capacity bound must demonstrate that
no assignment of each unassigned coordinate to any of its allowed digit masks,
while respecting both remaining count capacities, covers the uncovered times.
That establishes the advertised retained-path soundness.

A completed selected mask cover satisfying both strict counts is directly an
improper lift: it has no witness and fails every gcd properness condition. A
completed noncover or a capped branch establishes neither conclusion.

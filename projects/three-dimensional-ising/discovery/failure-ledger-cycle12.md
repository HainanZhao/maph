# Cycle 12 failure ledger

1. **KILLED implementation assertion:** the first incidence generator required
   every normal-island boundary edge to belong to the encoder tree `T_W^+`.
   This is false already for `W=4`: gauge boundary edges belong to the fixed
   gauge tree `T_W^0`, and `T_W^0` is not a subtree of the independently
   constructed encoder tree. The mathematical trichotomy requires membership
   in `T_W^0 union X_W^+`, not in `T_W^+`. The extra assertion was removed;
   the independently computed cellular boundary and its gauge/exceptional
   classification were retained unchanged.

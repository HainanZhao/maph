#!/usr/bin/env python3
from proof.verify_cycle_238_faddeev_fourier_dualization import audit
def test_one_kernel_fourier_identity_cannot_dualize_heterogeneous_word():
 r=audit();assert r["source_transform_applies_to_entire_residual_word"] is False;assert all(x["distinct_period_pair_count"]==4 for x in r["residual_blocks"])

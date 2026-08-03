from proof.verify_cycle_240_mixed_base_two_kernel import audit


def test_faddeev_two_kernel_closure_has_no_common_c228_period_system():
    result = audit()
    assert result["status"] == "FALSIFIED_FADDEEV_TWO_KERNEL_COMMON_PERIOD_CLOSURE"
    assert result["endpoint_field"]["irreducible_over_Q"] is True
    for row in result["starts"]:
        assert row["common_period_system_up_to_scale_or_swap"] is False
        assert row["faddeev_MIR_two_kernel_closure_available"] is False

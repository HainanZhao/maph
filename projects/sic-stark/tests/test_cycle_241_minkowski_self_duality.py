from proof.verify_cycle_241_minkowski_self_duality import audit
def test_trace_scaled_minkowski_lattice_is_self_dual():
    r=audit(); assert r["self_dual"] and r["determinant"]==-1 and r["signature"]=="(1,1)"
    assert r["fourier"]["unitary_on_L2"] and r["fourier"]["poisson_for_O_K"]

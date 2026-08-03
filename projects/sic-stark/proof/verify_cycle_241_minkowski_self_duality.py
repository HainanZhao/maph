"""Exact Minkowski trace-lattice audit for Cycle 241/B078."""
from fractions import Fraction as F


def audit():
    # omega^2=omega+5; for x=a+b*omega, Tr(x)=2a+b.
    # With c=1/sqrt(21), Tr(c)=0, Tr(c*omega)=1,
    # and Tr(c*omega^2)=Tr(c*(omega+5))=1.
    gram=((F(0),F(1)),(F(1),F(1)))
    inverse=((F(-1),F(1)),(F(1),F(0)))
    assert gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]==-1
    assert tuple(tuple(sum(gram[i][k]*inverse[k][j] for k in range(2)) for j in range(2)) for i in range(2))==((F(1),F(0)),(F(0),F(1)))
    render=lambda matrix:[[str(x) for x in row] for row in matrix]
    return {"epistemic_status":"PROVED","field":"Q(sqrt(21))","basis":["1","(1+sqrt(21))/2"],"trace_pairing_scale":"1/sqrt(21)","gram":render(gram),"determinant":-1,"signature":"(1,1)","dual_basis_coordinates":render(inverse),"self_dual":True,"fourier":{"definition":"F_B f(x)=integral_R2 f(y) exp(-2*pi*i*B(x,y)) dy","self_dual_measure":True,"unitary_on_L2":True,"square":"F_B^2 f(x)=f(-x)","poisson_for_O_K":True,"reason":"B is real, symmetric, nondegenerate and |det Gram|=1; standard Fourier inversion/Plancherel and Poisson summation apply to Schwartz(R2) and its B-self-dual lattice."},"claim_boundary":"This proves only algebraic/Fourier infrastructure; it does not supply contour convergence, a mixed-base identity, AFK, fusion, Stark, or TCC."}

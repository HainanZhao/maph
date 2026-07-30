#!/usr/bin/env python3
"""Independent Arb/Shintani certificate for RQ-000021."""
from fractions import Fraction
from flint import arb, ctx, fmpz_poly
from certify_q7_p7_packet import arb_fraction
from certify_rq000108_packet import (
    log_double_sine, determinant, matrix_vector,
    mod_one_upper, quotient_generator,
)

SAFE_EXPONENT=2016
BASE=((1,3),(0,2))
ACTION=((3,4),(2,3))

def matrix(step):
    first=(BASE[0][0],BASE[1][0]); second=(BASE[0][1],BASE[1][1])
    for _ in range(step):
        first=matrix_vector(ACTION,first);second=matrix_vector(ACTION,second)
    return ((first[0],second[0]),(first[1],second[1]))

def mod_one_lower(value):
    return value-value.numerator//value.denominator

def points(class_log,step,upper):
    m=matrix(step); det=determinant(m)
    if abs(det)!=2: raise RuntimeError("determinant changed")
    gen=quotient_generator(m,det); shift=(Fraction(3**class_log,7),Fraction(0))
    ans=[]
    for residue in range(2):
        a=shift[0]+residue*gen[0];b=shift[1]+residue*gen[1]
        first=Fraction(m[1][1]*a-m[0][1]*b,det)
        second=Fraction(-m[1][0]*a+m[0][0]*b,det)
        reduce=mod_one_upper if upper else mod_one_lower
        ans.append((reduce(first),reduce(second)))
    return ans

def main():
    ctx.dps=90;ctx.cap=16;tolerance=Fraction("1e-10")
    beta=3+2*arb(2).sqrt();logs=[];panels=0
    for c in range(6):
        convention_values=[]
        for upper in (True,False):
            value=arb(0)
            for step in range(3):
                for a,b in points(c,step,upper):
                    term,n=log_double_sine(arb_fraction(a)+arb_fraction(b)*beta,beta,tolerance/12)
                    value+=term;panels+=n
            convention_values.append(2*value)
        logs.append((convention_values[0]+convention_values[1])/2)
    Q=fmpz_poly([1,-20,144,-458,700,-784,827,-784,700,-458,144,-20,1])
    roots=[r.real for r,m in Q.complex_roots() if m==1 and r.imag.contains(0) and r.real>0]
    windows=[(6109,6110),(7496,7497),(4351,4352),(163,164),(133,134),(229,230)]
    maximum=arb(0)
    for i,(lo,hi) in enumerate(windows):
        print(f"CLASS_{i}_ANALYTIC_LOG={logs[i]}")
        selected=[r for r in roots if r>arb(lo)/1000 and r<arb(hi)/1000]
        if len(selected)!=1: raise RuntimeError(f"root window {i} failed")
        diff=logs[i]-selected[0].log()
        if not diff.contains(0): raise RuntimeError(f"class {i} mismatch {diff}")
        maximum=max(maximum,arb(abs(diff).upper()))
        print(f"CLASS_{i}_ALGEBRAIC_ROOT={selected[0]}")
        print(f"CLASS_{i}_LOG_DIFFERENCE={diff}")
    bounds=[(arb(d).log().log()/arb(d).log())**3/(4*d) for d in range(3,25)]
    lower=arb(min(x.lower() for x in bounds));powered=SAFE_EXPONENT*maximum;margin=lower/powered
    fallback=((1+arb(5).sqrt())/2).log()/2
    if not (margin>100 and fallback>powered):raise RuntimeError("height gate failed")
    print("CASE_ID=RQ-000021");print("CONE_POINTS_PER_CLASS=6")
    print("BOUNDARY_CONVENTION=AVERAGE_OF_UPPER_AND_LOWER_HALF_OPEN")
    print("UNIT_ORDER_MOD_FINITE=3");print(f"TOTAL_TAYLOR_PANELS={panels}")
    print(f"SHINTANI_SAFE_EXPONENT={SAFE_EXPONENT}")
    print(f"POWERED_HEIGHT_UPPER={powered}");print(f"VOUTIER_MARGIN={margin}")
    print(f"QUADRATIC_HEIGHT_FALLBACK={fallback}")
    print("DEGREE_1_FALLBACK=POSITIVE_RATIONAL_UNIT_IS_1")
    print("RQ000021_PACKET_IDENTITY_VERIFIED=1");print("CLAIM_TAG=VERIFIED")
if __name__=="__main__":main()

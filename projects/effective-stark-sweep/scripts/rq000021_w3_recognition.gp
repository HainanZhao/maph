\\ Numerical recognition only for RQ-000021.
default(realprecision,260); default(parisizemax,2000000000);
cv(c,a,n)=exp(2*Pi*I*c*a/n);
run_case() =
{
  my(K=bnfinit(y^2-2,1), f=[7,0;0,7]);
  my(r=bnrinit(K,[f,[1,0]],1), v=bnrL1(r,,6));
  my(s=bnrisprincipal(r,idealhnf(K,6),0)[1]);
  my(d=vector(6), q=1);
  for(a=0,5,my(u=0,w=0);for(i=1,#v,if(v[i][2][1]==1,
    u+=conj(cv(v[i][1][1],a,6))*v[i][2][2];
    w+=conj(cv(v[i][1][1],(a+s)%6,6))*v[i][2][2]));
    d[a+1]=real((u-w)/6));
  my(z=vector(6,i,exp(d[i])));for(i=1,6,q*=x-z[i]);
  print("CASE_ID=RQ-000021");print("RAY_STRUCTURE=",Vec(r.cyc));
  print("RAY_GENERATOR=",r.gen[1]);print("SIGN_LOG=",s);
  print("DIFFERENCED_DERIVATIVES=",d);
  print("NUMERICAL_INVARIANTS=",z);print("NUMERICAL_PACKET_POLYNOMIAL=",q);
  for(i=0,6,my(t=real(polcoef(q,i)),rel=lindep([t,1,sqrt(2)]));
    print("COEFFICIENT_",i,"_RELATION=",rel," RESIDUAL=",
      abs(rel[1]*t+rel[2]+rel[3]*sqrt(2))));
  print("SHINTANI_SAFE_EXPONENT=2016");
  print("CLAIM_TAG=NUMERICAL_RECOGNITION_ONLY");
};

run_case();

\\ Numerical recognition only for RQ-001107, Q(sqrt(33)), p_11 infinity_2.
default(realprecision,300);default(parisizemax,3000000000);
cv(c,a,n)=exp(2*Pi*I*c*a/n);

recognize() =
{
  my(K=bnfinit(y^2-y-8,1),f=[11,5;0,1]);
  my(r=bnrinit(K,[f,[1,0]],1),values=bnrL1(r,,6));
  my(sign_log=0,sign_integer=0);
  for(q=2,100,
    if(gcd(q,11)==1,
      my(log=lift(bnrisprincipal(r,idealhnf(K,q),0)[1]));
      if(log==5&&!sign_integer,sign_integer=q;sign_log=log)
    )
  );
  if(!sign_integer,error("no rational sign representative found"));
  my(derivatives=vector(10),invariants,packet=1);
  for(class_index=0,9,
    my(first=0,second=0);
    for(index=1,#values,
      if(values[index][2][1]==1,
        first+=conj(cv(values[index][1][1],class_index,10))
          *values[index][2][2];
        second+=conj(cv(values[index][1][1],
          (class_index+sign_log)%10,10))*values[index][2][2]
      )
    );
    derivatives[class_index+1]=real((first-second)/10)
  );
  invariants=vector(10,index,exp(derivatives[index]));
  for(index=1,10,packet*=x-invariants[index]);
  print("CASE_ID=RQ-001107");print("RAY_STRUCTURE=",Vec(r.cyc));
  print("RAY_GENERATOR=",r.gen[1]);print("SIGN_INTEGER=",sign_integer);
  print("SIGN_LOG=",sign_log);print("DIFFERENCED_DERIVATIVES=",derivatives);
  print("NUMERICAL_INVARIANTS=",invariants);
  print("NUMERICAL_PACKET_POLYNOMIAL=",packet);
  for(index=0,10,
    my(value=real(polcoef(packet,index)));
    my(relation=lindep([value,1,sqrt(33)]));
    print("COEFFICIENT_",index,"_RELATION=",relation,
      " RESIDUAL=",abs(relation[1]*value+relation[2]
      +relation[3]*sqrt(33)))
  );
  print("SHINTANI_SAFE_EXPONENT=15840");
  print("CLAIM_TAG=NUMERICAL_RECOGNITION_ONLY")
};

recognize();

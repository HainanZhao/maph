\\ Exact W3 algebraic candidate for RQ-001107.
default(parisizemax,4000000000);
ae(l,a,e)={if(a!=e,error(Str(l,": expected ",e,", got ",a)));print(l,"=",a)};

go() =
{
  my(Kp=y^2-y-8,K=bnfinit(Kp,1),f=[11,5;0,1]);
  my(r=bnrinit(K,[f,[1,0]],1));
  my(P=x^10-(8+4*y)*x^9+(74+30*y)*x^8-(294+125*y)*x^7
    +(669+281*y)*x^6-(871+368*y)*x^5+(669+281*y)*x^4
    -(294+125*y)*x^3+(74+30*y)*x^2-(8+4*y)*x+1);
  my(Q=polresultant(Kp,P,y),rr=bnrclassfield(r,,1));
  my(a=rnfequation(Kp,P,1),b=rnfequation(Kp,rr,1));
  my(iso=nfisisom(a[1],b[1]),kc=0);
  for(i=1,#iso,
    if(subst(lift(Mod(a[2],a[1])),x,Mod(iso[i],b[1]))
      ==Mod(b[2],b[1]),kc++)
  );
  ae("PACKET_ABSOLUTE_IRREDUCIBLE",polisirreducible(Q),1);
  ae("PACKET_RECIPROCAL",x^20*subst(Q,x,1/x)==Q,1);
  ae("PACKET_UNIT_NORM",polcoef(Q,0),1);
  ae("K_COMPATIBLE_RAY_ISOMORPHISM_COUNT",kc,10);
  ae("PACKET_FIELD_BNFCERTIFY",bnfcertify(bnfinit(Q,1)),1);
  ae("PACKET_REAL_ROOT_COUNT",polsturm(Q),10);
  print("RELATIVE_PACKET_POLYNOMIAL=",P);
  print("ABSOLUTE_PACKET_POLYNOMIAL=",Q);
  print("REAL_ROOTS=",polrootsreal(Q));
  print("MAXIMUM_PACKET_COMPARISON_DEGREE=40");
  print("RQ001107_EXACT_CANDIDATE_VERIFIED=1")
};

go();

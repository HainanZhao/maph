\\ Exact W3 algebraic candidate for RQ-000021.
default(parisizemax,2000000000);
ae(l,a,e)={if(a!=e,error(Str(l,": expected ",e,", got ",a)));print(l,"=",a)};
go() =
{
 my(Kp=y^2-2,K=bnfinit(Kp,1),r=bnrinit(K,[[7,0;0,7],[1,0]],1));
 my(P=x^6-(10+6*y)*x^5+(58+40*y)*x^4-(129+90*y)*x^3+(58+40*y)*x^2-(10+6*y)*x+1);
 my(Q=polresultant(Kp,P,y),rr=bnrclassfield(r,,1));
 my(a=rnfequation(Kp,P,1),b=rnfequation(Kp,rr,1),iso=nfisisom(a[1],b[1]),kc=0);
 for(i=1,#iso,if(subst(lift(Mod(a[2],a[1])),x,Mod(iso[i],b[1]))==Mod(b[2],b[1]),kc++));
 ae("PACKET_ABSOLUTE_IRREDUCIBLE",polisirreducible(Q),1);
 ae("PACKET_RECIPROCAL",x^12*subst(Q,x,1/x)==Q,1);
 ae("K_COMPATIBLE_RAY_ISOMORPHISM_COUNT",kc,6);
 ae("PACKET_FIELD_BNFCERTIFY",bnfcertify(bnfinit(Q,1)),1);
 print("RELATIVE_PACKET_POLYNOMIAL=",P);print("ABSOLUTE_PACKET_POLYNOMIAL=",Q);
 print("REAL_ROOTS=",polrootsreal(Q));
 print("RQ000021_EXACT_CANDIDATE_VERIFIED=1");
};

go();

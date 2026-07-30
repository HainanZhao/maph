\\ Exact cone data for RQ-001107.
default(parisizemax,3000000000);

run_case() =
{
  my(Kpol=y^2-y-8,K=bnfinit(Kpol,1),f=[11,5;0,1]);
  my(r=bnrinit(K,[f,[1,0]],1),eps=K.fu[1],ord=0);
  print("RAY_STRUCTURE=",Vec(r.cyc));print("RAY_GENERATOR=",r.gen[1]);
  for(e=1,128,if(!ord&&nfeltreduce(K,eps^e-1,f)==[0,0]~,ord=e));
  print("EPSILON=",eps);print("EPSILON_NORM=",nfeltnorm(K,eps));
  print("EPSILON_ORDER_MOD_FINITE=",ord);
  for(a=0,9,
    my(A=idealpow(K,r.gen[1],a),b=idealdiv(K,f,A));
    my(best=10^99,el=0,co=0,ma=0);
    for(u=-200,200,for(v=-200,200,if(u||v,
      my(c=b*[u,v]~,z=nfbasistoalg(K,c),em=nfeltembed(K,z));
      if(em[1]>0&&em[2]>0,
        my(c2=nfalgtobasis(K,z*eps),m=matconcat([c,c2]));
        my(ix=abs(matdet(m)/matdet(b)));
        if(ix<best,best=ix;el=z;co=[u,v];ma=m)
      )
    )));
    print("CLASS_LOG=",a);print("CLASS_IDEAL=",A);print("B_LATTICE=",b);
    print("BEST_ELEMENT=",el);print("BEST_B_COORDINATES=",co);
    print("BEST_CONE_MATRIX=",ma);print("CONE_INDEX=",best)
  )
};

run_case();

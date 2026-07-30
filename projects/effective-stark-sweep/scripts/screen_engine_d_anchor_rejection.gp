\\ Exact negative anchor for the rejected absolute-abelian Engine D.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 80);
default(parisizemax, 4000000000);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
};

run_anchor() =
{
  my(kpol = field_polynomial(D_VALUE));
  my(K = bnfinit(kpol, 1));
  my(finite_ideal = [H11,H12;H21,H22]);
  my(autos = nfgaloisconj(K), autq = autos[1]);
  my(conjugate_ideal, stable);
  my(ray, relative, absolute, absolute_nf, signature);
  if(autq == Mod(y,K.pol), autq = autos[2]);
  conjugate_ideal =
    idealhnf(K,nfgaloisapply(K,autq,finite_ideal));
  finite_ideal = idealhnf(K,finite_ideal);
  stable = conjugate_ideal == finite_ideal;
  ray = bnrinit(K,[finite_ideal,[1,0]],1);
  relative = bnrclassfield(ray,,1);
  absolute = rnfpolredbest(K,relative,2);
  absolute_nf = nfinit(absolute);
  signature = absolute_nf.sign;

  print("CASE_ID=",CASE_ID);
  print("PARI_VERSION=",version());
  print("FIELD_POLYNOMIAL=",kpol);
  print("FIELD_DISCRIMINANT=",K.disc);
  print("BNFCERTIFY=",bnfcertify(K));
  print("FINITE_IDEAL=",finite_ideal);
  print("FINITE_CONJUGATE_IDEAL=",conjugate_ideal);
  print("FINITE_MODULUS_GALOIS_STABLE=",stable);
  print("FINITE_NORM=",idealnorm(K,finite_ideal));
  print("ONE_PLACE_RAY_CYC=",Vec(ray.cyc));
  print("ONE_PLACE_RELATIVE_POLYNOMIAL=",relative);
  print("ONE_PLACE_ABSOLUTE_POLYNOMIAL=",absolute);
  print("ONE_PLACE_ABSOLUTE_DEGREE=",poldegree(absolute));
  print("ONE_PLACE_ABSOLUTE_DISCRIMINANT=",absolute_nf.disc);
  print("ONE_PLACE_ABSOLUTE_SIGNATURE=",signature);
  print("MIXED_SIGNATURE=",
    signature[1] > 0 && signature[2] > 0);
  print("ABSOLUTE_ABELIAN_INTERPRETATION_REJECTED=",
    !stable || (signature[1] > 0 && signature[2] > 0));
  print("ANCHOR_REJECTION_COMPLETE=1");
};

run_anchor();


\\ Stark-1980 hypothesis and normalization certificate for the
\\ Q(sqrt(-2)) reinduction route of RQ-000129.

default(parisizemax, 4000000000);

run_certificate() =
{
  my(M = bnfinit(y^2 + 2, 1));
  my(Epol =
    x^8 - 4*x^6 - 4*x^5 + 6*x^4 + 16*x^3 + 16*x^2 + 8*x + 2);
  my(E = bnfinit(Epol, 1));
  my(relative = nffactor(M, Epol)[1, 1]);
  my(conductor_data = rnfconductor(M, relative));
  my(factorization = idealfactor(M, conductor_data[1][1]));
  my(distinct_finite_primes = matsize(factorization)[1]);
  my(S_size = 1 + distinct_finite_primes);

  print("CM_BASE_POLYNOMIAL=", M.pol);
  print("CHARACTER_FIELD_POLYNOMIAL=", Epol);
  print("CHARACTER_FIELD_SIGNATURE=", E.sign);
  print("CHARACTER_FIELD_CLASS_NUMBER=", E.no);
  print("CHARACTER_FIELD_BNFCERTIFY=", bnfcertify(E));
  print("CHARACTER_FIELD_ROOTS_OF_UNITY=", E.tu[1]);
  print("CM_CONDUCTOR=", conductor_data[1]);
  print("CM_CONDUCTOR_FACTORIZATION=", factorization);
  print("CM_RAY_CYC=", Vec(conductor_data[2].cyc));
  print("CM_RAY_SUBGROUP_HNF=", conductor_data[3]);
  print("DISTINCT_FINITE_CONDUCTOR_PRIMES=", distinct_finite_primes);
  print("STARK_S_SIZE=", S_size);
  print("EVERY_FINITE_S_PRIME_RAMIFIED=",
    distinct_finite_primes == 2);
  print("GLOBAL_UNIT_CLAUSE_APPLIES=", S_size >= 3);
  print("E_NORMALIZATION=", E.tu[1]);
  print("ORDINARY_ABSOLUTE_VALUE_COEFFICIENT=",
    2 / E.tu[1]);
  print("Q6_NORM8_STARK_1980_CONDITIONS_VERIFIED=",
    E.sign == [0, 4]
    && bnfcertify(E)
    && E.tu[1] == 8
    && S_size >= 3);
};

run_certificate();

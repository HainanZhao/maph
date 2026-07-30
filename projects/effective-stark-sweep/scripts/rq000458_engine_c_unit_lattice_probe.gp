\\ Numerical lattice probe for the Q(sqrt(-42)) Stark unit.
\\ The selected exponent vector is exact-audited in a separate script.

default(realprecision, 160);
default(parisizemax, 3000000000);

unit_exponents(bnf, unit) =
{
  my(raw = bnfisunit(bnf, unit));
  vector(#bnf.fu, index, raw[index]);
};

unit_action_matrix(bnf, polynomial, automorphism) =
{
  my(rank = #bnf.fu, answer = matrix(rank, rank));
  for(column = 1, rank,
    my(image = Mod(subst(
      lift(bnf.fu[column]), x, automorphism), polynomial));
    my(exponents = unit_exponents(bnf, image));
    for(row = 1, rank,
      answer[row, column] = exponents[row]);
  );
  answer;
};

resolvent(field, polynomial, sigma, unit) =
{
  my(value = 0, conjugate = unit);
  for(exponent = 0, 3,
    value += (-I)^exponent
      * log(abs(nfeltembed(field, conjugate, 1)));
    conjugate = Mod(
      subst(lift(conjugate), x, sigma), polynomial);
  );
  value;
};

run_probe() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(source_ray = bnrinit(K, [[12, 0; 0, 6], [1, 0]], 1));
  my(values = bnrL1(source_ray, , 6));
  my(target = 0);
  for(index = 1, #values,
    if(Vec(values[index][1]) == [1, 1],
      target = values[index][2][2]);
  );
  if(target == 0, error("source L derivative missing"));

  my(Epol =
    x^8 - 4*x^7 + 20*x^6 - 28*x^5 + 106*x^4
      - 152*x^3 + 152*x^2 + 184*x + 58);
  my(E = bnfinit(Epol, 1));
  my(automorphisms = nfgaloisconj(Epol));
  my(sigma = automorphisms[2]);
  my(tau = automorphisms[3]);
  my(sigma_action = unit_action_matrix(E, Epol, sigma));
  my(tau_action = unit_action_matrix(E, Epol, tau));
  my(anti_lattice = matkerint(matid(#E.fu) + tau_action));
  my(fundamental_resolvents = vector(
    #E.fu,
    column,
    resolvent(E, Epol, sigma, E.fu[column])
  ));
  my(basis_resolvents = vector(
    matsize(anti_lattice)[2],
    column,
    resolvent(
      E,
      Epol,
      sigma,
      prod(index = 1, #E.fu,
        E.fu[index]^anti_lattice[index, column])
    )
  ));
  my(real_matrix = matrix(
    2, #basis_resolvents, row, column,
    if(row == 1,
      real(basis_resolvents[column]),
      imag(basis_resolvents[column])
    )
  ));

  print("SOURCE_CHARACTER=[1,1]");
  print("SOURCE_L_DERIVATIVE=", target);
  print("CHARACTER_FIELD_ROOTS_OF_UNITY=", E.tu[1]);
  print("STARK_ORDINARY_MODULUS_COEFFICIENT=", 2/E.tu[1]);
  print("SIGMA=", sigma);
  print("SIGMA_ACTION=", sigma_action);
  print("TAU=", tau);
  print("TAU_ACTION=", tau_action);
  print("ANTI_UNIT_LATTICE=", anti_lattice);
  print("FUNDAMENTAL_UNIT_RESOLVENTS=", fundamental_resolvents);
  print("ANTI_BASIS_RESOLVENTS=", basis_resolvents);
  print("COORDINATES_FOR_MINUS_TWO_L=", 
    matsolve(real_matrix, [-2*real(target), -2*imag(target)]~));
  print("COORDINATES_FOR_PLUS_TWO_L=", 
    matsolve(real_matrix, [2*real(target), 2*imag(target)]~));
  print("RQ000458_ENGINE_C_UNIT_LATTICE_PROBE_COMPLETE=1");
  print("CLAIM_TAG=NUMERICAL_PROBE_ONLY");
};

run_probe();

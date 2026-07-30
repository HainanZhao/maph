\\ Exact anti-unit lattice exporter for a cyclic quartic CM character
\\ field. Caller supplies CHARACTER_FIELD_POLYNOMIAL.

default(parisizemax, 4000000000);

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
    for(row = 1, rank, answer[row, column] = exponents[row]);
  );
  answer;
};

print_rational_polynomial(label, polynomial) =
{
  my(value = lift(polynomial), degree_value = poldegree(value));
  print(label, "_DEGREE=", degree_value);
  for(index = 0, degree_value,
    my(coefficient = polcoef(value, index));
    print(label, "_COEFF_", index, "=",
      numerator(coefficient), "/", denominator(coefficient));
  );
};

run_export() =
{
  my(polynomial = CHARACTER_FIELD_POLYNOMIAL);
  my(field = bnfinit(polynomial, 1));
  my(automorphisms = nfgaloisconj(polynomial));
  my(candidates = List());
  for(index = 1, #automorphisms,
    my(action =
      unit_action_matrix(field, polynomial, automorphisms[index]));
    if(action^2 != matid(#field.fu) &&
        action^4 == matid(#field.fu),
      listput(candidates, [
        Str(automorphisms[index]), automorphisms[index], action
      ]));
  );
  if(#candidates != 2,
    error(Str("expected inverse order-four pair, got ", #candidates)));
  my(sorted = vecsort(Vec(candidates), 1));
  my(sigma = sorted[1][2], action = sorted[1][3]);
  my(anti_lattice =
    matkerint(matid(#field.fu) + action^2));
  if(matsize(anti_lattice) != [#field.fu, 2],
    error(Str("unexpected anti-lattice shape: ",
      matsize(anti_lattice))));
  my(anti_units = vector(2, column,
    prod(row = 1, #field.fu,
      field.fu[row]^anti_lattice[row, column])));
  my(anti_action = matinverseimage(
    anti_lattice, action * anti_lattice));
  for(index = 1, 2,
    my(tau_image = Mod(subst(
      lift(anti_units[index]), x,
      Mod(subst(sigma, x, sigma), polynomial)), polynomial));
    if(unit_exponents(field, anti_units[index] * tau_image) !=
        vector(#field.fu),
      error(Str("anti-unit identity modulo torsion failed at ", index)));
  );

  print("CHARACTER_FIELD_SIGNATURE=", field.sign);
  print("CHARACTER_FIELD_CLASS_NUMBER=", field.no);
  print("CHARACTER_FIELD_BNFCERTIFY=", bnfcertify(field));
  print("CHARACTER_FIELD_ROOTS_OF_UNITY=", field.tu[1]);
  print("C4_ACTION_MATRIX=", action);
  print("ANTI_UNIT_LATTICE=", anti_lattice);
  print("ANTI_ACTION_11=", anti_action[1, 1]);
  print("ANTI_ACTION_12=", anti_action[1, 2]);
  print("ANTI_ACTION_21=", anti_action[2, 1]);
  print("ANTI_ACTION_22=", anti_action[2, 2]);
  print_rational_polynomial("CHARACTER_FIELD", polynomial);
  print_rational_polynomial("C4_SIGMA", sigma);
  print_rational_polynomial("ANTI_UNIT_1", anti_units[1]);
  print_rational_polynomial("ANTI_UNIT_2", anti_units[2]);
  print("EXACT_ANTI_UNIT_LATTICE_EXPORT_COMPLETE=1");
};

run_export();

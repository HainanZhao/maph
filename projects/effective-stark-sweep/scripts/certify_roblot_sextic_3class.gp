\\ Exact unramified cyclic cubic obstruction for one sextic field.
\\ Caller defines FIELD_KEY and ABSOLUTE_POLYNOMIAL.

default(realprecision, 80);
default(parisizemax, 1500000000);

run_certificate() =
{
  my(field_polynomial = subst(ABSOLUTE_POLYNOMIAL, x, y));
  my(field = bnfinit(field_polynomial, 1));
  my(subgroups = subgrouplist(Vec(field.cyc), [3]));
  my(subgroup, relative, roots, relative_discriminant);
  my(relative_discriminant_norm, cubic_discriminant_square);

  if(#subgroups < 1, error("no candidate index-three subgroup"));
  subgroup = subgroups[1];
  relative = bnrclassfield(field, subgroup, 1);
  if(poldegree(relative) != 3,
    error("candidate class field is not relative cubic"));
  roots = nfroots(field, relative);
  if(#roots != 0, error("candidate relative cubic is reducible"));
  relative_discriminant = rnfdisc(field, relative);
  relative_discriminant_norm =
    idealnorm(field, relative_discriminant[1]);
  if(relative_discriminant_norm != 1,
    error("candidate cubic is ramified at a finite prime"));
  cubic_discriminant_square =
    nfeltissquare(field, poldisc(relative));
  if(!cubic_discriminant_square,
    error("candidate irreducible cubic is not cyclic"));

  print("FIELD_KEY=", FIELD_KEY);
  print("COMPUTED_CLASS_GROUP_CYC=", field.cyc);
  print("INDEX_THREE_SUBGROUP_HNF=", subgroup);
  print("RELATIVE_CUBIC_POLYNOMIAL=", relative);
  print("RELATIVE_CUBIC_ROOT_COUNT_IN_H=", #roots);
  print("RELATIVE_DISCRIMINANT_IDEAL=",
    relative_discriminant[1]);
  print("RELATIVE_DISCRIMINANT_IDEAL_NORM=",
    relative_discriminant_norm);
  print("CUBIC_POLYNOMIAL_DISCRIMINANT_SQUARE=",
    cubic_discriminant_square);
  print("THREE_DIVIDES_CLASS_NUMBER_PROVED=1");
  print("ROBLOT_SEXTIC_3CLASS_CERTIFICATE=PASS");
};

run_certificate();

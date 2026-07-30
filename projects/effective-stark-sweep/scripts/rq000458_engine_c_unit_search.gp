\\ Exact small-unit search in the Q(sqrt(-42)) character field.
\\ Search output is a candidate only; the subsequent orientation and
\\ Stark normalization audit is the certificate.

default(realprecision, 120);
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

run_search() =
{
  my(Epol =
    x^8 - 4*x^7 + 20*x^6 - 28*x^5 + 106*x^4
      - 152*x^3 + 152*x^2 + 184*x + 58);
  my(target =
    x^8 - 40*x^7 + 172*x^6 + 488*x^5 + 694*x^4
      + 488*x^3 + 172*x^2 - 40*x + 1);
  my(E = bnfinit(Epol, 1));
  my(automorphisms = nfgaloisconj(Epol));

  print("CHARACTER_FIELD=", Epol);
  print("SIGNATURE=", E.sign);
  print("CLASS_NUMBER=", E.no);
  print("BNFCERTIFY=", bnfcertify(E));
  print("ROOTS_OF_UNITY=", E.tu[1]);
  print("FUNDAMENTAL_UNITS=", E.fu);
  print("AUTOMORPHISM_COUNT=", #automorphisms);
  for(index = 1, #automorphisms,
    print("AUTOMORPHISM_", index, "=", automorphisms[index]);
    print("UNIT_ACTION_", index, "=",
      unit_action_matrix(E, Epol, automorphisms[index]));
  );

  my(matches = List());
  for(first = -6, 6,
    for(second = -6, 6,
      for(third = -6, 6,
        my(unit =
          E.fu[1]^first * E.fu[2]^second * E.fu[3]^third);
        if(minpoly(unit) == target,
          listput(matches, [first, second, third, unit]));
      );
    );
  );
  print("TARGET_PACKET_ABSOLUTE_POLYNOMIAL=", target);
  print("MATCH_COUNT=", #matches);
  for(index = 1, #matches,
    print("MATCH_", index, "=", matches[index]));
  print("RQ000458_ENGINE_C_UNIT_SEARCH_COMPLETE=1");
  print("CLAIM_TAG=NUMERICAL_SEARCH_EXACTLY_CHECKED");
};

run_search();

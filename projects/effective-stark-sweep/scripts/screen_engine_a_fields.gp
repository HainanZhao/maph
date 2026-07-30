\\ Exact quadratic-field extraction for one nontrivial Engine-A row.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 80);
default(parisizemax, 1000000000);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
};

group_order(cyc) = vecprod(Vec(cyc));

decode_element(code, cyc) =
{
  my(answer = vector(#cyc), q = code);
  for(index = 1, #cyc,
    answer[index] = q % cyc[index];
    q = q \ cyc[index];
  );
  answer;
};

character_order(character, cyc) =
{
  my(answer = 1);
  for(index = 1, #cyc,
    answer = lcm(
      answer,
      cyc[index] / gcd(cyc[index], character[index])
    );
  );
  answer;
};

character_on(character, element, cyc) =
{
  sum(index = 1, #cyc,
    character[index] * element[index] / cyc[index]);
};

character_kernel_hnf(character, cyc) =
{
  my(columns = matdiagonal(cyc));
  for(code = 0, group_order(cyc) - 1,
    my(element = decode_element(code, cyc));
    if(denominator(character_on(character, element, cyc)) == 1,
      columns = concat(columns, element~);
    );
  );
  mathnf(columns);
};

run_screen() =
{
  my(K = bnfinit(field_polynomial(D_VALUE), 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc));
  my(sign_generator = if(H11 <= 2, 1, H11 - 1));
  my(sign_log = Vec(
    bnrisprincipal(ray, idealhnf(K, sign_generator), 0)
  ));
  my(supported = List(), fields = List());

  for(code = 1, group_order(cyc) - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 2
       && denominator(
         character_on(character, sign_log, cyc)
       ) != 1,
      listput(supported, character);
    );
  );
  supported = Vec(supported);
  print("CASE_ID=", CASE_ID);
  print("D=", D_VALUE);
  print("FINITE_NORM=", idealnorm(K, finite_ideal));
  print("RAY_CYC=", cyc);
  print("SIGN_LOG=", sign_log);
  print("SUPPORTED_QUADRATIC_CHARACTER_COUNT=", #supported);
  for(index = 1, #supported,
    my(character = supported[index]);
    my(kernel = character_kernel_hnf(character, cyc));
    my(relative = bnrclassfield(ray, kernel, 1));
    my(absolute = polredbest(rnfpolredbest(K, relative, 2)));
    my(field = bnfinit(absolute, 1));
    if(poldegree(absolute) != 4,
      error("quadratic ray field does not have absolute degree four"));
    print("QUADRATIC_", index, "_CHARACTER=", character);
    print("QUADRATIC_", index, "_KERNEL_HNF=", kernel);
    print("QUADRATIC_", index, "_CONDUCTOR=",
      bnrconductor(ray, character));
    print("QUADRATIC_", index, "_ABSOLUTE_FIELD=", absolute);
    print("QUADRATIC_", index, "_SIGNATURE=", field.sign);
    print("QUADRATIC_", index, "_CLASS_NUMBER=", field.no);
    print("QUADRATIC_", index, "_BNFCERTIFY=", bnfcertify(field));
    listput(fields, absolute);
  );
  print("DISTINCT_QUADRATIC_FIELD_COUNT=", #Set(Vec(fields)));
  print("ENGINE_A_FIELD_EXTRACTION_VERIFIED=1");
};

run_screen();

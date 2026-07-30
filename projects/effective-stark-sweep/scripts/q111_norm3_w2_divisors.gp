\\ Complete Engine-B divisor/exponent table for RQ-004467.
\\ The two-route census derives k=Q(i) and the ray subfield of
\\ conductor (111) with subgroup HNF diag(4,2).

default(realprecision, 100);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_table() =
{
  my(k = bnfinit(z^2 + 1, 1));
  my(conductor = [111, 0; 0, 111]);
  my(full_ray = bnrinit(k, conductor, 1));
  my(factorization = idealfactor(k, conductor));
  my(clearing = List(), w_values = List(), indices = List());
  my(divisor_count = prod(
    index = 1, matsize(factorization)[1],
    factorization[index, 2] + 1
  ));

  assert_equal("SELECTED_IMAGINARY_BASE_BNFCERTIFY",
    bnfcertify(k), 1);
  assert_equal("SELECTED_IMAGINARY_BASE_CLASS_NUMBER", k.no, 1);
  assert_equal("SELECTED_IMAGINARY_RAY_GROUP",
    Vec(full_ray.cyc), [72, 36]);
  assert_equal("SELECTED_CONDUCTOR_FACTORIZATION",
    factorization,
    [[3, [3, 0]~, 1, 2, 1], 1;
     [37, [-6, 1]~, 1, 1, [6, -1; 1, 6]], 1;
     [37, [6, 1]~, 1, 1, [-6, -1; 1, -6]], 1]);
  assert_equal("SHINTANI_DIVISOR_COUNT", divisor_count, 8);

  for(code = 0, divisor_count - 1,
    my(q = code, divisor = matid(2), exponent_vector =
      vector(matsize(factorization)[1]));
    for(index = 1, #exponent_vector,
      exponent_vector[index] = q % 2;
      q = q \ 2;
      if(exponent_vector[index],
        divisor = idealmul(k, divisor, factorization[index, 1]));
    );
    divisor = idealhnf(k, divisor);
    my(divisor_ray = bnrinit(k, divisor, 1));
    my(roots_of_unity = 0);
    for(root_power = 0, k.tu[1] - 1,
      if(nfeltreduce(
          k, k.tu[2]^root_power - 1, divisor
        ) == 0,
        roots_of_unity++;
      );
    );
    my(distribution_index =
      roots_of_unity * full_ray.no / divisor_ray.no);
    my(smallest_integer = divisor[1, 1]);
    my(clearing_exponent = if(
      code == 0,
      12 * k.no * distribution_index,
      12 * smallest_integer * distribution_index
    ));
    listput(clearing, clearing_exponent);
    listput(w_values, roots_of_unity);
    listput(indices, distribution_index);
    print(
      "SHINTANI_DIVISOR_", code,
      "_EXPONENT_VECTOR=", exponent_vector,
      " IDEAL=", divisor,
      " RAY_ORDER=", divisor_ray.no,
      " W=", roots_of_unity,
      " N_INDEX=", distribution_index,
      " F_D=", smallest_integer,
      " CLEARING_EXPONENT=", clearing_exponent
    );
  );
  print("SHINTANI_W_VALUES=", Vec(w_values));
  print("SHINTANI_DISTRIBUTION_INDICES=", Vec(indices));
  print("SHINTANI_CLEARING_EXPONENTS=", Vec(clearing));
  print("SHINTANI_SAFE_EXPONENT=", lcm(Vec(clearing)));
  print("Q111_NORM3_W2_DIVISOR_TABLE_CERTIFIED=1");
};

run_table();

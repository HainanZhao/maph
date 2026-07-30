\\ Complete minimal Engine-B divisor table for RQ-000419.
\\ The two-route census selects k=Q(sqrt(-2)), conductor (7).

default(realprecision, 100);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_table() =
{
  my(k = bnfinit(z^2 + 2, 1));
  my(conductor = [7, 0; 0, 7]);
  my(full_ray = bnrinit(k, conductor, 1));
  my(factorization = idealfactor(k, conductor));
  my(clearing = List(), w_values = List(), indices = List());

  assert_equal("SELECTED_IMAGINARY_BASE_BNFCERTIFY",
    bnfcertify(k), 1);
  assert_equal("SELECTED_IMAGINARY_BASE_CLASS_NUMBER", k.no, 1);
  assert_equal("SELECTED_IMAGINARY_RAY_GROUP",
    Vec(full_ray.cyc), [24]);
  assert_equal("SELECTED_CONDUCTOR_FACTORIZATION",
    factorization, Mat([[7, [7, 0]~, 1, 2, 1], 1]));

  for(exponent = 0, 1,
    my(divisor = if(
      exponent == 0,
      matid(2),
      idealpow(k, factorization[1, 1], exponent)
    ));
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
      exponent == 0,
      12 * k.no * distribution_index,
      12 * smallest_integer * distribution_index
    ));
    listput(clearing, clearing_exponent);
    listput(w_values, roots_of_unity);
    listput(indices, distribution_index);
    print(
      "SHINTANI_DIVISOR_", exponent,
      "_IDEAL=", divisor,
      " RAY_ORDER=", divisor_ray.no,
      " W=", roots_of_unity,
      " N_INDEX=", distribution_index,
      " F_D=", smallest_integer,
      " CLEARING_EXPONENT=", clearing_exponent
    );
  );
  assert_equal("SHINTANI_DIVISOR_COUNT", #clearing, 2);
  assert_equal("SHINTANI_W_VALUES", Vec(w_values), [2, 1]);
  assert_equal("SHINTANI_DISTRIBUTION_INDICES",
    Vec(indices), [48, 1]);
  assert_equal("SHINTANI_CLEARING_EXPONENTS",
    Vec(clearing), [576, 84]);
  assert_equal("SHINTANI_SAFE_EXPONENT",
    lcm(Vec(clearing)), 4032);
  print("Q14_P7_W2_DIVISOR_TABLE_CERTIFIED=1");
};

run_table();

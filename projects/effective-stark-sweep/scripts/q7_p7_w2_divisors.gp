\\ Complete Shintani divisor/exponent table for the selected minimal
\\ W2 base k=Q(i).  The two-route script proves independently that its
\\ ray field of conductor (7) is the required normal closure.

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
  my(conductor = [7, 0; 0, 7]);
  my(full_ray = bnrinit(k, conductor, 1));
  my(factorization = idealfactor(k, conductor));
  my(clearing = List(), w_values = List());
  my(K = bnfinit(y^2 - 7, 1));
  my(real_finite = [7, 0; 0, 1]);
  my(real_full = bnrinit(K, [real_finite, [1, 1]], 1));
  my(real_indices = List());

  assert_equal("SELECTED_IMAGINARY_BASE_BNFCERTIFY",
    bnfcertify(k), 1);
  assert_equal("SELECTED_IMAGINARY_BASE_CLASS_NUMBER", k.no, 1);
  assert_equal("SELECTED_IMAGINARY_RAY_GROUP",
    Vec(full_ray.cyc), [12]);
  assert_equal("SELECTED_CONDUCTOR_PRIME_COUNT",
    matsize(factorization)[1], 1);

  for(exponent = 0, factorization[1, 2],
    my(divisor = if(
      exponent == 0,
      matid(2),
      idealpow(k, factorization[1, 1], exponent)
    ));
    my(divisor_ray, roots_of_unity = 0);
    my(distribution_index, smallest_integer, clearing_exponent);
    divisor = idealhnf(k, divisor);
    divisor_ray = bnrinit(k, divisor, 1);
    for(root_power = 0, k.tu[1] - 1,
      if(nfeltreduce(
          k, k.tu[2]^root_power - 1, divisor
        ) == 0,
        roots_of_unity++
      )
    );
    distribution_index =
      roots_of_unity * full_ray.no / divisor_ray.no;
    smallest_integer = divisor[1, 1];
    clearing_exponent = if(
      exponent == 0,
      12 * k.no * distribution_index,
      12 * smallest_integer * distribution_index
    );
    listput(clearing, clearing_exponent);
    listput(w_values, roots_of_unity);
    print(
      "SHINTANI_DIVISOR_", exponent,
      "_IDEAL=", divisor,
      " RAY_ORDER=", divisor_ray.no,
      " W=", roots_of_unity,
      " N_INDEX=", distribution_index,
      " CLEARING_EXPONENT=", clearing_exponent
    );
  );
  assert_equal("SHINTANI_DIVISOR_COUNT", #clearing, 2);
  assert_equal("SHINTANI_W_VALUES", Vec(w_values), [4, 1]);
  assert_equal("SHINTANI_SAFE_EXPONENT",
    lcm(Vec(clearing)), 4032);

  \\ Audit every divisor obtained by deleting finite prime support on
  \\ the real side.  The lcm must already divide the safe exponent.
  for(keep_prime = 0, 1,
    my(divisor = if(keep_prime, real_finite, matid(2)));
    my(subray = bnrinit(K, [divisor, [1, 1]], 1));
    my(index_value = real_full.no / subray.no);
    listput(real_indices, index_value);
    print("REAL_DISTRIBUTION_", keep_prime,
      "_IDEAL=", divisor,
      " RAY_ORDER=", subray.no,
      " INDEX=", index_value);
  );
  print("REAL_DISTRIBUTION_INDICES=", Vec(real_indices));
  assert_equal("REAL_DISTRIBUTION_DENOMINATORS_CLEARED",
    4032 % lcm(Vec(real_indices)) == 0, 1);
  print("Q7_P7_W2_DIVISOR_TABLE_CERTIFIED=1");
};

run_table();

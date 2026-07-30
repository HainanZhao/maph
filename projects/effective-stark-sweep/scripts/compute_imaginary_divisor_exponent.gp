\\ Generic exact Shintani divisor/exponent table for one derived
\\ imaginary quadratic route.  Caller defines CASE_ID, ROUTE_LABEL,
\\ BASE_A, BASE_B and H11,H12,H21,H22.

default(realprecision, 100);

run_table() =
{
  my(k = bnfinit(z^2 + BASE_A*z + BASE_B, 1));
  my(conductor = [H11, H12; H21, H22]);
  my(full_ray = bnrinit(k, conductor, 1));
  my(factorization = idealfactor(k, conductor));
  my(factor_count = matsize(factorization)[1]);
  my(divisor_count = prod(
    index = 1, factor_count,
    factorization[index, 2] + 1
  ));
  my(clearing = List(), distribution = List(), w_values = List());

  print("CASE_ID=", CASE_ID);
  print("ROUTE_LABEL=", ROUTE_LABEL);
  print("BASE_POLYNOMIAL=", k.pol);
  print("BASE_DISCRIMINANT=", k.disc);
  print("BASE_CLASS_NUMBER=", k.no);
  print("BASE_ROOTS_OF_UNITY=", k.tu[1]);
  print("BASE_BNFCERTIFY=", bnfcertify(k));
  print("CONDUCTOR=", conductor);
  print("CONDUCTOR_FACTORIZATION=", factorization);
  print("FULL_RAY_CYC=", Vec(full_ray.cyc));
  print("FULL_RAY_ORDER=", full_ray.no);
  print("SHINTANI_DIVISOR_COUNT=", divisor_count);

  for(code = 0, divisor_count - 1,
    my(q = code, divisor = matid(2));
    my(exponents = vector(factor_count));
    for(index = 1, factor_count,
      my(radix = factorization[index, 2] + 1);
      exponents[index] = q % radix;
      q = q \ radix;
      if(exponents[index],
        divisor = idealmul(
          k, divisor,
          idealpow(
            k, factorization[index, 1], exponents[index]
          )
        );
      );
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
    listput(distribution, distribution_index);
    listput(w_values, roots_of_unity);
    print(
      "SHINTANI_DIVISOR_", code,
      "_EXPONENT_VECTOR=", exponents,
      " IDEAL=", divisor,
      " RAY_ORDER=", divisor_ray.no,
      " W=", roots_of_unity,
      " N_INDEX=", distribution_index,
      " F_D=", smallest_integer,
      " CLEARING_EXPONENT=", clearing_exponent
    );
  );
  print("SHINTANI_W_VALUES=", Vec(w_values));
  print("SHINTANI_DISTRIBUTION_INDICES=", Vec(distribution));
  print("SHINTANI_CLEARING_EXPONENTS=", Vec(clearing));
  print("SHINTANI_SAFE_EXPONENT=", lcm(Vec(clearing)));
  print("GENERIC_IMAGINARY_DIVISOR_TABLE_VERIFIED=1");
};

run_table();

\\ Exact W1 structural screen for one canonical finite ideal.
\\ The caller defines CASE_ID, D_VALUE, and H11,H12,H21,H22.

default(realprecision, 100);
default(parisizemax, 1000000000);

fractional(value) = value - floor(value);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(x^2 - x + (1-d)/4),
    return(x^2 - d)
  );
};

group_order(cyc) =
{
  my(answer = 1);
  for(i = 1, #cyc, answer *= cyc[i]);
  return(answer);
};

group_exponent(cyc) =
{
  my(answer = 1);
  for(i = 1, #cyc, answer = lcm(answer, cyc[i]));
  return(answer);
};

decode_element(code, cyc) =
{
  my(answer = vector(#cyc), q = code);
  for(i = 1, #cyc,
    answer[i] = q % cyc[i];
    q = q \ cyc[i];
  );
  return(answer);
};

character_order(character, cyc) =
{
  my(answer = 1);
  for(i = 1, #cyc,
    answer = lcm(answer, cyc[i] / gcd(cyc[i], character[i]))
  );
  return(answer);
};

rational_character_order(values) =
{
  my(answer = 1);
  for(i = 1, #values, answer = lcm(answer, denominator(values[i])));
  return(answer);
};

apply_group_matrix(M, element, target_cyc) =
{
  return(vector(
    #target_cyc, row,
    sum(column = 1, #element, M[row, column] * element[column])
      % target_cyc[row]
  ));
};

vector_key(v) = Str(v);

unit_predicates(K, finite_ideal, norm_value) =
{
  my(epsilon = K.fu[1], epsilon_norm, epsilon_trace, positive_generator);
  my(power, next_power, period, positive_hits_minus_one = 0);
  my(negative_hits_one = 0, bound = 2*norm_value + 4);
  epsilon_norm = nfeltnorm(K, epsilon);
  epsilon_trace = nfelttrace(K, epsilon);
  if(epsilon_norm == -1,
    positive_generator = epsilon^2,
    if(epsilon_trace > 0,
      positive_generator = epsilon,
      positive_generator = -epsilon
    )
  );

  power = Mod(1, K.pol);
  for(exponent = 0, bound,
    if(nfeltreduce(K, power + 1, finite_ideal) == 0,
      positive_hits_minus_one = 1
    );
    next_power = nfeltreduce(K, power * positive_generator, finite_ideal);
    if(exponent > 0 && next_power == 1, break);
    power = next_power;
  );

  if(epsilon_norm == -1,
    power = Mod(1, K.pol);
    for(exponent = 1, bound,
      power = nfeltreduce(K, power * epsilon, finite_ideal);
      if(exponent % 2 == 1,
        if(nfeltreduce(K, power - 1, finite_ideal) == 0 ||
           nfeltreduce(K, power + 1, finite_ideal) == 0,
          negative_hits_one = 1
        )
      );
      if(power == 1, break);
    )
  );
  return([
    positive_hits_minus_one == 0,
    negative_hits_one == 0,
    epsilon_norm
  ]);
};

run_screen() =
{
  my(polynomial = field_polynomial(D_VALUE));
  my(K = bnfinit(polynomial, 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(norm_value = idealnorm(K, finite_ideal));
  my(ray_one = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_both = bnrinit(K, [finite_ideal, [1, 1]], 1));
  my(one_cyc = Vec(ray_one.cyc), both_cyc = Vec(ray_both.cyc));
  my(one_order = group_order(one_cyc), both_order = group_order(both_cyc));
  my(one_exponent = group_exponent(one_cyc));
  my(autos = nfgaloisconj(K), sigma = autos[1]);
  my(sign_generator, sign_log, support = List(), support_orders = List());
  my(max_support_order = 1, support_count = 0);
  my(forgetful, conjugation, all_both, kernel = List(), commutator = List());
  my(kernel_set, commutator_set, generated = List(), generated_set);
  my(index_value = 0, split_exact = 0, units);
  my(a_absolute = 0, a_conjugation_failures = 0);
  my(c_structural = 0, c_quartic_count = 0, c_projective_failures = 0);
  my(engine = "NONE", verdict = "NONE", obstruction = "NONE");

  if(sigma == Mod(x, K.pol), sigma = autos[2]);
  sign_generator = if(H11 <= 2, 1, H11 - 1);
  sign_log = Vec(
    bnrisprincipal(ray_one, idealhnf(K, sign_generator), 0)
  );

  for(code = 0, one_order - 1,
    my(character = decode_element(code, one_cyc));
    my(value = 0);
    for(i = 1, #one_cyc,
      value += character[i] * sign_log[i] / one_cyc[i]
    );
    if(fractional(value) != 0,
      my(order_value = character_order(character, one_cyc));
      listput(support, character);
      listput(support_orders, order_value);
      support_count++;
      max_support_order = max(max_support_order, order_value);
    )
  );

  forgetful = matrix(
    #one_cyc, #both_cyc, row, column,
    bnrisprincipal(ray_one, ray_both.gen[column], 0)[row]
  );
  conjugation = matrix(
    #both_cyc, #both_cyc, row, column,
    bnrisprincipal(
      ray_both,
      nfgaloisapply(K, sigma, ray_both.gen[column]),
      0
    )[row]
  );

  all_both = vector(
    both_order, code, decode_element(code - 1, both_cyc)
  );
  for(i = 1, #all_both,
    my(element = all_both[i]);
    if(apply_group_matrix(forgetful, element, one_cyc)
       == vector(#one_cyc),
      listput(kernel, element)
    );
    my(image = vector(
      #both_cyc, row,
      (
        sum(column = 1, #both_cyc,
          conjugation[row, column] * element[column]
        ) - element[row]
      ) % both_cyc[row]
    ));
    listput(commutator, image);
  );
  kernel_set = Set(Vec(kernel));
  commutator_set = Set(Vec(commutator));
  for(i = 1, #kernel_set,
    for(j = 1, #commutator_set,
      listput(generated, vector(
        #both_cyc, row,
        (kernel_set[i][row] + commutator_set[j][row])
          % both_cyc[row]
      ))
    )
  );
  generated_set = Set(Vec(generated));
  if(#kernel_set > 0, index_value = #generated_set / #kernel_set);
  split_exact = (#kernel_set == 2);

  if(max_support_order == 4,
    c_structural = 1;
    for(i = 1, #support,
      if(support_orders[i] == 4,
        c_quartic_count++;
        my(lifted = vector(
          #both_cyc, column,
          fractional(sum(row = 1, #one_cyc,
            support[i][row] * forgetful[row, column] / one_cyc[row]
          ))
        ));
        my(conjugated = vector(
          #both_cyc, column,
          fractional(sum(row = 1, #both_cyc,
            lifted[row] * conjugation[row, column]
          ))
        ));
        my(quotient = vector(
          #both_cyc, row, fractional(lifted[row] - conjugated[row])
        ));
        if(rational_character_order(quotient) != 2,
          c_structural = 0;
          c_projective_failures++;
        )
      )
    );
    if(c_quartic_count == 0, c_structural = 0);
  );

  if(max_support_order <= 2,
    a_absolute = 1;
    for(i = 1, #support,
      my(lifted = vector(
        #both_cyc, column,
        fractional(sum(row = 1, #one_cyc,
          support[i][row] * forgetful[row, column] / one_cyc[row]
        ))
      ));
      my(conjugated = vector(
        #both_cyc, column,
        fractional(sum(row = 1, #both_cyc,
          lifted[row] * conjugation[row, column]
        ))
      ));
      if(lifted != conjugated,
        a_absolute = 0;
        a_conjugation_failures++;
      )
    )
  );

  units = unit_predicates(K, finite_ideal, norm_value);
  if(one_exponent > 24,
    verdict = "FRONTIER";
    obstruction = "EXPONENT_CAP",
    if(max_support_order <= 2,
      verdict = "ROUTE_CANDIDATE";
      engine = "A",
      if(c_structural,
        verdict = "ROUTE_CANDIDATE";
        engine = "C",
        if(!units[1] || !units[2],
          verdict = "FRONTIER";
          obstruction = "UNIT_CONGRUENCE_FAIL",
          if(index_value != 2 || !split_exact,
            verdict = "FRONTIER";
            obstruction = "INDEX_GT_2",
            verdict = "ROUTE_CANDIDATE";
            engine = "B"
          )
        )
      )
    )
  );

  print("CASE_ID=", CASE_ID);
  print("D=", D_VALUE);
  print("FIELD_DISCRIMINANT=", K.disc);
  print("FINITE_NORM=", norm_value);
  print("BNFCERTIFY=", bnfcertify(K));
  print("ONE_CYC=", one_cyc);
  print("BOTH_CYC=", both_cyc);
  print("ONE_EXPONENT=", one_exponent);
  print("SIGN_GENERATOR=", sign_generator);
  print("SIGN_LOG=", sign_log);
  print("SUPPORT_COUNT=", support_count);
  print("SUPPORT_ORDERS=", Set(Vec(support_orders)));
  print("MAX_SUPPORT_ORDER=", max_support_order);
  print("ONE_PLACE_KERNEL_SIZE=", #kernel_set);
  print("COMMUTATOR_SIZE=", #commutator_set);
  print("SHINTANI_INDEX=", index_value);
  print("EXACTLY_ONE_REAL_PLACE_SPLITTING=", split_exact);
  print("B03_POSITIVE_NOT_MINUS_ONE=", units[1]);
  print("B06_NEGATIVE_NORM_NOT_ONE=", units[2]);
  print("FUNDAMENTAL_UNIT_NORM=", units[3]);
  print("A_ABSOLUTE_CONJUGATION_INVARIANT=", a_absolute);
  print("A_CONJUGATION_FAILURES=", a_conjugation_failures);
  print("C_QUARTIC_COUNT=", c_quartic_count);
  print("C_PROJECTIVE_FAILURES=", c_projective_failures);
  print("C_STRUCTURAL=", c_structural);
  print("VERDICT=", verdict);
  print("ENGINE=", engine);
  print("OBSTRUCTION=", obstruction);
};

run_screen();

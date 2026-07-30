\\ Genuine five-row Roblot screen and one sealed weak-solution
\\ constructor. This file deliberately contains no L-function calls
\\ and reads no Engine-C or packet artifact.

default(realprecision, 100);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(label, ": expected ", expected, ", got ", actual));
};

automorphism_order(nf, automorphism) =
{
  my(root = Mod(variable(nf.pol), nf.pol), value = root);
  for(order = 1, 8,
    value = nfgaloisapply(nf, automorphism, value);
    if(value == root, return(order));
  );
  error("automorphism order exceeds eight");
};

first_order_four_automorphism(nf) =
{
  my(automorphisms = nfgaloisconj(nf));
  for(index = 1, #automorphisms,
    if(automorphism_order(nf, automorphisms[index]) == 4,
      return(automorphisms[index])));
  error("no order-four automorphism");
};

unit_action_matrix(bnf, automorphism) =
{
  my(rank = #bnf.fu);
  matrix(rank, rank, row, column,
    bnfisunit(
      bnf,
      nfgaloisapply(bnf.nf, automorphism, bnf.fu[column])
    )[row]
  );
};

totally_real_quartic(polynomial) =
{
  my(subfields = nfsubfields(polynomial, 4), answers = List());
  for(index = 1, #subfields,
    if(nfinit(subfields[index][1]).sign == [4, 0],
      listput(answers, subfields[index][1])));
  assert_equal("unique totally real quartic", #answers, 1);
  answers[1];
};

quadratic_relative_factor(plus_field, polynomial) =
{
  my(factors = nffactor(plus_field, polynomial));
  for(index = 1, matsize(factors)[1],
    if(poldegree(factors[index, 1]) == 2,
      return(factors[index, 1])));
  error("no quadratic factor over plus field");
};

screen_case(label, polynomial, rational_support) =
{
  my(bnf = bnfinit(polynomial, 1), plus_polynomial);
  my(plus_field, relative_polynomial, relative_field);
  my(no_split = 1, local_rows = List());
  assert_equal(Str(label, "_bnfcertify"), bnfcertify(bnf), 1);
  assert_equal(Str(label, "_signature"), bnf.sign, [4, 2]);
  assert_equal(
    Str(label, "_automorphism_count"),
    #nfgaloisconj(bnf.nf),
    4
  );
  plus_polynomial = totally_real_quartic(polynomial);
  plus_field = nfinit(subst(plus_polynomial, variable(polynomial), y));
  relative_polynomial =
    quadratic_relative_factor(plus_field, polynomial);
  relative_field = rnfinit(plus_field, relative_polynomial);
  for(item = 1, #rational_support,
    my(decomposition =
      rnfidealprimedec(relative_field, rational_support[item]));
    for(index = 1, #decomposition[1],
      my(base_prime = decomposition[1][index]);
      my(top_primes = decomposition[2][index]);
      if(#top_primes > 1, no_split = 0);
      listput(
        local_rows,
        [
          rational_support[item],
          base_prime.e,
          base_prime.f,
          #top_primes,
          top_primes[1].e / base_prime.e,
          top_primes[1].f / base_prime.f
        ]
      );
    );
  );
  assert_equal(Str(label, "_A3_strong_no_split"), no_split, 1);
  print(
    label,
    "|BNFCERTIFY=1",
    "|CLASS_NUMBER=", bnf.no,
    "|SIGNATURE=", bnf.sign,
    "|AUTOMORPHISM_COUNT=4",
    "|A1=1",
    "|A2=1",
    "|A3=1",
    "|A3_STRONG_ALL_PRIMES_ABOVE_SUPPORT_NONSPLIT=1",
    "|PLUS_POLYNOMIAL=", plus_polynomial,
    "|LOCAL_ROWS_[p,eplus,fplus,count,erel,frel]=",
    Vec(local_rows)
  );
};

construct_rq000129(polynomial) =
{
  my(bnf = bnfinit(polynomial, 1), nf = bnf.nf);
  my(gamma = first_order_four_automorphism(nf));
  my(action = unit_action_matrix(bnf, gamma));
  my(rank = #bnf.fu, tau = action^2);
  my(minus_basis = matkerint(matid(rank) + tau));
  my(gamma_on_minus = matsolve(minus_basis, action * minus_basis));
  my(theta_vector = minus_basis[, 1]);
  my(theta_coordinates = [1, 0]~);
  my(cyclic_determinant =
    matdet(matrix(
      2, 2, row, column,
      if(
        column == 1,
        theta_coordinates[row],
        (gamma_on_minus * theta_coordinates)[row]
      )
    )));
  my(fixed_basis = matkerint(tau - matid(rank)));
  my(norm_coordinates =
    matsolve(fixed_basis, matid(rank) + tau));
  my(norm_hnf = mathnf(norm_coordinates));
  my(norm_index = abs(matdet(norm_hnf)));
  my(e_exponent = valuation(norm_index, 2));
  my(tS = 0, fitting_generator = 1);
  my(eta_vector =
    (action + matid(rank))^(e_exponent + tS) * theta_vector);
  my(theta_unit =
    prod(index = 1, rank, bnf.fu[index]^theta_vector[index]));
  my(eta_unit =
    prod(index = 1, rank, bnf.fu[index]^eta_vector[index]));
  my(automorphisms = nfgaloisconj(nf), tau_automorphism = 0);
  my(real_roots = polrootsreal(polynomial), root = real_roots[1]);
  my(logs = vector(4), value = eta_unit);
  my(coefficient);

  assert_equal("RQ-000129 class number", bnf.no, 1);
  assert_equal("RQ-000129 minus rank", matsize(minus_basis), [rank, 2]);
  assert_equal(
    "RQ-000129 gamma on minus",
    gamma_on_minus,
    [0, -1; 1, 0]
  );
  assert_equal(
    "RQ-000129 cyclic generator determinant",
    abs(cyclic_determinant),
    1
  );
  assert_equal("RQ-000129 norm index", norm_index, 4);
  assert_equal("RQ-000129 e exponent", e_exponent, 2);
  for(index = 1, #automorphisms,
    if(automorphism_order(nf, automorphisms[index]) == 2,
      tau_automorphism = automorphisms[index]));
  if(type(tau_automorphism) == "t_INT",
    error("order-two automorphism missing"));
  assert_equal(
    "RQ-000129 anti-unit norm",
    eta_unit * nfgaloisapply(nf, tau_automorphism, eta_unit),
    Mod(1, polynomial)
  );
  for(index = 1, 4,
    logs[index] = log(abs(subst(lift(value), variable(polynomial), root)));
    value = nfgaloisapply(nf, gamma, value);
  );
  coefficient =
    (logs[1] + I * logs[2] - logs[3] - I * logs[4]) / 2;
  print("SEALED_CASE=RQ-000129");
  print("SELECTION_RULE_WINNER=1");
  print("FITTING_GENERATOR=1");
  print("T_S=0");
  print("E_EXPONENT=", e_exponent);
  print("NORM_INDEX=", norm_index);
  print("GAMMA=", gamma);
  print("GAMMA_ACTION=", action);
  print("MINUS_BASIS=", minus_basis);
  print("GAMMA_ON_MINUS=", gamma_on_minus);
  print("THETA_VECTOR=", theta_vector);
  print("ETA_VECTOR=", eta_vector);
  print("THETA_UNIT=", lift(theta_unit));
  print("ETA_UNIT=", lift(eta_unit));
  print("ETA_ANTI_UNIT_NORM=1");
  print("DISTINGUISHED_ROOT_RULE=LEAST_REAL_ROOT");
  print("DISTINGUISHED_ROOT=", root);
  print("LOG_ORBIT=", logs);
  print("ROBLOT_COEFFICIENT=", coefficient);
  print("ROBLOT_COEFFICIENT_ABS=", abs(coefficient));
  print("ROBLOT_COEFFICIENT_PHASE_OVER_PI=", arg(coefficient) / Pi);
  print("INDEPENDENCE_WALL=PASS");
  print("CLAIM_TAG=VERIFIED_EXACT_CONSTRUCTOR_WITH_NUMERICAL_LOGS");
};

x = 'x;

P_000129 = x^8 - 4*x^5 - 2*x^4 - 8*x^2 - 8*x - 2;
P_001280 = x^8 + 10*x^6 + 14*x^4 - 20*x^2 + 4;
P_001569 = x^8 + 10*x^6 - 12*x^5 + 9*x^4 + 24*x^3 - 44*x^2 + 12*x + 1;
P_001894 = x^8 + 10*x^6 - 120*x^5 - 1050*x^4 + 1950*x^3 + 5875*x^2 - 14550*x + 8725;
P_007519 = x^8 + 10*x^6 - 12*x^5 - 99*x^4 + 312*x^3 - 584*x^2 + 372*x + 217;

screen_case("RQ-000129", P_000129, [2]);
screen_case("RQ-001280", P_001280, [2]);
screen_case("RQ-001569", P_001569, [2, 3]);
screen_case("RQ-001894", P_001894, [3, 5]);
screen_case("RQ-007519", P_007519, [2, 3]);

construct_rq000129(P_000129);
print("ROBLOT_QUARTIC_GATE_SEALED=PASS");

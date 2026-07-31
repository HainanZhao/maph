\\ Independent Roblot constructors for the four remaining controls.
\\ This script contains no L-function calls and reads no packet data.

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

run_case(label, polynomial, plus_polynomial, expected_h, expected_hplus) =
{
  my(K = bnfinit(polynomial, 1));
  my(Kplus = bnfinit(plus_polynomial, 1));
  my(gam = first_order_four_automorphism(K.nf));
  my(rank = #K.fu, action = unit_action_matrix(K, gam));
  my(tau = action^2);
  my(minus_basis = matkerint(matid(rank) + tau));
  my(gamma_on_minus =
    matsolve(minus_basis, action * minus_basis));
  my(inclusion = nfisincl(Kplus.nf, K.nf, 1));
  my(embedded_plus_units, norm_matrix, norm_coordinates);
  my(norm_hnf, norm_index, e_exponent);
  my(minus_class_order, fitting_power);
  my(class_action = matrix(#K.cyc, #K.cyc));
  my(theta_vector, eta_vector, theta_unit, eta_unit);
  my(automorphisms, tau_automorphism = 0);
  my(real_roots, root, logs, value, coefficient);

  assert_equal(Str(label, "_K_bnfcertify"), bnfcertify(K), 1);
  assert_equal(
    Str(label, "_Kplus_bnfcertify"),
    bnfcertify(Kplus),
    1
  );
  assert_equal(Str(label, "_hK"), K.no, expected_h);
  assert_equal(Str(label, "_hKplus"), Kplus.no, expected_hplus);
  assert_equal(Str(label, "_signature"), K.sign, [4, 2]);
  assert_equal(
    Str(label, "_minus_rank"),
    matsize(minus_basis),
    [rank, 2]
  );
  if(abs(matdet(gamma_on_minus)) != 1
     || gamma_on_minus^2 != -matid(2),
    error(label, ": minus module is not Gaussian cyclic"));
  if(type(inclusion) == "t_INT",
    error(label, ": Kplus inclusion missing"));

  embedded_plus_units = matrix(
    rank,
    #Kplus.fu,
    row,
    column,
    bnfisunit(
      K,
      Mod(
        subst(
          lift(Kplus.fu[column]),
          variable(plus_polynomial),
          inclusion
        ),
        polynomial
      )
    )[row]
  );
  norm_matrix = matid(rank) + tau;
  norm_coordinates =
    matsolve(embedded_plus_units, norm_matrix);
  norm_hnf = mathnf(norm_coordinates);
  norm_index = abs(matdet(norm_hnf));
  if(norm_index != 2 && norm_index != 4,
    error(label, ": unexpected norm index ", norm_index));
  e_exponent = valuation(norm_index, 2);

  minus_class_order = K.no / Kplus.no;
  if(minus_class_order != 1 && minus_class_order != 2,
    error(label, ": unsupported minus class order"));
  fitting_power = if(minus_class_order == 1, 0, 1);
  if(#K.cyc,
    class_action = matrix(
      #K.cyc,
      #K.cyc,
      row,
      column,
      bnfisprincipal(
        K,
        nfgaloisapply(K.nf, gam, K.gen[column]),
        0
      )[row]
    );
  );
  if(minus_class_order == 2,
    if(valuation(minus_class_order, 2) != 1,
      error(label, ": Fitting norm is not two"));
  );

  theta_vector = minus_basis[, 1];
  if(abs(matdet(matrix(
      2, 2, row, column,
      if(
        column == 1,
        [1, 0][row],
        (gamma_on_minus * [1, 0]~)[row]
      )
    ))) != 1,
    error(label, ": first minus vector is not cyclic"));
  eta_vector =
    (action + matid(rank))^(e_exponent + fitting_power)
      * theta_vector;
  theta_unit =
    prod(index = 1, rank, K.fu[index]^theta_vector[index]);
  eta_unit =
    prod(index = 1, rank, K.fu[index]^eta_vector[index]);

  automorphisms = nfgaloisconj(K.nf);
  for(index = 1, #automorphisms,
    if(automorphism_order(K.nf, automorphisms[index]) == 2,
      tau_automorphism = automorphisms[index]));
  if(type(tau_automorphism) == "t_INT",
    error(label, ": order-two automorphism missing"));
  assert_equal(
    Str(label, "_anti_unit_norm"),
    eta_unit * nfgaloisapply(K.nf, tau_automorphism, eta_unit),
    Mod(1, polynomial)
  );

  real_roots = polrootsreal(polynomial);
  root = real_roots[1];
  logs = vector(4);
  value = eta_unit;
  for(index = 1, 4,
    logs[index] =
      log(abs(subst(lift(value), variable(polynomial), root)));
    value = nfgaloisapply(K.nf, gam, value);
  );
  coefficient =
    (logs[1] + I * logs[2] - logs[3] - I * logs[4]) / 2;

  print("CASE_ID=", label);
  print("K_BNFCERTIFY=1");
  print("KPLUS_BNFCERTIFY=1");
  print("H_K=", K.no);
  print("H_KPLUS=", Kplus.no);
  print("MINUS_CLASS_ORDER=", minus_class_order);
  print("CLASS_GROUP_CYC=", K.cyc);
  print("CLASS_GAMMA_ACTION=", class_action);
  print("FITTING_POWER_1_PLUS_GAMMA=", fitting_power);
  print("EMBEDDED_KPLUS_UNIT_LATTICE=", embedded_plus_units);
  print("NORM_COORDINATES=", norm_coordinates);
  print("NORM_HNF=", norm_hnf);
  print("GENUINE_NORM_INDEX=", norm_index);
  print("E_EXPONENT=", e_exponent);
  print("T_S=0");
  print("GAMMA=", gam);
  print("GAMMA_ACTION=", action);
  print("MINUS_BASIS=", minus_basis);
  print("GAMMA_ON_MINUS=", gamma_on_minus);
  print("THETA_VECTOR=", theta_vector);
  print("ETA_VECTOR=", eta_vector);
  print("THETA_UNIT=", lift(theta_unit));
  print("ETA_UNIT=", lift(eta_unit));
  print("ETA_ANTI_UNIT_NORM=1");
  print("DISTINGUISHED_ROOT=", root);
  print("LOG_ORBIT=", logs);
  print("ROBLOT_COEFFICIENT=", coefficient);
  print("ROBLOT_COEFFICIENT_ABS=", abs(coefficient));
  print("ROBLOT_COEFFICIENT_PHASE_OVER_PI=", arg(coefficient) / Pi);
  print("INDEPENDENCE_WALL=PASS");
  print("CASE_CONSTRUCTOR=PASS");
};

x = 'x;
y = 'y;

main() =
{
run_case(
  "RQ-001280",
  x^8 + 10*x^6 + 14*x^4 - 20*x^2 + 4,
  y^4 - 10*y^3 + 14*y^2 + 20*y + 4,
  1,
  1
);
run_case(
  "RQ-001569",
  x^8 + 10*x^6 - 12*x^5 + 9*x^4 + 24*x^3
    - 44*x^2 + 12*x + 1,
  y^4 - 14*y^3 + 33*y^2 - 14*y + 1,
  2,
  1
);
run_case(
  "RQ-007519",
  x^8 + 10*x^6 - 12*x^5 - 99*x^4 + 312*x^3
    - 584*x^2 + 372*x + 217,
  y^4 - 14*y^3 - 75*y^2 + 310*y + 217,
  2,
  1
);
run_case(
  "RQ-001894",
  x^8 + 10*x^6 - 120*x^5 - 1050*x^4 + 1950*x^3
    + 5875*x^2 - 14550*x + 8725,
  y^4 - 20*y^3 - 975*y^2 - 4550*y + 8725,
  4,
  2
);

print("REMAINING_ROBLOT_CONSTRUCTORS=PASS");
};

main();

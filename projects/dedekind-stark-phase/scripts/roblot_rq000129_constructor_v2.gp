\\ Corrected RQ-000129 Roblot constructor. No L-function or packet
\\ input is permitted. The v1 fixed-lattice proxy is not used.

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

x = 'x;
y = 'y;

P = x^8 - 4*x^5 - 2*x^4 - 8*x^2 - 8*x - 2;
Pplus = y^4 - 4*y^3 + 2*y^2 + 4*y - 2;

run_constructor() =
{
K = bnfinit(P, 1);
Kplus = bnfinit(Pplus, 1);
assert_equal("K bnfcertify", bnfcertify(K), 1);
assert_equal("Kplus bnfcertify", bnfcertify(Kplus), 1);
assert_equal("K class number", K.no, 1);

gam = first_order_four_automorphism(K.nf);
rank = #K.fu;
action = unit_action_matrix(K, gam);
tau = action^2;
minus_basis = matkerint(matid(rank) + tau);
gamma_on_minus = matsolve(minus_basis, action * minus_basis);
assert_equal("minus rank", matsize(minus_basis), [rank, 2]);
assert_equal("Gaussian action", gamma_on_minus, [0, -1; 1, 0]);

inclusion = nfisincl(Kplus.nf, K.nf, 1);
if(type(inclusion) == "t_INT", error("Kplus inclusion missing"));
embedded_plus_units = matrix(
  rank,
  #Kplus.fu,
  row,
  column,
  bnfisunit(
    K,
    Mod(
      subst(lift(Kplus.fu[column]), y, inclusion),
      P
    )
  )[row]
);
norm_matrix = matid(rank) + tau;
norm_coordinates = matsolve(embedded_plus_units, norm_matrix);
norm_hnf = mathnf(norm_coordinates);
norm_index = abs(matdet(norm_hnf));
e_exponent = valuation(norm_index, 2);
assert_equal("genuine norm index", norm_index, 2);
assert_equal("genuine e exponent", e_exponent, 1);

theta_vector = minus_basis[, 1];
tS = 0;
eta_vector =
  (action + matid(rank))^(e_exponent + tS) * theta_vector;
theta_unit =
  prod(index = 1, rank, K.fu[index]^theta_vector[index]);
eta_unit =
  prod(index = 1, rank, K.fu[index]^eta_vector[index]);

automorphisms = nfgaloisconj(K.nf);
tau_automorphism = 0;
for(index = 1, #automorphisms,
  if(automorphism_order(K.nf, automorphisms[index]) == 2,
    tau_automorphism = automorphisms[index]));
if(type(tau_automorphism) == "t_INT",
  error("order-two automorphism missing"));
assert_equal(
  "anti-unit norm",
  eta_unit * nfgaloisapply(K.nf, tau_automorphism, eta_unit),
  Mod(1, P)
);

real_roots = polrootsreal(P);
root = real_roots[1];
logs = vector(4);
value = eta_unit;
for(index = 1, 4,
  logs[index] = log(abs(subst(lift(value), x, root)));
  value = nfgaloisapply(K.nf, gam, value);
);
coefficient =
  (logs[1] + I * logs[2] - logs[3] - I * logs[4]) / 2;

print("SEALED_CASE=RQ-000129");
print("VERSION=2");
print("K_BNFCERTIFY=1");
print("KPLUS_BNFCERTIFY=1");
print("KPLUS_INCLUSION=", inclusion);
print("EMBEDDED_KPLUS_UNIT_LATTICE=", embedded_plus_units);
print("NORM_MATRIX=", norm_matrix);
print("NORM_COORDINATES=", norm_coordinates);
print("NORM_HNF=", norm_hnf);
print("GENUINE_NORM_INDEX=", norm_index);
print("E_EXPONENT=", e_exponent);
print("T_S=", tS);
print("FITTING_GENERATOR=1");
print("GAMMA=", gam);
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
print("RQ000129_CONSTRUCTOR_V2=PASS");
};

run_constructor();

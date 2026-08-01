\\ Exact algebraic inputs for the five-control Arb anchor.
\\ No L-function or phase-target artifact is read.

default(realprecision, 100);

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

coefficient_pairs(polynomial, length) =
{
  vector(length, index,
    my(value = polcoef(polynomial, index - 1));
    [numerator(value), denominator(value)]
  );
};

export_case(label, polynomial, eta) =
{
  my(nf = nfinit(polynomial));
  my(gamma = first_order_four_automorphism(nf));
  my(value = Mod(eta, polynomial));
  print("CASE_ID=", label);
  print("POLYNOMIAL_ASCENDING_PAIRS=",
    coefficient_pairs(polynomial, 9));
  print("GAMMA_ASCENDING_PAIRS=",
    coefficient_pairs(lift(gamma), 8));
  for(index = 1, 4,
    print("ORBIT_", index, "_ASCENDING_PAIRS=",
      coefficient_pairs(lift(value), 8));
    value = nfgaloisapply(nf, gamma, value);
  );
  if(value != Mod(eta, polynomial),
    error(label, ": four-step orbit did not close"));
  print("CONTROL_ORBIT_EXPORT=PASS");
};

x = 'x;

main() =
{
export_case(
  "RQ-000129",
  x^8 - 4*x^5 - 2*x^4 - 8*x^2 - 8*x - 2,
  (88*x^7 - 50*x^6 + 29*x^5 - 367*x^4 + 34*x^3
    - 14*x^2 - 686*x - 303)/13
);
export_case(
  "RQ-001280",
  x^8 + 10*x^6 + 14*x^4 - 20*x^2 + 4,
  (-10615*x^7 - 5337*x^6 - 108839*x^5 - 54720*x^4
    - 176182*x^3 - 88560*x^2 + 167662*x + 84339)/3
);
export_case(
  "RQ-001569",
  x^8 + 10*x^6 - 12*x^5 + 9*x^4 + 24*x^3
    - 44*x^2 + 12*x + 1,
  (236940*x^7 - 18214*x^6 + 2369406*x^5 - 3025838*x^4
    + 2351694*x^3 + 5518936*x^2 - 10854318*x
    + 3641835)/10693
);
export_case(
  "RQ-001894",
  x^8 + 10*x^6 - 120*x^5 - 1050*x^4 + 1950*x^3
    + 5875*x^2 - 14550*x + 8725,
  (-197529271802*x^7 + 802567258245*x^6
    - 5235754606142*x^5 + 44976720281450*x^4
    + 24676735408500*x^3 - 485472790362030*x^2
    + 811883752358220*x - 424254308764920)/8301948755
);
export_case(
  "RQ-007519",
  x^8 + 10*x^6 - 12*x^5 - 99*x^4 + 312*x^3
    - 584*x^2 + 372*x + 217,
  (23893092464*x^7 - 8375086158*x^6 + 241866442362*x^5
    - 371496417582*x^4 - 2235201166494*x^3
    + 8238147563444*x^2 - 16841256174274*x
    + 14791522862557)/241535
);

print("B3_CONTROL_ORBITS=PASS");
};

main();

\\ Exact W3 algebraic candidate for RQ-000108.

default(parisizemax, 2000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_exact() =
{
  my(Kpol = y^2 - y - 1, K = bnfinit(Kpol, 1));
  my(ray = bnrinit(K, [[15, 6; 0, 3], [1, 0]], 1));
  my(P =
    x^4 - (1 + 6*y)*x^3 + (9 + 9*y)*x^2
      - (1 + 6*y)*x + 1);
  my(Q = polresultant(Kpol, P, y));
  my(ray_relative = bnrclassfield(ray, , 1));
  my(candidate_data = rnfequation(Kpol, P, 1));
  my(ray_data = rnfequation(Kpol, ray_relative, 1));
  my(isomorphisms =
    nfisisom(candidate_data[1], ray_data[1]));
  my(k_compatible = 0);
  for(index = 1, #isomorphisms,
    my(mapped = subst(
      lift(Mod(candidate_data[2], candidate_data[1])),
      x, Mod(isomorphisms[index], ray_data[1])));
    if(mapped == Mod(ray_data[2], ray_data[1]),
      k_compatible++));
  assert_equal("PACKET_RELATIVE_IRREDUCIBLE",
    polisirreducible(P), 1);
  assert_equal("PACKET_ABSOLUTE_IRREDUCIBLE",
    polisirreducible(Q), 1);
  assert_equal("PACKET_RECIPROCAL",
    x^8*subst(Q, x, 1/x) == Q, 1);
  assert_equal("K_COMPATIBLE_RAY_ISOMORPHISM_COUNT",
    k_compatible, 4);
  assert_equal("PACKET_FIELD_BNFCERTIFY",
    bnfcertify(bnfinit(Q, 1)), 1);
  print("RELATIVE_PACKET_POLYNOMIAL=", P);
  print("ABSOLUTE_PACKET_POLYNOMIAL=", Q);
  print("REAL_ROOTS=", polrootsreal(Q));
  print("RQ000108_EXACT_CANDIDATE_VERIFIED=1");
  print("RQ000108_ANALYTIC_ARB_GATE=PENDING");
};

run_exact();

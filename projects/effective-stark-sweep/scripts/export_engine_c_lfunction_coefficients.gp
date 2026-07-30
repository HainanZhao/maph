\\ Exact coefficient exporter for the generic Engine-C theta evaluator.
\\ Caller supplies CM_BASE_POLYNOMIAL, CM_CONDUCTOR, CM_CHARACTER,
\\ and COEFFICIENT_LIMIT.

default(parisizemax, 4000000000);

run_export() =
{
  my(base = bnfinit(CM_BASE_POLYNOMIAL, 1));
  my(ray = bnrinit(base, CM_CONDUCTOR, 1));
  my(L = lfuncreate([ray, CM_CHARACTER]));
  my(parameters = lfunparams(L));
  my(coefficients = lfunan(L, COEFFICIENT_LIMIT));

  if(parameters[3] != [0, 1],
    error(Str("unexpected gamma shifts: ", parameters[3])));
  print("ANALYTIC_CONDUCTOR=", parameters[1]);
  print("GAMMA_SHIFTS=", parameters[3]);
  for(n = 1, COEFFICIENT_LIMIT,
    print("A ", n, " ", real(coefficients[n]), " ",
      imag(coefficients[n])));
  print("EXACT_COEFFICIENT_EXPORT_COMPLETE=1");
};

run_export();

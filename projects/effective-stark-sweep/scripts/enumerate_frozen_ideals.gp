\\ Enumerate integral ideals in the frozen real-quadratic range.
\\ Output is deliberately line-oriented so the independent Python
\\ canonicalizer can deduplicate Galois-conjugate pairs.

is_squarefree(n) =
{
  my(f = factor(n));
  if(#f == 0, return(0));
  for(i = 1, matsize(f)[1], if(f[i, 2] > 1, return(0)));
  return(1);
};

field_polynomial(D) =
{
  if(D % 4 == 1,
    return(x^2 - x + (1-D)/4),
    return(x^2 - D)
  );
};

run_enumeration() =
{
  my(K, autos, sigma, lists, finite_ideal, conjugate);
  for(D = D_MIN, D_MAX,
    if(is_squarefree(D),
      K = bnfinit(field_polynomial(D), 1);
      autos = nfgaloisconj(K);
      sigma = autos[1];
      if(sigma == Mod(x, K.pol), sigma = autos[2]);
      lists = ideallist(K, NORM_MAX);
      print("FIELD|", D, "|", K.disc, "|", bnfcertify(K));
      for(norm_value = 1, #lists,
        for(index = 1, #lists[norm_value],
          finite_ideal = idealhnf(K, lists[norm_value][index]);
          conjugate = idealhnf(
            K, nfgaloisapply(K, sigma, finite_ideal)
          );
          print(
            "IDEAL|", D, "|", norm_value, "|",
            finite_ideal[1,1], ",", finite_ideal[1,2], ",",
            finite_ideal[2,1], ",", finite_ideal[2,2], "|",
            conjugate[1,1], ",", conjugate[1,2], ",",
            conjugate[2,1], ",", conjugate[2,2]
          );
        )
      );
    )
  );
};

run_enumeration();

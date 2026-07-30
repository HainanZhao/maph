\\ Find small prime-ideal representatives for every RQ-000458 ray log.

default(parisizemax, 1000000000);

run_search() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(finite_ideal = [12, 0; 0, 6]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(found = vector(8), ideals = vector(8));
  found[1] = 1;
  ideals[1] = matid(2);
  forprime(p = 2, 2000,
    if(gcd(p, 6) == 1,
      my(dec = idealprimedec(K, p));
      for(index = 1, #dec,
        my(prime = dec[index]);
        if(prime.f == 1,
          my(log = Vec(bnrisprincipal(ray, prime, 0)));
          my(code = 1 + log[1] + 4*log[2]);
          if(!found[code],
            found[code] = 1;
            ideals[code] = idealhnf(K, prime);
            print("CLASS_LOG=", log,
              " PRIME=", p,
              " IDEAL=", ideals[code],
              " NORM=", idealnorm(K, prime));
          );
        );
      );
    );
    if(vecsum(found) == 8, break);
  );
  if(vecsum(found) != 8, error("not every ray class found"));
  print("REPRESENTATIVES=", ideals);
  print("SMALL_RAY_REPRESENTATIVES_COMPLETE=1");
};

run_search();

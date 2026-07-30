\\ Numerical recognition only for RQ-002057, Q(sqrt(57)), norm 27.

default(realprecision, 260);
default(parisizemax, 2000000000);

character_value(character, class_log, cycle) =
  exp(2*Pi*I*character*class_log/cycle);

run_recognition() =
{
  my(K = bnfinit(y^2 - y - 14, 1));
  my(finite_ideal = [9, 3; 0, 3]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(values = bnrL1(ray, , 6));
  my(sign_log = bnrisprincipal(
    ray, idealhnf(K, 8), 0
  )[1]);
  my(derivatives = vector(6), invariants, polynomial = 1);

  for(class_index = 0, 5,
    my(first = 0, second = 0);
    for(index = 1, #values,
      if(values[index][2][1] == 1,
        first += conj(character_value(
          values[index][1][1], class_index, 6
        )) * values[index][2][2];
        second += conj(character_value(
          values[index][1][1],
          (class_index + sign_log) % 6, 6
        )) * values[index][2][2];
      )
    );
    derivatives[class_index + 1] = real((first - second)/6);
  );
  invariants = vector(6, index, exp(derivatives[index]));
  for(index = 1, 6, polynomial *= x - invariants[index]);

  print("RAY_STRUCTURE=", Vec(ray.cyc));
  print("RAY_GENERATOR=", ray.gen[1]);
  print("SIGN_LOG=", sign_log);
  print("DIFFERENCED_DERIVATIVES=", derivatives);
  print("NUMERICAL_INVARIANTS=", invariants);
  print("NUMERICAL_PACKET_POLYNOMIAL=", polynomial);
  for(coefficient_index = 0, 6,
    my(value = real(polcoef(polynomial, coefficient_index)));
    my(relation = lindep([value, 1, sqrt(57)]));
    my(residual = abs(
      relation[1]*value + relation[2] + relation[3]*sqrt(57)
    ));
    print("COEFFICIENT_", coefficient_index,
      "_RELATION=", relation,
      " RESIDUAL=", residual);
  );
  print("SHINTANI_SAFE_EXPONENT=2592");
  print("CLAIM_TAG=NUMERICAL_RECOGNITION_ONLY");
};

run_recognition();

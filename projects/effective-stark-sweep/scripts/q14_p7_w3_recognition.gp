\\ Numerical recognition only for Q(sqrt(14)), p_7 infinity_2.
\\ Exact and Arb gates are separate.

default(realprecision, 240);
default(parisizemax, 1000000000);

character_value(character, class_log, cycle) =
  exp(2*Pi*I*character*class_log/cycle);

run_recognition() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(finite_ideal = [7, 0; 0, 1]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(values = bnrL1(ray, , 6));
  my(sign_log = bnrisprincipal(
    ray, idealhnf(K, 6), 0
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
  print("SIGN_LOG=", sign_log);
  print("DIFFERENCED_DERIVATIVES=", derivatives);
  print("NUMERICAL_INVARIANTS=", invariants);
  print("NUMERICAL_PACKET_POLYNOMIAL=", polynomial);
  for(coefficient_index = 0, 6,
    my(value = real(polcoef(polynomial, coefficient_index)));
    my(relation = lindep([value, 1, sqrt(14)]));
    my(residual = abs(
      relation[1]*value + relation[2] + relation[3]*sqrt(14)
    ));
    print("COEFFICIENT_", coefficient_index,
      "_RELATION=", relation,
      " RESIDUAL=", residual);
  );
  print("SHINTANI_SAFE_EXPONENT=4032");
  print("CLAIM_TAG=NUMERICAL_RECOGNITION_ONLY");
};

run_recognition();

\\ Numerical candidate recognition for the Q(sqrt(7)), p7 infinity_2
\\ differenced ray invariants.  Algebraic verification follows below;
\\ recognition alone is never a theorem tag.

default(realprecision, 220);
default(parisizemax, 1000000000);

character_value(character, class_log, cycle) =
  exp(2*Pi*I*character*class_log/cycle);

run_recognition() =
{
  my(K = bnfinit(y^2 - 7, 1));
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
    my(relation = lindep([value, 1, sqrt(7)]));
    my(residual = abs(
      relation[1]*value + relation[2] + relation[3]*sqrt(7)
    ));
    print("COEFFICIENT_", coefficient_index,
      "_RELATION=", relation,
      " RESIDUAL=", residual);
  );
  my(exact_positive = subst(
    x^6 - (6 + 2*y)*x^5 + (22 + 8*y)*x^4
      - (34 + 13*y)*x^3 + (22 + 8*y)*x^2
      - (6 + 2*y)*x + 1,
    y, sqrt(7.0)
  ));
  my(exact_roots = polrootsreal(exact_positive));
  my(maximum_log_difference = 0);
  for(index = 1, 6,
    my(best = vecmin(vector(
      6, root_index,
      abs(derivatives[index] - log(exact_roots[root_index]))
    )));
    maximum_log_difference = max(maximum_log_difference, best);
  );
  my(voutier_lower = 1);
  for(degree = 3, 12,
    my(bound = (log(log(degree))/log(degree))^3/(4*degree));
    voutier_lower = min(voutier_lower, bound);
  );
  print("NUMERICAL_MAXIMUM_LOG_DIFFERENCE=",
    maximum_log_difference);
  print("SHINTANI_SAFE_EXPONENT=4032");
  print("NUMERICAL_POWERED_HEIGHT_UPPER=",
    4032*maximum_log_difference);
  print("VOUTIER_MINIMUM_DEGREE_3_TO_12=", voutier_lower);
  print("NUMERICAL_VOUTIER_MARGIN=",
    voutier_lower/(4032*maximum_log_difference));
  print("CLAIM_TAG=NUMERICAL_NOT_ENCLOSED");
};

run_recognition();

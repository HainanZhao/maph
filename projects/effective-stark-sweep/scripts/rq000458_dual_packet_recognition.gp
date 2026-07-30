\\ Numerical recognition and exact character bookkeeping for the
\\ RQ-000458 dual-engine alignment gate.  This script makes no
\\ certification claim; its purpose is to freeze the candidate packet
\\ before the two independent W3 routes are attempted.

default(realprecision, 260);
default(parisizemax, 2000000000);

decode_element(code, cyc) =
{
  my(answer = vector(#cyc), quotient = code);
  for(index = 1, #cyc,
    answer[index] = quotient % cyc[index];
    quotient = quotient \ cyc[index];
  );
  answer;
};

character_value(character, class_log, cyc) =
{
  my(angle = 0);
  for(index = 1, #cyc,
    angle += character[index]*class_log[index]/cyc[index]);
  exp(2*Pi*I*angle);
};

run_recognition() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(finite_ideal = [12, 0; 0, 6]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc), total = vecprod(cyc));
  my(values = bnrL1(ray, , 6));
  my(sign_log = Vec(bnrisprincipal(
    ray, idealhnf(K, 11), 0
  )));
  my(full_derivatives = vector(total));
  my(packet2_derivatives = vector(total));
  my(full_invariants, packet2_invariants);
  my(full_polynomial = 1, packet2_polynomial = 1);

  for(code = 0, total - 1,
    my(class_log = decode_element(code, cyc));
    my(translated = vector(#cyc, index,
      (class_log[index] + sign_log[index]) % cyc[index]));
    my(full_first = 0, full_second = 0);
    my(p2_first = 0, p2_second = 0);
    for(index = 1, #values,
      if(values[index][2][1] == 1,
        my(character = Vec(values[index][1]));
        my(first_term =
          conj(character_value(character, class_log, cyc))
            * values[index][2][2]);
        my(second_term =
          conj(character_value(character, translated, cyc))
            * values[index][2][2]);
        full_first += first_term;
        full_second += second_term;
        if(character == [1, 1] || character == [3, 1],
          p2_first += first_term;
          p2_second += second_term;
        );
      );
    );
    full_derivatives[code + 1] =
      real((full_first - full_second)/total);
    packet2_derivatives[code + 1] =
      real((p2_first - p2_second)/total);
  );

  full_invariants =
    vector(total, index, exp(full_derivatives[index]));
  packet2_invariants =
    vector(total, index, exp(packet2_derivatives[index]));
  for(index = 1, total,
    full_polynomial *= x - full_invariants[index];
    packet2_polynomial *= x - packet2_invariants[index];
  );

  print("CASE_ID=RQ-000458");
  print("FINITE_IDEAL=", finite_ideal);
  print("RAY_STRUCTURE=", cyc);
  print("SIGN_LOG=", sign_log);
  print("SUPPORTED_CHARACTERS=[[1,0],[3,0],[1,1],[3,1]]");
  print("ENGINE_C_PASSING_PACKET_CHARACTERS=[[1,1],[3,1]]");
  print("CLASS_LOG_ORDER=",
    vector(total, index, decode_element(index - 1, cyc)));
  print("FULL_DIFFERENCED_DERIVATIVES=", full_derivatives);
  print("PACKET2_DIFFERENCED_DERIVATIVES=", packet2_derivatives);
  print("FULL_NUMERICAL_INVARIANTS=", full_invariants);
  print("PACKET2_NUMERICAL_INVARIANTS=", packet2_invariants);
  print("FULL_NUMERICAL_PACKET_POLYNOMIAL=", full_polynomial);
  print("PACKET2_NUMERICAL_PACKET_POLYNOMIAL=", packet2_polynomial);

  for(coefficient_index = 0, total,
    my(value = real(polcoef(full_polynomial, coefficient_index)));
    my(relation = lindep([value, 1, sqrt(14)]));
    print("FULL_COEFFICIENT_", coefficient_index,
      "_RELATION=", relation,
      " RESIDUAL=", abs(
        relation[1]*value + relation[2] + relation[3]*sqrt(14)
      ));
  );
  for(coefficient_index = 0, total,
    my(value = real(polcoef(packet2_polynomial, coefficient_index)));
    my(relation = lindep([value, 1, sqrt(14)]));
    print("PACKET2_COEFFICIENT_", coefficient_index,
      "_RELATION=", relation,
      " RESIDUAL=", abs(
        relation[1]*value + relation[2] + relation[3]*sqrt(14)
      ));
  );
  print("SHINTANI_SAFE_EXPONENT=1152");
  print("CLAIM_TAG=NUMERICAL_RECOGNITION_ONLY");
};

run_recognition();

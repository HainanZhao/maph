\\ Experimental recognition of the d=7 scalar Stark-unit class polynomials.
\\ Recognition is numerical evidence until the resulting coefficients are
\\ verified inside the corresponding class field.

default(realprecision, 160);

K = bnfinit(y^2 - 2, 1);

character_value(character, class_log, cycles) =
{
  my(angle = 0);
  for(index = 1, #cycles,
    angle += character[index]*class_log[index]/cycles[index]);
  exp(2*Pi*I*angle);
};

partial_zeta_derivative(ray, values, class_log) =
{
  my(total = 0);
  for(index = 1, #values,
    if(values[index][2][1] == 1,
      total += conj(character_value(
        values[index][1], class_log, ray.cyc
      ))*values[index][2][2]
    )
  );
  total/prod(index = 1, #ray.cyc, ray.cyc[index]);
};

difference_derivative(ray, values, class_log, sign_log) =
{
  my(signed_class_log = vector(#ray.cyc, index,
    (class_log[index] + sign_log[index]) % ray.cyc[index])~);
  real(
    partial_zeta_derivative(ray, values, class_log)
    - partial_zeta_derivative(ray, values, signed_class_log)
  );
};

recognize_quadratic(value) =
{
  my(relation = lindep([value, 1, sqrt(2)]));
  if(relation[1] == 0, return(["FAILED", value, relation]));
  [
    -relation[2]/relation[1],
    -relation[3]/relation[1],
    abs(relation[1]*value + relation[2] + relation[3]*sqrt(2))
  ];
};

audit_scalar_modulus(modulus, label) =
{
  my(ray = bnrinit(K, [modulus, [1, 0]], 1));
  my(values = bnrL1(ray, , 6));
  my(sign_log = bnrisprincipal(ray, idealhnf(K, 13), 0));
  my(class_polynomial = 1);

  forvec(class_vector = vector(#ray.cyc, index,
      [0, ray.cyc[index] - 1]),
    class_log = Vec(class_vector)~;
    derivative = difference_derivative(
      ray, values, class_log, sign_log
    );
    class_polynomial *= x - exp(derivative);
  );

  print(label, "_RAY_STRUCTURE=", ray.cyc);
  print(label, "_SIGN_LOG=", sign_log);
  print(label, "_NUMERICAL_CLASS_POLYNOMIAL=", class_polynomial);
  for(coefficient_index = 0, poldegree(class_polynomial),
    coefficient = real(polcoef(class_polynomial, coefficient_index));
    recognition = recognize_quadratic(coefficient);
    print(
      label, "_COEFFICIENT_", coefficient_index,
      "_RECOGNITION=", recognition
    );
  );
};

audit_scalar_modulus([7, 0; 0, 7], "MODULUS_7");
audit_scalar_modulus([14, 0; 0, 14], "MODULUS_14");

quit();

\\ Shared Engine-A place and orientation conventions for the census.

CENSUS_SOURCE_INFINITY_VECTOR = [1, 0];
CENSUS_RAMIFIED_REAL_PLACE = 1;
CENSUS_SPLIT_REAL_PLACE = 2;

census_orient_trace(base_nf, trace_value) =
{
  my(trace_sign =
    nfeltsign(base_nf, trace_value, [CENSUS_SPLIT_REAL_PLACE])[1]);
  if(trace_sign == 0,
    error("relative-unit trace vanishes at the selected split place"));
  if(trace_sign < 0, -trace_value, trace_value);
};

census_trace_is_positive(base_nf, trace_value) =
{
  nfeltsign(
    base_nf, trace_value, [CENSUS_SPLIT_REAL_PLACE]
  )[1] == 1;
};

census_polynomial_has_positive_root_sign_pattern(base_nf, polynomial) =
{
  my(degree = poldegree(polynomial));
  for(exponent = 0, degree,
    my(coefficient = polcoef(polynomial, exponent));
    if(coefficient == 0, return(0));
    my(expected_sign = (-1)^(degree - exponent));
    my(actual_sign =
      nfeltsign(
        base_nf, coefficient, [CENSUS_SPLIT_REAL_PLACE]
      )[1]);
    if(actual_sign != expected_sign, return(0));
  );
  1;
};

\\ Exact finite Dirichlet-coefficient separator for the two inverse
\\ Q(sqrt(-42)) ray characters reinducing to RQ-000458 packet 2.

default(parisizemax, 2000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_label() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(source_ray =
    bnrinit(K, [[12, 0; 0, 6], [1, 0]], 1));
  my(source_character = [1, 1]);
  my(M = bnfinit(y^2 + 42, 1));
  my(cm_ray = bnrinit(M, [[12, 0; 0, 2], []], 1));
  my(candidates = [[1, 0, 1], [3, 0, 1]]);
  my(bound = 200);
  my(source_coefficients =
    lfunan(lfuncreate([source_ray, source_character]), bound));
  my(matches = List(), separating_index = 0);

  for(index = 1, #candidates,
    my(coefficients =
      lfunan(lfuncreate([cm_ray, candidates[index]]), bound));
    if(coefficients == source_coefficients,
      listput(matches, candidates[index]));
    if(index == 2,
      for(n = 1, bound,
        if(!separating_index
           && coefficients[n] != source_coefficients[n],
          separating_index = n));
    );
  );
  matches = Vec(matches);
  assert_equal("SOURCE_CHARACTER", source_character, [1, 1]);
  assert_equal("CM_RAY_STRUCTURE", Vec(cm_ray.cyc), [4, 2, 2]);
  assert_equal("EXHAUSTIVE_INVERSE_CANDIDATES",
    candidates, [[1, 0, 1], [3, 0, 1]]);
  assert_equal("MATCH_COUNT", #matches, 1);
  assert_equal("SELECTED_CM_CHARACTER", matches[1], [1, 0, 1]);
  if(!separating_index,
    error("inverse character was not separated"));
  print("SEPARATING_DIRICHLET_INDEX=", separating_index);
  print("SOURCE_SEPARATING_COEFFICIENT=",
    source_coefficients[separating_index]);
  print("INVERSE_SEPARATING_COEFFICIENT=",
    lfunan(
      lfuncreate([cm_ray, candidates[2]]),
      separating_index
    )[separating_index]);
  print("LINEAR_REINDUCTION_LABEL_ORIENTED=1");
  print("RQ000458_ENGINE_C_RAY_LABEL_VERIFIED=1");
  print("CLAIM_TAG=VERIFIED");
};

run_label();

\\ Exact modular-form identification of the primitive dimension-six
\\ Hecke character.
\\
\\ The character chi(g)=zeta_6 of
\\ Cl_(6,infinity_2)(Q(sqrt(21))) has absolute Artin conductor
\\ 21*N((6))=756.  Its theta series is compared through the Sturm bound
\\ with every weight-one newform at level 756.

default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

base = bnfinit(u^2 - 5*u + 1, 1);
ray = bnrinit(base, [6, [1, 0]], 1);
character_conductor = bnrconductor(ray, [1]);

assert_equal("ONE_PLACE_RAY_GROUP", ray.cyc, [6]);
assert_equal("PRIMITIVE_CHARACTER_FINITE_CONDUCTOR", \
  character_conductor[1], [6, 0; 0, 6]);
assert_equal("PRIMITIVE_CHARACTER_INFINITE_CONDUCTOR", \
  character_conductor[2], [1, 0]);

absolute_level = abs(base.disc) * matdet(character_conductor[1]);
assert_equal("ABSOLUTE_ARTIN_CONDUCTOR", absolute_level, 756);

\\ The Sturm bound for weight one and Gamma_0(756) is
\\ 756*(1+1/2)*(1+1/3)*(1+1/7)/12 = 144.
sturm_bound = 144;
zeta_six = Mod(t, t^2 - t + 1);
ideals_by_norm = ideallist(base, sturm_bound);

theta_coefficient(norm_index) =
{
  my(value = Mod(0, t^2 - t + 1));
  if(gcd(norm_index, 6) == 1,
    for(ideal_index = 1, #ideals_by_norm[norm_index],
      my(ray_log = bnrisprincipal(
        ray, ideals_by_norm[norm_index][ideal_index], 0)[1]);
      value += zeta_six^ray_log));
  value;
};

theta_coefficients = concat([Mod(0, t^2-t+1)], \
  vector(sturm_bound, norm_index, theta_coefficient(norm_index)));

spaces = mfinit([absolute_level, 1, 0], 0);
find_matches() =
{
  my(result = List());
  for(space_index = 1, #spaces,
    my(eigenforms = mfeigenbasis(spaces[space_index]));
    for(form_index = 1, #eigenforms,
      my(coefficients = mfcoefs(
        eigenforms[form_index], sturm_bound));
      my(transformed = vector(#coefficients, coefficient_index,
        Mod(
          subst(lift(coefficients[coefficient_index]), y, 1-t),
          t^2-t+1)));
      if(transformed == theta_coefficients,
        listput(result, [
          space_index,
          form_index,
          mfparams(spaces[space_index])[3],
          mfgaloistype(spaces[space_index])[form_index]
        ]))));
  Vec(result);
};

matches = find_matches();
matching_forms = #matches;
matching_space = matches[1][1];
matching_form = matches[1][2];
matching_character = matches[1][3];
matching_galois_type = matches[1][4];

assert_equal("STURM_BOUND", sturm_bound, 144);
assert_equal("MATCHING_WEIGHT_ONE_NEWFORMS", matching_forms, 1);
assert_equal("MATCHING_SPACE_INDEX", matching_space, 1);
assert_equal("MATCHING_FORM_INDEX", matching_form, 1);
assert_equal("MATCHING_NEBENTYPUS", matching_character, -7);
assert_equal("MATCHING_PROJECTIVE_GALOIS_TYPE", matching_galois_type, 12);
print("MATCHING_COEFFICIENT_FIELD=t^2-t+1");
print("TARGET_WEIGHT_ONE_LABEL_DATA=[756,1,-7,D12]");
print("MODULARITY_ORIENTS_STARK_UNIT=0");

quit();

\\ Exact projective CM-descent gate for the two d=8 quartic characters.
\\ The one-place characters do not literally satisfy chi^sigma=chi^-1,
\\ because sigma interchanges the labeled infinite places.  Their quotient
\\ is nevertheless quadratic on the full two-place ray group.

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

fractional(value) = value - floor(value);

K = bnfinit(y^2 - y - 1, 1);
ray_infinity_2 = bnrinit(K, [24, [1, 0]], 1);
ray_infinity_1 = bnrinit(K, [24, [0, 1]], 1);
ray_both = bnrinit(K, [24, [1, 1]], 1);

assert_equal("RAY_INFINITY_2_STRUCTURE", ray_infinity_2.cyc, [4, 2, 2]);
assert_equal("RAY_INFINITY_1_STRUCTURE", ray_infinity_1.cyc, [4, 2, 2]);
assert_equal("RAY_BOTH_STRUCTURE", ray_both.cyc, [4, 2, 2, 2]);

map_to_infinity_2 = matrix(#ray_infinity_2.cyc, #ray_both.cyc, row, column, bnrisprincipal(ray_infinity_2, ray_both.gen[column], 0)[row]);
map_to_infinity_1 = matrix(#ray_infinity_1.cyc, #ray_both.cyc, row, column, bnrisprincipal(ray_infinity_1, ray_both.gen[column], 0)[row]);
base_conjugation = Mod(1-y, y^2-y-1);
conjugation = matrix(#ray_both.cyc, #ray_both.cyc, row, column, bnrisprincipal(ray_both, nfgaloisapply(K, base_conjugation, ray_both.gen[column]), 0)[row]);

assert_equal("MAP_BOTH_TO_INFINITY_2", map_to_infinity_2, [3, 0, 0, 0; 0, 0, 0, 1; 0, 0, 1, 0]);
assert_equal("MAP_BOTH_TO_INFINITY_1", map_to_infinity_1, [3, 2, 0, 0; 0, 1, 1, 0; 1, 1, 1, 1]);
assert_equal("BASE_CONJUGATION_MATRIX", conjugation, [3, 2, 0, 2; 0, 1, 0, 0; 0, 1, 1, 0; 0, 0, 0, 1]);

lift_character(character) = vector(#ray_both.cyc, column, fractional(sum(row = 1, #ray_infinity_2.cyc, character[row] * map_to_infinity_2[row, column] / ray_infinity_2.cyc[row])));
conjugate_character(values) = vector(#ray_both.cyc, column, fractional(sum(row = 1, #ray_both.cyc, values[row] * conjugation[row, column])));
inverse_character(values) = vector(#values, index, fractional(-values[index]));
quotient_character(values, conjugate_values) = vector(#values, index, fractional(values[index] - conjugate_values[index]));
dual_coordinates(values) = vector(#values, index, lift(values[index] * ray_both.cyc[index]));

quartic_characters = [[1, 0, 0], [1, 1, 0]];
audit_character(character) =
{
  my(lifted, conjugated, inverted, quotient);
  lifted = lift_character(character);
  conjugated = conjugate_character(lifted);
  inverted = inverse_character(lifted);
  quotient = quotient_character(lifted, conjugated);
  print(Str("CHARACTER_", character, "_FULL_DUAL="), dual_coordinates(lifted));
  print(Str("CHARACTER_", character, "_CONJUGATE_DUAL="), dual_coordinates(conjugated));
  print(Str("CHARACTER_", character, "_INVERSE_DUAL="), dual_coordinates(inverted));
  print(Str("CHARACTER_", character, "_CONJUGATE_EQUALS_INVERSE="), conjugated == inverted);
  assert_equal(Str("CHARACTER_", character, "_PROJECTIVE_QUOTIENT_DUAL"), dual_coordinates(quotient), [2, 1, 0, 1]);
};
audit_character(quartic_characters[1]);
audit_character(quartic_characters[2]);

projective_character = [2, 1, 0, 1];
assert_equal("PROJECTIVE_CHARACTER_CONDUCTOR", bnrconductor(ray_both, projective_character), [[24, 0; 0, 24], [1, 1]]);

\\ Kernel of the character (2,1,0,1) on C4 x C2^3:
\\ a+b+d is even.  Its class field is the projective quadratic
\\ extension over K.
projective_kernel = Mat([2, 1, 0, 1; 0, 1, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1]);
projective_relative = bnrclassfield(ray_both, projective_kernel, 1);
projective_absolute = rnfpolredbest(K, projective_relative, 2);
assert_equal("PROJECTIVE_RELATIVE_FIELD", projective_relative, x^2 + 6);
print("PROJECTIVE_ABSOLUTE_FIELD=", projective_absolute);

quadratic_subfields = nfsubfields(projective_absolute, 2);
quadratic_models = vector(#quadratic_subfields, index, polredbest(quadratic_subfields[index][1]));
print("PROJECTIVE_BIQUADRATIC_SUBFIELDS=", quadratic_models);
assert_equal("PROJECTIVE_HAS_REAL_BASE_Q_SQRT_5", sum(index = 1, #quadratic_models, quadratic_models[index] == x^2-x-1), 1);
assert_equal("PROJECTIVE_HAS_CM_BASE_Q_SQRT_MINUS_6", sum(index = 1, #quadratic_models, quadratic_models[index] == x^2+6), 1);
assert_equal("PROJECTIVE_HAS_CM_BASE_Q_SQRT_MINUS_30", sum(index = 1, #quadratic_models, quadratic_models[index] == x^2+30), 1);
print("PROJECTIVE_IMAGE_V4_GATE=1");

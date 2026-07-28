\\ Exact quadratic-character unit audit for the maximal-order d=8 tuple.

default(realprecision, 100);
default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

assert_small(label, actual, tolerance) =
{
  if(abs(actual) > tolerance,
    error(Str(label, ": residual ", actual, " exceeds ", tolerance)));
  print(label, "=", actual);
};

find_l_record(records, character) =
{
  for(index = 1, #records,
    if(records[index][1] == character, return(records[index][2])));
  error(Str("character not found: ", character));
};

K = bnfinit(y^2 - y - 1, 1);
ray8 = bnrinit(K, [8, [1, 0]], 1);
values = bnrL1(ray8, , 6);

character0 = [0, 1];
character1 = [1, 1];
kernel0 = Mat([1, 0; 0, 2]);
kernel1 = Mat([1, 0; 1, 2]);

relative0 = bnrclassfield(ray8, kernel0, 1);
relative1 = bnrclassfield(ray8, kernel1, 1);
absolute0 = rnfpolredbest(K, relative0, 2);
absolute1 = rnfpolredbest(K, relative1, 2);
field0 = bnfinit(absolute0, 1);
field1 = bnfinit(absolute1, 1);

assert_equal("PARI_VERSION", version(), version());
assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
assert_equal("RAY_STRUCTURE", ray8.cyc, [2, 2]);
assert_equal("CHARACTER_0_CONDUCTOR", \
  bnrconductor(ray8, character0), [[4, 0; 0, 4], [1, 0]]);
assert_equal("CHARACTER_1_CONDUCTOR", \
  bnrconductor(ray8, character1), [[8, 0; 0, 8], [1, 0]]);
assert_equal("RELATIVE_POLYNOMIAL_0", relative0, x^2 - y);
assert_equal("RELATIVE_POLYNOMIAL_1", relative1, x^2 - 2*y);
assert_equal("ABSOLUTE_POLYNOMIAL_0", absolute0, x^4 - x^2 - 1);
assert_equal("ABSOLUTE_POLYNOMIAL_1", absolute1, x^4 - 2*x^2 - 4);

for(index = 0, 1, \
{
  my(field = if(index == 0, field0, field1));
  assert_equal(Str("SIGNATURE_", index), field.sign, [2, 1]);
  assert_equal(Str("CLASS_NUMBER_", index), field.no, 1);
  assert_equal(Str("BNFCERTIFY_", index), bnfcertify(field), 1);
});

h = Mod(x, absolute0);
phi0 = h^2;
unit0 = phi0 + h;
r = Mod(x, absolute1);
phi1 = r^2/2;
unit1 = (r + phi1)/(r - phi1);

assert_equal("UNIT_0_IS_UNIT", #bnfisunit(field0, unit0) > 0, 1);
assert_equal("UNIT_1_IS_UNIT", #bnfisunit(field1, unit1) > 0, 1);
phi0_coordinates = bnfisunit(field0, phi0);
unit0_coordinates = bnfisunit(field0, unit0);
phi1_coordinates = bnfisunit(field1, phi1);
unit1_coordinates = bnfisunit(field1, unit1);
assert_equal("PHI_0_UNIT_COORDINATES", phi0_coordinates, [-2, 0, 0]~);
assert_equal("UNIT_0_COORDINATES", unit0_coordinates, [0, -1, 1]~);
assert_equal("PHI_1_UNIT_COORDINATES", phi1_coordinates, [1, 0, 0]~);
assert_equal("UNIT_1_COORDINATES", unit1_coordinates, [-1, -2, 0]~);
assert_equal("REGULATOR_INDEX_0", \
  abs(matdet(Mat([phi0_coordinates[1..2], \
                  unit0_coordinates[1..2]]))), 2);
assert_equal("REGULATOR_INDEX_1", \
  abs(matdet(Mat([phi1_coordinates[1..2], \
                  unit1_coordinates[1..2]]))), 2);
assert_equal("UNIT_0_MINPOLY", minpoly(unit0), \
  x^4 - 2*x^3 - 2*x^2 - 2*x + 1);
print("UNIT_1_MINPOLY=", minpoly(unit1));

l0 = find_l_record(values, character0);
l1 = find_l_record(values, character1);
assert_equal("CHARACTER_0_VANISHING_ORDER", l0[1], 1);
assert_equal("CHARACTER_1_VANISHING_ORDER", l1[1], 1);

\\ Since h_K=h_L=1 and w_K=w_L=2 in both quadratic extensions,
\\ the exact unit-coordinate determinants above give R_L/R_K=log(u).
\\ The analytic class-number formula then gives L'(0,chi)=log(u).
assert_small("REGULATOR_FORMULA_0", \
  field0.reg/K.reg - log(abs(nfeltembed(field0, unit0, 2))), 1e-80);
assert_small("REGULATOR_FORMULA_1", \
  field1.reg/K.reg - log(abs(nfeltembed(field1, unit1, 2))), 1e-80);
assert_small("BNRL1_UNIT_0", \
  l0[2] - log(abs(nfeltembed(field0, unit0, 2))), 1e-80);
assert_small("BNRL1_UNIT_1", \
  l1[2] - log(abs(nfeltembed(field1, unit1, 2))), 1e-80);

print("UNIT_0=", unit0);
print("UNIT_1=", unit1);
print("QUADRATIC_CHARACTER_PACKET_UNCONDITIONAL=1");

quit();

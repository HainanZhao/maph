\\ Exact scope audit for the two admissible dimension-seven form orders.

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - 2, 1);
epsilon = Mod(3 + 2*y, y^2 - 2);
sqrt_discriminant = 2*Mod(y, y^2 - 2);
f1 = polcoef(lift((epsilon - epsilon^(-1))/sqrt_discriminant), 0);
f2 = polcoef(lift((epsilon^2 - epsilon^(-2))/sqrt_discriminant), 0);

assert_equal("D7_BNFCERTIFY", bnfcertify(K), 1);
assert_equal("D7_F1", f1, 2);
assert_equal("D7_F2", f2, 12);
assert_equal("D7_FORM_CONDUCTORS", divisors(f1), [1, 2]);
assert_equal("D7_DISCRIMINANTS", [K.disc, f1^2*K.disc], [8, 32]);

Q8 = [1, -4, 2];
Q32 = [1, -6, 1];
form_discriminant(Q) = Q[2]^2 - 4*Q[1]*Q[3];
assert_equal("D7_Q8", Q8, [1, -4, 2]);
assert_equal("D7_Q8_DISCRIMINANT", form_discriminant(Q8), 8);
assert_equal("D7_Q32", Q32, [1, -6, 1]);
assert_equal("D7_Q32_DISCRIMINANT", form_discriminant(Q32), 32);
assert_equal("D7_WIDE_CLASS_NUMBER_8", qfbclassno(8), 1);
assert_equal("D7_WIDE_CLASS_NUMBER_32", qfbclassno(32), 1);

L7 = [6, -1; 1, 0];
A7 = L7^3;
assert_equal("D7_Q32_STABILIZER", A7, [204, -35; 35, -6]);
assert_equal("D7_Q32_FIXED_POINT_MINPOLY", minpoly(epsilon), x^2 - 6*x + 1);

L7max = [7, -4; 2, -1];
A7max = L7max^3;
assert_equal("D7_Q8_STABILIZER", A7max, [239, -140; 70, -41]);
assert_equal("D7_Q8_FIXED_POINT_MINPOLY", \
  minpoly(Mod(2 + y, y^2 - 2)), x^2 - 4*x + 2);

print("D7_CERTIFIED_STRATA_DISCRIMINANTS=[8, 32]");
print("D7_OPEN_STRATA=[]");

quit();

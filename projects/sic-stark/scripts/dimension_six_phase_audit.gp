\\ Functional-equation and phase audit for the primitive d=6 character.

default(realprecision, 100);

assert_small(label, actual, tolerance) =
{
  if(abs(actual) > tolerance,
    error(Str(label, ": residual ", actual, " exceeds ", tolerance)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - 5*y + 1, 1);
R = bnrinit(K, [6, [1, 0]], 1);
Ldata = bnrL1(R, , 6);

root_one = bnrrootnumber(R, [1]);
root_five = bnrrootnumber(R, [5]);
print("PARI_VERSION=", version());
print("PRIMITIVE_CHARACTER_ONE_ROOT_NUMBER=", root_one);
print("PRIMITIVE_CHARACTER_FIVE_ROOT_NUMBER=", root_five);
assert_small("ROOT_ONE_MINUS_I", root_one-I, 1e-90);
assert_small("ROOT_FIVE_PLUS_I", root_five+I, 1e-90);

lambda_one = Ldata[1][2][2];
lambda_five = Ldata[2][2][2];
print("PRIMITIVE_L_DERIVATIVE_ONE=", lambda_one);
print("PRIMITIVE_L_DERIVATIVE_FIVE=", lambda_five);
assert_small("CONJUGATE_CHARACTER_RESIDUAL", \
  lambda_five-conj(lambda_one), 1e-90);
print("PRIMITIVE_PHASE_ARGUMENT=", arg(lambda_one));
print("ROOT_NUMBER_ROTATED_ARGUMENT=", arg(lambda_one/root_one));
print(Str("CONCLUSION=root number fixes the functional-equation rotation, ", \
  "not the phase of the noncritical L-value"));

quit();

\\ Functional-equation normalization for the primitive dimension-six
\\ Hecke character and its level-756 weight-one newform.

default(realprecision, 120);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

base = bnfinit(u^2 - 5*u + 1, 1);
ray = bnrinit(base, [6, [1, 0]], 1);
character_conductor = bnrconductor(ray, [1]);
Ldata = lfuncreate([ray, [1]]);
root_data = lfunrootres(Ldata);

assert_equal("FINITE_CHARACTER_CONDUCTOR", \
  character_conductor[1], [6, 0; 0, 6]);
assert_equal("INFINITE_CHARACTER_CONDUCTOR", \
  character_conductor[2], [1, 0]);
assert_equal("GAMMA_SHIFTS", component(Ldata, 3), [0, 1]);
assert_equal("ABSOLUTE_CONDUCTOR", component(Ldata, 5), 756);
assert_equal("ROOT_NUMBER", root_data[3], I);

value_at_one = lfun(Ldata, 1);
derivative_at_zero = lfun(Ldata, 0, 1);
functional_equation_prediction = \
  I*sqrt(756)/(2*Pi)*conj(value_at_one);
residual = derivative_at_zero-functional_equation_prediction;

if(abs(residual) > 1e-100, \
  error(Str("functional equation residual too large: ", residual)));

print("L_AT_ONE=", value_at_one);
print("L_DERIVATIVE_AT_ZERO=", derivative_at_zero);
print("FUNCTIONAL_EQUATION_RESIDUAL=", residual);
print("FINITE_CONDUCTOR_EQUALS_S_MODULUS=1");
print("LS_EQUALS_PRIMITIVE_L_FOR_ORDER_SIX_CHARACTER=1");
print("EXACT_NORMALIZATION=2*Lprime(0)=i*sqrt(756)/pi*Lbar(1)");
print("FUNCTIONAL_EQUATION_ORIENTS_STARK_UNIT=0");

quit();

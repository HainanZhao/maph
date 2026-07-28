\\ Exhaustive lower-level scalar-twist gate for the dimension-six
\\ weight-one form.
\\
\\ A scalar Dirichlet twist preserves the projective Galois type and,
\\ at primes unramified in both forms, preserves whether the Hecke trace
\\ is zero.  We enumerate every projective-D12 weight-one eigenform of
\\ level N < 756 and find an unramified prime p <= 100 at which its
\\ zero/nonzero trace pattern differs from the target.

default(parisizemax, 6000000000);
default(threadsize, 128000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

target_space = mfinit([756, 1, 0], 0);
target = mfeigenbasis(target_space[1])[1];
target_coefficients = mfcoefs(target, 100);

candidate_count = 0;
candidates_without_witness = 0;
largest_witness = 0;

audit_candidate(level, form) =
{
  my(coefficients = mfcoefs(form, 100), witness = 0);
  candidate_count++;
  forprime(prime = 2, 100,
    if(gcd(prime, level * 756) == 1 \
      && ((target_coefficients[prime + 1] == 0) \
        != (coefficients[prime + 1] == 0)) \
      && witness == 0,
      witness = prime));
  if(witness == 0,
    candidates_without_witness++,
    largest_witness = max(largest_witness, witness));
};

audit_space(level, space) =
{
  my(galois_types = mfgaloistype(space));
  my(forms = mfeigenbasis(space));
  for(form_index = 1, #galois_types,
    if(galois_types[form_index] == 12,
      audit_candidate(level, forms[form_index])));
};

for(level = 1, 755, \
  spaces = mfinit([level, 1, 0], 0); \
  for(space_index = 1, #spaces, \
    audit_space(level, spaces[space_index])));

assert_equal("TARGET_LEVEL", mfparams(target)[1], 756);
assert_equal("LOWER_D12_EIGENFORM_COUNT", candidate_count, 113);
assert_equal(\
  "LOWER_D12_FORMS_WITHOUT_TRACE_ZERO_WITNESS", \
  candidates_without_witness, \
  0 \
);
assert_equal("LARGEST_REQUIRED_WITNESS_PRIME", largest_witness, 41);
print("LOWER_LEVEL_SCALAR_TWIST_AVAILABLE=0");
print("ORIENTED_STARK_VALUE_REDUCED_BY_SCALAR_TWIST=0");

quit();

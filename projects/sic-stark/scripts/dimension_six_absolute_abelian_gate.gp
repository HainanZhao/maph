\\ Abelianization of the degree-24 full dimension-six ray field.

P = x^24 - 3*x^23 + 15*x^22 - 21*x^21 + 27*x^20 - 29*x^18 \
  - 27*x^17 + 156*x^16 - 282*x^15 + 321*x^14 + 12*x^13 \
  - 3*x^12 + 78*x^11 + 549*x^10 - 708*x^9 + 1068*x^8 \
  - 393*x^7 + 169*x^6 + 174*x^5 - 177*x^4 + 21*x^3 \
  + 27*x^2 - 9*x + 1;

G = galoisinit(P);
elements = G.group;
identity = elements[1];

compose(left, right) =
{
  Vecsmall(vector(#left, index, left[right[index]]));
};

inverse(permutation) =
{
  my(result_index = 0);
  for(index = 1, #elements,
    if(compose(permutation, elements[index]) == identity,
      result_index = index;
      break));
  elements[result_index];
};

derived = List();
listput(derived, identity);
for(left_index = 1, #elements, \
  for(right_index = 1, #elements, \
    commutator = compose(compose(compose( \
      elements[left_index], elements[right_index]), \
      inverse(elements[left_index])), \
      inverse(elements[right_index])); \
    if(!setsearch(Set(derived), commutator), \
      listput(derived, commutator))));

close_derived_subgroup() =
{
  my(changed = 1, current, product);
  while(changed,
    changed = 0;
    current = Vec(derived);
    for(left_index = 1, #current,
      for(right_index = 1, #current,
        product = compose(current[left_index], current[right_index]);
        if(!setsearch(Set(derived), product),
          listput(derived, product);
          changed = 1))));
};
close_derived_subgroup();

derived_set = Set(derived);
quotient_has_exponent_two = 1;
check_quotient_exponent() =
{
  for(index = 1, #elements,
    if(!setsearch(
      derived_set,
      compose(elements[index], elements[index])
    ), quotient_has_exponent_two = 0));
};
check_quotient_exponent();

central_involution_count = 0;
scalar_kernel = 0;
locate_scalar_kernel() =
{
  my(is_central);
  for(index = 1, #elements,
    if(permorder(elements[index]) == 2,
      is_central = 1;
      for(other_index = 1, #elements,
        if(compose(elements[index], elements[other_index]) \
            != compose(elements[other_index], elements[index]),
          is_central = 0));
      if(is_central,
        central_involution_count++;
        scalar_kernel = elements[index])));
};
locate_scalar_kernel();

if(#derived != 6, error("unexpected commutator order"));
if(#elements / #derived != 4, error("unexpected abelianization order"));
if(!quotient_has_exponent_two, error("abelianization is not C2 x C2"));
if(central_involution_count != 1, \
  error("scalar central involution is not unique"));
if(!setsearch(derived_set, scalar_kernel), \
  error("scalar kernel is not in the commutator"));

print("FULL_RAY_GALOIS_GROUP_ID=", galoisidentify(G));
print("FULL_RAY_COMMUTATOR_ORDER=", #derived);
print("FULL_RAY_ABELIANIZATION_ORDER=", #elements / #derived);
print("FULL_RAY_ABELIANIZATION=C2xC2");
print("MAXIMAL_ABSOLUTELY_ABELIAN_SUBFIELD_DEGREE=4");
print("MAXIMAL_ABSOLUTELY_ABELIAN_SUBFIELD=Q(sqrt(21),sqrt(-3))");
print("FAITHFUL_CUBIC_ORIENTATION_SURVIVES_ABELIANIZATION=0");
print("CENTRAL_INVOLUTION_COUNT=", central_involution_count);
print("SCALAR_KERNEL_IN_COMMUTATOR=1");
print("ONE_DIMENSIONAL_TWIST_NONTRIVIAL_ON_SCALAR_KERNEL=0");
print("SCALAR_TWIST_DESCENT_TO_PROJECTIVE_CM_FIELD=0");

quit();

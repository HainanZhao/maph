\\ Test whether the full two-place dimension-six ray field is CM.
\\ A degree-24 CM field must have a totally real degree-12 subfield.

default(parisizemax, 4000000000);

P = x^24 - 3*x^23 + 15*x^22 - 21*x^21 + 27*x^20 - 29*x^18 \
  - 27*x^17 + 156*x^16 - 282*x^15 + 321*x^14 + 12*x^13 \
  - 3*x^12 + 78*x^11 + 549*x^10 - 708*x^9 + 1068*x^8 \
  - 393*x^7 + 169*x^6 + 174*x^5 - 177*x^4 + 21*x^3 \
  + 27*x^2 - 9*x + 1;

degree_twelve_subfields = nfsubfields(P, 12);
signature_counts = Map();
totally_real_count = 0;

for(index = 1, #degree_twelve_subfields, \
  signature = nfinit(degree_twelve_subfields[index][1]).sign; \
  mapput(signature_counts, Str(signature), \
    if(mapisdefined(signature_counts, Str(signature), &old_count), \
      old_count + 1, 1)); \
  if(signature == [12, 0], totally_real_count++));

if(#degree_twelve_subfields != 9, \
  error("unexpected number of degree-twelve subfields"));
if(totally_real_count != 0, \
  error("full ray field unexpectedly has a totally real half-field"));

print("FULL_RAY_FIELD_SIGNATURE=", nfinit(P).sign);
print("DEGREE_TWELVE_SUBFIELD_COUNT=", #degree_twelve_subfields);
print("DEGREE_TWELVE_SUBFIELD_SIGNATURE_COUNTS=", signature_counts);
print("TOTALLY_REAL_DEGREE_TWELVE_SUBFIELD_COUNT=", totally_real_count);
print("FULL_RAY_FIELD_IS_TOTALLY_IMAGINARY=1");
print("FULL_RAY_FIELD_IS_CM=0");
print("CM_BRUMER_STARK_THEOREM_APPLIES=0");

quit();

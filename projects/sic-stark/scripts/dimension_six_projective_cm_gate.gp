\\ The faithful projective D12 quotient is CM, but its characters are
\\ trivial on the scalar kernel and cannot contain the target linear
\\ representation, on which that kernel acts by -1.

P = x^12 - 3*x^11 + x^9 + 48*x^8 - 189*x^7 + 431*x^6 \
  - 654*x^5 + 624*x^4 - 340*x^3 + 96*x^2 - 12*x + 4;

G = galoisinit(P);
half_degree_subfields = nfsubfields(P, 6);
totally_real_count = 0;
totally_imaginary_count = 0;

for(index = 1, #half_degree_subfields, \
  signature = nfinit(half_degree_subfields[index][1]).sign; \
  if(signature == [6, 0], totally_real_count++); \
  if(signature == [0, 3], totally_imaginary_count++));

if(galoisidentify(G) != [12, 4], error("unexpected projective group"));
if(nfinit(P).sign != [0, 6], error("projective field is not imaginary"));
if(totally_real_count != 1, error("CM real half-field is not unique"));
if(totally_imaginary_count != 6, error("unexpected half-field signatures"));

print("PROJECTIVE_QUOTIENT_GROUP_ID=", galoisidentify(G));
print("PROJECTIVE_QUOTIENT_SIGNATURE=", nfinit(P).sign);
print("PROJECTIVE_DEGREE_SIX_SUBFIELD_COUNT=", #half_degree_subfields);
print("PROJECTIVE_TOTALLY_REAL_HALF_FIELD_COUNT=", totally_real_count);
print("PROJECTIVE_QUOTIENT_IS_CM=1");
print("TARGET_SCALAR_KERNEL_EIGENVALUE=-1");
print("PROJECTIVE_CM_CHARACTERS_SCALAR_KERNEL_EIGENVALUE=1");
print("TARGET_LINEAR_REPRESENTATION_IN_PROJECTIVE_CM_PACKET=0");
print("PROJECTIVE_CM_BRUMER_STARK_ORIENTS_TARGET=0");

quit();

\\ Exploratory class-field structure for the dimension-six ray packet.

default(realprecision, 80);
default(parisizemax, 4000000000);

K = bnfinit(y^2 - 5*y + 1, 1);
Rone = bnrinit(K, [6, [1, 0]], 1);
Rboth = bnrinit(K, [6, [1, 1]], 1);

Hrelative = bnrclassfield(Rone, , 1);
Nrelative = bnrclassfield(Rboth, , 1);
Habsolute = rnfpolredbest(K, Hrelative, 2);
Nabsolute = rnfpolredbest(K, Nrelative, 2);

print("PARI_VERSION=", version());
print("ONE_INFINITY_RAY_GROUP=", Rone.cyc);
print("BOTH_INFINITY_RAY_GROUP=", Rboth.cyc);
print("ONE_INFINITY_ABSOLUTE_POLYNOMIAL=", Habsolute);
print("BOTH_INFINITY_ABSOLUTE_POLYNOMIAL=", Nabsolute);
print("ONE_INFINITY_SIGNATURE=", nfinit(Habsolute).sign);
print("BOTH_INFINITY_SIGNATURE=", nfinit(Nabsolute).sign);

audit_subfields(polynomial, label) =
{
  my(subfields, subpolynomial, group);
  for(degree_index = 1, poldegree(polynomial),
    if(poldegree(polynomial) % degree_index, next());
    subfields = nfsubfields(polynomial, degree_index);
    print(label, "_SUBFIELD_DEGREE_", degree_index, "_COUNT=", #subfields);
    for(index = 1, #subfields,
      subpolynomial = subfields[index][1];
      if(degree_index <= 11,
        group = polgalois(subpolynomial);
        print(
          label, "_SUBFIELD_DEGREE_", degree_index, "_", index,
          "_POLYNOMIAL=", subpolynomial,
          " GALOIS_GROUP=", group
        )
      )
    )
  )
};

audit_subfields(Habsolute, "ONE_INFINITY");

\\ The C6 ray group splits into its quadratic and cubic character parts.
\\ The lower-stratum value y has U=y^2 satisfying
\\ U^2-(beta-2)U+1=0.  Its absolute polynomial is the quartic below.
beta = Mod(y, y^2 - 5*y + 1);
lower_relative = x^2 - (beta-2)*x + 1;
lower_absolute = rnfpolredbest(K, lower_relative, 2);
print("LOWER_QUADRATIC_COMPONENT_RELATIVE=", lower_relative);
print("LOWER_QUADRATIC_COMPONENT_ABSOLUTE=", lower_absolute);

\\ The finite Stark polynomial gives the three traces V=U+U^-1.
trace_relative = x^3 + (2-5*beta)*x^2 \
  + (35*beta-11)*x + (13-78*beta);
trace_absolute = rnfpolredbest(K, trace_relative, 2);
print("TRACE_CUBIC_COMPONENT_RELATIVE=", trace_relative);
print("TRACE_CUBIC_COMPONENT_ABSOLUTE=", trace_absolute);

\\ Lifting each trace through U+U^-1 gives the full C6 ray-unit field.
unit_relative = x^3 * subst(trace_relative, x, x + 1/x);
unit_absolute = rnfpolredbest(K, unit_relative, 2);
print("PRIMITIVE_UNIT_RELATIVE=", unit_relative);
print("PRIMITIVE_UNIT_ABSOLUTE=", unit_absolute);
print("PRIMITIVE_UNIT_FIELD_IS_ONE_INFINITY_RAY_FIELD=", #nfisisom(unit_absolute, Habsolute) > 0);
quartic_subfield = nfsubfields(Habsolute, 4)[1][1];
sextic_subfield = nfsubfields(Habsolute, 6)[1][1];
print("LOWER_COMPONENT_IS_QUARTIC_SUBFIELD=", #nfisisom(lower_absolute, quartic_subfield) > 0);
print("TRACE_COMPONENT_IS_SEXTIC_SUBFIELD=", #nfisisom(trace_absolute, sextic_subfield) > 0);

component_compositum = polcompositum(lower_absolute, trace_absolute)[1];
print("COMPONENT_COMPOSITUM_POLYNOMIAL=", component_compositum);
print("COMPONENT_COMPOSITUM_IS_ONE_INFINITY_RAY_FIELD=", #nfisisom(component_compositum, Habsolute) > 0);

quit();

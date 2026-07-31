\\ Cycle-104 exact Hilbert/ray containment controls.
default(parisizemax, 3000000000);

run_case(case_id, selector, hilbert) =
{
  my(normal, subfields, isomorphisms, matches);
  normal = nfsplitting(selector, 16, 1)[1];
  subfields = nfsubfields(normal, 4);
  isomorphisms = vector(#subfields, i, nfisisom(hilbert, subfields[i][1]));
  matches = sum(i = 1, #isomorphisms, isomorphisms[i] != 0);
  print("CASE_ID=", case_id);
  print("SELECTOR_IRREDUCIBLE=", polisirreducible(selector));
  print("HILBERT_FIELD_IRREDUCIBLE=", polisirreducible(hilbert));
  print("NORMAL_CLOSURE_DEGREE=", poldegree(normal));
  print("NORMAL_CLOSURE_IRREDUCIBLE=", polisirreducible(normal));
  print("DEGREE4_SUBFIELD_COUNT=", #subfields);
  print("HILBERT_FIELD_MATCH_COUNT=", matches);
  print("HILBERT_FIELD_ISOMORPHISMS=", isomorphisms);
  print("HILBERT_FIELD_CONTAINED=", if(matches > 0, 1, 0));
}

run_case("RQ-001569", x^8 + 10*x^6 - 12*x^5 + 9*x^4 + 24*x^3 - 44*x^2 + 12*x + 1, y^4 - 46*y^2 + 361);
run_case("RQ-001894", x^8 + 10*x^6 - 120*x^5 - 1050*x^4 + 1950*x^3 + 5875*x^2 - 14550*x + 8725, y^4 - 40*y^2 + 196);
run_case("RQ-007519", x^8 + 10*x^6 - 12*x^5 - 99*x^4 + 312*x^3 - 584*x^2 + 372*x + 217, y^4 - 190*y^2 + 8281);

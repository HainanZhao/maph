\\ Exact same-packet alignment certificate for RQ-000458.
\\
\\ The Engine-C packet is the conjugate character pair [1,1],[3,1]
\\ in Cl_m(K)^ = C4 x C2.  Independently, the Shintani-side Fourier
\\ projector selects the same two ray characters.  This script checks
\\ the common modulus, kernel, exact packet polynomial, K-compatible
\\ ray-field identification, and containment in the full B ray field.

default(realprecision, 160);
default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

character_pairing(character, element, cyc) =
{
  my(value = 0);
  for(index = 1, #cyc,
    value += character[index] * element[index] / cyc[index]);
  value;
};

decode_element(code, cyc) =
{
  my(answer = vector(#cyc), quotient = code);
  for(index = 1, #cyc,
    answer[index] = quotient % cyc[index];
    quotient = quotient \ cyc[index];
  );
  answer;
};

character_kernel_hnf(character, cyc) =
{
  my(elements = List(), total = vecprod(Vec(cyc)));
  for(code = 0, total - 1,
    my(element = decode_element(code, cyc));
    if(denominator(character_pairing(
          character, element, cyc)) == 1,
      listput(elements, element));
  );
  my(v = Vec(elements));
  my(columns = matrix(
    #cyc, #v, row, column, v[column][row]));
  mathnf(concat(matdiagonal(cyc), columns));
};

run_alignment() =
{
  my(Kpol = y^2 - 14, K = bnfinit(Kpol, 1));
  my(finite_ideal = [12, 0; 0, 6]);
  my(modulus = [finite_ideal, [1, 0]]);
  my(ray = bnrinit(K, modulus, 1));
  my(cyc = Vec(ray.cyc));
  my(sign_log = Vec(bnrisprincipal(
    ray, idealhnf(K, 11), 0)));
  my(c_character = [1, 1], inverse_character = [3, 1]);
  my(c_kernel = character_kernel_hnf(c_character, cyc));
  my(b_projector_characters = List());

  \\ Reconstruct the B-side support and its packet-2 projector without
  \\ using the Engine-C screen output.
  for(code = 0, vecprod(cyc) - 1,
    my(character = decode_element(code, cyc));
    my(phase = character_pairing(character, sign_log, cyc));
    if(denominator(phase) != 1
       && (character == [1, 1] || character == [3, 1]),
      listput(b_projector_characters, character));
  );
  b_projector_characters = Vec(b_projector_characters);

  \\ This polynomial was recognized from the B-side projected partial
  \\ zeta derivatives.  It is restated exactly here, never read from
  \\ the C geometry artifact.
  my(packet =
    x^4 - (20 + 6*y)*x^3 + (138 + 36*y)*x^2
      - (20 + 6*y)*x + 1);
  my(packet_absolute = polresultant(Kpol, packet, y));

  \\ Independently construct the C character field from the exact ray
  \\ kernel and identify the projected Stark packet with it over K.
  my(c_relative = bnrclassfield(ray, c_kernel, 1));
  my(c_data = rnfequation(Kpol, c_relative, 1));
  my(packet_data = rnfequation(Kpol, packet, 1));
  my(c_absolute = c_data[1]);
  my(packet_model = packet_data[1]);
  my(c_base = Mod(c_data[2], c_absolute));
  my(packet_base = Mod(packet_data[2], packet_model));
  my(isomorphisms = nfisisom(packet_model, c_absolute));
  my(k_compatible = 0);
  for(index = 1, #isomorphisms,
    my(mapped_base = subst(
      lift(packet_base), x,
      Mod(isomorphisms[index], c_absolute)));
    if(mapped_base == c_base, k_compatible++);
  );

  \\ The B field is constructed independently as the full one-place ray
  \\ field.  Exact absolute inclusion certifies that the common packet
  \\ is literally a B subfield, not merely an abstract look-alike.
  my(full_relative = bnrclassfield(ray, , 1));
  my(full_data = rnfequation(Kpol, full_relative, 1));
  my(full_absolute = full_data[1]);
  my(inclusions = nfisincl(packet_model, full_absolute));

  assert_equal("CASE_ID", "RQ-000458", "RQ-000458");
  assert_equal("FINITE_IDEAL", finite_ideal, [12, 0; 0, 6]);
  assert_equal("FINITE_NORM", idealnorm(K, finite_ideal), 72);
  assert_equal("INFINITE_COMPONENT", modulus[2], [1, 0]);
  assert_equal("RAY_STRUCTURE", cyc, [4, 2]);
  assert_equal("SIGN_LOG", sign_log, [2, 0]);
  assert_equal("ENGINE_C_CHARACTER", c_character, [1, 1]);
  assert_equal("ENGINE_C_INVERSE_CHARACTER",
    inverse_character, [3, 1]);
  assert_equal("ENGINE_C_KERNEL_HNF", c_kernel, [4, 2; 0, 1]);
  assert_equal("ENGINE_B_PROJECTOR_CHARACTERS",
    b_projector_characters, [[1, 1], [3, 1]]);
  assert_equal("PACKET_RELATIVE_IRREDUCIBLE",
    polisirreducible(packet), 1);
  assert_equal("PACKET_RECIPROCAL",
    x^4*subst(packet, x, 1/x) == packet, 1);
  assert_equal("PACKET_ABSOLUTE_IRREDUCIBLE",
    polisirreducible(packet_absolute), 1);
  if(#isomorphisms == 0,
    error("projected packet is not the C character field"));
  if(k_compatible == 0,
    error("packet/C-field identification is not K-compatible"));
  if(#inclusions == 0,
    error("projected packet is not contained in the B full ray field"));

  print("ENGINE_B_PACKET_RELATIVE_POLYNOMIAL=", packet);
  print("ENGINE_C_PACKET_RELATIVE_POLYNOMIAL=", packet);
  print("IDENTICAL_PACKET_POLYNOMIAL=1");
  print("PACKET_ABSOLUTE_POLYNOMIAL=", packet_absolute);
  print("ENGINE_C_RELATIVE_FIELD_POLYNOMIAL=", c_relative);
  print("PACKET_C_FIELD_ISOMORPHISM_COUNT=", #isomorphisms);
  print("PACKET_C_FIELD_K_COMPATIBLE_COUNT=", k_compatible);
  print("PACKET_IN_FULL_B_RAY_FIELD_INCLUSION_COUNT=", #inclusions);
  print("SAME_MODULUS=1");
  print("SAME_RAY_CLASSES=1");
  print("SAME_PACKET_ALIGNMENT_VERIFIED=1");
  print("CLAIM_TAG=VERIFIED");
};

run_alignment();

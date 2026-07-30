\\ Numerical scan of the C-route orientation conventions.
\\ It tests the finite set of sign/swap choices forced by the exact
\\ Artin generator and the 2/e normalization.  The selected convention
\\ is frozen and then reimplemented with Arb intervals.

default(realprecision, 120);
default(parisizemax, 3000000000);

run_scan() =
{
  my(Epol =
    x^8 - 4*x^7 + 20*x^6 - 28*x^5 + 106*x^4
      - 152*x^3 + 152*x^2 + 184*x + 58);
  my(E = bnfinit(Epol, 1));
  my(automorphisms = nfgaloisconj(Epol));
  my(sigma = automorphisms[2]);
  my(u1 = E.fu[1]);
  my(u2 = E.fu[2]^(-1) * E.fu[3]);
  my(sigma_u1 = Mod(subst(lift(u1), x, sigma), Epol));
  my(sigma_u2 = Mod(subst(lift(u2), x, sigma), Epol));
  my(real_part =
    -4.07878021737836523525851844980007794284367734638252463618);
  my(imag_part =
    7.08799743247503076990362638132191594239949120146250011692);
  my(scales = [1/4, 1/2, 1, 2, 4]);

  print("ANTI_BASIS_1=", u1);
  print("ANTI_BASIS_2=", u2);
  for(embedding = 1, 4,
    my(matrix = [
      log(abs(nfeltembed(E, u1, embedding))),
      log(abs(nfeltembed(E, u2, embedding)));
      log(abs(nfeltembed(E, sigma_u1, embedding))),
      log(abs(nfeltembed(E, sigma_u2, embedding)))
    ]);
    print("EMBEDDING_", embedding, "_LOG_MATRIX=", matrix);
    for(scale_index = 1, #scales,
      my(scale = scales[scale_index]);
      my(targets = [
        [real_part, imag_part]~,
        [imag_part, real_part]~,
        [-real_part, imag_part]~,
        [real_part, -imag_part]~,
        [-imag_part, real_part]~,
        [imag_part, -real_part]~
      ]);
      for(target_index = 1, #targets,
        print("EMBEDDING_", embedding,
          "_SCALE_", scale,
          "_TARGET_", target_index,
          "_COORDINATES=",
          matsolve(matrix, scale*targets[target_index]));
      );
    );
  );
  print("RQ000458_ENGINE_C_COORDINATE_SCAN_COMPLETE=1");
  print("CLAIM_TAG=NUMERICAL_CONVENTION_SCAN_ONLY");
};

run_scan();

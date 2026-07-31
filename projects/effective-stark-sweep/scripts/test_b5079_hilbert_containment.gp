\\ Cycle-102 exact containment test, run only after the RQ-005298 job.
default(parisizemax, 3000000000);
H = y^4 - 24*y^2 + 4;
N = x^32 - 8*x^31 + 44*x^30 - 182*x^29 + 622*x^28 - 1820*x^27 + 4684*x^26 - 10952*x^25 + 23538*x^24 - 46718*x^23 + 84969*x^22 - 140448*x^21 + 210414*x^20 - 285240*x^19 + 351250*x^18 - 391614*x^17 + 394587*x^16 - 358656*x^15 + 298423*x^14 - 237038*x^13 + 185840*x^12 - 143556*x^11 + 99988*x^10 - 57852*x^9 + 26057*x^8 - 8552*x^7 + 3255*x^6 - 960*x^5 + 352*x^4 - 42*x^3 + 16*x^2 - 2*x + 1;
print("CASE_ID=RQ-001262");
print("HILBERT_FIELD_POLYNOMIAL=", H);
print("NORMAL_CLOSURE_DEGREE=", poldegree(N));
print("HILBERT_FIELD_DEGREE=", poldegree(H));
print("HILBERT_FIELD_IRREDUCIBLE=", polisirreducible(H));
print("NORMAL_CLOSURE_IRREDUCIBLE=", polisirreducible(N));
S = nfsubfields(N, 4);
V = vector(#S, i, nfisisom(H, S[i][1]));
M = sum(i = 1, #V, V[i] != 0);
print("DEGREE4_SUBFIELD_COUNT=", #S);
print("HILBERT_FIELD_MATCH_COUNT=", M);
print("HILBERT_FIELD_ISOMORPHISMS=", V);
print("HILBERT_FIELD_CONTAINED=", if(M > 0, 1, 0));

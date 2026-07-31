# Roblot email — long draft, not sent

Status: `DRAFTED_NOT_SENT`.  
Publication placeholder: `[RESULTS_V1.4_DOI]`.  
Attachment: `effective-stark-results-companion-v16.tar.gz`.  
Attachment SHA-256:
`9e4169375bf862f3d934d7dba0e2dff1c40de54bcecafb59beb3695027415b73`.

The recipient address should be rechecked on the official Lyon 1 page
immediately before sending. This draft deliberately omits the withdrawn
raw quarter-turn labels.

---

To: X.-F. Roblot `<roblot@math.univ-lyon1.fr>`  
Subject: A phase consequence of your quartic Stark-unit uniqueness theorem

Dear Professor Roblot,

Your Theorem 6.1 leaves a weak quartic Stark solution unique up to a
trivial group-ring unit. While checking explicit one-place Stark
packets, I found that this ambiguity gives a useful exact phase
statement, and I would be grateful for your view on whether I have
interpreted the theorem and its conventions correctly.

I checked five cyclic-quartic cases arising from one-place ray fields
over
\(\mathbf Q(\sqrt6)\), \(\mathbf Q(\sqrt{35})\),
\(\mathbf Q(\sqrt{42})\), \(\mathbf Q(\sqrt{51})\), and
\(\mathbf Q(\sqrt{186})\). **PROVED:** exact computations verify your
hypotheses (A1)--(A3) in all five cases. **PROVED:** independently, the
corresponding Stark packets follow by cyclic-quartic CM descent.

With \(G=\langle\gamma\rangle\simeq C_4\),
\(\chi(\gamma)=i\), and
\[
c_\chi(\eta)=\frac12\sum_{g\in G}\chi(g)\log|\eta^g|_w,
\]
let \(\eta\) be the weak solution supplied by Theorem 6.1 and let
\(\epsilon\) be the proved Stark unit in the same convention.
Uniqueness gives \(\bar\eta=h\bar\epsilon\) for a trivial group-ring
unit \(h\). Under the right-action convention used in my replay,
\[
c_\chi(h\bar\epsilon)=\chi(h)c_\chi(\bar\epsilon),
\]
and hence
\[
\frac{L'(0,\chi)}{c_\chi(\eta)}
   =\chi(h)^{-1}\in\mu_4.
\]
**PROVED:** with these checked hypotheses, the fourth-root phase
relation in the already-certified cases is a consequence of your
uniqueness theorem, rather than new evidence for algebraicity.

There is also a cautionary point. I independently constructed the five
weak solutions and initially compared their coefficients with rigorous
\(L'(0,\chi)\) balls. Each case matched a unique fourth-root rotation
for one of the two conjugate character orientations. A later
provenance audit found, however, that the archived code chose between
\(\chi\) and \(\chi^{-1}\) after inspecting the analytic target. I have
therefore withdrawn the claim that this was a fully oriented
independent replay. The retained numerical observation is only the
two-orientation statement (**OBSERVED** against certified
\(L'\)-balls); the exact \(\mu_4\) corollary above instead uses the
independently proved Stark packets and your uniqueness theorem.

May I ask three specific questions?

1. With the displayed Fourier and right-action conventions, does
   Theorem 6.1 indeed imply the ratio
   \(L'(0,\chi)/c_\chi(\eta)=\chi(h)^{-1}\), or is an additional
   hypothesis needed to compare the weak solution with a proved Stark
   unit?
2. Do your construction or later results determine the class of the
   trivial unit \(h\)—and therefore its value under \(\chi\)—from the
   algebraic input alone, without consulting an \(L'\)-value?
3. Is there a known exact transport that fixes the choice between
   \(\chi\) and \(\chi^{-1}\) from the ray-field Artin generator and
   the weak solution before the analytic target is evaluated?

The correction release and replay archive are available at
`[RESULTS_V1.4_DOI]`. I would be happy to send a shorter case table or
the exact PARI transcripts if useful. The attached deterministic
archive has SHA-256
`9e4169375bf862f3d934d7dba0e2dff1c40de54bcecafb59beb3695027415b73`.

For transparency, I used AI systems (OpenAI GPT-5.6 and Anthropic
Claude) for code review, proof-audit assistance, and editing. I
reviewed the mathematical argument and replayed the exact and certified
computations.

With best regards,

Hainan Zhao  
Independent Researcher  
hainzhao@gmail.com

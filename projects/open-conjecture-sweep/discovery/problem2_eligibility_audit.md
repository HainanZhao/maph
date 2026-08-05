# Problem 2 eligibility audit: (K_{5,5}\setminus C_{10})

Audit date: 2026-08-05 UTC.

## Exact target

Let (H=K_{5,5}\setminus C_{10}), where the removed (C_{10}) is a
Hamiltonian alternating cycle.  Thus (e(H)=25-10=15).  The target is

\[
t_H(W)\ge t_{K_2}(W)^{15}
\]

for every graphon (W).

## Literature boundary

- `PROVED` (as quoted from the stated theorem): Lee--Schülke define the
  graphon inequality in their Conjecture 1.2 and state that this Möbius ladder
  remains undetermined; their Theorem 1.3 proves only that it is **not weakly
  norming**.  Source: <https://arxiv.org/abs/1910.08454>, lines 19--35.
- `PROVED` (as quoted from the stated corollary): Kral', Volec, and Wei show
  (H-e^{15}) is not SOS, including no multiplier of the specified
  (1+g) form can make it SOS.  This excludes their SOS route, not the
  Sidorenko inequality.  Source: <https://par.nsf.gov/servlets/purl/10277018>,
  Corollary 1.6 / pp. 3 and 10.
- `OBSERVED` from a 2025/26 primary preprint: the introduction to *A reverse
  Sidorenko inequality* still calls this the first open case.  Its result is
  an upper bound for triangle-free regular graphs, not the needed lower
  bound.  Source: <https://par.nsf.gov/servlets/purl/10249528>, pp. 3--4.
- `OBSERVED`: a bounded search of OpenAI's current research index, mathematics
  announcements, and First Proof release found no official announcement
  resolving this target.  The current official announced conjecture result is
  instead the planar unit-distance problem.  Sources:
  <https://openai.com/index/model-disproves-discrete-geometry-conjecture/> and
  <https://openai.com/index/first-proof-submissions/>.  Absence from this
  bounded audit is not a proof of no announcement.
- `PROVED` (as quoted from a 2026 preprint's theorem): Zhao's Theorem 1.3
  reduces strong Sidorenko for a fixed bipartite (H) to the comparison
  (t_{\mathrm{Cay}}(H;\Gamma,a)\ge
  t_{\mathrm{Cay}}(H;\Gamma,a^{\mathrm{cl}})) for every finite group and
  nonnegative function.  Theorem 1.4 concerns 1-subdivisions only, so it does
  not cover (K_{5,5}\setminus C_{10}).  Source:
  <https://arxiv.org/html/2606.15368v1>, Theorems 1.3--1.4.

## Eligibility decision

`PROVISIONALLY_ELIGIBLE`: no checked source resolves the target, and the two
known route barriers are precise rather than universal.  Any Cycle 51 must
not rebrand a norming or ordinary SOS proof.  The current first route is an
exact finite-group test of Zhao's conjugacy-averaging comparison: it can
falsify that proposed route but cannot certify the universal comparison from a
finite pass.

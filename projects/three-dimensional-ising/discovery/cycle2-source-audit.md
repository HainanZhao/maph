# Cycle 2 source audit

Checked 2026-08-07. `PROVED`: the applicability statements below follow from
the identified primary theorem or explicit equations. They define the
algebraic tests; they do not transfer any purported 3D Ising solution.

1. V. V. Bazhanov and Yu. G. Stroganov, “Conditions of commutativity of
   transfer matrices on a multidimensional lattice,” *Theoretical and
   Mathematical Physics* **52** (1982), 685--691,
   [doi:10.1007/BF01027789](https://doi.org/10.1007/BF01027789). The paper
   proves that the vertex tetrahedron equations are sufficient for
   commutativity of the associated three-dimensional layer transfer
   matrices. Cycle 2 tests the standard constant equation
   `R123 R145 R246 R356 = R356 R246 R145 R123`; it does not claim necessity.

2. David Cimasoni, “A generalized Kac--Ward formula,” *Journal of
   Statistical Mechanics* (2010) P07023,
   [arXiv:1004.3158v2](https://arxiv.org/pdf/1004.3158). Theorem 2.1 and its
   proof express the square-root determinant for a spin structure as a signed
   sum of even subgraphs classified by surface homology, and recover the
   physical even-subgraph polynomial by the Arf-weighted spin-structure sum.
   Lane B computes that Boolean transform directly on pinned cellular
   embeddings.

3. Jin-Yi Cai and Aaron Gorenstein, “Matchgates Revisited,” *Theory of
   Computing* **10** (2014), 41--155,
   [journal article](https://theoryofcomputing.org/articles/v010a007/). The
   matchgate identities are proved necessary and sufficient for planar
   matchgate signatures and imply the parity condition. Lane D uses their
   Grassmann--Pluecker/Pfaffian-minor form, including the sign of the
   four-leg crossing identity.

4. Yu-An Chen, Anton Kapustin, and Djordje Radicevic, “Exact bosonization in
   two spatial dimensions and a new class of lattice gauge theories,”
   *Annals of Physics* **393** (2018), 234--253,
   [arXiv:1711.00515](https://arxiv.org/abs/1711.00515). Equations (23) and
   (40), with the surrounding discussion, distinguish the modified Gauss law
   and `U_e` kinetic term required for a local free-fermion dual from the
   standard `Z2` gauge theory dual to the 3D Ising model. Equations (59)--(60)
   also retain the topological sign term in the Euclidean action.

5. Yu-An Chen, “Exact bosonization in arbitrary dimensions,”
   [arXiv:1911.00017](https://arxiv.org/abs/1911.00017). The main result maps
   local even fermionic observables in `n` spatial dimensions to a local
   `(n-1)`-form `Z2` gauge theory with a modified Gauss law, explicit spin
   structure, and Stiefel--Whitney dependence. Lane C therefore does not
   equate “locality preserving” with “free” or with the unmodified Ising-dual
   gauge theory.

`PROVED` withheld scope: none of these sources proves that all tetrahedron,
higher-form, holographic, or exact-renormalization mechanisms for the uniform
3D Ising model fail.

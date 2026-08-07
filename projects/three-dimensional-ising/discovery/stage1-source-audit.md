# Stage 1 primary-source audit

Checked 2026-08-07. This is a lightweight research-stage source audit, not a
paper-stage hostile novelty audit.

`PROVED`: each applicability statement below follows from the cited source at
the identified theorem, section, or scope. No novelty claim is made.

## Sources and applicable statements

1. M. Kac and J. C. Ward, “A Combinatorial Solution of the Two-Dimensional
   Ising Model,” *Physical Review* **88** (1952), 1332,
   [doi:10.1103/PhysRev.88.1332](https://doi.org/10.1103/PhysRev.88.1332).
   The original paper proposes the planar determinant mechanism. It is not
   used alone as a proof source because parts of the original argument were
   heuristic.

2. David Cimasoni, “A generalized Kac--Ward formula,” *Journal of
   Statistical Mechanics* (2010) P07023,
   [arXiv:1004.3158v2](https://arxiv.org/pdf/1004.3158). Theorem 2.1, pp. 4--5,
   applies to any finite graph embedded in a closed oriented genus-`g`
   surface. It gives the even-subgraph polynomial as an Arf-weighted sum over
   all `2^(2g)` spin structures of chosen square roots of generalized
   Kac--Ward determinants. The introduction and Section 4 also identify this
   construction with the Fisher--Kasteleyn Pfaffian method. These hypotheses
   match our use after the finite cubic graph is embedded in an orientable
   surface.

3. Theodore D. Schultz, Daniel C. Mattis, and Elliott H. Lieb,
   “Two-Dimensional Ising Model as a Soluble Problem of Many Fermions,”
   *Reviews of Modern Physics* **36** (1964), 856--871,
   [accessible PDF](https://physics.ucsc.edu/~sriram/Courses_All/Physics-220-2011/Lieb_Schulz_Mattis.pdf).
   Section VI, p. 870, explicitly separates the general transfer-matrix step
   from the fermion step and states that the latter is convenient when
   interacting spins are nearest neighbours in a one-dimensional ordering;
   it then obtains commuting paired quadratic forms. This supports only the
   obstruction to that ordinary ordering-based free-fermion route.

4. Franz J. Wegner, “Duality in Generalized Ising Models and Phase
   Transitions without Local Order Parameters,” *Journal of Mathematical
   Physics* **12** (1971), 2259--2272,
   [doi:10.1063/1.1665530](https://doi.org/10.1063/1.1665530). The paper's
   `M_{d,n}` dualities map the three-dimensional nearest-neighbour Ising model
   to a local gauge-invariant model with plaquette interactions. This supports
   the type-change statement, not a claim that duality is useless.

5. Francisco Barahona, “On the computational complexity of Ising spin glass
   models,” *Journal of Physics A* **15** (1982), 3241--3253,
   [doi:10.1088/0305-4470/15/10/028](https://doi.org/10.1088/0305-4470/15/10/028).
   The three-dimensional hardness result concerns spin-glass instances with
   selectable signs/weights on finite sublattices. It does not by itself
   classify the one-parameter uniform ferromagnetic full-box sequence.

6. Sorin Istrail, “Statistical Mechanics, Three-Dimensionality and
   NP-completeness. I,” STOC 2000 extended abstract,
   [author PDF](https://istrail-lab.github.io/papers/Statistical%20Mechanics%2C%20Three-Dimensionality%20and%20NP-completeness.pdf).
   Sections 4--5 encode arbitrary cubic graphs in finite sublattices of
   nonplanar crystal lattices and use interaction alphabets including zero or
   signed couplings. Theorem statements around pp. 7--8 therefore constrain
   representations uniform over those richer instance families, but they do
   not prove hardness of evaluating only complete `L x L x L` boxes with one
   positive coupling.

## Withheld claims

- No source above proves that every exact representation of the uniform 3D
  ferromagnet must have exponential complexity.
- No source above proves that a higher-form, noncommutative, or exactly
  renormalizable representation cannot exist.
- The absence of a two-dimensional self-duality does not prove the absence of
  a critical-point characterization.
- No purported published 3D exact solution was imported into the project.

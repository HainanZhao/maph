# Targeted prior-art audit: general Fourier-cat identifiability

Date: 2026-07-26

## Question audited

Does prior work already give the following combined construction?

1. an \(m\)-mode passive Fourier multiport;
2. the \(m\)-photon balanced path cat
   \(m^{-1/2}\sum_j|m e_j\rangle\);
3. the modularly dark outcomes
   \(s_{p,c}=(m-1)e_p+e_{p+c}\);
4. the exact amplitude-gradient blocks
   \(L_{p,c}=(m-1)z_p+z_{p+c}\), with the antipodal
   even-\(m\) real form;
5. two fixed global probe generators, used at four signed settings;
6. full local rank on all \(m(m-1)\) real off-diagonal Hermitian
   directions;
7. \(m(m-1)/2\) selected dark outcomes and \(m(m-1)\) scalar limiting
   contrasts, saturating the corresponding tangent-dimension bounds?

## Verdict

No direct antecedent was found in the targeted primary-literature search.
The ingredients have substantial prior art separately, and one 2024
general-\(d\) unitary-estimation paper has a notably similar
opposite-index/even-d parameter pairing.  The defensible novelty is therefore
the **explicit passive-bosonic synthesis and its all-\(m\) rank/minimality
proof**, not the Fourier-cat sector identity, null displacement, local
unitary estimation, or parameter counting by themselves.

Absence from a targeted search is not proof of absolute priority.  Use “to
our knowledge” and describe exactly which combination was not found.

## Closest comparator

J. Escandón-Monardes, D. Uzcátegui, M. Rivera-Tapia, S. P. Walborn, and
A. Delgado, “Estimation of high-dimensional unitary transformations
saturating the Quantum Cramér-Rao bound,” *Quantum* **8**, 1405 (2024),
DOI: 10.22331/q-2024-07-10-1405.

This is the closest conceptual comparator because it:

- estimates arbitrary \(d\)-dimensional unitaries near the identity for
  every \(d>2\);
- exposes the pairing of Weyl--Heisenberg coefficients indexed by
  \(p\) and \(-p\);
- treats the exceptional self-paired indices that occur for even \(d\);
- estimates all \(d^2-1\) unitary parameters;
- proves saturation of the quantum Cramér--Rao bound in its model.

It is not the present construction.  Its physical procedure uses one target
qudit, two control qudits, controlled shift and phase gates, Fourier
transforms on the controls, and computational-basis measurements after
mapping the unitary coefficients to a two-control-qudit state.  It does not
use a passive bosonic Fourier multiport, a fixed-number path cat, modularly
dark photon-counting events, signed global output probes, the
\((m-1)I+P_c\) cyclic systems, or an outcome-minimal frame for the
off-diagonal passive-optical tangent slice.  It also targets the full
\(d^2-1\)-parameter unitary, whereas the present theorem intentionally
excludes the \(m-1\) output-diagonal directions.

This paper should be discussed explicitly rather than left for a referee to
raise.  The similarity of opposite-index pairing, especially in even
dimension, makes it the most important comparison.

## Prior work containing individual ingredients

### Fourier-cat modular sector identity

A. Vourdas and J. A. Dunningham, “Fourier multiport devices,”
*Phys. Rev. A* **71**, 013809 (2005),
DOI: 10.1103/PhysRevA.71.013809.

Equations (18)--(20) already give the relevant arbitrary-\(d\) Fourier-cat
number-sector structure: a balanced superposition of all-bunched
number states is mapped to occupation configurations satisfying one
root-of-unity/modular constraint.  The present charge-sector darkness is an
equivalent orientation of that known identity.  It must not be claimed as a
new suppression theorem.

### General symmetry suppression

C. Dittel *et al.*, “Totally Destructive Many-Particle Interference,”
*Phys. Rev. Lett.* **120**, 240404 (2018),
DOI: 10.1103/PhysRevLett.120.240404; and
“Totally Destructive Interference for Permutation-Symmetric Many-Particle
States,” *Phys. Rev. A* **97**, 062116 (2018),
DOI: 10.1103/PhysRevA.97.062116.

These works derive broad suppression laws from input permutation symmetry,
including arbitrary pure inputs in the detailed paper.  They subsume why the
cat has forbidden sectors, but do not differentiate those dark amplitudes
with respect to coherent unitary errors or construct a complete local
tomographic frame.

### Displaced-null identifiability

F. Girotti, A. Godley, and M. Guţă, “Optimal estimation of pure states with
displaced-null measurements,” *J. Phys. A: Math. Theor.* **57**, 245304
(2024), DOI: 10.1088/1751-8121/ad4c2b.

This establishes the general principle that an exactly null measurement can
lose local identifiability and that a calibrated displacement restores
phase-sensitive information.  It develops asymptotically optimal state
estimation and uses separate real/imaginary displaced-null measurements for
pure qudit models.  It does not give the bosonic Fourier-cat events, cyclic
gradient formula, two passive global probes, or process-error rank theorem.

### General and photonic unitary estimation

- C. H. Baldwin, A. Kalev, and I. H. Deutsch, “Quantum process tomography
  of unitary and near-unitary maps,” *Phys. Rev. A* **90**, 012110 (2014),
  DOI: 10.1103/PhysRevA.90.012110.  A global unitary map is characterized
  using a minimal collection of \(d^2+d\) POVM elements and \(d\) probe
  states.  This is a different global-QPT resource model.
- N. Liu and H. Cable, “Quantum-enhanced multi-parameter estimation for
  unitary photonic systems,” *Quantum Sci. Technol.* **2**, 025008 (2017),
  DOI: 10.1088/2058-9565/aa6fea.  The explicit analysis is for
  two-mode \(SU(2)\) estimation with photon counting and compares
  Holland--Burnett and NOON probes; extension to \(SU(d)\), \(d>2\), is
  left open.
- X.-Q. Zhou *et al.*, “Quantum-enhanced tomography of unitary processes,”
  *Optica* **2**, 510--516 (2015),
  DOI: 10.1364/OPTICA.2.000510.  This gives multiphoton-enhanced photonic
  process tomography, but not the general passive-multiport dark-event
  construction.
- S. Rahimi-Keshari *et al.*, “Direct characterization of linear-optical
  networks,” *Opt. Express* **21**, 13450--13458 (2013),
  DOI: 10.1364/OE.21.013450.  This efficiently reconstructs multimode
  transfer matrices with coherent light and intensity measurements; it is
  an important practical baseline, not a collision.
- L. Banchi, W. S. Kolthammer, and M. S. Kim, “Multiphoton Tomography with
  Linear Optics and Photon Counting,” *Phys. Rev. Lett.* **121**, 250402
  (2018), DOI: 10.1103/PhysRevLett.121.250402.  This concerns tomography of
  unknown multiphoton states and minimum measurement bases, not tomography
  of the multiport generator.

### Local dimension-minimal state measurements

N. Li, C. Ferrie, J. A. Gross, A. Kalev, and C. M. Caves,
“Fisher-Symmetric Informationally Complete Measurements for Pure States,”
*Phys. Rev. Lett.* **116**, 180402 (2016),
DOI: 10.1103/PhysRevLett.116.180402.

This establishes locally informationally complete pure-state measurements
with \(2d-1\) outcomes and Fisher symmetry.  It means that “dimension
minimal” is not a new general tomography concept.  The present claim must be
restricted to the number of scalar first-order contrasts and complex dark
outcomes for the declared off-diagonal tangent slice.

## Claim language recommended for the manuscript

### Safe main claim

> We give an explicit passive-bosonic realization of locally complete
> coherent-error sensing at an \(m\)-mode Fourier multiport.  For every
> \(m\geq3\), a balanced \(m\)-photon path cat and
> \(m(m-1)/2\) specified modularly dark \((m-1,1)\) outcomes produce
> analytically invertible cyclic amplitude-gradient blocks.  Two fixed
> global probes, each used with both signs, convert their complex
> differentials into \(m(m-1)\) real contrasts of full rank on the
> off-diagonal Hermitian tangent space.

### Safe novelty sentence

> To our knowledge, previous work has not combined Fourier-cat suppression
> with displaced-null readout to obtain an explicit all-mode,
> dimension-saturating local frame for coherent off-diagonal errors of a
> passive multiport.

### Safe minimality sentence

> Each selected dark outcome has only one complex first-order amplitude and
> can therefore contribute at most two independent real limiting
> differentials.  The construction uses exactly
> \(m(m-1)/2\) outcomes and \(m(m-1)\) scalar contrasts, meeting these
> lower bounds for the declared \(m(m-1)\)-dimensional tangent slice.

### Claims to avoid

- “the first tomography of an arbitrary \(d\)-dimensional unitary”;
- “full \(SU(m)\) tomography”;
- “a new Fourier suppression law”;
- “the first displaced-null measurement”;
- “minimum number of experimental settings,” since four settings and
  dimension-minimal scalar contrasts are different resource notions;
- “optimal tomography” or “quantum-enhanced,” absent a Fisher-information
  or sample-complexity comparison;
- “QCRB saturation,” which is proved by the closest comparator but not by
  the present Jacobian-rank theorem;
- “scalable” without qualification, because the \(m\)-photon cat and rare
  selected events impose severe physical scaling costs.

## Venue assessment

### Physical Review A: strong and realistic

The all-\(m\) theorem materially strengthens the earlier \(F_4\)-only
certificate.  An exact passive-optical construction, closed-form rank proof,
even-\(m\) treatment, outcome lower bound, and conditioning result form a
coherent PRA theory paper.  The safest presentation is a foundational
quantum-optics/tomography result with a detailed comparison to the 2024
general-\(d\) estimator and realistic limitations.

### Quantum Science and Technology or New Journal of Physics: plausible

These venues become attractive if the paper includes a credible protocol,
finite-shot likelihood analysis, probe uncertainty, cat dephasing,
partial distinguishability, loss/background robustness, and numerical
performance for \(m=3,4,5\).  The applications story is then stronger than
a purely algebraic construction.

### Quantum: possible but currently demanding

The theorem has the right arbitrary-dimension and local-estimation flavor,
but the submission would need to establish broader information-theoretic
significance relative to Escandón-Monardes *et al.* and generic
displaced-null estimation.  A Fisher-information comparison, a genuine
resource advantage in a well-defined model, or a general optimality theorem
beyond row counting would make this target much more credible.

### Physical Review Letters / Optica: not supported by the theorem alone

The present result does not yet show metrological advantage, QCRB
optimality, experimental feasibility at useful scale, or a broad physical
effect of sufficiently immediate reach.  A convincing experiment or a
surprising universal precision/robustness advantage would be needed for
these venues.  The theorem by itself is better matched to PRA.

## Bottom line

The all-\(m\) construction appears publishably distinct, but its novelty is
**architectural and theorem-level**, not elemental: known Fourier-cat dark
sectors plus known displaced-null logic are assembled into a particularly
economical passive-optical local frame whose cyclic invertibility is proved
for every mode number.  Cite the ingredients generously, highlight the
explicit frame and lower-bound saturation, and do not claim statistical
optimality until it is demonstrated.

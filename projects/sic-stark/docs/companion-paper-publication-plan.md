# SIC--Stark companion-paper publication plan

## Publication architecture

The results remain one mathematical program but are divided at the
change in proof technology.

### Paper I: dimensions four and five

Working title:

> Twisted-Convolution Identities in Dimensions Four and Five from
> Shintani Ray Units

The paper proves the common AFK/Kopp bridge, uses dimension four as the
quadratic convention calibration, and develops the powered-algebraicity
and height-rigidity argument required in dimension five.

Essential source files:

- `paper/sic-stark-dimensions-four-five.tex`;
- the dimension-four certificate generator and verifier;
- the dimension-four PARI audit;
- all dimension-five bridge, Shintani, Arb, embedding, and exact-minor
  certificates;
- the general SIC/TCC regression tests.

Dimension-six, dimension-seven, and dimension-eight research scripts
must not be required to verify Paper I.

### Paper II: dimensions seven and eight

Working title:

> Twisted-Convolution Identities in Dimensions Seven and Eight:
> Shintani Height Rigidity and CM Descent

The paper recalls the common bridge in a compact self-contained form,
then proves:

- dimension seven by conductor lowering, Shintani's index-two theorem,
  Arb isolation, Voutier rigidity, labeled ray fields, and exact
  compositum arithmetic;
- the discriminant-45 dimension-eight stratum by genuine linear CM
  reinduction and the proved imaginary-quadratic rank-one theorem;
- the discriminant-5 dimension-eight stratum by quadratic ray units
  and exact symbolic phase reduction.

Essential source files:

- the dimension-seven conductor, Shintani, phase, Artin-label, field,
  and exact-TCC scripts;
- the dimension-eight conductor-three CM scripts and Arb transcript;
- the dimension-eight maximal-order tuple, unit, phase, and exact-TCC
  scripts;
- dedicated end-to-end tests for both dimensions.

Paper II may cite Paper I for motivation, but its statement of the
formal TCC and its characteristic-to-Weyl normalization must be
self-contained.

## Audit gates

### Gate A: dimension-eight CM bridge

An independent referee must confirm:

1. equality of the induced linear characters, not merely projective
   equivalence;
2. equality of all local Artin factors and the removed \(S\)-factors;
3. the exact character and embedding labels;
4. applicability and normalization of Stark's proved
   imaginary-quadratic rank-one theorem;
5. the logical use of Arb only to isolate integral unit coordinates;
6. the exact return from CM unit norms to the real-quadratic units.

### Gate B: maximal-order phase bridge

An independent referee must confirm:

1. the continued-fraction word and specialized six-factor AFK formula;
2. the negative-index finite \(q\)-Pochhammer convention;
3. positivity of the reciprocal double sine in its fundamental strip;
4. every recurrence sign and initial Weyl chirp;
5. exact cancellation of the \(\sqrt5\)-coefficient in all 63 phases;
6. identity of the resulting sign table with the table used by the
   exact TCC certificate.

### Gate C: form-class scope

The manuscript must prove that dimension-eight admissibility permits
exactly conductors one and three, and must transport within both
discriminants independently.  It must not claim that AFK covariance
transports between discriminants.

## Archive layout

The release should contain two deterministic archives:

```text
sic-stark-paper-I/
  paper/
  certificates/d4/
  certificates/d5/
  scripts/common/
  scripts/d4/
  scripts/d5/
  tests/

sic-stark-paper-II/
  paper/
  certificates/d7/
  certificates/d8/
  scripts/common/
  scripts/d7/
  scripts/d8/
  tests/
```

Each archive must contain:

- its own `README.md`, `REPRODUCE.md`, software lock file, and checksum
  manifest;
- the exact compiled PDF corresponding to the source;
- complete generated transcripts, not only the scripts;
- a clean-extraction test;
- a citation file and final Zenodo DOI.

The existing combined archive remains useful as the project-level
research archive, but it is not a substitute for the two
submission-specific packages.

## Completion order

1. Resolve the independent dimension-eight referee report.
2. Freeze the theorem and certificate interfaces.
3. Cut Paper I and verify it without higher-dimensional artifacts.
4. Draft Paper II and verify every theorem citation against an
   archived certificate.
5. Build and test the two clean-extraction archives.
6. Obtain a final independent report on each paper.
7. Deposit immutable releases and add their DOIs.
8. Resume the dimension-six oriented order-six problem.

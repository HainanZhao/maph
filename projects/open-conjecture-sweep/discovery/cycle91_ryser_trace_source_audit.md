# C91 Ryser deletion-cover trace source audit

`PROVED` source facts used by this gate:

- Abu-Khazneh--Pokrovskiy, *Intersecting extremal constructions for Ryser's
  conjecture*, Section 2.2 and Appendix A, give the labelled 13-edge
  intersecting six-partite construction and establish \(f(6)=13\).  The
  checked transcription is `cycle69_r6_extremal_control.py`; it has 31
  vertices (six in part 1 and five in each remaining part), and its exact
  exhaustive cover check verifies \(\tau(H)=5\).
- Haxell--Scott, *On Ryser's Conjecture*, pp. 2--3, reports the intersecting
  conjecture open from \(r=6\).  This is eligibility context only.
- Aharoni--Barat--Wanless, *A fractional version of Ryser's conjecture for
  intersecting hypergraphs*, abstract, proves a fractional matching-reduction
  result while noting the corresponding integral strengthening fails above
  \(r=3\).

`PROVED` finite implication: if \(C\) is a four-vertex cover of \(H-e\) and
meets \(e\), then it covers all of \(H\), contradicting the exact
\(\tau(H)=5\) control.  Thus every enumerated member of \(\mathcal C_e\) must
avoid \(e\).  This is the only use of edge-minimal deletion-cover logic.

`CONJECTURED` mechanism boundary: reciprocal shared-coordinate trace
compatibility is a newly stipulated gluing axiom, not a known consequence of
Ryser, and its outcome is not evidence for the \(r=6\) conjecture.  It has no
fractional variables, matching number, residual LP, private-region partition,
or greedy vertex deletion; consequently it is outside the C87/C88 method
boundaries and the ABW fractional theorem interface.

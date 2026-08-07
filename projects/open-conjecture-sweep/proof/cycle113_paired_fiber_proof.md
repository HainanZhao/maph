# C113 balanced paired-fiber boundary

**`PROVED` claim boundary (conditional on the displayed state).** Let
\(q=2n-1\). For every \(x\), the two vertices in fiber \(x\) have one
internal edge of colour \(r_x\), and for \(x\ne y\) set cross edges red when
\(\epsilon\delta=h_{xy}\), for symmetric \(h_{xy}\in\{\pm1\}\). The
Seidel row sum \(-1\) is equivalent to red degree \(q\); since each vertex
has exactly \(q-1\) red cross-fiber neighbours, it forces every \(r_x\) red.

For \(z\notin\{x,y\}\), put
\[N_\pm(x,y)=\#\{z:h_{xy}h_{xz}h_{yz}=\pm1\},\qquad N_++N_-=q-2.\]
If the \(x,y\) red cross pair is red, it has \(N_+\) common red and
\(N_+\) common blue neighbours. If it is blue, it has \(N_-+2\) common red
and \(N_-\) common blue neighbours. The two added red neighbours are exactly
the endpoint-fiber vertices; this is the C110 correction. They do *not*
enter the asymmetric book maxima, since they occur on a blue edge while the
red book counts red edges. Every fiber pair contains both a red and a blue
matching edge, so the relevant maxima are \(\max_{x<y}N_+(x,y)\) and
\(\max_{x<y}N_-(x,y)\), respectively; the sign only exchanges the two
matching endpoints. These identities are direct from the matching equation,
and the independent matrix replay checks them for every normalized q=7 sign
state.

The sealed finite result is a q=7 boundary unless a separate all-q cap
argument is supplied. It does not constrain other paired-fiber colourings
without the Seidel row-sum, general F001 states, or any new problem.

# C85 source audit: Möbius-ladder triple-kernel route

`PROVED` as a direct algebraic reduction: label the left and right vertices
of \(H=K_{5,5}\setminus C_{10}\) by \(\mathbb Z_5\) so that right vertex
\(i\) is adjacent to left vertices \(i,i+1,i+2\).  Integrating those five
right variables first yields the product-of-five-triple-kernels formula in
`cycle85_sidorenko_tensor_selection.md`.  Each left vertex occurs in three
triple kernels, so the graph has 15 edges as required.

`OBSERVED` from the current primary audit
`discovery/problem2_eligibility_audit.md`: Lee--Schülke identify this graph
as unresolved; Kral', Volec, and Wei block an SOS route; and Zhao's 2026
finite-group comparison does not settle it.  C68's fixed-\(S_3\) theorem is
therefore a separate, contained route.  The bounded audit does not prove
universal openness or novelty.

`CONJECTURED`: (C5-K) is not attributed to the sources above.  It is a new
proof-state-space test.  Its failure would not contradict their results or
the Sidorenko inequality.

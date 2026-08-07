# C114 full two-block-circulant q=7 boundary

**`PROVED` finite claim.** Let
\(\Gamma_{\mathbb Z_7}(D_{11},D_{12},D_{22})\) have the two copies of
\(\mathbb Z_7\), within-copy red differences \(D_{11},D_{22}\), and cross
red difference set \(D_{12}\). Simplicity and undirectedness require
\(0\notin D_{ii}\) and \(D_{ii}=-D_{ii}\). Red degree seven forces
\[|D_{11}|=|D_{22}|=a,\qquad |D_{12}|=7-a.\]
The three inverse pairs of \(\mathbb Z_7\setminus\{0\}\) therefore give
\[\sum_{j=0}^3 {3\choose j}^2{7\choose 7-2j}=512\]
labelled states.

For a within-copy difference \(d\), red or blue common-neighbour counts are
the corresponding colour intersections in \(D_{ii}\) and in the appropriate
cross difference set. For a cross difference \(d\), they are the two colour
intersections \((D_{11},-D_{12})\) and \((D_{12},D_{22})\). In a blue count,
the two endpoints appear in complement intersections and are deleted. The
difference-set evaluator implements exactly these identities. The independent
bitset replay constructs every 14-vertex adjacency matrix and counts common
neighbours directly.

Both routes give zero states with red maximum at most 2 and blue maximum at
most 3. This closes only the complete q=7 degree-seven two-block-circulant
family, not larger q, non-circulant states, or F001.

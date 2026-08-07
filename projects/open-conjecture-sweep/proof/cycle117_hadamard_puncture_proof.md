# C117/B115 Sylvester-Hadamard puncture q=7 boundary

**`PROVED` finite claim.** Index the order-16 Sylvester matrix by
\(\mathbb F_2^4\), with \(H_{xy}=(-1)^{x\cdot y}\). Replace its diagonal by
zero, delete an unordered pair of indices, and switch the remaining signed
matrix by arbitrary vertex signs modulo global sign. Interpreting sign \(-1\)
as red gives a 14-vertex colouring.

There are \({16\choose2}\) deletion pairs and \(2^{13}\) normalized
switches, hence exactly 983,040 declared states. The C++ route reconstructs
every adjacency array and counts same-colour common neighbours directly. The
independent Python route rebuilds the Walsh signs and uses 14-bit adjacency
rows. They agree on every profile and find no state with red maximum at most 2
and blue maximum at most 3.

This is only the fixed Sylvester parent, this two-vertex puncture operation,
and q=7. It does not constrain other Hadamard matrices, other punctures,
general switching classes, or F001.

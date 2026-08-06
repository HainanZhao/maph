# C001 (legacy C100) control outcome

`OBSERVED` control-specification failure. This outcome record is separate from
the frozen source screen named by the preregistration.

The amended five-layer n=25, k=7 control generated exactly 179,400 variables
and 3,504,438 clauses (CNF SHA-256
`d4d0f0927e924e1acd7466700a07e81643507dbfb23b37d1a8d5d29b153060de`). The
frozen lower-memory CaDiCaL configuration returned SAT in 13.94 seconds at
996.52 MiB solver RSS. Its printed complete 179,400-variable assignment was
independently evaluated against every generated clause; all 3,504,438 clauses
were satisfied.

This does not produce a geometric counterexample: the reduced encoding is a
relaxation and no realizability audit was authorized. It instead refutes the
preregistered requirement that this n=25, k=7 control be UNSAT. Such a
sub-threshold no-convex-7-gon instance is not an appropriate UNSAT scalability
control. Under the frozen failure rule, C001 stops without a canonical retry;
the next problem selection, if allowed, must begin D001.

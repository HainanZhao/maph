# Cycle 108 — exact B5-015 packet transport

## Statement

Let `m_49 = (7) infinity_2` (RQ-000021) and
`m_98 = (7) q infinity_2` (RQ-000039), where `q` is the unique
norm-two prime of Q(sqrt(2)).  Under the exact canonical ray-class-map
identification `Cl_m98 = Cl_m49 = C6`, with `q` having class log one,
the packet satisfies, for every class `A`,

\[
 X_{m_{98}}(A)=X_{m_{49}}(A)X_{m_{49}}(Aq^{-1})^{-1}.
\]

This is an Artin-labelled identity: the target label is sent to the
same source label by the map `[Mat(1),[6],[6]]`, and `Aq^{-1}` has log
one less modulo six.  It is not an equality of the two packets.

## Proof

For a source ray-class character `chi`, Euler deletion at the prime
`q` gives

\[
 L_{m_{98}}(s,\chi)=(1-\chi(q)Nq^{-s})L_{m_{49}}(s,\chi).
\]

Character inversion gives the corresponding partial-zeta identity

\[
 Z_{m_{98}}(s,A)=Z_{m_{49}}(s,A)-Nq^{-s}Z_{m_{49}}(s,Aq^{-1}).
\]

Every character surviving the `Z` difference is odd at the one
distinguished real place.  Its rank-one functional equation gives
`L_m49(0,chi)=0`, hence `Z_m49(0,A)=0`.  Differentiation at zero
therefore yields

\[
 Z'_{m_{98}}(0,A)=Z'_{m_{49}}(0,A)-Z'_{m_{49}}(0,Aq^{-1}).
\]

Exponentiation proves the displayed packet formula.  The source packet
is the independently certified RQ-000021 packet.  Each source entry is
positive at the frozen split real embedding; its quotient is positive,
so the transported formula preserves the required positive orientation.

## Exact hypothesis checks

- Cycle 107 proves `m_98/m_49=q`, `Nq=2`, and the identity ray-class
  map, including identity, generator, and sign labels.
- The source and target sign logs are both three, so exactly the odd
  exponents in `C6` survive the differenced Fourier transform.
- RQ-000021's direct certified packet replay supplies the source
  Artin-labelled packet.

The local Euler factor is nontrivial: `q` has ray log one.  Thus the
formula is a distribution relation, not a packet-equality shortcut.

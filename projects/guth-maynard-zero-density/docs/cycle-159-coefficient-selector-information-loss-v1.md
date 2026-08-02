# Cycle 159: the primitive-ray map loses the coefficient atom multiplier

## Claim boundary

`PROVED`: the Cycle-92 primitive-ray compression loses the ray multiplier
needed to reconstruct a nonconstant Cycle-124 coefficient fibre.  Cycle 124
has coefficient atoms `c_(a,n)(ell)`. A Cycle-92 ray is

```text
(n,n')=t(q,p),       p/q reduced.                  (1)
```

Suppose two admissible multipliers `t_1!=t_2` have different oriented
coefficient products

```text
c_(a',t_i p)(ell) conjugate(c_(a,t_i q)(ell)).     (2)
```

Then no selection pushforward depending only on the retained primitive ray
`p/q`, ordered modes, and downstream continued-fraction decorations can
reconstruct both values in (2). Within the original atom-label system, the
minimal repair is to retain `t`, or, equivalently, the ordered atom pair
`(n,n')`.

This does not assert that a differing pair has target mass in the frozen
operator. It does not construct the actual selector, prove spectral
concentration, a moment, density, or an interval theorem.

## Proof

The retained primitive ray metadata is identical for the two pairs in (1).
Any proposed coefficient pushforward which is a function of that metadata
therefore has one value for both. The two values in (2) are different, a
contradiction. Conversely, after retaining `p,q,t`, equation (1) recovers the
ordered polynomial atoms; their frequency-dependent coefficients can then be
evaluated without substituting a scalar edge weight.

This is the first loss in the Cycle 124--136 path: Cycle 92 explicitly
compresses all multiples to `p/q`; the later continued-fraction data decorate
the primitive ray but do not recover `t`.

## Gate effect

The actual selection-kernel reconstruction cannot start from the primitive
ray web alone. Any coefficient-faithful continuation must carry a multiplier-
resolved collision measure, or explicitly classify the loss as an escape
component. This seals Cycle 159's registered information-loss alternative.

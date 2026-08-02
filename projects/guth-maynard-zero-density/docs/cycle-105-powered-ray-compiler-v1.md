# Cycle 105: perfect-power aliases compile to powered rays

## Exact compiler

`PROVED`. In the Cycle-104 rational class, write the reduced label as

```text
N=n0^d, R=r0^d, (n0,r0)=1,
```

and write `w=h*d`. Then

```text
(w,N/R)=(h*d,(n0/r0)^d).                           (1)
```

Thus the exception is the `d`th power of the anchored base rational ray
`(h,n0/r0)`.

## Root-error transfer

`PROVED`. For positive `a,b`,

```text
|a^d-b^d|=|a-b| sum_{j=0}^{d-1}a^(d-1-j)b^j
           >=d min(a,b)^(d-1)|a-b|.
```

Taking `a=n0/r0`, `b=exp(hx)`, and using the Cycle-99 error `delta` gives

```text
|n0/r0-exp(hx)|
 <=delta/(d min(n0/r0,exp(hx))^(d-1)).             (2)
```

If `|hdx|<=L` and `delta<=exp(-L)/2`, both powered quantities show that the
minimum in (2) is at least `(exp(-L)/2)^(1/d)`. Hence the phase anchor and an
explicit error budget survive taking roots.

## Exponent cap and repeated rays

`PROVED`. For nonunit reduced base height `Z=max(n0,r0)`, the height condition
`Z^d<=H` gives

```text
d<=floor(log(H)/log(Z));
```

the mode range also gives `d<=2M/|h|`. Repetition of one base ray therefore
has a finite exact exponent set. On that set the modes are arithmetic
multiples `h*d` and the labels are the geometric powers `(n0/r0)^d`.

This is an E16 powered-ray witness. Missing exponents are not supplied by the
theorem, and the witness is not yet a realized original packet seed.

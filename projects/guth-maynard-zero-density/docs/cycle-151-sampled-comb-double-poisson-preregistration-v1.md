# Cycle 151 preregistration: sampled-comb double Poisson

Date frozen: 2026-08-02 UTC.

Fix the Cycle-149 witness denominator `h`.  For one smooth halo mode, write

```text
c0g^b=r_b/h_b+epsilon_b,
gcd(r_b,h_b)=1,
tau_b=KQ epsilon_b,
```

with `h_b<=QX^(-delta)` and bounded `tau_b`.  Correlate its length-`Q`
coefficient sum with the sampled comb `k=h ell`.

Use Cycle 148 to remove every `k` for which `h_b` does not divide `k`.
The surviving lattice is exactly

```text
k multiple of lcm(h,h_b)=h h_b/gcd(h,h_b).
```

If this lcm is at most the frequency scale, rescale the surviving frequency
and coefficient variables and derive the leading two-variable tail transform
at `tau_b`, with an explicit smooth Riemann-sum error.  If the lcm exceeds the
frequency support, prove power-negligibility.

Success is a per-mode signed correlation formula, a weighted-gcd condition
for target negative mass, and the requirement that contributing tails lie in
a negative lobe of the actual transform.  Keep denominators within a fixed
power of `Q` as a separate unresolved boundary class.

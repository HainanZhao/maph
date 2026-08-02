# Cycle 91 correction v2: zero-count slope normalization

## Claim boundary

This is a versioned correction to discovery output only. Every corrected
count and slope remains `OBSERVED`; no proof claim is promoted.

## Error and cause

The v1 preregistration froze the regression inputs

```text
max(C,1),  max(C,1)/(DQ/K),  max(C,1)/Q.
```

The v1 script correctly used `max(C,1)` for the raw count but incorrectly
used `max(C/scale,1e-300)` for the two normalized regressions. Zero-count
rows therefore inserted `1e-300`, producing meaningless positive slopes.

## Correction

Version 2 preserves every frozen scale, range, count, nearest-integer rule,
classification threshold, and raw row. It changes only the two regression
inputs to the preregistered formulas above. The v1 script and JSON remain
preserved as the failed record.

Affected claims: only the v1 normalized slopes and their classifications.
Unaffected observations: all finite collision counts, labels, raw ratios,
codegrees, and smallest scaled errors.


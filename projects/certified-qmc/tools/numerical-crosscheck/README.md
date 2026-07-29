# Numerical cross-check tools

Everything below this directory is `NUMERICAL` validation tooling.  It
is not in the Certified-QMC trusted base, is not built by the release
target, and is excluded from source-release archives.

The tools preserve the historical FFTW plan inspection and compiled
LatNet Builder midpoint/search cross-checks.  They may require FFTW and
an independently built LatNet Builder binary.  Their transcripts can
show that a producer model is realistic; they cannot promote a merit,
CBC decision, or production-table entry to `VERIFIED`.

Build the optional FFTW harness explicitly:

```bash
make -C tools/numerical-crosscheck
```

The production build remains:

```bash
make -C native release
```

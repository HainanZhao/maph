# Preserved Phase-0 preparation validation failure v1

Date: 2026-07-29 UTC

Tag: `FAILED_RUN_PRESERVED`

The preparation audit, unit tests, and generic validation command were
started concurrently.  The validation branch used the zsh glob
`artifacts/*.json` before the audit branch had created the artifacts
directory.  With zsh's default `nomatch` behavior, that branch stopped:

```text
zsh:1: no matches found: artifacts/*.json
```

This was an orchestration race, not a failed mathematical check.  In
the same invocation:

- the preparation audit passed 12/12 checks;
- the Phase-0 contract suite passed 8/8 tests.

The amended replay orders artifact creation before JSON validation and
uses `find` rather than an unmatched shell glob.  No threshold, source
freeze, predicate, or expected result changed.

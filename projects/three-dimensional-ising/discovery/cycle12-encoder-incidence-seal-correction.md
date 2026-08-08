# Cycle 12 sealing correction

The v1 encoder-incidence artifact correctly records the mathematical payload,
but its frozen inputs include the entire active manuscript. The manuscript is
supposed to evolve during the remaining Phase 0 tasks, so that dependency
would make the v1 immutable check fail after legitimate unrelated revisions.

Version 2 supersedes v1 as the canonical replay record. It freezes the
standalone proof, generator, tests, generated table, recurrence/rotation
dependencies, and v1 itself, but not the mutable manuscript. No mathematical
field, incidence row, claim boundary, or gate outcome changes.

# C103 / F001 correction: replay dependency freeze

**`PROVED` correction scope:** C103 v1's mathematical no-hit is unchanged,
but its frozen-input inventory omitted the C101 character constructor imported
by `proof/cycle103_book_ramsey_reflection.py`. The correction freezes that
dependency and replaces the unavailable `pytest` invocation with the
one-command standard-library replay `python3 proof/replay_cycle103_book_ramsey_reflection.py`.

The affected claim is only v1's proof-grade replay packaging. The replayed
enumeration, independent checker, family, q=7 no-hit, and method boundary are
unchanged. The correction supersedes v1 for reliance; v1 remains immutable.

# Repository Git hooks

PDF files are tracked by Git LFS through the root `.gitattributes` rule.
Enable the versioned verification and upload hooks in a fresh clone with:

```sh
git lfs install --local
git config core.hooksPath .githooks
```

The pre-commit hook rejects a staged PDF unless its index entry is an LFS
pointer. The pre-push hook uploads referenced LFS objects and fails clearly
when `git-lfs` is unavailable.

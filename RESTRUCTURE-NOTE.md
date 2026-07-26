# Repository restructure handoff

The repository now contains independent research projects under `projects/`.
Rebase ongoing branches onto the commit that introduced this note before
continuing work.

## Path map

| Previous root path | New project path |
|---|---|
| `src/erdos700.py` | `projects/erdos-700/src/erdos700.py` |
| Erdos scripts, tests, data, and notes | `projects/erdos-700/{scripts,tests,data,docs}` |
| `paper/` | `projects/fourier-dark-tomography/paper/` |
| `src/fourier_suppression.py` | `projects/fourier-dark-tomography/src/fourier_suppression.py` |
| Fourier/photonic scripts, tests, and notes | `projects/fourier-dark-tomography/{scripts,tests,docs}` |

Run project-specific commands from the relevant project directory so imports
such as `from src...` continue to resolve:

```sh
cd projects/erdos-700
python3 -m unittest discover -s tests -v

cd ../fourier-dark-tomography
python3 -m unittest discover -s tests -v
```

When resolving rebase conflicts, preserve the new project-local paths. Do not
recreate the retired root-level `src/`, `scripts/`, `tests/`, `docs/`, `data/`,
or `paper/` trees. A change formerly targeting one of those paths should be
replayed at its mapped location above.

Suggested synchronization sequence:

```sh
git fetch
git rebase <commit-containing-this-note>
```

If a branch contains changes to both topics, split or relocate each conflict by
subject before completing the rebase.

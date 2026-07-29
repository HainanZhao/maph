# Agent instructions: maph (root)

This file is the shared instructions file for coding agents working
anywhere in this repository (`CLAUDE.md` and `GEMINI.md` at the repo
root are symlinks to this file — edit only this file). Individual
projects under `projects/*/` may have their own `AGENTS.md` for
project-specific knowledge; this file holds knowledge that's generic
across the whole repo, most notably **publishing research artifacts to
Zenodo**, since more than one project here produces a paper or
reproducibility archive.

## Repository layout

Independent research programs live under `projects/*/`, each
self-contained (see the root `README.md` for the current list and
`RESTRUCTURE-NOTE.md` for history). Projects share only repo history
and top-level ignore rules — no shared source, scripts, or CI. If a
project needs its own detailed instructions (e.g. a paper-publishing
procedure specific to its own build scripts), put them in that
project's own `AGENTS.md` and reference this file for the generic
parts, rather than duplicating this file's content per-project.

## Publishing a paper / reproducibility archive to Zenodo

This procedure was developed against `projects/sic-stark/` but nothing
in it is specific to that project — use it for any project's Zenodo
submission.

### Prerequisites and environment gotchas

- **Zenodo API token, never a password.** The user generates a
  Personal Access Token at
  `zenodo.org/account/settings/applications` (scopes `deposit:write` +
  `deposit:actions`) and sets it as an env var (e.g. `ZENODO_TOKEN` in
  their shell rc file). Never ask for or accept a Zenodo password.
  Never put the token in a URL query string (`?access_token=...`) —
  always `-H "Authorization: Bearer $ZENODO_TOKEN"`, so it can't leak
  into server logs.
- **GNU `find`/`tar` on macOS.** macOS ships BSD `find`/`tar`, which
  don't support GNU-only flags like `-regextype`/`-regex` or
  `--sort=name`/`--mtime` that a deterministic-archive build script is
  likely to use. Install and prepend to `PATH`:
  ```bash
  brew install findutils gnu-tar
  export PATH="/opt/homebrew/opt/findutils/libexec/gnubin:/opt/homebrew/opt/gnu-tar/libexec/gnubin:$PATH"
  ```
- **pdflatex on macOS.** Not present by default. `brew install --cask
  basictex` is much lighter than full MacTeX and has sufficed for
  every paper we've built this way (common packages — `amsmath`,
  `amssymb`, `amsthm`, `mathtools`, `geometry`, `hyperref`, `booktabs`
  — resolved with no extra `tlmgr install` needed). Its installer needs
  an interactive `sudo` password, so an agent can't install it —
  the user has to run `! brew install --cask basictex` themselves.
  After install: `eval "$(/usr/libexec/path_helper)"` or add
  `/Library/TeX/texbin` to `PATH`.
- **PARI/GP version pinning — read this if the project uses PARI/GP
  for exact certificates.** If a project's dependency lock file pins a
  specific PARI/GP version, take that seriously: certificate scripts
  often assert exact hardcoded values (polynomials, unit coordinates,
  etc.), and different PARI versions can legitimately pick different
  but mathematically equivalent generator conventions for the same
  object (we hit this for real in sic-stark: `bnrclassfield` returned
  `x^2 - y` under 2.15.4 vs. `x^2 - (y-1)` under 2.17.4 for the
  identical ray class field — provably the same field, since the two
  generators differ by a unit square, but a byte-for-byte test
  comparison fails). **Never "fix" a failing exact-value test by
  patching the expected value to match a newer tool's output without
  first proving the two outputs describe the same object** — that is
  exactly the kind of change that can silently launder a real error
  into a passing suite, or paper over a genuine one.

  Homebrew typically only ships the current release. Old versions are
  usually archived (for PARI/GP:
  `https://pari.math.u-bordeaux.fr/pub/pari/OLD/<branch>/pari-<version>.tar.gz`);
  build from source with `./Configure --prefix=<dir> && make install`.

  **On macOS/arm64, a natively-built PARI/GP 2.15.4 has a real,
  reproducible bug**: any script calling `default(parisize, N)` or
  `default(parisizemax, N)` silently truncates execution right after
  that call — `gp` exits 0 with no error and no further output, as if
  the rest of the script never existed. This traces into
  `gp_main_loop`'s stack-resize recovery path in PARI's `src/gp/gp.c` /
  `src/language/gplib.c` (the `longjmp` taken for `numerr < 0`, i.e.
  "stack size changed"), and does **not** reproduce on Linux/aarch64
  with the identical source — a platform-specific interaction, not a
  bug in whatever certificate scripts call it. Don't attempt a source
  patch: hand-patching a `longjmp`/buffer-lifecycle bug in a tool whose
  entire job is verifying exact-value math certificates risks a build
  that looks fine but silently computes (or drops) the wrong thing,
  which is the one failure mode to avoid above all others.

  **What works**: run the pinned version inside a Linux container. A
  `podman` (or `docker`) machine with a plain `debian` image is
  enough — build once per session:
  ```bash
  podman run -d --name simbuild -v "$PWD":/repo:ro debian:bookworm sleep infinity
  podman exec simbuild bash -c "apt-get update -qq && apt-get install -y -qq \
    build-essential wget libgmp-dev libreadline-dev python3 python3-pip \
    python3-numpy texlive-latex-base texlive-latex-recommended \
    texlive-latex-extra texlive-fonts-recommended poppler-utils >/tmp/apt.log 2>&1"
  podman exec simbuild bash -c "cd /tmp && wget -q \
    https://pari.math.u-bordeaux.fr/pub/pari/OLD/2.15/pari-2.15.4.tar.gz && \
    tar xzf pari-2.15.4.tar.gz && cd pari-2.15.4 && \
    ./Configure --prefix=/usr/local >/tmp/configure.log 2>&1 && \
    make -j4 >/tmp/build.log 2>&1 && make install >/tmp/install.log 2>&1"
  ```
  Copy a writable copy of the repo in (a read-only bind mount isn't
  enough if the build writes into the tree), run everything from
  there:
  ```bash
  podman exec simbuild bash -c "cp -r /repo /tmp/repo-rw"
  podman exec simbuild bash -c "cd /tmp/repo-rw && export PATH=/usr/local/bin:\$PATH && \
    PYTHONPATH=scripts python3 -m unittest discover -s tests -v"
  ```
  If a fully local workflow is preferred and the user accepts the
  tradeoff, a current Homebrew PARI/GP works natively and is fast, but
  any exact-match test failure must be hand-verified for mathematical
  equivalence (as above), not treated as pass/fail. Ask the user which
  they want rather than assuming — don't default to the heavier
  container path if they've asked for local-only, and don't default to
  local-only if a non-trivial version mismatch is in play; surface the
  tradeoff and let them pick.

### Reserve the DOI before finalizing the manuscript

Zenodo lets you create an empty deposit and get its DOI before
uploading anything — do this first so the DOI can be printed inside
the PDF itself (in a "reproducibility"/"data availability" section)
and in a `CITATION.cff`, rather than leaving a "DOI will be inserted
after deposit" placeholder:

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZENODO_TOKEN" \
  "https://zenodo.org/api/deposit/depositions" -d '{}'
# -> read .id and .metadata.prereserve_doi.doi from the response
```

If there are companion papers that cite each other, cross-reference
DOIs in both directions once all of them are reserved, then recompile
every affected manuscript **twice** (LaTeX cross-references need a
second pass) and confirm the DOI actually rendered, e.g.:
```bash
pdflatex -interaction=nonstopmode -halt-on-error paper/your-paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper/your-paper.tex
pdftotext paper/your-paper.pdf - | grep -A1 -B1 '10.5281/zenodo'
```

### Build and verify before uploading anything

- If the project has a deterministic-archive build script, build twice
  into separate output directories and `cmp` the results — they must
  be byte-identical. If they aren't, something non-deterministic
  (timestamps, file ordering, uid/gid) is leaking into the archive and
  must be fixed before this goes anywhere near Zenodo.
- **Run the test suite against the extracted archive, not just the
  live repo tree.** A file-selection pattern (e.g. "everything matching
  `dimension_six_*`") can miss a shared helper script from outside that
  pattern that something inside it imports — this only surfaces as a
  `ModuleNotFoundError` (or equivalent) once you've extracted the
  tarball in isolation, because the live repo has every file so
  nothing looks missing until then.

### Upload, in this order: metadata → archive → standalone reader files

```bash
BUCKET=<links.bucket from the reserved deposit>
DEP_ID=<the deposit id>

# metadata
curl -X PUT -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ZENODO_TOKEN" \
  "https://zenodo.org/api/deposit/depositions/$DEP_ID" \
  -d "{\"metadata\": $(cat path/to/zenodo-metadata.json)}"

# the reproducibility archive
curl -X PUT --upload-file dist/your-archive.tar.gz \
  -H "Authorization: Bearer $ZENODO_TOKEN" "$BUCKET/your-archive.tar.gz"

# ALSO upload a standalone PDF (and source, e.g. .tex) as separate
# top-level files -- Zenodo can preview a PDF in-browser, but only for
# a file uploaded at the top level, not one sitting inside a tar.gz.
# Skipping this means every reader has to download and extract the
# archive just to read the paper.
curl -X PUT --upload-file paper/your-paper.pdf \
  -H "Authorization: Bearer $ZENODO_TOKEN" "$BUCKET/your-paper.pdf"
curl -X PUT --upload-file paper/your-paper.tex \
  -H "Authorization: Bearer $ZENODO_TOKEN" "$BUCKET/your-paper.tex"
```

**Verify every upload before publishing**: the upload response's
`checksum` (md5) must match the local file's md5 exactly (`md5 -q
<file>` on macOS, `md5sum <file>` on Linux). Never trust an upload
without this check — treat a mismatch as a hard stop, not a warning.

**Zenodo's API returns intermittent `504 Gateway Time-out` even on
writes that actually succeeded.** On a timeout, poll with a plain `GET`
on the deposition a few seconds later before assuming the write
failed — don't blindly retry a mutating call without checking state
first, or you risk double-creating something.

### Publish

```bash
curl -X POST -H "Authorization: Bearer $ZENODO_TOKEN" \
  "https://zenodo.org/api/deposit/depositions/$DEP_ID/actions/publish"
```

**This is irreversible** — the record becomes permanent and public
under the DOI. Confirm explicitly with the user before calling this,
every single time, even if they approved a previous paper's publish
earlier in the same conversation. Always show them the draft's files,
metadata, and verified checksums first, and let them look at the draft
URL themselves if they want to.

### Adding or fixing files after publishing

A published deposition is read-only. To add or change files (e.g. the
standalone-PDF fix above, applied after an initial archive-only
publish), create a new version first:

```bash
curl -X POST -H "Authorization: Bearer $ZENODO_TOKEN" \
  "https://zenodo.org/api/deposit/depositions/$DEP_ID/actions/newversion"
# -> follow links.latest_draft to the new draft id, which starts as a
#    copy of the previous version's files
```

Upload/replace files on the new draft's bucket, verify checksums, then
publish it the same way. The old version stays intact and citable; the
concept DOI (`conceptdoi` on the published record) always resolves to
the latest version. If a manuscript's own text cites a specific version
DOI (the exact archive it was built and hash-verified against), that's
fine to leave pointing at that version rather than bumping it forward —
Zenodo's version selector and the concept DOI both make the latest
version reachable regardless.

## Watch for concurrent/automated changes to a project you're working in

At least one project in this repo (`sic-stark`) has had commits land
mid-session from a git identity that isn't the interactive session's
configured user — meaning something else (a scheduled job, another
agent, a cron-driven research loop) is actively committing and pushing
to this exact repository outside of any given conversation. Before
trusting that a project's working tree reflects only your own edits,
or before publishing anything from it, check:
```bash
git log --format='%h %ad %an <%ae> %s' --date=iso -10
git fetch && git log HEAD..origin/main --oneline
```
If you find commits you didn't make, from an unfamiliar identity, or
that change the scope of something already published — stop and
surface it to the user rather than silently building on top of it or
silently reconciling it yourself.

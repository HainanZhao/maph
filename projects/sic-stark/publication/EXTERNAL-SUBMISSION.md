# External submission handoff

The mathematical and local artifact gates are closed. The remaining
actions require the author's Zenodo and arXiv accounts and must not be
represented as complete until those services return identifiers.

## Zenodo

Create two records, one for each submission-specific reproducibility
archive:

| Paper | File | Metadata |
|---|---|---|
| I | `dist/sic-stark-paper-I.tar.gz` | `publication/paper-I-zenodo.json` |
| II | `dist/sic-stark-paper-II.tar.gz` | `publication/paper-II-zenodo.json` |

Reserve each DOI before publication. Insert the Paper-II DOI in Paper
I's companion-paper citation and insert each archive DOI in its own
reproducibility section and `CITATION.cff`. Recompile both papers,
rebuild both archives twice, rerun `tests/test_companion_archives.sh`,
and upload those final bytes. Publish only after the uploaded hashes
match the final local hashes.

## arXiv

Build the source-only submissions:

```bash
scripts/build_arxiv_submissions.sh
bash tests/test_arxiv_submissions.sh
```

Suggested primary category for both papers: `math.NT`. Suggested
cross-list: `quant-ph`.

Upload:

- `dist/sic-stark-paper-I-arxiv.tar.gz`;
- `dist/sic-stark-paper-II-arxiv.tar.gz`.

Use the titles and abstracts embedded in `main.tex`. Add each returned
arXiv identifier to the corresponding Zenodo record and citation file.

## Correspondence

After both arXiv pages and both archive DOIs resolve, replace the four
bracketed link placeholders in `docs/kopp-correspondence-draft.md`.
The author must review and send the message; no external email has
been sent by the build process.

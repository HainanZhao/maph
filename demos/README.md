# maph research demos

This directory is the single GitHub Pages application for the repository.
Each project may expose one or more independent pages at:

```text
demos/<project>/<demo>/index.html
demos/<project>/<demo>/src/...
```

Register every public page in `src/catalog.ts` and add its HTML entry to
`vite.config.ts`. The root index is the public catalogue. The shared GitHub
Actions workflow installs, tests, builds, and deploys the complete site.

Local commands:

```bash
cd demos
npm ci
npm test
npm run dev
npm run build
```

GitHub Pages builds set `BASE_PATH=/<repository-name>/`; local development
uses `/`. The CI build runs on every relevant push. Once GitHub Pages is
available for the repository, set the repository variable
`ENABLE_GITHUB_PAGES=true` to enable the upload/deploy jobs. Never present an
extrapolated benchmark point as measured data.

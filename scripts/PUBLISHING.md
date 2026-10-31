# Publishing notes (editors)

- One folder per issue and article: `v15i1/214/index.html` is served at `https://articles.wskw.org/v15i1/214/`.
- To add or update an article: `scripts/publish.sh 2026 214 "short note"`. It copies the
  article's published HTML from `jkw-manuscripts`, rebuilds the index page, commits and pushes.
  The change is live about a minute later.
- Only published articles go here; this repository is public. Content changes to a published
  article need a correction notice in OJS.

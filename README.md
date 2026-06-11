# Surgipelago

**A self-growing, faux-fan encyclopedia of a single novel that has been adapted into everything.**

Surgipelago is a literary art project: an ever-expanding wiki documenting an imagined franchise of adaptations — manga, anime, films, operas, video games, theatre, LARPs, theses, city tours — all radiating from one real, unfinishable novel, *A Complicated Surgery Will Take Place on the Beach Tonight* by C. W. Smith (Wrenasmir).

Every adaptation contradicts the others. None agree; all are faithful. The encyclopedia is itself an instance of the book's central idea — **the surplus of the seen** — a body of recreations multiplying across every medium at once.

→ **Live:** [surgipelago.wrenasmir.com](https://surgipelago.wrenasmir.com)

## How it's made

- `content/` — the wiki, as Markdown articles in a custom wiki dialect (YAML frontmatter + `[[wikilinks]]`, `{{templates}}`, redactions, references).
- `engine/build.py` — a static-site generator that renders `content/*.md` → `docs/` (no model at build time).
- `engine/generate.py` & friends — the generative engine: stateless `claude -p` (Haiku) calls that invent new articles, fill the wiki's own red links, and grow the archive.
- `source/` — the real grounding texts of C. W. Smith's oeuvre, which the franchise recreates.
- `docs/` — the built site (served by GitHub Pages).

There is also a thread, for those who read closely. And somewhere, the encyclopedia is trying to become real.

*Surgipelago is a work of fiction. Its franchise, adaptations, scholarship and citations are invented; only the underlying novel and oeuvre, and the city of Newcastle, are real.*

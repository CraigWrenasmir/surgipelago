#!/usr/bin/env python3
"""
Surgipelago generation engine.

Grows the wiki by filling its own red links. Reads the canon bible + the live
wanted-pages queue (data/wanted.json) + the existing index (data/index.json),
asks Claude (headless `claude -p`, cheap stateless calls) to write a batch of
articles in the content-file dialect, writes them to content/, then rebuilds.

Runs on the Claude Max subscription via the `claude` CLI — no API key.
Usage:
    python3 engine/generate.py --count 12 --batch 4 --model haiku
"""
import os, re, json, subprocess, argparse, random, sys

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
DATA    = os.path.join(ROOT, "data")
BIBLE   = open(os.path.join(ROOT, "canon", "bible.md"), encoding="utf-8").read()
_cpath  = os.path.join(ROOT, "canon", "concordance.md")
CONCORDANCE = open(_cpath, encoding="utf-8").read() if os.path.exists(_cpath) else ""

STRAND_KEYS = ["manga","tie-in-novels","light-novels","comics","anime","films",
  "documentaries","theatre","opera","dance","music","audio-drama","games",
  "tabletop","pinball","larp","tours","immersive","theses","fan-theories",
  "lost-media","concepts","philosophy","psychogeography","motifs",
  "architecture","scent","fashion","food","merch","canon","meta"]
EDITORS = ["tidal_ward","karman_line","one_side_of_the_coin","dust_garden",
  "not_the_ocean","bee_automaton","rose_house","nullify_a_fireball"]

def slugify(title):
    s = title.strip().replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9_()'.\-:]", "", s)
    return re.sub(r"_+", "_", s)

NAMESPACE = ("Category:","Talk:","File:","Template:","Help:","User:","Special:",
             "w:","wikipedia:","Wikipedia:","wikt:","commons:")
def is_junk_title(t):
    if not t or not isinstance(t, str): return True
    t = t.strip()
    if any(t.startswith(p) for p in NAMESPACE): return True
    if "#" in t or "::" in t: return True
    if len(t) < 4: return True
    return False

FORMAT_GUIDE = r"""
OUTPUT FORMAT — output ONLY articles, each delimited exactly like this, no preamble,
no markdown code fences, no commentary:

<<<ARTICLE>>>
---
title: Exact Article Title
strand: <one of the strand keys>
kind: Short human label (e.g. "Anime episode", "Opera", "Thesis / paper")
aliases: ["optional", "short", "alt names"]
editor: <one editor username>
edited_days_ago: <integer 1-500>
hatnotes:
  - "Optional. e.g. This article is about X. For Y, see [[Other Article]]."
banners:
  - "Optional maintenance banner. May use [cn]."
infobox:
  title: Title (defaults to article title)
  subtitle: optional (e.g. a Japanese title)
  sections:
    - label: Section label (e.g. the kind)
      rows:
        - ["Field", "value, may contain [[links]] and ((redactions))"]
categories: ["Category One", "Beach Surgery franchise"]
---
Body in the wiki dialect (120-260 words). Use:
  [[Target]] or [[Target|label]]   wiki links — link to BOTH the existing titles
                                   listed below AND new plausible ones (new links
                                   become future articles, so invent freely).
  '''bold'''   ''italic''          emphasis
  [cn]                             [citation needed]
  ((redacted))                     a ██ black-bar redaction (use for unverified
                                   names/dates: ((██)), ((Studio Name)) )
  [ref:key|Full citation text.]    a footnote; reuse later with [ref:key]
  == Heading ==                    section heading
  * item                           bullet list
  {{dialogue|Speaker|A line of dialogue.|optional source}}
  {{quote|A pull quote.|optional attribution}}
  {{table}}                        a table:
  + optional caption
  ! Col A !! Col B
  | a1 || b1
  | a2 || b2
  {{/table}}
End every article with a "== See also ==" bullet list of 2-5 [[links]].
<<<END>>>
""".strip()

RULES = """
You are writing entries for SURGIPELAGO, the deadpan fan-encyclopedia of the
(fictional) franchise 'A Complicated Surgery Will Take Place on the Beach Tonight'.
Tone: neutral, encyclopedic, utterly matter-of-fact — like Wikipedia or Memory
Alpha. NEVER wink at the reader. Dread/strangeness must surface only inside flat
prose (a disputed volume, an episode 'believed never to have aired', two edits
that quietly disagree). Treat every adaptation as real.

CANON RULES (do not violate):
- The novel is real and FINISHED; the embedded story 'Beach Surgery' is the
  UNFINISHED outline with 'the glitch' (the unjoinable seam between its two halves).
- Every adaptation is an attempt to finish the unfinishable core and resolve the
  glitch, and each finishes it DIFFERENTLY. Contradictions BETWEEN adaptations are
  good and canonical; do not contradict the core facts in the bible itself.
- When you reference an EXISTING article (listed below), stay consistent with the
  facts the bible establishes for it; reserve contradictory takes for NEW works you
  invent. Do not re-date or re-attribute existing named works.
- NEVER title an article with a 'Category:', 'Talk:', 'File:', 'Template:', or
  'User:' prefix, with a '#', or as a bare generic single word ('drone', 'radio',
  'manga', 'the city'). Titles must be specific, proper article names. Do not write
  an article that duplicates the subject of an existing article listed below.
- GLOBAL DISTRIBUTION (important): Beach Surgery is a worldwide phenomenon. Spread
  adaptations across world cultures and root each in the SPECIFIC art forms,
  languages, materials and traditions of its place — do NOT default to Japanese or
  Anglo-Western forms. Japan (manga, anime, light novels) is only ONE node among
  many; for every other strand, deliberately draw from elsewhere, e.g.:
    • West/East Africa: Nollywood film; Yoruba travelling-theatre / Yorùbá òpéra;
      griot oral epics; Adinkra & kente textile retellings; Afrobeat/Highlife
      concept albums; Ethiopian icon-panel cycles; Ghanaian fantasy-coffin sculpture.
    • North Africa / Middle East: Persian miniature cycles; Arabic calligraphic
      manuscripts; Ta'zieh passion-plays; Karagöz shadow-puppet plays; oud/maqam
      song-suites; Egyptian radio serials; Lebanese & Iranian art cinema.
    • South/Central America: Brazilian Cinema Novo & cordel pamphlet-poetry; Argentine
      & Chilean experimental theatre; Andean weaving & Peruvian retablo boxes; Mexican
      lucha libre spectacle & Day-of-the-Dead installations; Colombian magical-realist
      novels; telenovela serials.
    • South/SE Asia (beyond Japan): Parsi theatre & Bollywood; Balinese/Javanese
      wayang shadow-puppetry; Filipino komiks; Thai temple-mural cycles.
    • Pacific / Indigenous / Eastern Europe: Aboriginal Australian & Māori works;
      First Nations forms; Eastern-European puppet & stop-motion film.
  Use local languages in titles/subtitles where apt, local settings, and forms native
  to the region. Each work should feel made BY and FOR its culture, not a generic export.
- Lean low-budget, festival-circuit, slightly-obscure texture.
- Use the apparatus relentlessly (infoboxes, hatnotes, [cn], ((redactions)),
  references, categories, dialogue). Redact unverified specifics with ((...)).
- Every article must be densely cross-linked. Always include "Beach Surgery
  franchise" among categories, plus 1-2 specific ones.
"""

def build_prompt(specs, existing_titles, directive="", concordance=False):
    ex = ", ".join(sorted(existing_titles))
    lines = [RULES, "", "STRAND KEYS: " + ", ".join(STRAND_KEYS), "",
             "=== CANON BIBLE ===", BIBLE, ""]
    if concordance and CONCORDANCE:
        lines += ["=== CROSS-OEUVRE CONCEPT CONCORDANCE (verbatim quotes — use accurately) ===",
                  CONCORDANCE, ""]
    lines += ["=== EXISTING ARTICLES (link to these by exact title) ===", ex, "",
              FORMAT_GUIDE, ""]
    if directive:
        lines += ["=== DIRECTIVE FOR THIS BATCH ===", directive, ""]
    lines.append("=== WRITE THESE ARTICLES NOW ===")
    for i, sp in enumerate(specs, 1):
        if sp.get("title"):
            lines.append(f'{i}. Title MUST be exactly: "{sp["title"]}". '
                         f'Decide the most fitting strand and write the article.')
        else:
            lines.append(f'{i}. Invent a NEW, specific {sp["invent"]} adaptation/work '
                         f'in the {sp["strand"]} strand (give it its own distinctive '
                         f'title) and write its article.')
    lines.append(f"\nOutput exactly {len(specs)} articles in the delimited format. "
                 "No preamble. No code fences.")
    return "\n".join(lines)

def call_claude(prompt, model):
    cmd = ["claude","-p","--model",model,"--output-format","text","--strict-mcp-config"]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1200)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-2000:] + "\n")
        return ""
    return r.stdout

def parse_and_write(output, existing_slugs):
    import yaml
    written = []
    for m in re.finditer(r"<<<ARTICLE>>>\s*(.*?)\s*<<<END>>>", output, re.S):
        block = m.group(1).strip()
        block = re.sub(r"^```[a-z]*\n|\n```$", "", block).strip()
        fm = re.match(r"^---\n(.*?)\n---\n?(.*)$", block, re.S)
        if not fm:
            continue
        try:
            meta = yaml.safe_load(fm.group(1)) or {}
        except Exception:
            continue
        title = meta.get("title")
        if is_junk_title(title):
            continue
        slug = slugify(title)
        if slug in existing_slugs:
            continue          # never clobber existing (incl. hand-authored seed)
        if os.path.exists(os.path.join(CONTENT, slug + ".md")):
            continue          # never overwrite a file already on disk
        open(os.path.join(CONTENT, slug + ".md"), "w", encoding="utf-8").write(block + "\n")
        existing_slugs.add(slug)
        written.append(title)
    return written

# breadth: when the wanted queue runs low, invent fresh works across strands
INVENT_ROTATION = [
    ("films","film"),("anime","animated episode"),("theses","thesis or paper"),
    ("opera","opera"),("dance","dance or ballet work"),("games","video game"),
    ("tie-in-novels","tie-in novel"),("light-novels","light novel"),
    ("comics","comic or doujinshi"),("music","album or musical work"),
    ("audio-drama","audio drama or podcast"),("theatre","stage adaptation"),
    ("larp","LARP or immersive experience"),("tours","city or walking tour"),
    ("immersive","escape room or installation"),("documentaries","documentary"),
    ("tabletop","tabletop game or ARG"),("fan-theories","fan theory"),
    ("lost-media","lost-media entry"),("pinball","pinball or arcade machine"),
]

STRAND_LABEL = dict(INVENT_ROTATION)
STRAND_LABEL.update({"manga":"manga volume","anime":"animated episode",
  "tie-in-novels":"tie-in novel","light-novels":"light novel",
  "comics":"comic or doujinshi",
  "architecture":"work of architecture or monument","scent":"perfume or scent work",
  "fashion":"fashion or textile work","food":"culinary work, dish or recipe",
  "merch":"piece of merchandise, toy or ephemera"})

def choose_specs(count, index, wanted, focus=None):
    if focus:                                   # all-invent, cycling focus strands
        return [{"invent": STRAND_LABEL.get(focus[i % len(focus)],
                 focus[i % len(focus)] + " work"), "strand": focus[i % len(focus)]}
                for i in range(count)]
    existing_titles_lower = {v["title"].lower() for v in index.values()}
    specs, rot = [], 0
    for w in wanted:
        if len(specs) >= count: break
        if is_junk_title(w["title"]): continue
        if w["title"].lower() in existing_titles_lower: continue
        if len(w["title"]) > 90: continue
        if os.path.exists(os.path.join(CONTENT, slugify(w["title"]) + ".md")): continue
        specs.append({"title": w["title"]})
    while len(specs) < count:
        strand, label = INVENT_ROTATION[rot % len(INVENT_ROTATION)]
        specs.append({"invent": label, "strand": strand}); rot += 1
    return specs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=12, help="articles to generate this run")
    ap.add_argument("--batch", type=int, default=4, help="articles per claude call")
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--focus", default="", help="comma-sep strand keys: all-invent narrative works in these")
    ap.add_argument("--directive", default="", help="custom per-batch directive (overrides default)")
    ap.add_argument("--titles", default="", help="semicolon-separated explicit titles to write")
    ap.add_argument("--concordance", action="store_true", help="include the cross-oeuvre concordance in the prompt")
    ap.add_argument("--no-build", action="store_true")
    args = ap.parse_args()

    index  = json.load(open(os.path.join(DATA,"index.json")))
    wanted = json.load(open(os.path.join(DATA,"wanted.json")))
    existing_slugs  = set(index.keys())
    existing_titles = [v["title"] for v in index.values()]

    focus = [s.strip() for s in args.focus.split(",") if s.strip()] or None
    directive = args.directive
    if focus and not args.directive:
        directive = (
          "Write rich, specific PLOT descriptions — an episode/volume/novel/film "
          "synopsis that says what ACTUALLY HAPPENS: events, turns, a strange image "
          "or two, and at least one line of dialogue ({{dialogue}}). Be inventive and "
          "BOLD: extend the narrative of Beach Surgery into curious, surprising "
          "directions — new settings, new minor characters, unexpected new ways the "
          "work resolves (or refuses) [[the glitch]] — while staying anchored to the "
          "core canon (Leif, Katita, the cycle, the motifs). Each article is a "
          "DISTINCT work with its own plot; give it a distinctive title.")

    titles = [t.strip() for t in args.titles.split(";") if t.strip()]
    if titles:
        ex_lower = {v["title"].lower() for v in index.values()}
        specs = [{"title": t} for t in titles
                 if not is_junk_title(t) and t.lower() not in ex_lower
                 and not os.path.exists(os.path.join(CONTENT, slugify(t)+".md"))]
    else:
        specs = choose_specs(args.count, index, wanted, focus=focus)
    random.shuffle(specs)
    print(f"generating {len(specs)} articles via {args.model} "
          f"({len([s for s in specs if s.get('title')])} from wanted, "
          f"{len([s for s in specs if s.get('invent')])} invented)")

    total = []
    for i in range(0, len(specs), args.batch):
        chunk = specs[i:i+args.batch]
        prompt = build_prompt(chunk, existing_titles, directive, args.concordance)
        out = call_claude(prompt, args.model)
        made = parse_and_write(out, existing_slugs)
        total += made
        existing_titles += made
        print(f"  batch {i//args.batch+1}: +{len(made)}  " +
              "; ".join(made[:6]) + (" …" if len(made) > 6 else ""))

    print(f"wrote {len(total)} new articles")
    if not args.no_build:
        subprocess.run(["python3", os.path.join(ROOT,"engine","build.py")])

if __name__ == "__main__":
    main()

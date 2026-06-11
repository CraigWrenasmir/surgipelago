#!/usr/bin/env python3
"""Generate grounded articles for the real Newcastle places in the atlas
gazetteer. Reads the inline GAZ array from assets/map/newcastle-map.html (the
single source of truth, with real per-work context + verbatim quotes), skips any
place that already resolves to an existing article, and writes the rest into the
'gazetteer' strand. Deterministic — no model, no fabrication; every quote is the
one extracted from the source texts. Re-runnable (won't clobber existing files)."""
import os, re, ast, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import build

MAP = os.path.join(ROOT, "assets", "map", "newcastle-map.html")
CONTENT = os.path.join(ROOT, "content")
WIKI = os.path.join(ROOT, "docs", "wiki")

WORK_TITLE = {
 "novel":   "A Complicated Surgery Will Take Place on the Beach Tonight",
 "antinom": "Antinomicity",
 "pastoral":"Pastoral Scanlines",
 "disjecta":"Fellow Disjecta",
 "everyone":"Everyone I Love is Alive in the Unlimited Present of the City and its Waters",
}
WORK_SHORT = {"novel":"A Complicated Surgery…","antinom":"Antinomicity","pastoral":"Pastoral Scanlines",
              "disjecta":"Fellow Disjecta","everyone":"Everyone I Love…"}
CAT_LABEL = {"cbd":"city & civic","coast":"coastal","harbour":"harbour & industry",
             "suburb":"suburb & rail","region":"regional"}
EDITORS = ["rose_house","one_side_of_the_coin","dust_garden","karman_line","tidal_ward"]

# --- parse the inline GAZ array ---
html = open(MAP, encoding="utf-8").read()
m = re.search(r"const GAZ = \[(.*?)\n\];", html, re.S)
raw = "[" + m.group(1) + "\n]"
raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)        # strip JS block comments
# quote barewords keys (only right after { or ,) so ast can read it as a literal
raw = re.sub(r"([{,]\s*)(id|name|real|lat|lng|cat|conf|w)\s*:", r'\1"\2":', raw)
GAZ = ast.literal_eval(raw)
print(f"parsed {len(GAZ)} gazetteer entries")

# --- resolver: skip places that already have an article ---
arts = build.load_articles()
ALIAS = {}
for slug, a in arts.items():
    ALIAS[build.normkey(a["title"])] = slug
    for al in a.get("aliases", []) or []:
        ALIAS.setdefault(build.normkey(al), slug)
def exists(slug): return slug and os.path.exists(os.path.join(WIKI, slug + ".html"))
def already(entry):
    for c in [entry["name"], re.sub(r"\s*\(.*?\)", "", entry["name"]).strip(),
              entry["name"].split(",")[0].strip(), entry.get("real","")]:
        s = ALIAS.get(build.normkey(c))
        if s and (s in arts): return s
    return None

def esc_q(s): return s.replace('"', "'")

def article(entry, idx):
    name, real = entry["name"], entry.get("real","")
    cat, conf, works = entry["cat"], entry.get("conf"), entry["w"]
    region = cat == "region"
    where = ("in the wider Hunter region beyond [[Newcastle]]" if region
             else "in [[Newcastle]], New South Wales")
    wkeys = []
    for w in works:
        if w[0] not in wkeys: wkeys.append(w[0])
    worklinks = " · ".join(f"''[[{WORK_TITLE[k]}|{WORK_SHORT[k]}]]''" for k in wkeys)

    fm = ["---", f"title: {name}", "strand: gazetteer", "kind: Real location",
          f"editor: {EDITORS[idx % len(EDITORS)]}"]
    if conf:
        fm.append("banners:")
        fm.append('  - "The identification or placement of this location is an interpretive reading, '
                  'not stated outright in the text. [cn]"')
    fm += ["infobox:", f"  title: {esc_q(name)}", "  sections:",
           "    - label: Real location", "      rows:",
           f'        - ["Place", "{esc_q(real)}"]',
           f'        - ["Where", "{ "Hunter region, NSW" if region else "[[Newcastle]], NSW" }"]',
           f'        - ["Coordinates", "{entry["lat"]:.4f}, {entry["lng"]:.4f}"]',
           f'        - ["Named in", "{esc_q(worklinks)}"]']
    fm += ['categories: ["Newcastle", "Real-world locations", "Newcastle gazetteer", "Beach Surgery franchise"]',
           "---"]

    body = []
    lead = (f"'''{name}''' is a real location {where}, named across the written works of "
            f"[[C. W. Smith]].")
    if real: lead += f" {real}."
    lead += (f" It is plotted on the [[Newcastle#The Literary Atlas of Newcastle|Literary Atlas of "
             f"Newcastle]] among the city's {CAT_LABEL.get(cat,'')} sites.")
    body.append(lead)

    body.append("\n== Across the works ==")
    for k in wkeys:
        body.append(f"\n=== {WORK_SHORT[k]} ===")
        for w in works:
            if w[0] != k: continue
            ctx, q = (w[1] or "").strip(), (w[2] or "").strip()
            if ctx: body.append(ctx)
            if q: body.append("{{quote|" + q + "|''" + WORK_SHORT[k] + "''}}")

    body.append("\n== See also ==")
    see = ["[[Newcastle]]"] + [f"''[[{WORK_TITLE[k]}|{WORK_SHORT[k]}]]''" for k in wkeys]
    body.append("* " + " · ".join(see))
    body.append("* The [[Newcastle#The Literary Atlas of Newcastle|Literary Atlas of Newcastle]]")

    return "\n".join(fm) + "\n" + "\n".join(body) + "\n"

made = skipped = 0
for idx, entry in enumerate(GAZ):
    hit = already(entry)
    slug = build.slugify(entry["name"])
    if hit or os.path.exists(os.path.join(CONTENT, slug + ".md")):
        skipped += 1; continue
    open(os.path.join(CONTENT, slug + ".md"), "w", encoding="utf-8").write(article(entry, idx))
    print(f"  + {entry['name']}")
    made += 1

print(f"\nwrote {made} gazetteer articles, skipped {skipped} (already had one). Rebuild.")

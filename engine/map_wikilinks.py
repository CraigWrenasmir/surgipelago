#!/usr/bin/env python3
"""Resolve each Newcastle-atlas pin to an existing wiki article and inject a
WIKI = {pin_id: slug} map into assets/map/newcastle-map.html.

Uses build.py's own slugify/normkey + the article/alias index, so a pin links to
the same page its [[wikilink]] would. Pins with no matching article are left
unlinked (no dead links). Re-runnable; rewrites the WIKI const each time."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP  = os.path.join(ROOT, "assets", "map", "newcastle-map.html")
WIKI_DIR = os.path.join(ROOT, "docs", "wiki")

# Build the alias map exactly as build.main() does.
arts = build.load_articles()
ALIAS = {}
for slug, a in arts.items():
    ALIAS[build.normkey(a["title"])] = slug
    for al in a.get("aliases", []) or []:
        ALIAS.setdefault(build.normkey(al), slug)

def exists(slug):
    return slug and os.path.exists(os.path.join(WIKI_DIR, slug + ".html"))

# Hand-tuned candidates for pins whose article title differs from the pin name.
OVERRIDES = {
    "newcastle-beach": ["the beach", "the public baths"],
    "bolton-carpark": ["Bolton Street car park"],
    "the-watt": ["the Watt Hotel", "The Watt"],
    "dampened-cardboard": ["the Dampened Cardboard", "Dampened Cardboard"],
    "donut": ["Newcastle City Hall", "the council headquarters"],
    "harbour": ["Newcastle"],
    "coal-terminal": ["Carrington coal loader", "the coal loader"],
    "obelisk": ["the Obelisk"],
    "nobbys-breakwall": ["the breakwall", "Nobbys breakwall"],
    "ocean-baths": ["Newcastle Ocean Baths", "the public baths"],
}

# Parse pins: each begins '{id:"x", name:"y", real:"z", ...'
pins = re.findall(r'\{id:"([^"]+)",\s*name:"([^"]+)",\s*real:"([^"]+)"', open(MAP, encoding="utf-8").read())

def candidates(pid, name, real):
    cands = list(OVERRIDES.get(pid, []))
    cands += [name, re.sub(r"^the\s+", "", name, flags=re.I), real]
    # strip parentheticals like "Stockton (suburb)" / trailing qualifiers
    cands.append(re.sub(r"\s*\(.*?\)", "", name).strip())
    cands.append(name.split(",")[0].strip())
    return cands

resolved = {}
unresolved = []
for pid, name, real in pins:
    hit = None
    for c in candidates(pid, name, real):
        slug = ALIAS.get(build.normkey(c))
        if exists(slug):
            hit = slug; break
        # also try a direct slugify of the candidate
        s2 = build.slugify(c)
        if exists(s2):
            hit = s2; break
    if hit:
        resolved[pid] = hit
    else:
        unresolved.append((pid, name))

# Inject WIKI map.
items = ",\n  ".join(f'"{pid}":"{slug}"' for pid, slug in sorted(resolved.items()))
block = "const WIKI = {\n  " + items + "\n};" if items else "const WIKI = {};"
html = open(MAP, encoding="utf-8").read()
html = re.sub(r"const WIKI = \{.*?\};", block, html, count=1, flags=re.S)
open(MAP, "w", encoding="utf-8").write(html)

print(f"linked {len(resolved)}/{len(pins)} pins")
if unresolved:
    print("unlinked:")
    for pid, name in unresolved:
        print(f"  {pid:22} {name}")

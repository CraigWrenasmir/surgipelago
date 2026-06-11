#!/usr/bin/env python3
"""Curated second-pass dedup: explicit (keeper -> losers) by exact title, so the
keeper choice is hand-controlled (e.g. keep the Ideas-strand concept page even if
a canon stub is longer). Folds loser titles+aliases into the keeper, deletes the
loser content + docs html. Skips anything already gone. Rebuild afterwards.

Only same-subject pairs are listed here; every cross-media namesake
(Surplus of the Seen novel vs concept, The Suture film vs suture motif, the
manga/anime/opera adaptation pages, etc.) is deliberately omitted and left intact.
"""
import os, re, glob, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
WIKI    = os.path.join(ROOT, "docs", "wiki")
import sys; sys.path.insert(0, os.path.join(ROOT, "engine"))
import build

# (keeper_title, [loser_titles])
PLAN = [
    # --- embedded Beach Surgery chapters: standardise on digit form ---
    ("Chapter 1", ["Chapter One"]),
    ("Chapter 2", ["Chapter Two"]),
    ("Chapter 4", ["Chapter Four (the interior)"]),
    ("Chapter 5", ["Chapter Five"]),
]

def norm(t): return re.sub(r"[^a-z0-9]", "", t.lower())

# index every content file by exact title
bytitle = {}
for path in sorted(glob.glob(os.path.join(CONTENT, "*.md"))):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
    if not m: continue
    meta = yaml.safe_load(m.group(1)) or {}
    t = meta.get("title")
    if not t: continue
    bytitle[t] = {"path": path, "aliases": meta.get("aliases") or [],
                  "strand": meta.get("strand",""), "slug": build.slugify(t)}

merged = 0
for keeper_t, losers in PLAN:
    k = bytitle.get(keeper_t)
    if not k:
        print(f"  ! keeper missing, skip: {keeper_t!r}"); continue
    present = [(lt, bytitle[lt]) for lt in losers if lt in bytitle]
    if not present:
        print(f"  · nothing to merge into {keeper_t!r} (losers already gone)"); continue
    ktext = open(k["path"], encoding="utf-8").read()
    have = {norm(keeper_t)} | {norm(a) for a in k["aliases"]}
    add = []
    for lt, _ in present:
        rec = bytitle[lt]
        for cand in [lt, *rec["aliases"]]:
            if norm(cand) not in have:
                have.add(norm(cand)); add.append(cand)
    if add:
        cur = k["aliases"] + add
        line = "aliases: [" + ", ".join('"' + a.replace('"', "'") + '"' for a in cur) + "]"
        if re.search(r"^aliases:.*$", ktext, flags=re.M):
            ktext = re.sub(r"^aliases:.*$", line, ktext, count=1, flags=re.M)
        else:
            ktext = re.sub(r"^(title:.*)$", r"\1\n" + line, ktext, count=1, flags=re.M)
        open(k["path"], "w", encoding="utf-8").write(ktext)
    for lt, rec in present:
        os.remove(rec["path"])
        h = os.path.join(WIKI, rec["slug"] + ".html")
        if os.path.exists(h): os.remove(h)
        print(f"  merged {lt!r}  ->  {keeper_t!r}  [{k['strand']}]")
        merged += 1

print(f"\nmerged {merged} article(s) across {len(PLAN)} groups. Rebuild to regenerate the index.")

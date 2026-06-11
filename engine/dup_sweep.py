#!/usr/bin/env python3
"""Find near-duplicate articles whose titles collide once normalised.

CRITICAL: parenthetical qualifiers are SUBJECT-BEARING in this wiki — "(anime)",
"(manga)", "(opera)", "(game)", "(volume)" are distinct adaptations of the same
title and must NEVER be merged. So the match key KEEPS parenthetical content.
Only titles differing purely by a leading article (the/a/an) and case/punctuation
are treated as true duplicates.

Tiers:
  A  auto-mergeable: identical key (leading-article/case/punct only)  -> --merge resolves
  B  review only: collide only after folding singular/plural
  C  review only: a bare title coexists with parenthetical variant(s) sharing the
     same parens-stripped base (usually intentional different media — listed so a
     genuine dup can be spotted; never auto-merged)

--merge resolves TIER A only: keep the fullest article (longest body, then
infobox, then alias count), fold losers' titles+aliases into the keeper's
aliases, delete loser files. Re-runnable; rebuild afterwards.
"""
import os, re, sys, glob, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import build

CONTENT = os.path.join(ROOT, "content")
WIKI    = os.path.join(ROOT, "docs", "wiki")
MERGE   = "--merge" in sys.argv

def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())

def key(t):                                       # leading article + case/punct only (KEEP parens)
    s = re.sub(r"^(the|a|an)\s+", "", t.lower().strip())
    return re.sub(r"[^a-z0-9]", "", s)

def pluralkey(t):
    return re.sub(r"s$", "", key(t))

def naked(t):                                     # parens stripped (for tier C review)
    s = re.sub(r"\(.*?\)", "", t.lower())
    s = re.sub(r"^(the|a|an)\s+", "", s.strip())
    return re.sub(r"[^a-z0-9]", "", s)

def has_paren(t): return "(" in t

arts = []
for path in sorted(glob.glob(os.path.join(CONTENT, "*.md"))):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
    if not m: continue
    meta = yaml.safe_load(m.group(1)) or {}
    title = meta.get("title")
    if not title: continue
    body = m.group(2).strip()
    arts.append({"path":path, "title":title, "slug":build.slugify(title),
        "aliases":meta.get("aliases") or [], "strand":meta.get("strand",""),
        "blen":len(body), "has_ib":bool(meta.get("infobox")),
        "key":key(title), "pkey":pluralkey(title), "naked":naked(title), "paren":has_paren(title)})

def groupby(fn):
    g={}
    for a in arts: g.setdefault(a[fn],[]).append(a)
    return {k:v for k,v in g.items() if len(v)>1}

def score(a): return (a["blen"], a["has_ib"], len(a["aliases"]), -len(a["title"]))

# Tier A: identical key AND same strand (true accidental dups).
# Cross-strand key collisions are quarantined to A2 (review) — they're often a
# concept-vs-adaptation distinction (e.g. the novel "Surplus of the Seen" vs the
# concept "the surplus of the seen"), not a duplicate.
tierA, tierA2 = {}, {}
for k, v in groupby("key").items():
    if len({a["strand"] for a in v}) == 1:
        tierA[k] = v
    else:
        tierA2[k] = v
# Tier B: plural-only collisions not already in A
tierB={}
for k,v in groupby("pkey").items():
    if len({a["key"] for a in v})>1:              # genuinely differ before plural fold
        tierB[k]=v
# Tier C: bare + parenthetical variants sharing naked base (review)
tierC={}
for k,v in groupby("naked").items():
    keys={a["key"] for a in v}
    if len(keys)>1 and any(not a["paren"] for a in v) and any(a["paren"] for a in v):
        tierC[k]=v

def report(tier, label, withplan=False):
    print(f"\n=== {label}: {len(tier)} group(s) ===")
    plan=[]
    for k,v in sorted(tier.items()):
        v=sorted(v,key=score,reverse=True)
        keep,lose=v[0],v[1:]
        tag=lambda a:f"{a['title']!r} [{a['strand']},{a['blen']}b{',ib' if a['has_ib'] else ''}]"
        print(f"  keep {tag(keep)}")
        for l in lose: print(f"    drop {tag(l)}")
        plan.append((keep,lose))
    return plan

planA=report(tierA,"TIER A — auto-merge (same strand; article/case/punct only)")
report(tierA2,"TIER A2 — REVIEW (same title, different strand; may be concept-vs-adaptation)")
report(tierB,"TIER B — REVIEW (singular/plural)")
report(tierC,"TIER C — REVIEW (bare vs parenthetical; usually distinct media)")

if not MERGE:
    print("\n(report only — re-run with --merge to resolve TIER A; B and C are never auto-merged)")
    sys.exit(0)

merged=0
for keep,lose in planA:
    ktext=open(keep["path"],encoding="utf-8").read()
    have={norm(keep["title"])}|{norm(x) for x in keep["aliases"]}
    add=[]
    for l in lose:
        for cand in [l["title"],*l["aliases"]]:
            if norm(cand) not in have:
                have.add(norm(cand)); add.append(cand)
    if add:
        cur=keep["aliases"]+add
        line="aliases: ["+", ".join('"'+a.replace('"',"'")+'"' for a in cur)+"]"
        if re.search(r"^aliases:.*$",ktext,flags=re.M):
            ktext=re.sub(r"^aliases:.*$",line,ktext,count=1,flags=re.M)
        else:
            ktext=re.sub(r"^(title:.*)$",r"\1\n"+line,ktext,count=1,flags=re.M)
        open(keep["path"],"w",encoding="utf-8").write(ktext)
    for l in lose:
        os.remove(l["path"])
        h=os.path.join(WIKI,l["slug"]+".html")
        if os.path.exists(h): os.remove(h)
        print(f"  merged {l['title']!r} -> {keep['title']!r} (+{len(add)} alias)")
        merged+=1
print(f"\nmerged {merged} duplicate(s). Rebuild to regenerate the index.")

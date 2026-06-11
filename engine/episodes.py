#!/usr/bin/env python3
"""
Generate numbered episodes of the Beach Surgery animated series.

Each episode becomes content/<slug>.md carrying `episode: N` frontmatter, so the
auto-built "List of episodes" page (in build.py) assembles itself in order.
Runs on the Claude Max subscription via `claude -p` (Haiku). Rebuilds at the end.

    python3 engine/episodes.py --start 1 --end 212 --batch 5
"""
import os, re, json, subprocess, argparse, sys

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
DATA    = os.path.join(ROOT, "data")
BIBLE   = open(os.path.join(ROOT, "canon", "bible.md"), encoding="utf-8").read()

def slugify(title):
    s = title.strip().replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9_()'.\-:]", "", s)
    return re.sub(r"_+", "_", s)

NAMESPACE = ("Category:","Talk:","File:","Template:","User:","Special:")
def is_junk(t):
    if not t or not isinstance(t, str): return True
    t = t.strip()
    if any(t.startswith(p) for p in NAMESPACE): return True
    if "#" in t or "::" in t or len(t) < 4: return True
    if re.fullmatch(r"(?i)episode\s*\d+", t): return True   # reject bland "Episode N"
    return False

GUIDE = r"""
OUTPUT FORMAT — output ONLY episodes, each delimited EXACTLY like this, no preamble, no code fences:

<<<EP>>>
---
title: <an evocative, specific episode title — NOT "Episode N">
strand: anime
kind: Animated episode
episode: <THE NUMBER>
editor: <one of: tidal_ward, karman_line, not_the_ocean, dust_garden, one_side_of_the_coin>
edited_days_ago: <1-600>
infobox:
  title: <title>
  sections:
    - label: Episode
      rows:
        - ["No.", "<N> of 212"]
        - ["Series", "[[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|the animated series]]"]
        - ["Runtime", "<mm:ss>"]
categories: ["Anime episodes", "Beach Surgery franchise"]
---
<A plot synopsis of 90-160 words: say what HAPPENS — events, a strange image, a turn — advancing or
re-staging the canon (Leif, Katita, the cycle, the glitch, the motifs). Include at least one
{{dialogue|Speaker|line|optional source}}. Inventive and, where apt, globally textured. Cross-link
with [[...]] to canon and neighbouring episodes.>
== See also ==
* <2-4 [[links]]>
<<<END>>>
""".strip()

RULES = """You are writing episode entries for SURGIPELAGO, the deadpan fan-encyclopedia of the
franchise 'A Complicated Surgery Will Take Place on the Beach Tonight'. Tone: neutral, encyclopedic,
matter-of-fact; treat the series as real. Each episode is a DISTINCT work with its own plot; never
title an article 'Episode N' or with a Category:/Talk:/# prefix. Stay consistent with the canon
bible (contradictions only as the disputed lore fandom argues over). Lean inventive and varied
across the run — draw from many world settings, registers and forms."""

def call_claude(prompt, model):
    cmd = ["claude","-p","--model",model,"--output-format","text","--strict-mcp-config"]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=1200)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-1500:] + "\n"); return ""
    return r.stdout

def build_prompt(nums, existing_titles):
    ex = ", ".join(sorted(existing_titles)[:120])
    return "\n".join([RULES, "", "=== CANON BIBLE ===", BIBLE, "",
        "=== EXISTING ARTICLES (link to these by exact title where apt) ===", ex, "",
        GUIDE, "",
        f"=== WRITE THESE EPISODES NOW: numbers {nums[0]}-{nums[-1]} ===",
        "Write exactly one delimited <<<EP>>> block for EACH of these episode numbers, IN ORDER: "
        + ", ".join(str(n) for n in nums) + ".",
        f"Output exactly {len(nums)} episodes. No preamble. No code fences."])

def parse_and_write(output, nums, existing_slugs):
    import yaml
    blocks = re.findall(r"<<<EP>>>\s*(.*?)\s*<<<END>>>", output, re.S)
    written = []
    for i, block in enumerate(blocks):
        if i >= len(nums): break
        n = nums[i]
        block = re.sub(r"^```[a-z]*\n|\n```$", "", block.strip()).strip()
        fm = re.match(r"^---\n(.*?)\n---\n?(.*)$", block, re.S)
        if not fm: continue
        try: meta = yaml.safe_load(fm.group(1)) or {}
        except Exception: continue
        title = meta.get("title")
        if is_junk(title): continue
        slug = slugify(title)
        if slug in existing_slugs or os.path.exists(os.path.join(CONTENT, slug + ".md")): continue
        front = fm.group(1)
        if re.search(r"^episode:", front, re.M):
            front = re.sub(r"^episode:.*$", f"episode: {n}", front, flags=re.M)
        else:
            front = front + f"\nepisode: {n}"
        open(os.path.join(CONTENT, slug + ".md"), "w", encoding="utf-8").write(
            "---\n" + front + "\n---\n" + fm.group(2).strip() + "\n")
        existing_slugs.add(slug); written.append((n, title))
    return written

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=212)
    ap.add_argument("--batch", type=int, default=5)
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--no-build", action="store_true")
    args = ap.parse_args()

    index = json.load(open(os.path.join(DATA, "index.json")))
    existing_slugs  = set(index.keys())
    existing_titles = [v["title"] for v in index.values()]
    present = {v["episode"] for v in index.values()
               if v.get("strand") == "anime" and isinstance(v.get("episode"), int)}
    todo = [n for n in range(args.start, args.end + 1) if n not in present]
    print(f"episodes to write: {len(todo)} (range {args.start}-{args.end}, {len(present)} already present)")

    total = []
    for i in range(0, len(todo), args.batch):
        nums = todo[i:i+args.batch]
        made = parse_and_write(call_claude(build_prompt(nums, existing_titles), args.model),
                               nums, existing_slugs)
        total += made
        existing_titles += [t for _n, t in made]
        print(f"  eps {nums[0]}-{nums[-1]}: +{len(made)}  " +
              ", ".join(f"{n}:{t[:22]}" for n, t in made))
    print(f"wrote {len(total)} episodes")
    if not args.no_build:
        subprocess.run(["python3", os.path.join(ROOT, "engine", "build.py")])

if __name__ == "__main__":
    main()

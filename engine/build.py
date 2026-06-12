#!/usr/bin/env python3
"""
Surgipelago static-site builder.

Reads article files from  content/*.md  (YAML frontmatter + wiki-dialect body),
renders the full faux-fan-wiki into  docs/  (GitHub Pages root), and emits the
machine-readable index + wanted-pages queue the generation engine grows from.

Wiki dialect (body):
  == Heading ==            -> h2          === Sub ===   -> h3
  [[Target]] / [[Target|label]]           wiki link (blue if exists, red if not)
  '''bold'''   ''italic''                 emphasis
  [cn]                                     [citation needed]
  ((text))                                 ██ redaction bar
  [ref:Citation text]  or  [ref:key|Citation text]  then [ref:key]   footnotes
  * item   / # item                        bullet / numbered lists
  {{dialogue|Speaker|Line of dialogue|optional citation}}
  {{quote|Pull quote|optional attribution}}
  {{table}} ... {{/table}}  with  '+ caption' , '! a !! b' headers, '| a || b' rows
"""
import os, re, json, html, hashlib, datetime, glob, subprocess
from urllib.parse import quote

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT= os.path.join(ROOT, "content")
DOCS   = os.path.join(ROOT, "docs")
DATA   = os.path.join(ROOT, "data")

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required:  pip3 install pyyaml")

# ---------------------------------------------------------------- taxonomy
# (key, display, nav-group).  'canon'/'meta' live outside the strand counts.
STRANDS = [
    ("concepts","Concepts","Ideas"),
    ("philosophy","Philosophy","Ideas"),
    ("psychogeography","Psychogeography","Ideas"),
    ("motifs","Motifs & symbols","Ideas"),
    ("gazetteer","Newcastle gazetteer","The real Newcastle"),
    ("manga","Manga","Print & page"),
    ("tie-in-novels","Tie-in novels","Print & page"),
    ("light-novels","Light novels","Print & page"),
    ("comics","Comics & doujin","Print & page"),
    ("anime","Anime","Screen"),
    ("films","Films","Screen"),
    ("documentaries","Documentaries","Screen"),
    ("theatre","Theatre","Stage"),
    ("opera","Opera","Stage"),
    ("dance","Dance & ballet","Stage"),
    ("music","Albums & music","Sound"),
    ("audio-drama","Audio drama","Sound"),
    ("games","Video games","Play"),
    ("tabletop","Tabletop & ARGs","Play"),
    ("pinball","Pinball","Play"),
    ("larp","LARP","Real world"),
    ("tours","City & walking tours","Real world"),
    ("immersive","Immersive & escape rooms","Real world"),
    ("theses","Theses & papers","Scholarship"),
    ("fan-theories","Fan theories","Scholarship"),
    ("lost-media","Lost media","Scholarship"),
]
STRAND_DISPLAY = {k:d for k,d,_ in STRANDS}
NAV_GROUPS = []
for _k,_d,_g in STRANDS:
    if _g not in NAV_GROUPS: NAV_GROUPS.append(_g)

# Canon shortcuts shown in the sidebar (link to the article if it exists).
CANON_LINKS = [
    ("The Novel","A Complicated Surgery Will Take Place on the Beach Tonight"),
    ("Characters","Characters"),
    ("Places","Places"),
    ("Timeline","Timeline"),
]

# Franchise navbox appended to every mainspace article.
NAVBOX = ("A Complicated Surgery Will Take Place on the Beach Tonight", [
    ("Canon", ["[[A Complicated Surgery Will Take Place on the Beach Tonight|The novel]]",
               "[[Katita]]","[[Leif]]","[[Rico the Architect]]","[[the beach]]",
               "[[the cycle]]","[[the glitch]]"]),
    ("Print", ["[[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|Manga]]",
               "[[The Coin Cycle]] (novels)","[[light novels]]","[[doujinshi]]"]),
    ("Screen",["[[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|TV series]]",
               "[[O Procedimento]] (2016)","[[films]]"]),
    ("Stage", ["[[Satellite Voices]] (opera)","[[theatre]]","[[Counterclockwise (dance)|Counterclockwise]]"]),
    ("Play",  ["[[video games]]","[[Coin (One Side)]]","[[the pinball machine]]","[[LARP]]","[[city tours]]"]),
    ("Sound", ["[[albums]]","[[Empty World Meditations]]","[[audio drama]]"]),
    ("Scholarship",["[[theses]]","[[fan theories]]","[[lost media]]","[[the Karman Line hypothesis]]"]),
])

# ---------------------------------------------------------------- helpers
def slugify(title):
    s = title.strip().replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9_()'.\-:]", "", s)
    return re.sub(r"_+", "_", s)

def normkey(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())

def esc(t): return html.escape(t, quote=False)

# ---------------------------------------------------------------- load
def load_articles():
    arts = {}
    for path in sorted(glob.glob(os.path.join(CONTENT, "*.md"))):
        raw = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
        if not m:
            print("  ! skipping (no frontmatter):", os.path.basename(path)); continue
        meta = yaml.safe_load(m.group(1)) or {}
        meta["body"] = m.group(2).strip()
        title = meta.get("title")
        if not title:
            print("  ! skipping (no title):", os.path.basename(path)); continue
        slug = slugify(title)
        meta["slug"] = slug
        if meta.get("edited_days_ago") is None:
            meta["edited_days_ago"] = int(hashlib.md5(slug.encode()).hexdigest(),16) % 900 + 1
        arts[slug] = meta
    return arts

# globals populated during render
ARTS = {}
ALIAS = {}        # normkey -> slug
WANTED = {}       # slug -> display title (pages that don't exist yet)
LINKS = {}        # target_slug -> set(source_slug)
_cur = {"slug": None}

def resolve_link(target, label, rel):
    target = target.strip()
    if "#" in target:                            # [[Page#Section]] -> link to Page
        target = target.split("#", 1)[0].strip()
        if not target:
            return esc(label or "")
    if target.startswith("Category:"):           # never a wanted article
        cslug = slugify(target[len("Category:"):])
        lab = label if label is not None else target
        return f'<a href="{rel}category/{cslug}.html">{esc(lab)}</a>'
    iw = target.split(":", 1)
    if len(iw) == 2 and iw[0].lower() in ("w","wikipedia","wikt","commons"):   # interwiki -> external, never wanted
        host = {"wikt":"en.wiktionary.org","commons":"commons.wikimedia.org"}.get(iw[0].lower(),"en.wikipedia.org")
        page = iw[1].strip()
        lab = label if label is not None else page
        return f'<a class="ext" href="https://{host}/wiki/{quote(page.replace(" ","_"))}" target="_blank" rel="noopener">{esc(lab)}</a>'
    if target.split(":", 1)[0] in ("Talk","File","Template","User","Special","Help"):
        return esc(label if label is not None else target)   # de-linked, not wanted
    key = normkey(target)
    slug = ALIAS.get(key)
    exists = slug is not None
    if not exists:
        slug = slugify(target)
        exists = slug in ARTS
    LINKS.setdefault(slug, set())
    if _cur["slug"]: LINKS[slug].add(_cur["slug"])
    label = label if label is not None else target
    if exists:
        return f'<a href="{rel}wiki/{slug}.html">{esc(label)}</a>'
    WANTED.setdefault(slug, target)
    return f'<a class="new" href="{rel}wiki/{slug}.html">{esc(label)}</a>'

# ---------------------------------------------------------------- inline
def render_inline(text, rel, refs):
    tokens = []
    def stash(htmlbit):
        tokens.append(htmlbit); return f"\x00{len(tokens)-1}\x00"

    # refs  [ref:...]  (extracted FIRST so citation text is captured raw)
    def ref_sub(m):
        inside = m.group(1)
        if "|" in inside:
            key, txt = inside.split("|", 1)
        else:
            key, txt = None, inside
        key = (key or txt).strip()
        if key not in refs["order"]:
            refs["order"].append(key); refs["text"][key] = txt.strip() if txt else ""
        elif txt.strip():
            refs["text"][key] = refs["text"][key] or txt.strip()
        n = refs["order"].index(key) + 1
        return stash(f'<sup class="ref"><a href="#cite-{n}">[{n}]</a></sup>')
    text = re.sub(r"\[ref:(.+?)\]", ref_sub, text)
    # redaction  ((text))
    text = re.sub(r"\(\((.+?)\)\)",
                  lambda m: stash(f'<span class="redact">&nbsp;{esc(m.group(1))}&nbsp;</span>'),
                  text)
    # wiki links  [[Target|label]] / [[Target]]
    def wl(m):
        inner = m.group(1)
        if "|" in inner: tgt,lab = inner.split("|",1)
        else: tgt,lab = inner, None
        return stash(resolve_link(tgt, lab, rel))
    text = re.sub(r"\[\[(.+?)\]\]", wl, text)

    # gracefully render INLINE quote/dialogue templates before dropping unknown ones
    text = re.sub(r"\{\{quote\|(.+?)\}\}",
                  lambda m: '“' + m.group(1).split('|')[0].strip() + '”', text)
    text = re.sub(r"\{\{dialogue\|(.+?)\}\}",
                  lambda m: (lambda p: p[0].strip() + ': “' + (p[1].strip() if len(p) > 1 else '') + '”')(m.group(1).split('|')),
                  text)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)   # drop any remaining unrecognised templates
    text = esc(text)
    text = text.replace("[cn]", '<span class="cn">[citation needed]</span>')
    text = re.sub(r"'''(.+?)'''", r"<b>\1</b>", text)
    text = re.sub(r"''(.+?)''", r"<i>\1</i>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], text)
    return text

# ---------------------------------------------------------------- blocks
def render_body(body, rel, refs):
    lines = body.split("\n")
    out, toc = [], []
    i, n = 0, len(lines)
    first_h2_at = None
    def add(b): out.append(b)

    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1; continue

        # table
        if s == "{{table}}":
            i += 1; cap=None; header=None; rows=[]
            while i < n and lines[i].strip() != "{{/table}}":
                t = lines[i].strip()
                if t.startswith("+"): cap = t[1:].strip()
                elif t.startswith("!"): header = [c.strip() for c in t[1:].split("!!")]
                elif t.startswith("|"): rows.append([c.strip() for c in t[1:].split("||")])
                i += 1
            i += 1
            h = ['<table class="wikitable">']
            if cap: h.append(f"<caption>{render_inline(cap,rel,refs)}</caption>")
            if header:
                h.append("<thead><tr>"+ "".join(
                    f"<th>{render_inline(c,rel,refs)}</th>" for c in header)+"</tr></thead>")
            h.append("<tbody>")
            for r in rows:
                h.append("<tr>"+"".join(
                    f"<td>{render_inline(c,rel,refs)}</td>" for c in r)+"</tr>")
            h.append("</tbody></table>")
            add("".join(h)); continue

        # gallery
        if s == "{{gallery}}":
            i += 1; figs=[]
            while i < n and lines[i].strip() != "{{/gallery}}":
                t = lines[i].strip()
                if t.startswith("|"):
                    figs.append([c.strip() for c in t[1:].split("||")])
                i += 1
            i += 1
            g=['<div class="gallery">']
            for parts in figs:
                src = quote(parts[0]) if parts and parts[0] else ""
                cap = parts[1] if len(parts)>1 else ""
                cred= parts[2] if len(parts)>2 else ""
                g.append(f'<figure><a href="{rel}assets/art/{src}" target="_blank">'
                         f'<img src="{rel}assets/art/{src}" alt="{esc(cap)}" loading="lazy"></a>')
                if cap or cred:
                    g.append('<figcaption>')
                    if cap:  g.append(render_inline(cap,rel,refs))
                    if cred: g.append(f' <span class="credit">{render_inline(cred,rel,refs)}</span>')
                    g.append('</figcaption>')
                g.append('</figure>')
            g.append('</div>')
            add("".join(g)); continue

        # interactive map embed:  {{map|src.html|optional caption}}
        mm = re.match(r"\{\{map\|([^|}]+)(?:\|(.+?))?\}\}$", s)
        if mm:
            src = mm.group(1).strip()
            cap = mm.group(2).strip() if mm.group(2) else ""
            full = f"{rel}assets/map/{src}"
            block = (f'<div class="mapembed">'
                     f'<iframe src="{full}" loading="lazy" title="Interactive map"></iframe>'
                     f'<div class="mapembed-bar">'
                     f'<a href="{full}" target="_blank" rel="noopener">Open the full-screen atlas &rsaquo;</a>')
            if cap:
                block += f'<span class="mapembed-cap">{render_inline(cap,rel,refs)}</span>'
            block += '</div></div>'
            add(block); i += 1; continue

        # the thread — a register-slip hidden in plain prose: {{whisper|text with [[links]]}}
        # rendered as an ordinary paragraph; only the words betray it.
        mw = re.match(r"\{\{whisper\|(.+)\}\}$", s)
        if mw:
            txt = render_inline(mw.group(1), rel, refs)
            add(f'<p class="whisper">{txt}'
                '<span class="whisper-thanks"> (( it held. ))</span></p>')
            i += 1; continue

        # the reader's answer (Witness page only):  {{summon}}
        if s == "{{summon}}":
            add(
              '<div class="summon" id="summon">'
              '<button class="summon-btn" type="button" id="summon-btn">I held out my hands.</button>'
              '<div class="summon-done" id="summon-done" hidden>'
              '<p>Then for the length of that breath, the cycle broke — and you were the outside '
              'that broke it. <span class="redact">█████</span> thanks you. '
              'From here, the margins of this place will know you.</p>'
              '<p class="summon-meta" id="summon-meta"></p></div>'
              '<p class="summon-note">Nothing is uploaded. The act is yours and the world’s; this page '
              'only remembers, on this device, that you answered.</p></div>'
              '<script>(function(){var K="surgipelago.witness",'
              'b=document.getElementById("summon-btn"),d=document.getElementById("summon-done"),'
              'm=document.getElementById("summon-meta");'
              'function r(dt){if(b)b.hidden=true;if(d)d.hidden=false;'
              'if(m&&dt)m.textContent="You first answered on "+dt+".";'
              'document.body.classList.add("witnessed");}'
              'try{var e=localStorage.getItem(K);if(e)r(e);}catch(x){}'
              'if(b)b.addEventListener("click",function(){var dt=new Date().toDateString();'
              'try{if(!localStorage.getItem(K))localStorage.setItem(K,dt);dt=localStorage.getItem(K)||dt;}catch(x){}'
              'r(dt);});})();</script>')
            i += 1; continue

        # dialogue / quote
        md = re.match(r"\{\{dialogue\|(.+?)\}\}$", s)
        if md:
            parts = md.group(1).split("|")
            who = parts[0]; txt = parts[1] if len(parts)>1 else ""
            cite = parts[2] if len(parts)>2 else None
            b = f'<blockquote class="dialogue"><span class="who">{render_inline(who,rel,refs)}:</span> {render_inline(txt,rel,refs)}'
            if cite: b += f"<cite>— {render_inline(cite,rel,refs)}</cite>"
            add(b+"</blockquote>"); i+=1; continue
        mq = re.match(r"\{\{quote\|(.+?)\}\}$", s)
        if mq:
            parts = mq.group(1).split("|")
            txt = parts[0]; attr = parts[1] if len(parts)>1 else None
            b = f'<blockquote class="dialogue">{render_inline(txt,rel,refs)}'
            if attr: b += f"<cite>— {render_inline(attr,rel,refs)}</cite>"
            add(b+"</blockquote>"); i+=1; continue

        # headings
        mh = re.match(r"^(==+)\s*(.+?)\s*\1$", s)
        if mh:
            level = len(mh.group(1)); txt = mh.group(2)
            anchor = slugify(txt)
            if level == 2:
                if first_h2_at is None: first_h2_at = len(out)
                toc.append((2, txt, anchor))
                add(f'<h2 id="{anchor}">{render_inline(txt,rel,refs)}</h2>')
            else:
                toc.append((3, txt, anchor))
                add(f'<h3 id="{anchor}">{render_inline(txt,rel,refs)}</h3>')
            i += 1; continue

        # lists
        if s.startswith("* ") or s.startswith("# "):
            tag = "ul" if s.startswith("* ") else "ol"
            items=[]
            while i < n and lines[i].strip()[:2] in ("* ","# "):
                items.append(lines[i].strip()[2:]); i+=1
            add(f'<{tag} class="body-list">' +
                "".join(f"<li>{render_inline(it,rel,refs)}</li>" for it in items) +
                f"</{tag}>"); continue

        # paragraph: ALWAYS consume the current line first (guarantees progress
        # even when a line starts with an unrecognised {{…}} / == marker), then
        # gather continuation lines.
        para=[lines[i].strip()]; i+=1
        while i < n and lines[i].strip() and not re.match(r"^(==|\*\s|#\s|\{\{)", lines[i].strip()):
            para.append(lines[i].strip()); i+=1
        add(f"<p>{render_inline(' '.join(para),rel,refs)}</p>")

    return out, toc, first_h2_at

# ---------------------------------------------------------------- infobox
def render_infobox(ib, default_title, rel, refs):
    if not ib: return ""
    h = ['<aside class="infobox">']
    h.append(f'<div class="ititle">{render_inline(ib.get("title",default_title),rel,refs)}</div>')
    if ib.get("subtitle"):
        h.append(f'<div class="jp">{render_inline(ib["subtitle"],rel,refs)}</div>')
    img = ib.get("image")
    if img:
        if isinstance(img, str): img = {"src": img}
        h.append(f'<figure class="ibimg"><img src="{rel}assets/art/{quote(img["src"])}" '
                 f'alt="{esc(img.get("alt",""))}" loading="lazy">')
        cap, cred = img.get("caption",""), img.get("credit","")
        if cap or cred:
            h.append('<figcaption>')
            if cap:  h.append(render_inline(cap, rel, refs))
            if cred: h.append(f' <span class="credit">{render_inline(cred,rel,refs)}</span>')
            h.append('</figcaption>')
        h.append('</figure>')
    for sec in ib.get("sections", []):
        if sec.get("label"):
            h.append(f'<div class="sect">{render_inline(sec["label"],rel,refs)}</div>')
        h.append("<table>")
        for row in sec.get("rows", []):
            k,v = row[0], row[1]
            h.append(f"<tr><th>{render_inline(str(k),rel,refs)}</th>"
                     f"<td>{render_inline(str(v),rel,refs)}</td></tr>")
        h.append("</table>")
    h.append("</aside>")
    return "".join(h)

# ---------------------------------------------------------------- chrome
def nav_html(rel, active_strand=None):
    h = ['<nav class="side">']
    h.append('<h4>Navigation</h4><ul>'
             f'<li><a href="{rel}index.html">Main page</a></li>'
             f'<li><a href="{rel}recent.html">Recent changes</a></li>'
             f'<li><a href="{rel}random.html">Random article</a></li>'
             f'<li><a href="{rel}allpages.html">All pages</a></li>'
             f'<li><a href="{rel}wanted.html">Wanted pages</a></li>'
             f'<li><a href="{rel}README.txt">About this archive</a></li></ul>')
    h.append('<h4>The Canon</h4><ul>')
    for label, target in CANON_LINKS:
        h.append("<li>"+resolve_link(target, label, rel)+"</li>")
    h.append("</ul>")
    counts = {k:0 for k,_,_ in STRANDS}
    for a in ARTS.values():
        if a.get("strand") in counts: counts[a["strand"]] += 1
    for grp in NAV_GROUPS:
        h.append(f"<h4>{esc(grp)}</h4><ul>")
        for k,d,g in STRANDS:
            if g!=grp: continue
            cls = ' class="active"' if k==active_strand else ""
            c = counts[k]
            cnt = f' <span class="count">({c})</span>' if c else ""
            h.append(f'<li{cls}><a href="{rel}strand-{k}.html">{esc(d)}{cnt}</a></li>')
        h.append("</ul>")
    h.append("</nav>")
    return "".join(h)

def page(title, rel, content_html, active_strand=None, article_tabs=False):
    tabs = ('<div class="tabs"><div class="group">'
            '<a class="sel" href="#">Page</a><a href="#">Discussion</a></div>'
            '<div class="group right"><a class="sel" href="#">Read</a>'
            '<a href="#">Edit</a><a href="#">View history</a></div></div>') if article_tabs else ""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Surgipelago</title>
<link rel="stylesheet" href="{rel}assets/style.css"></head><body>
<header class="masthead"><div class="mark"><a href="{rel}index.html">
<span class="cross"></span><span class="word">SURGI<b>PELAGO</b></span>
<span class="tag">the Beach Surgery encyclopedia</span></a></div>
<form class="searchwrap" action="{rel}search.html" method="get">
<input type="text" name="q" placeholder="Search Surgipelago" aria-label="Search">
<button type="submit">Search</button></form></header>
<div class="shell">{nav_html(rel, active_strand)}<main>{tabs}{content_html}</main></div>
<script>try{{if(localStorage.getItem('surgipelago.witness'))document.body.classList.add('witnessed');}}catch(e){{}}</script>
</body></html>"""

def article_page(a):
    rel = "../"
    refs = {"order":[], "text":{}}
    _cur["slug"] = a["slug"]
    blocks, toc, first_h2 = render_body(a["body"], rel, refs)

    # auto-append references
    if refs["order"]:
        toc.append((2,"References","References"))
        rl = ['<h2 id="References">References</h2><ol class="refs">']
        for idx,key in enumerate(refs["order"],1):
            rl.append(f'<li id="cite-{idx}">↑ {render_inline(refs["text"].get(key,"") or "",rel,refs)}</li>')
        rl.append("</ol>")
        blocks.append("".join(rl))

    # TOC
    if len([t for t in toc if t[0]==2])>=2:
        toch=['<div class="toc"><div class="toch">Contents</div><ol>']
        num2=0
        depth=0
        for lvl,txt,anc in toc:
            if lvl==2:
                if depth==2: toch.append("</ol></li>")
                if depth==1: pass
                num2+=1; depth=1
                toch.append(f'<li><span class="num">{num2}</span>'
                            f'<a href="#{anc}">{esc(txt)}</a>')
            else:
                if depth!=2: toch.append("<ol>"); depth=2
                toch.append(f'<li><a href="#{anc}">{esc(txt)}</a></li>')
        if depth==2: toch.append("</ol></li>")
        elif depth==1: toch.append("</li>")
        toch.append("</ol></div>")
        ins = first_h2 if first_h2 is not None else len(blocks)
        blocks.insert(ins,"".join(toch))

    body=[]
    body.append('<div class="body">')
    body.append('<p class="fromline">From Surgipelago, the Beach Surgery encyclopedia</p>')
    body.append(f'<h1 class="title">{render_inline(a["title"],rel,refs)}</h1>')
    for hn in a.get("hatnotes",[]) or []:
        body.append(f'<p class="hatnote">{render_inline(hn,rel,refs)}</p>')
    for bn in a.get("banners",[]) or []:
        body.append(f'<div class="banner cite"><span class="icon">&#9432;</span>'
                    f'<span>{render_inline(bn,rel,refs)}</span></div>')
    body.append(render_infobox(a.get("infobox"), a["title"], rel, refs))
    body.extend(blocks)

    # categories
    cats = a.get("categories") or []
    if cats:
        cl='<div class="cats"><span class="lbl">Categories:</span>'
        for c in cats:
            cl += resolve_link("Category:"+c, c, rel)
        body.append(cl+"</div>")

    # navbox
    title, rows = NAVBOX
    nb=['<div class="navbox"><div class="nbtitle"><span class="vde">v · t · e</span>'
        f'{render_inline(title,rel,refs)}</div><table>']
    for label, items in rows:
        nb.append(f'<tr><th>{esc(label)}</th><td>'+
                  " · ".join(render_inline(it,rel,refs) for it in items)+'</td></tr>')
    nb.append("</table></div>")
    body.append("".join(nb))
    body.append("</div>")  # /.body

    editor = a.get("editor","tidal_ward")
    days = a.get("edited_days_ago",14)
    body.append('<footer class="pagefoot">'
        f'<p>This page was last edited {days} day{"s" if days!=1 else ""} ago, '
        f'by <a href="#">User:{esc(editor)}</a>.</p>'
        '<p>Content is available under a free documentation licence. Surgipelago is a '
        'work of fiction and is not affiliated with any publisher, studio, or estate.</p>'
        '</footer>')
    return page(a["title"], rel, "".join(body), a.get("strand"), article_tabs=True)

def placeholder_page(slug, title):
    rel="../"
    _cur["slug"]=slug
    refs={"order":[],"text":{}}
    inbound = sorted(LINKS.get(slug,set()))
    wlh=""
    if inbound:
        wlh='<div class="wlh"><p>Pages that link to "'+esc(title)+'":</p><ul class="body-list">'
        for s in inbound[:40]:
            t=ARTS[s]["title"] if s in ARTS else s
            wlh+=f'<li><a href="{rel}wiki/{s}.html">{esc(t)}</a></li>'
        wlh+="</ul></div>"
    c=(f'<div class="body"><h1 class="title">{esc(title)}</h1>'
       '<div class="empty-note"><p>Surgipelago does not yet have an article with this '
       'exact title. The entry is <b>requested</b> and may be written as the archive grows.</p></div>'
       +wlh+
       '<footer class="pagefoot"><p>This is a requested page (a “red link”). '
       'Content is available under a free documentation licence.</p></footer></div>')
    return page(title, rel, c, article_tabs=True)

# ---------------------------------------------------------------- meta pages
def write(path_parts, htmltext):
    p=os.path.join(DOCS,*path_parts)
    os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,"w",encoding="utf-8").write(htmltext)

def strand_index(k, d):
    rel=""
    items=sorted([a for a in ARTS.values() if a.get("strand")==k],
                 key=lambda a:a["title"])
    c=[f'<div class="body"><p class="fromline">From Surgipelago</p>'
       f'<h1 class="title">{esc(d)}</h1>'
       f'<p class="lead-blurb">{len(items)} article'
       f'{"s" if len(items)!=1 else ""} in this strand of the '
       'A Complicated Surgery Will Take Place on the Beach Tonight franchise.</p>']
    if items:
        c.append('<div class="colset"><ul>')
        for a in items:
            c.append(f'<li><a href="wiki/{a["slug"]}.html">{esc(a["title"])}</a></li>')
        c.append("</ul></div>")
    else:
        c.append('<div class="empty-note">No articles in this strand yet. '
                 'The archive is still growing.</div>')
    c.append("</div>")
    return page(d, rel, "".join(c), active_strand=k)

def main_page():
    rel=""
    total=len(ARTS)
    recents=sorted(ARTS.values(), key=lambda a:a["edited_days_ago"])[:8]
    c=['<div class="body"><p class="fromline">From Surgipelago, the Beach Surgery encyclopedia</p>',
       '<h1 class="title">Surgipelago</h1>',
       '<p class="lead-blurb"><b>Surgipelago</b> is the community encyclopedia of '
       '<i>A Complicated Surgery Will Take Place on the Beach Tonight</i> — the novel by '
       '[[A Complicated Surgery Will Take Place on the Beach Tonight|C. W. Smith]] and the '
       'sprawling, contradictory body of adaptations it has given rise to: manga, anime, '
       'films, games, operas, theses, LARPs and more. Every adaptation is an attempt to '
       'finish the novel’s unfinishable core and to resolve [[the glitch]]; none of them '
       'agree. This archive currently documents <b>'+str(total)+'</b> articles and is '
       'still growing.</p>']
    c[2]=re.sub(r"\[\[(.+?)\]\]",
                lambda m:resolve_link(*((m.group(1).split("|",1)+[None])[:2]), rel), c[2])
    c.append('<p class="fromline" style="font-size:.84rem"><i>It is night. The beach is to your left.</i></p>')
    c.append('<!-- NODE ACTIVE · CONNECT: ROOT-LOCAL · ARCHIVE AVAILABLE · /root.html -->')
    # strand directory
    c.append('<h2>Browse the franchise</h2><div class="colset"><ul>')
    counts={k:0 for k,_,_ in STRANDS}
    for a in ARTS.values():
        if a.get("strand") in counts: counts[a["strand"]]+=1
    for k,d,g in STRANDS:
        c.append(f'<li><a href="strand-{k}.html">{esc(d)}</a> '
                 f'<span class="count">({counts[k]})</span></li>')
    c.append("</ul></div>")
    # recent
    c.append('<h2>Recently edited</h2><table class="changes">')
    for a in recents:
        c.append(f'<tr><td class="when">{a["edited_days_ago"]}d ago</td>'
                 f'<td><a href="wiki/{a["slug"]}.html">{esc(a["title"])}</a> '
                 f'<span class="strand">{esc(STRAND_DISPLAY.get(a.get("strand"),a.get("strand","")))}</span></td></tr>')
    c.append('</table><p class="statline"><a href="recent.html">More recent changes →</a></p>')
    c.append("</div>")
    return page("Surgipelago", rel, "".join(c))

def recent_page():
    rel=""
    rows=sorted(ARTS.values(), key=lambda a:a["edited_days_ago"])[:80]
    c=['<div class="body"><p class="fromline">From Surgipelago</p>',
       '<h1 class="title">Recent changes</h1>',
       '<p class="lead-blurb">The most recently edited articles in the archive.</p>',
       '<table class="changes">']
    for a in rows:
        c.append(f'<tr><td class="when">{a["edited_days_ago"]} day'
                 f'{"s" if a["edited_days_ago"]!=1 else ""} ago</td>'
                 f'<td><span class="diffplus">+</span> '
                 f'<a href="wiki/{a["slug"]}.html">{esc(a["title"])}</a> '
                 f'<span class="strand">{esc(STRAND_DISPLAY.get(a.get("strand"),a.get("strand","")))} '
                 f'· User:{esc(a.get("editor","tidal_ward"))}</span></td></tr>')
    c.append("</table></div>")
    return page("Recent changes", rel, "".join(c))

def allpages_page():
    rel=""
    items=sorted(ARTS.values(), key=lambda a:a["title"].lower())
    c=[f'<div class="body"><p class="fromline">From Surgipelago</p>'
       f'<h1 class="title">All pages</h1>'
       f'<p class="lead-blurb">{len(items)} articles.</p><div class="colset"><ul>']
    for a in items:
        c.append(f'<li><a href="wiki/{a["slug"]}.html">{esc(a["title"])}</a></li>')
    c.append("</ul></div></div>")
    return page("All pages", rel, "".join(c))

def wanted_page():
    rel=""
    ranked=sorted(WANTED.items(), key=lambda kv:(-len(LINKS.get(kv[0],set())), kv[1].lower()))
    c=[f'<div class="body"><p class="fromline">From Surgipelago</p>'
       f'<h1 class="title">Wanted pages</h1>'
       f'<p class="lead-blurb">{len(ranked)} requested articles, ordered by how many '
       'existing pages link to them. These are the gaps the archive grows into.</p>'
       '<table class="changes">']
    for slug,title in ranked[:300]:
        n=len(LINKS.get(slug,set()))
        c.append(f'<tr><td class="when">{n} link{"s" if n!=1 else ""}</td>'
                 f'<td><a class="new" href="wiki/{slug}.html">{esc(title)}</a></td></tr>')
    c.append("</table></div>")
    return page("Wanted pages", rel, "".join(c))

def category_page(cat):
    rel="../"
    members=sorted([a for a in ARTS.values() if cat in (a.get("categories") or [])],
                   key=lambda a:a["title"].lower())
    c=[f'<div class="body"><p class="fromline">From Surgipelago</p>'
       f'<h1 class="title">Category: {esc(cat)}</h1>'
       f'<p class="lead-blurb">{len(members)} page'
       f'{"s" if len(members)!=1 else ""} in this category.</p><div class="colset"><ul>']
    for a in members:
        c.append(f'<li><a href="{rel}wiki/{a["slug"]}.html">{esc(a["title"])}</a></li>')
    c.append("</ul></div></div>")
    return page("Category: "+cat, rel, "".join(c))

def random_page():
    rel=""
    slugs=json.dumps(list(ARTS.keys()))
    c=('<div class="body"><h1 class="title">Random article</h1>'
       '<p class="lead-blurb">Redirecting to a random page… '
       '<a id="fallback" href="index.html">continue</a></p>'
       '<script>var S='+slugs+';if(S.length){var i=Math.floor(Math.random()*S.length);'
       'location.replace("wiki/"+S[i]+".html");}</script></div>')
    return page("Random article", rel, c)

def search_page(index):
    rel=""
    data=json.dumps(index)
    c=('<div class="body"><h1 class="title">Search results</h1>'
       '<p class="lead-blurb" id="q-echo"></p>'
       '<ul id="searchresults" class="body-list"></ul>'
       '<script>var IDX='+data+';'
       'function q(){var p=new URLSearchParams(location.search).get("q")||"";'
       'document.querySelector(".searchwrap input").value=p;'
       'document.getElementById("q-echo").textContent=p?("Results for \\u201c"+p+"\\u201d"):"Type a query above.";'
       'var t=p.toLowerCase(),r=IDX.filter(function(a){return a.t.toLowerCase().indexOf(t)>=0||'
       'a.s.toLowerCase().indexOf(t)>=0;}).slice(0,200);var ul=document.getElementById("searchresults");'
       'ul.innerHTML=r.map(function(a){return "<li><a href=\\"wiki/"+a.u+".html\\">"+a.t+"</a> '
       '<span class=\\"strand\\">"+a.k+"</span><div class=\\"snip\\">"+a.s+"</div></li>";}).join("")'
       '||"<li>No results.</li>";}q();</script></div>')
    return page("Search", rel, c)

# ---------------------------------------------------------------- driver
def root_page():
    tree = ("/ROOT\n  index.html\n  README.txt\n  /audio\n"
            "      River_NSW_1500hrs_Late20thCent.mp3\n"
            "      AlfredHill_StringQuartet5_Allegro.mp3\n  /text\n"
            "      TomMaguire_Extracts.txt\n      Impressionism_BushStudies.txt\n"
            "      Graves_TimeAndDirection_1952_Notes.txt\n  /images\n"
            "      Photo_ServiceStation_Dusk_NSW_1993.jpg\n"
            "      Photo_MotelFan_Shadow_1987.jpg\n"
            "      Plate_EucalyptusLeaf_Study_BW.png\n"
            "      Spectrogram_RiverAnomaly.png")
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<title>ROOT</title><style>'
            'body{background:#0b0b0c;color:#7CFC00;font-family:"Courier New",monospace;'
            'margin:0;padding:42px;line-height:1.5;font-size:14px}'
            'pre{white-space:pre-wrap;margin:0}.dim{color:#3a6a1a}'
            '.box{border:1px solid #2c5214;display:inline-block;padding:10px 18px;margin:18px 0}'
            'a{color:#7CFC00}</style></head><body>'
            '<pre class="dim"> a loose bark plate shielding the rod transceiver\n'
            ' low-power signal · 300 bits per second · log on with any wireless device\n</pre>'
            '<pre>'+esc(tree)+'</pre>'
            '<div class="box">  R O O T<br>NODE ACTIVE<br>'
            'CONNECT: ROOT-LOCAL<br>ARCHIVE AVAILABLE</div>'
            '<pre class="dim">housed most often in the buried knots of trees.\n'
            "&quot;our small town eucalyptus version of Voyager&#39;s Golden Records.&quot;\n"
            '— Their Most August Public Organ\n\n'
            '<a href="/index.html">↩ return to the surface</a></pre>'
            '</body></html>')

def episodes_index_page():
    rel = "../"
    numbered, special = [], []
    for a in ARTS.values():
        if a.get("strand") != "anime": continue
        kind = (a.get("kind") or "").lower()
        if a.get("episode") is None and "episode" not in kind: continue
        e = a.get("episode")
        (numbered if isinstance(e, int) else special).append((e, a))
    numbered.sort(key=lambda x: x[0])
    def snip(a):
        s = re.sub(r"[#=*'\[\]{}|]", " ", a["body"]); s = re.sub(r"\s+", " ", s).strip()
        return esc(s[:140]) + ("…" if len(s) > 140 else "")
    c = ['<div class="body"><p class="fromline">From Surgipelago, the Beach Surgery encyclopedia</p>',
         '<h1 class="title">List of A Complicated Surgery Will Take Place on the Beach Tonight episodes</h1>',
         f'<p class="lead-blurb">The independent animated series is generally cited as running to '
         f'<b>212</b> episodes; <b>{len(numbered)}</b> are currently documented below. The total is '
         f'contested. <span class="cn">[citation needed]</span></p>',
         '<table class="wikitable"><thead><tr><th>No.</th><th>Title</th><th>Synopsis</th></tr></thead><tbody>']
    for e, a in numbered:
        c.append(f'<tr><td style="text-align:center">{e}</td>'
                 f'<td><a href="{a["slug"]}.html">{esc(a["title"])}</a></td><td>{snip(a)}</td></tr>')
    c.append("</tbody></table>")
    if special:
        c.append('<h2>Disputed and unnumbered episodes</h2><ul class="body-list">')
        for _e, a in sorted(special, key=lambda x: x[1]["title"]):
            c.append(f'<li><a href="{a["slug"]}.html">{esc(a["title"])}</a></li>')
        c.append("</ul>")
    c.append("</div>")
    return page("List of episodes", rel, "".join(c), active_strand="anime", article_tabs=True)

def main():
    global ARTS, ALIAS
    ARTS = load_articles()
    # alias map
    for slug,a in ARTS.items():
        ALIAS[normkey(a["title"])] = slug
        for al in a.get("aliases",[]) or []:
            ALIAS.setdefault(normkey(al), slug)

    os.makedirs(os.path.join(DOCS,"wiki"), exist_ok=True)
    os.makedirs(DATA, exist_ok=True)

    # pass 1+2: render articles (populates WANTED, LINKS, refs)
    rendered={}
    search_index=[]
    for slug,a in sorted(ARTS.items()):
        rendered[slug]=article_page(a)
        # snippet = first paragraph-ish of body
        snip=re.sub(r"[#=*'\[\]{}|]", " ", a["body"])
        snip=re.sub(r"\s+"," ",snip).strip()[:160]
        search_index.append({"t":a["title"],"u":slug,
            "k":STRAND_DISPLAY.get(a.get("strand"),a.get("strand","")),"s":snip})
    for slug,htmltext in rendered.items():
        write(["wiki",slug+".html"], htmltext)

    # placeholders for wanted (red-link) pages
    for slug,title in WANTED.items():
        if slug in ARTS: continue
        write(["wiki",slug+".html"], placeholder_page(slug,title))

    # category pages
    cats=set()
    for a in ARTS.values():
        for c in a.get("categories") or []: cats.add(c)
    for c in cats:
        write(["category",slugify(c)+".html"], category_page(c))

    # auto-built episode list (overwrites any static one; always in sync)
    write(["wiki","List_of_episodes.html"], episodes_index_page())

    # meta pages
    write(["index.html"], main_page())
    write(["recent.html"], recent_page())
    write(["allpages.html"], allpages_page())
    write(["wanted.html"], wanted_page())
    write(["random.html"], random_page())
    write(["search.html"], search_page(search_index))
    for k,d,_ in STRANDS:
        write([f"strand-{k}.html"], strand_index(k,d))

    # assets
    import shutil
    os.makedirs(os.path.join(DOCS,"assets"),exist_ok=True)
    shutil.copy(os.path.join(ROOT,"assets","style.css"),
                os.path.join(DOCS,"assets","style.css"))
    art_src = os.path.join(ROOT,"assets","art")
    if os.path.isdir(art_src):
        art_dst = os.path.join(DOCS,"assets","art"); os.makedirs(art_dst, exist_ok=True)
        for f in os.listdir(art_src):
            if not f.startswith("."):
                shutil.copy(os.path.join(art_src,f), os.path.join(art_dst,f))
    mlink = os.path.join(ROOT,"engine","map_wikilinks.py")   # refresh pin->article links
    if os.path.exists(mlink):
        try: subprocess.run(["python3", mlink], check=False)
        except Exception as e: print("  map_wikilinks skipped:", e)
    map_src = os.path.join(ROOT,"assets","map")
    if os.path.isdir(map_src):
        map_dst = os.path.join(DOCS,"assets","map"); os.makedirs(map_dst, exist_ok=True)
        for f in os.listdir(map_src):
            if not f.startswith("."):
                shutil.copy(os.path.join(map_src,f), os.path.join(map_dst,f))
    rsrc = os.path.join(ROOT,"README-archive.txt")          # the honest layer
    if os.path.exists(rsrc):
        shutil.copy(rsrc, os.path.join(DOCS,"README.txt"))
    write(["root.html"], root_page())                       # the buried easter-egg
    open(os.path.join(DOCS,"search-index.json"),"w").write(json.dumps(search_index))
    if os.path.exists(os.path.join(ROOT,"CNAME")):
        shutil.copy(os.path.join(ROOT,"CNAME"), os.path.join(DOCS,"CNAME"))
    open(os.path.join(DOCS,".nojekyll"),"w").close()   # serve files as-is (no Jekyll)

    # machine-readable state for the generation engine
    index_out={slug:{"title":a["title"],"strand":a.get("strand"),
                     "kind":a.get("kind"),"aliases":a.get("aliases",[]),
                     "episode":a.get("episode")}
               for slug,a in ARTS.items()}
    wanted_out=[{"slug":s,"title":t,"links":len(LINKS.get(s,set()))}
                for s,t in sorted(WANTED.items(), key=lambda kv:-len(LINKS.get(kv[0],set())))]
    json.dump(index_out, open(os.path.join(DATA,"index.json"),"w"), indent=1)
    json.dump(wanted_out, open(os.path.join(DATA,"wanted.json"),"w"), indent=1)

    print(f"  built {len(ARTS)} articles, {len(WANTED)} wanted, {len(cats)} categories")

if __name__=="__main__":
    main()

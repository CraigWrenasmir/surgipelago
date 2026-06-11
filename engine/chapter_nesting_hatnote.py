#!/usr/bin/env python3
"""Add a 'this is an embedded chapter' hatnote to Chapter_1..6, so embedded
chapters are never confused with the frame's own chapter numbering.
Text-level insertion (keeps frontmatter formatting). Idempotent."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

NOTE = ("This is a chapter of the embedded story ''[[Beach Surgery (story)|Beach Surgery]]'', "
        "set down within the frame's Chapter 3. For the novel's two levels, see "
        "[[The frame and the embedded novel]].")
MARK = "set down within the frame's Chapter 3"

for n in range(1, 7):
    p = os.path.join(CONTENT, f"Chapter_{n}.md")
    if not os.path.exists(p):
        print(f"  ! missing Chapter_{n}.md"); continue
    t = open(p, encoding="utf-8").read()
    if MARK in t:
        print(f"  · Chapter {n}: already has nesting hatnote"); continue
    # locate frontmatter block
    m = re.match(r"^(---\n)(.*?)(\n---\n)(.*)$", t, re.S)
    if not m:
        print(f"  ! Chapter {n}: no frontmatter"); continue
    open_, fm, close_, body = m.groups()
    if re.search(r"^hatnotes:\s*$", fm, flags=re.M):
        fm = re.sub(r"^(hatnotes:\s*)$", r'\1\n  - "' + NOTE + '"', fm, count=1, flags=re.M)
    else:
        fm = fm.rstrip("\n") + '\nhatnotes:\n  - "' + NOTE + '"'
    open(p, "w", encoding="utf-8").write(open_ + fm + close_ + body)
    print(f"  + Chapter {n}: nesting hatnote added")

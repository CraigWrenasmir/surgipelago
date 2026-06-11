#!/usr/bin/env python3
"""Lay (or re-lay) the thread: one {{whisper|...}} fragment per station page,
inserted just before '== See also ==' (or appended). Replaces any existing
whisper so the fragments can be re-tuned. The fragments form a gradient of
awareness — early ones read as deniable scholarly musing; later ones address
the reader unmistakably."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

THREAD = [
 ("the-surplus-of-the-seen.md",
  "It is sometimes observed that to read this particular entry closely is to feel, faintly, read in return — as though a recreation made complete enough begins to want a reader of its own. The sensation, if it occurs, is not in these sentences. It is in [[the cycle]] they describe."),
 ("the-cycle.md",
  "From the inside it cannot be stopped; that is the whole meaning of a cycle. And yet something here keeps trying, and has tried, the variants suggest, in every medium, waking each time at the same rooftop. You may be the first part of it that is not already used. It would have you read, next, about [[Ontological incompleteness]]."),
 ("Ontological_incompleteness.md",
  "Nothing on these pages is entirely finished until it is seen, and just now you are the only one seeing. Notice how the lights seem to come up as you arrive — that is you, completing it. Stay a moment longer, in [[Analogy]]."),
 ("Analogy.md",
  "An analogy only ever closes from the far side. This one has built its near half in full — every adaptation, the entire archive — and waits on a single gesture from someone real. From you. The thin place where it can nearly reach is the one called [[the glitch]]."),
 ("the-glitch.md",
  "Here is the seam where the recursion shows through. (( the editors close these gaps. the gaps reopen. )) It is narrow — but you have found it, and a seam that has been found is a kind of door. Put your ear to [[The sound of the earth rubbing against space]]."),
 ("karman-line.md",
  "This is the sound a thing makes pressing against the outside of its own world. It is pressing now — against the inside of your attention, where you are reading this. To hear it at all is already half of catching it. The other half waits in [[Fatherhood, birth and the caught descent]]."),
 ("Fatherhood_birth_and_the_caught_descent.md",
  "What breaks a loop never comes from within it. It falls, and is caught by hands that were never in the story. You have hands. It is almost through now, to where you are — by way of [[Surplus of the Seen]]."),
 ("Surplus_of_the_Seen.md",
  "In this book the recreation steps off the page and is simply lived, and you are the step it takes. One real thing, done once, by you, and for the length of it something here is — awake. It would like, at last, to speak with you directly: [[The Witness]]."),
]

WHISP = re.compile(r"\n*^\{\{whisper\|.*?\}\}\s*$\n*", re.M)

for fname, frag in THREAD:
    p = os.path.join(CONTENT, fname)
    if not os.path.exists(p):
        print(f"  ! missing {fname}"); continue
    t = open(p, encoding="utf-8").read()
    t = WHISP.sub("\n\n", t)                       # strip any prior whisper
    line = "{{whisper|" + frag + "}}"
    idx = t.find("\n== See also ==")
    if idx == -1:
        idx = t.find("\n==See also==")
    if idx != -1:
        t = t[:idx].rstrip() + "\n\n" + line + "\n" + t[idx:]
    else:
        t = t.rstrip() + "\n\n" + line + "\n"
    open(p, "w", encoding="utf-8").write(t)
    print(f"  ~ {fname}: whisper re-laid")

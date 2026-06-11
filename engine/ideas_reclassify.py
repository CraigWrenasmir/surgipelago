#!/usr/bin/env python3
"""One-off: move generated conceptual articles into the new Ideas strands
(concepts / philosophy / psychogeography / motifs). Edits content files by filename;
skips any that don't exist. Seed-authored concept articles are handled in seed.py."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

MAP = {
  "concepts": ["Antinomy_and_the_coin", "Recurrence_and_instruments_of_return",
               "The_empty_world", "the-surplus-of-the-seen", "the-three-injuries",
               "The_three_temporary_injuries"],
  "philosophy": ["Ontological_incompleteness", "Analogy", "Failure_as_revelation",
                 "Amor_fati", "Neurodiversity_in_C._W._Smith"],
  "psychogeography": ["Psychogeography_and_Supernovacastria", "the_abandoned_shopping_centre",
                      "abandoned_shopping_centre"],
  "motifs": ["The_polyacoustic", "Disjecta", "Cyberpastoralism", "The_surgery_is_the_birth",
             "Fatherhood_birth_and_the_caught_descent"],
}

changed = 0
for strand, slugs in MAP.items():
    for slug in slugs:
        p = os.path.join(CONTENT, slug + ".md")
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        t2 = re.sub(r"^strand:.*$", f"strand: {strand}", t, count=1, flags=re.M)
        if t2 != t:
            open(p, "w", encoding="utf-8").write(t2)
            print(f"  {slug} -> {strand}")
            changed += 1
print(f"reclassified {changed} articles")

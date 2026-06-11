#!/bin/bash
# Sustained abundance: successive large general waves. Each fills the most-linked
# red links (real content) and invents fresh works across strands, rebuilding each pass.
cd ~/Surgipelago
L=/tmp/surgi-abundance.log
: > "$L"
PASSES="${1:-5}"
for pass in $(seq 1 "$PASSES"); do
  echo "=== abundance pass $pass/$PASSES $(date), from $(ls content/*.md|wc -l) articles ===" >> "$L"
  python3 engine/generate.py --count 120 --batch 5 --model haiku >> "$L" 2>&1
  echo "--- pass $pass done $(date), total $(ls content/*.md|wc -l) ---" >> "$L"
done
echo "=== ABUNDANCE RUN DONE $(date), total $(ls content/*.md|wc -l) articles, $(python3 -c "import json;print(len(json.load(open('data/wanted.json'))))") red links ===" >> "$L"

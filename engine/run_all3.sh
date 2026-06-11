#!/bin/bash
cd ~/Surgipelago
L=/tmp/surgi-all3.log
: > "$L"

echo "=== STEP 1: episode gap top-up $(date) ===" >> "$L"
python3 engine/episodes.py --start 1 --end 212 --batch 5 --model haiku >> "$L" 2>&1
echo "--- step 1 done $(date), total $(ls content/*.md|wc -l) ---" >> "$L"

echo "=== STEP 2: manga volumes $(date) ===" >> "$L"
python3 engine/generate.py --batch 4 --model haiku \
  --titles 'The Rooftop and the Wire;Home Invasion;The Dust Garden (volume);The Preschool on the Roof;Rico the Architect (volume);The Underground Baths (volume);Crocodiles and the Drone;The Photographs (volume);The Boar and the Robot;The Cabin (volume);The Wild Dogs;The Rocket Cart (volume)' \
  --directive 'Each title is a VOLUME of the Beach Surgery manga ([[A Complicated Surgery Will Take Place on the Beach Tonight (manga)]]). Write an accurate manga-volume article: strand manga, kind Manga volume, an infobox carrying its volume number (1-14) plus Preceded by / Followed by links, and a plot synopsis of the events in that volume drawn from the canon bible (the rooftop, the wire and the Mighty Mechas; the hotdog and the protest news; the dust-garden sleep; the rooftop preschool and the seagull; Rico the Architect; the underground baths and the harbour; the desert drive, the mechanic and the radio igloo; the crocodiles and the drone photographs that reveal Leif; the boar and the car chase; the cabin, rocket cart and leather armour; the wild dogs and Dirtheart; the rocket-cart ride to the city). Number them in order: Rooftop and the Wire=1, Home Invasion=2, The Dust Garden=3, The Preschool on the Roof=4, Rico the Architect=5, The Underground Baths=6, Crocodiles and the Drone=8, The Photographs=9, The Boar and the Robot=10, The Cabin=11, The Wild Dogs=12, The Rocket Cart=13 (The Tidal Ward is volume 7 and The Wings is volume 14, already written). Include one {{dialogue}}. Cross-link to canon, the manga series, and adjacent volumes.' >> "$L" 2>&1
echo "--- step 2 done $(date), total $(ls content/*.md|wc -l) ---" >> "$L"

echo "=== STEP 3a: red-link sweep $(date) ===" >> "$L"
python3 engine/generate.py --count 90 --batch 5 --model haiku >> "$L" 2>&1
echo "=== STEP 3b: red-link sweep $(date) ===" >> "$L"
python3 engine/generate.py --count 90 --batch 5 --model haiku >> "$L" 2>&1

echo "=== ALL THREE DONE $(date), total $(ls content/*.md|wc -l), red links $(python3 -c "import json;print(len(json.load(open('data/wanted.json'))))") ===" >> "$L"

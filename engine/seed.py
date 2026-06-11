#!/usr/bin/env python3
"""Writes the hand-authored canonical seed corpus into content/.
Each entry is one article file (YAML frontmatter + wiki-dialect body)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
os.makedirs(CONTENT, exist_ok=True)

ART = {}

ART["novel"] = """---
title: A Complicated Surgery Will Take Place on the Beach Tonight
strand: canon
kind: Novel (2020)
aliases: ["the novel", "Beach Surgery", "ACSWTPOTB", "the source novel"]
editor: one_side_of_the_coin
edited_days_ago: 2
hatnotes:
  - "This article is about the 2020 novel. For the franchise and its many adaptations, see [[Beach Surgery (disambiguation)]]."
banners:
  - "This article describes a finished work whose central story is, by design, unfinished. Editors are reminded not to 'resolve' [[the glitch]] in the plot summary. [cn]"
infobox:
  title: A Complicated Surgery Will Take Place on the Beach Tonight
  subtitle: 複雑な手術は今夜浜辺で
  image:
    src: kim-jung-gi-cover.jpg
    caption: "Cover illustration depicting [[Katita]] and [[Leif]]"
    credit: "Kim Jung Gi"
  sections:
    - label: Novel
      rows:
        - ["Author", "[[C. W. Smith]]"]
        - ["Publisher", "((Abrachas Publishing))"]
        - ["Published", "2020"]
        - ["Cover", "Kim Jung Gi"]
        - ["Genre", "Literary fiction · metafiction"]
    - label: Franchise
      rows:
        - ["Adaptations", "see [[Beach Surgery (disambiguation)]]"]
        - ["Core problem", "[[the glitch]]"]
categories: ["The novel", "Beach Surgery franchise", "Metafiction"]
---
'''A Complicated Surgery Will Take Place on the Beach Tonight''' is a 2020 novel by [[C. W. Smith]], published by ((Abrachas Publishing)). It is the source text of the [[Beach Surgery (disambiguation)|Beach Surgery]] franchise. The novel is a first-person testament: its narrator, recovering from a public breakdown he calls [[the eruption]] at a conference in [[Shanbudia]], sits at his desk in the weeks before his first child is born and tries to account for an unfinished story he has tinkered with for some eighteen years — the story of [[Leif]] and [[Katita]].[ref:smith2020|Smith, C. W. ''A Complicated Surgery Will Take Place on the Beach Tonight''. Abrachas Publishing, 2020.]

{{quote|The invisible is only what is too brightly lit.|Gerald Murnane, ''The Plains'', quoted as the novel's epigraph}}

== Structure ==
The embedded story, [[Beach Surgery (story)|Beach Surgery]], unfolds across two days divided into two halves of one day each: [[the cycle|six chapters]], three per half, four scenes per chapter. The first half is set in the coastal city of [[Newcastle]]; the second in the [[the interior|red interior]] of New South Wales. [[Leif]] begins with three injuries — he cannot walk, cannot see, and his heart is "out of whack" — one for each chapter of a half.[ref:smith2020]

== The two stories ==
Readers distinguish the '''frame''' (the narrator's own life: meeting his wife at a [[Street Fighter (tournament)|Street Fighter tournament]], the [[the eruption|eruption]] in [[Shanbudia]]) from the '''embedded''' story of [[Leif]] and [[Katita]]. The novel is complete; the embedded story is deliberately left as an outline, containing [[the glitch]] — the unresolved seam between its two halves, which "does not compute."[ref:glitchessay|"The Glitch That Will Not Compute." Surgipelago essays.]

It is this unfinishable core that the franchise endlessly attempts to complete — and that every adaptation completes differently. See [[Beach Surgery (disambiguation)]].

== See also ==
* [[Katita]] · [[Leif]] · [[the beach]] · [[the cycle]] · [[the glitch]]
* [[The sound of the earth rubbing against space]] (the story's "white whale")
* [[Beach Surgery (disambiguation)|List of adaptations]]
"""

ART["cw-smith"] = """---
title: C. W. Smith
strand: canon
kind: Author
aliases: ["Craig Warren Smith", "the narrator", "C.W. Smith"]
editor: rose_house
hatnotes:
  - "This article is about the author. For the narrator of the novel, who closely resembles him, see [[the narrator]] (redirects here)."
infobox:
  title: C. W. Smith
  sections:
    - label: Author
      rows:
        - ["Born", "((1983))"]
        - ["Occupation", "Writer; play & development researcher"]
        - ["Known for", "''[[A Complicated Surgery Will Take Place on the Beach Tonight|A Complicated Surgery…]]''"]
        - ["Publisher", "((Abrachas Publishing))"]
categories: ["People", "Beach Surgery franchise"]
---
'''C. W. Smith''' (Craig Warren Smith) is an Australian writer based in [[Newcastle]], and the author of ''[[A Complicated Surgery Will Take Place on the Beach Tonight]]'' (2020). Beach Surgery is one node in a larger, tightly interlinked body of work — novels, novellas, prose, poetry, essays, radio and stage plays, and digital pieces — that returns obsessively to walking, [[Newcastle]] (mythologised elsewhere as "Supernovacastria"), the depopulated "empty world," collected "disjecta," pastoral land repurposed as data, and the contradiction Smith names '''ontological incompleteness'''.[ref:wren|Author site, wrenasmir.com.] Within the novel the narrator is an unnamed researcher of children's play whose biography shadows Smith's own.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

== Selected works ==
{{table}}
! Title !! Form !! Year
| ''[[A Complicated Surgery Will Take Place on the Beach Tonight]]'' || novel || 2020
| ''[[Antinomicity]]'' || novella || 2022
| ''[[Postseasonal (collection)|Postseasonal]]'' || collection || 2023
| ''[[Fellow Disjecta, Oh Sunny Danger Time]]'' || lyric essay / autofiction || 2024
| ''[[Pastoral Scanlines]]'' || selected works '20–'25 || 2025
| ''[[Everyone I Love is Alive in the Unlimited Present of the City and its Waters]]'' || hybrid essay || 2025
{{/table}}
Essays include ''[[Subject (Ontological Incompleteness)]]'', ''[[Beyond Correct and Incorrect Nature]]'', ''[[Polyacoustic]]'' and ''[[Nothingness Mirror]]''; the radio plays ''Prompt'' and ''Selector''; and digital works including ''[[Weather Window]]'' and the Newcastle psychogeography games ''[[Ridin' Newcastle]]'' and ''[[Play Newcastle: Gregson Park]]''.

== Recurring concerns ==
Smith's essay ''[[Subject (Ontological Incompleteness)]]'' supplies the philosophical key to much of his work, and to Beach Surgery in particular: consciousness as "an analogy of itself," the subject as an irreducible split — a Möbius-shaped gap between the real and the ideal.

{{quote|That gap is you.|''Subject (Ontological Incompleteness)''}}

This is the same gap the novel dramatises as [[the glitch]] and figures as [[the coin]] with only one side. ''[[Beyond Correct and Incorrect Nature]]'' states the novel's closing ethic plainly — "Nature is perfect, but we are not" — while ''[[Antinomicity]]'' rehearses, years earlier, the love of empty quarters, the drain-walks, and a '''fall from a cliff onto a beach''' that uncannily prefigures [[Leif]]'s dive for [[the boy in the waves]].

== Relation to Beach Surgery ==
* ''[[Everyone I Love is Alive in the Unlimited Present of the City and its Waters]]'' opens a trilogy — ''[[Their Most August Public Organ]]'' and ''[[Surplus of the Seen]]'' — whose final volume sets out to '''recreate the novel''' through the author and his wife's real-world exploration and philosophy; Surgipelago is its media-side counterpart.
* The data-farmed countryside of the novel's second half echoes the hacked agricultural systems of ''[[Fellow Disjecta, Oh Sunny Danger Time]]''.
* The [[Empty World Meditations]] recur as a sequence across ''[[Everyone I Love is Alive in the Unlimited Present of the City and its Waters]]''.
* Smith's recurring citation of '''Gerald Murnane''' — the novel's epigraph author — runs throughout the oeuvre.

Scholars caution against collapsing author and narrator entirely; see [[On the unfinishable: recurrence and the outline form|the standard thesis]].

== See also ==
* [[the eruption]] · [[Les]] · [[the bird on the rail line]] · [[Ontological incompleteness]]
"""

ART["katita"] = """---
title: Katita
strand: canon
kind: Character
aliases: ["Katita"]
editor: not_the_ocean
edited_days_ago: 5
infobox:
  title: Katita
  image:
    src: katita-sketch-dokinana.jpg
    caption: "Katita (sketch)"
    credit: "Dokinana"
  sections:
    - label: Character
      rows:
        - ["First appearance", "''[[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]]''"]
        - ["Occupation", "Nurse; agent of [[the cycle]]"]
        - ["Affiliation", "her [[the surgery|desert surgery]]"]
        - ["Weapon", "[[the sword|bastardised samurai sword]]"]
        - ["Motif", "red"]
        - ["Based on", "the narrator's wife"]
categories: ["Characters", "Beach Surgery franchise"]
---
'''Katita''' is one of the two protagonists of [[Beach Surgery (story)|Beach Surgery]]. She presents as a hybrid of '''nurse and sword-bearing assassin''': a first-aid kit on her belt, a [[the sword|bastardised samurai sword]] across her back, a flak jacket dusted with [[the interior|red desert sand]], thigh-high socks and red kitten heels. '''Red is her master motif''' — her hair, the cross on her kit, possibly blood wiped across her face.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

She does not smile for the entire story until one of the final scenes. Cold, strategic and grief-stricken, she is the agent of [[the cycle]]: she is trying to '''break''' it — to make the spinning of the world reverse. She can hear [[the sound of the earth rubbing against space]], which sickens her.

== Method ==
Katita's devotion to [[Leif]] is, in her own words, "fashioned in the most surgically strategic of ways."

{{dialogue|Katita|There is one side to a coin, and it goes the whole way around. And around. And around we go.|widely cited as her thesis statement}}

She is derived by [[C. W. Smith]] from his memory of the redhead medical intern he married; the name is synthesised from the fox ears his wife wore the night they met.

== Appearances across the C. W. Smith oeuvre ==
Katita is a '''recurring character''' across [[C. W. Smith]]'s works — one of the "[[Surplus of the Seen|instruments of return]]." Besides [[Beach Surgery (story)|Beach Surgery]] she appears in ''[[Saltando]]'' (the rockpool meeting), ''[[Leaving/Leading]]'' (a first date, dissolving into [[Newcastle]] as a boat), ''[[Summer Endzone]]'' (the radio downhill after a pirate station), ''[[A Billiard Table with Five Balls and Twelve Cues]]'' (the academic's wife on a [[Shanbudia]] island), ''[[Pugil]]'' (a sleepless writer who watches Leif fight — renamed Adria in the standalone version), ''[[Fellow Disjecta, Oh Sunny Danger Time]]'' (the community's property manager), ''[[Their Most August Public Organ]]'' (building [[the surplus of the seen|the archive]]), and — alone, as the narrator's wife and a biologist — ''[[Garden Monologue #1]]''.

== See also ==
* [[Leif]] · [[the cycle]] · [[the glitch]] · [[the boy in the waves]]
"""

ART["leif"] = """---
title: Leif
strand: canon
kind: Character
aliases: ["Leif"]
editor: bee_automaton
infobox:
  title: Leif
  sections:
    - label: Character
      rows:
        - ["First appearance", "''[[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]]''"]
        - ["Occupation", "[[military engineer]]"]
        - ["Condition", "amnesia; cannot walk / see; faulty heart"]
        - ["Equipment", "[[the hand cannon]]; [[the pacemaker]]"]
        - ["Name", "anagram of 'Life'"]
categories: ["Characters", "Beach Surgery franchise"]
---
'''Leif''' is one of the two protagonists of [[Beach Surgery (story)|Beach Surgery]], a [[military engineer]] in a state of physical damage and memory loss. He begins the story with three temporary injuries — he '''cannot walk''', '''cannot see''' (his eyes are bandaged), and his heart is "out of whack," kept going by a hacked-together [[the pacemaker|external pacemaker]] with a blinking red diode on his floral shirt. He clutches [[the hand cannon|a massive hand cannon]] "as though he hopes to fuse it with his bones."[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

The three injuries map to the three chapters of each half of the story. The name '''Leif''' is an anagram of "Life."

== Backstory ==
In a conflict zone near a beachfront, Leif dives from a cliff to save [[the boy in the waves|a boy taken by the waves]] and is smashed unconscious. [[Katita]], the triage nurse who resuscitates him, decides from that moment that "Leif is her tool of change." At the story's climax, white wings push from his shoulder-blades and he briefly flies — before he falls. See [[the wings]].

== Appearances across the C. W. Smith oeuvre ==
Like [[Katita]], Leif '''recurs''' across [[C. W. Smith]]'s works as one of the "[[Surplus of the Seen|instruments of return]]" — in ''[[Saltando]]'' (a composer who falls into the ocean), ''[[Leaving/Leading]]'' (an obelisk to reach her), ''[[Summer Endzone]]'' (a settled garden couple), ''[[A Billiard Table with Five Balls and Twelve Cues]]'' (a UN-conference academic on a [[Shanbudia]] island), ''[[Pugil]]'' (a baker and prizefighter — renamed Max in the standalone version), ''[[Fellow Disjecta, Oh Sunny Danger Time]]'' (a one-armed solar-punk leader), and ''[[Their Most August Public Organ]]''. The name is an anagram of "Life."

== See also ==
* [[Katita]] · [[the wheelchair]] · [[the rocket cart]] · [[the wings]]
"""

ART["the-cycle"] = """---
title: The cycle
strand: concepts
kind: Concept
aliases: ["the cycle", "eternal recurrence", "breaking the cycle", "the loop"]
editor: one_side_of_the_coin
infobox:
  title: The cycle
  sections:
    - label: Concept
      rows:
        - ["Type", "Structural & thematic engine"]
        - ["Associated with", "[[Katita]]; [[the coin]]; the Kármán line"]
        - ["Katita's aim", "to stop and REVERSE it"]
        - ["Figured as", "the one-sided coin; the Möbius strip"]
        - ["Broken by", "[[Fatherhood, birth and the caught descent|the birth]]"]
categories: ["Concepts", "Beach Surgery franchise"]
---
'''The cycle''' is the central engine of [[Beach Surgery (story)|Beach Surgery]] — structurally, thematically, and as the whole of [[Katita]]'s intent. The story ends where it began: at the climax [[Katita]] gathers the broken [[Leif]], sets him back in [[the wheelchair]], replaces his bandages and [[the hand cannon|hand cannon]], reforges [[the sword]] from the heat-flattened pipe ("you cannot do surgery without a sword"), and repeats her vow — "we need to break the cycle. We can do it we can do it we can do it we—". The narrative loops; this is the loop the reader has been inside all along.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

== Katita's intention ==
Almost everything [[Katita]] does is bent toward '''ending the cycle''' — not winning it, but stopping it. In the [[the abandoned shopping centre|abandoned shopping centre]], raking dust with her [[the sword|sword]] "like a zen garden," she states it plainly: "It is time to get off the merry go round… No more meaningless revolutions around the sun… This geometry stops now." She "never wants to hear [[the sound of the earth rubbing against space]] again" — the low Kármán-line drone she alone can hear, the sound of the world turning.

{{quote|This geometry stops now.|Katita, in the abandoned shopping centre}}

== The geometry of recurrence ==
[[Katita]] rejects the idea that history is a clash of opposites. To [[Leif]] she explains that the magnets of history are not positive and negative poles colliding but '''same poles repelling''' — pushed together so that they spin endlessly around one another. There are not two sides to a coin:

{{dialogue|Katita|There is one side to a coin, and it goes the whole way around. And around. And around we go.}}

The narrator finds the same figure in the [[the coin|one-sided coin]] and, in the [[the frame|frame]], in the Möbius strip — "History as a Möbius strip. It rhymes as it repeats and passes over itself in one eternally recurring wave." Her secret physics: if the earth's spin could be made to '''reverse''', the screech of its braking would rise to match the high resonance of the human spine — the inversion of the [[the sound of the earth rubbing against space|Kármán]] drone. To stop the world turning is to turn the nausea of recurrence into the pitch of a body at rest.

== Leif as the instrument ==
[[Katita]] cannot break the cycle alone, so she fashions an instrument. From the moment [[Leif]] dove for [[the boy in the waves]], she decided "Leif is her tool of change," binding his devotion "in the most surgically strategic of ways." Each loop she drives him toward [[the beach]]; each loop [[the wings]] erupt from his back and he flies — and each loop he '''crashes'''. The miracle she needs him to perform is also the thing that destroys him; the cycle's promise is a [[The three temporary injuries|temptation never finally refused]]. [[Surplus of the Seen|Later]], Smith names this exactly: "Leif and Katita are not recycled characters. They are instruments of return."

== Why the loop never closes ==
The cycle is also a '''failure''': the two halves of the story cannot be made to meet, the loop never quite seals. That unjoinable seam is [[the glitch]] — the reason the recurrence keeps having to begin again, and the reason the franchise can adapt the story forever.

== How the cycle breaks ==
What [[Katita]] cannot do from inside the story, the [[the frame|frame]] does from outside it. At the novel's end the embedded loop and reality fuse in a birthing suite, and the daughter — "shot into the air… floating like a feather back down" — falls and is '''caught''' (the descent that answers every fall; see [[Fatherhood, birth and the caught descent]]). The narrator, standing over her, writes: "I forgot how to think about the future." Recurrence is broken not by stopping it but by turning it forward — into a new generation. This is why "[[The surgery is the birth|love is always surgery]]."

== Return, not repetition ==
Even unbroken, the cycle is never mere repetition. The novel's closing turn — "You never outlearn the old mistakes of your youth… they were never really mistakes to begin with" — recasts recurrence as '''amor fati''', a deepening of the one life rather than an escape into many (see [[amor fati]] and [[Recurrence and instruments of return]]). The whole franchise is the cycle made literal: every adaptation returns to the one unfinishable story, and [[Surgipelago]] is itself an instrument of return. It rests on a single line that is both the cycle's first move and its last: "The first breath is just a breath."

== See also ==
* [[the coin]] · [[the glitch]] · [[the wings]] · [[the sound of the earth rubbing against space]]
* [[Fatherhood, birth and the caught descent]] · [[The surgery is the birth]] · [[amor fati]]
* [[Katita]] · [[Leif]] · [[Counterclockwise (dance)]] · [[Surplus of the Seen]]
"""

ART["the-glitch"] = """---
title: The glitch
strand: concepts
kind: Concept
aliases: ["the glitch", "the two-half problem"]
editor: karman_line
edited_days_ago: 3
banners:
  - "The nature of '''the glitch''' is disputed. This article documents readings without endorsing one. Do not 'fix' it. [cn]"
categories: ["Concepts", "Beach Surgery franchise", "Disputed canon"]
---
'''The glitch''' is the name given by [[C. W. Smith]]'s narrator to the irreparable structural fault at the centre of [[Beach Surgery (story)|Beach Surgery]]: the seam between the story's two halves, which "does not compute." The narrator could never make the [[the interior|desert half]] connect to the [[Newcastle]] half, and abandoned the work in part for this reason.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

Because the core is unfinishable, '''every adaptation must invent its own bridge''' across the glitch — and they disagree. The [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|manga]] resolves it one way; [[O Procedimento]] another; the [[the Karman Line hypothesis|Karman Line hypothesis]] argues none of them are right.

This proliferation of incompatible resolutions is, for many editors, the true engine of the franchise. See also [[lost media]] and [[On the unfinishable: recurrence and the outline form|the standard thesis]].

== See also ==
* [[the cycle]] · [[the beach]] · [[Beach Surgery (disambiguation)]]
"""

ART["the-beach"] = """---
title: The beach
strand: canon
kind: Place / motif
aliases: ["the beach"]
editor: not_the_ocean
infobox:
  title: The beach
  sections:
    - label: Place
      rows:
        - ["Role", "Destination; site of the 'surgery'"]
        - ["Heartbeat", "one thump ('beach')"]
        - ["Adjacent", "[[Newcastle]]; [[the interior]]"]
categories: ["Places", "Beach Surgery franchise"]
---
'''The beach''' is the destination toward which [[Katita]] drives [[Leif]] across both halves of [[Beach Surgery (story)|Beach Surgery]]: the place where "a complicated surgery will take place tonight." In the narrator's private system, the word ''beach'' is one thump of a heartbeat, while ''surgery'' is three — a heartbeat trying to skip a beat.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

The beach is where the lovers first spend the night in the [[the frame|frame story]], where [[the boy in the waves]] is lost, and where [[the wings]] finally erupt and fail. It is also where [[the sound of the earth rubbing against space]] is most audible.

== See also ==
* [[the cycle]] · [[the wings]] · [[the public baths]]
"""

ART["karman-line"] = """---
title: The sound of the earth rubbing against space
strand: motifs
kind: Motif
aliases: ["the Karman line", "the Karman Line", "white whale", "the white whale", "the drone", "the droning"]
editor: karman_line
infobox:
  title: The sound of the earth rubbing against space
  sections:
    - label: Motif
      rows:
        - ["Also called", "the Kármán line; the 'white whale'"]
        - ["Pitch", "low; nauseating"]
        - ["Opposite", "the spine's resonance (high D / high G)"]
        - ["Heard by", "[[Katita]]"]
categories: ["Concepts", "Beach Surgery franchise"]
---
'''The sound of the earth rubbing against space''' is a low, nauseating drone that [[Katita]] can hear at the edge of silence. She names it the '''Kármán line''' — the boundary where atmosphere gives way to outer space — and editors call it the story's "white whale."[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

Its opposite is the '''high resonance of the human spine''' (described as a high D for men and a high G for women), which surfaces whenever [[Leif]]'s doubled vision is "corrected" at the [[the radio igloo|radio igloo]]. [[Katita]]'s theory of [[the cycle]] turns on the claim that if the earth's spin reversed, its braking would scream at exactly that high pitch.

{{dialogue|Katita|Can you hear the sound of the earth rubbing against space? Look up towards the curved roof of the world and listen.|on the beach, in the frame story}}

== See also ==
* [[the cycle]] · [[the wings]] · [[Satellite Voices]] · [[Empty World Meditations]]
"""

ART["rico"] = """---
title: Rico the Architect
strand: canon
kind: Embedded tale
aliases: ["Rico", "Rico the Architect", "the story of Rico"]
editor: dust_garden
infobox:
  title: Rico the Architect
  sections:
    - label: Embedded tale
      rows:
        - ["Told by", "[[Katita]] (to [[Leif]])"]
        - ["Characters", "Rico; Mylar"]
        - ["Theme", "the builder who cannot build inside himself"]
categories: ["Embedded tales", "Beach Surgery franchise"]
---
'''Rico the Architect''' is a story-within-the-story told by [[Katita]] to [[Leif]] as they descend in a construction elevator in Chapter Two of [[Beach Surgery (story)|Beach Surgery]]. Rico, youngest of a line of architects, can build '''functioning miniature cities inside other people's bodies''' — but never inside himself, because no mirror lets him teach and do at once.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

Children will not help him (his problem is "too small"; they only solve apocalypses); lovers will not (secrets die outside their private language). Finally '''Mylar''', youngest of a line of surgeons, presses his hand to the wall of the town hall and performs "her surgery": Rico's body grows into and ''becomes'' the breathing building, its windows glowing crimson, its doorway warped into "a contented smile."

Hearing it, Leif says: "I knew every word of it before you said it." The tale is a favourite of adapters; the [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|manga]] gives it a full colour interlude.

== See also ==
* [[the surgery]] · [[architecture and installations]] · [[Mylar]]
"""

ART["mechanical-seagull"] = """---
title: The mechanical seagull
strand: canon
kind: Recurring entity
aliases: ["the mechanical seagull", "the seagull", "the giant seagull"]
editor: tidal_ward
infobox:
  title: The mechanical seagull
  sections:
    - label: Entity
      rows:
        - ["Type", "Aerial machine / drone"]
        - ["Wingspan", "((20)) metres"]
        - ["Grapples", "excavator claws on a pneumatic arm"]
        - ["Role", "recurring pursuer"]
categories: ["Machines", "Beach Surgery franchise"]
---
'''The mechanical seagull''' is a recurring antagonist of [[Beach Surgery (story)|Beach Surgery]]: a roughly twenty-metre aerial machine whose metal wings beat hard enough to blow people off rooftops, with excavator-style grapples on a pneumatic arm. It snatches [[Katita]] and [[Leif]] from the harbour and later reappears over [[the interior|the country–city seam]] as they near the climax.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

It crashes into the sandstone [[the post office|city post office]] mid-story, and its later return at the cabin signals to Katita that the city — and [[the beach]] — are near. Adapters frequently confuse or merge it with the smaller bird-shaped [[the data-harvesters|surveillance drones]] of the plains.

== See also ==
* [[the data-harvesters]] · [[the drone with the camera]]
"""

ART["newcastle"] = """---
title: Newcastle
strand: canon
kind: Place
aliases: ["Newcastle"]
editor: rose_house
infobox:
  title: Newcastle
  sections:
    - label: Place
      rows:
        - ["Region", "East coast, Australia"]
        - ["Role", "setting of the first half"]
        - ["Quality", "'ontological incompleteness'"]
        - ["Landmarks", "[[Bolton Street car park]]; [[the public baths]]"]
categories: ["Places", "Beach Surgery franchise"]
---
'''Newcastle''' is the coastal Australian city in which the first half of [[Beach Surgery (story)|Beach Surgery]] takes place, and the narrator's real home in the [[the frame|frame story]]. He calls it a "bite-sized labyrinth" of "ontological incompleteness" — a place of buildings that seem to vanish when you look away, such as [[Rose House]], glimpsed only from certain angles.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

Key locations include [[Bolton Street car park]] (where the story opens), [[the public baths]] (the astronaut's [[the alarm-clock baptism|alarm-clock baptism]]), [[the Watt Hotel]], [[Styx Creek]], and [[the Dampened Cardboard]] jazz club. The city's psychogeography has spawned its own strand of [[city tours]].

== See also ==
* [[Shanbudia]] · [[the interior]] · [[The Bolton Street Walk]]
"""

ART["shanbudia"] = """---
title: Shanbudia
strand: canon
kind: Place
aliases: ["Shanbudia"]
editor: nullify_a_fireball
infobox:
  title: Shanbudia
  sections:
    - label: Place
      rows:
        - ["Region", "West Asian peninsula (fictional)"]
        - ["Type", "desert megacity"]
        - ["Role", "site of [[the eruption]]"]
categories: ["Places", "Beach Surgery franchise"]
---
'''Shanbudia''' is the desert megacity where the narrator of [[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]] runs a United Nations workshop on "how children might play in the cities of the future," and where, at the closing dinner, he suffers the public breakdown he calls [[the eruption]].[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

On his final, strangely depopulated day he walks the empty motorways and climbs the dome of the conference centre in the heat — the episode that gives rise to the [[Empty World Meditations]]. Its interiors of synthesised nature (ski slopes, aquariums) prefigure the [[the data-harvesters|data-farmed]] countryside of the embedded story.

== See also ==
* [[the eruption]] · [[Empty World Meditations]] · [[the dome]]
"""

ART["characters"] = """---
title: Characters
strand: canon
kind: List
aliases: ["Characters", "list of characters"]
editor: tidal_ward
---
This is a list of characters in [[Beach Surgery (story)|Beach Surgery]] and its [[Beach Surgery (disambiguation)|adaptations]].

== Principal ==
* [[Katita]] — nurse and agent of [[the cycle]]
* [[Leif]] — amnesiac [[military engineer]]

== The frame ==
* [[C. W. Smith]] — author / narrator
* [[Les]] — the narrator's late friend; maker of the [[the bee automaton|aluminium bee automaton]]
* [[the wife]] — artist; original of [[Katita]]

== Embedded & recurring ==
* [[Rico the Architect]] and [[Mylar]]
* [[Mr and Mrs McRae]] — the [[the Mighty Mechas|Mighty Mechas]]
* [[the mechanic]] — who is also [[the military officer]]
* [[the boy in the waves]]

== See also ==
* [[Places]] · [[Timeline]]
"""

ART["places"] = """---
title: Places
strand: canon
kind: List
aliases: ["Places", "list of places", "locations"]
editor: rose_house
---
Locations in [[Beach Surgery (story)|Beach Surgery]] and the [[the frame|frame story]].

== Newcastle (first half) ==
* [[Bolton Street car park]] · [[the apartment]] · [[the abandoned shopping centre]]
* [[the preschool]] · [[the underground baths]] · [[the post office]]
* [[the public baths]] · [[the Watt Hotel]] · [[Styx Creek]] · [[the Dampened Cardboard]] · [[Rose House]]

== The interior (second half) ==
* [[the surgery]] · [[the service station]] · [[the radio igloo]]
* [[the watering hole]] · [[the cabin]]

== Elsewhere ==
* [[Shanbudia]] · [[the dome]] · [[the beach]]

== See also ==
* [[Characters]] · [[Newcastle]] · [[city tours]]
"""

ART["timeline"] = """---
title: Timeline
strand: canon
kind: List
aliases: ["Timeline", "chronology"]
editor: one_side_of_the_coin
banners:
  - "Because of [[the cycle]], this timeline is necessarily circular. Entries after the climax may also be entries before the opening. [cn]"
---
A chronology of [[Beach Surgery (story)|Beach Surgery]]. Times are given as in the novel's structural notes.

== Half One — Newcastle ==
* '''Ch.1''' (10:30pm–5:30am): [[Bolton Street car park]]; [[the Mighty Mechas]]; [[the hotdog]]; the [[the abandoned shopping centre|dust garden]].
* '''Ch.2''' (5:30am–12:30pm): rooftops; [[Dirtheart]]; [[the mechanical seagull]]; [[the preschool]]; [[Rico the Architect]].
* '''Ch.3''' (12:30pm–7:30pm): [[the underground baths]]; the harbour; the dissolve to [[the surgery|the desert hospital room]].

== Half Two — The interior ==
* '''Ch.4''' (7:30am–2:30pm): the drive; [[the service station]]; [[the radio igloo]].
* '''Ch.5''' (2:30pm–9:30pm): [[the watering hole]]; the [[the drone with the camera|photographs]]; [[the cabin]].
* '''Ch.6''' (9:30pm–4:30am): chaos at the cabin; [[the rocket cart]]; [[the wings]]; the reset.

Then [[the cycle|Ch.1 again]].

== See also ==
* [[the glitch]] · [[Characters]] · [[Places]]
"""

ART["disambig"] = """---
title: Beach Surgery (disambiguation)
strand: meta
kind: Disambiguation
aliases: ["Beach Surgery (disambiguation)", "Beach Surgery"]
editor: tidal_ward
---
'''A Complicated Surgery Will Take Place on the Beach Tonight''' may refer to:

== Source ==
* [[A Complicated Surgery Will Take Place on the Beach Tonight|The novel]] (2020) by [[C. W. Smith]]
* [[Beach Surgery (story)|The embedded story]] (''Beach Surgery''), the unfinished outline within it

== Print ==
* [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|The manga]] (2009–2017)
* [[The Coin Cycle]] — the tie-in novel series

== Screen ==
* [[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|The animated series]]
* [[O Procedimento]] (2016 Brazilian film)
* [[Karman (film)|Karman]] (2019 film)

== Stage & sound ==
* [[Satellite Voices]] (opera) · [[Counterclockwise (dance)]] · [[Empty World Meditations]] (album)

== Play & place ==
* [[Coin (One Side)]] (video game) · [[the pinball machine]] · [[Half Seven on the Beach]] (LARP) · [[The Bolton Street Walk]] (tour)

''If an internal link led you here, you may wish to change it to point directly to the intended article.''
"""

# ---------------------------------------------------------------- adaptations
ART["manga"] = """---
title: A Complicated Surgery Will Take Place on the Beach Tonight (manga)
strand: manga
kind: Manga series
aliases: ["the manga"]
editor: tidal_ward
edited_days_ago: 14
hatnotes:
  - "This article is about the manga. For the original novel, see [[A Complicated Surgery Will Take Place on the Beach Tonight]]. For the animated series, see [[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)]]."
banners:
  - "This article relies excessively on primary sources. Several volume release dates remain unverified, and the existence of [[Volume 0: The Outline]] is disputed by editors. [cn]"
infobox:
  title: A Complicated Surgery Will Take Place on the Beach Tonight
  subtitle: 複雑な手術は今夜浜辺で
  image:
    src: manga-cover-dokinana.jpg
    caption: "Cover art"
    credit: "Dokinana"
  sections:
    - label: Manga
      rows:
        - ["Genre", "Seinen · surreal action"]
        - ["Written by", "((Itsuki Maro))"]
        - ["Published by", "((Abrachas Shōten))"]
        - ["Magazine", "[[Monthly Karman Line]]"]
        - ["Original run", "2009 – 2017"]
        - ["Volumes", "14 [cn]"]
    - label: Related
      rows:
        - ["Based on", "[[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]]"]
categories: ["Manga", "Beach Surgery franchise", "Seinen manga"]
---
'''A Complicated Surgery Will Take Place on the Beach Tonight''' is a seinen manga adapting the [[A Complicated Surgery Will Take Place on the Beach Tonight|novel of the same name]]. Serialised in [[Monthly Karman Line]] from 2009, it follows [[Katita]] and [[Leif]] across [[the cycle|a single repeating day]].[ref:guide|''A Complicated Surgery: The Official Guidebook''. Abrachas Shōten, 2013.] It is regarded as the most faithful adaptation of the [[Newcastle]] half, though its handling of [[the glitch]] remains contentious.[ref:glitchessay|"The Glitch That Will Not Compute." Surgipelago essays.]

== Volumes ==
{{table}}
+ Tankōbon volumes (dates marked ██ are unverified).
! # !! Title !! Release
| 1 || [[The Rooftop and the Wire]] || 25 Mar 2009
| 5 || [[Rico the Architect (volume)|Rico the Architect]] || 30 Sep 2010
| 7 || [[The Tidal Ward]] || 22 Dec 2011
| 8 || [[Crocodiles and the Drone]] || ((██ ██ 2012))
| 14 || [[The Wings (volume)|The Wings]] || ((██ ██ 2017))
{{/table}}

== Reception ==
Critics praised its "deadpan rendering of catastrophe as weather."[ref:prq|''Plains Review Quarterly'', issue ((██)).] The Volume 7 hospital-room frame ([[The Tidal Ward]]) prompted a lasting dispute over whether [[the surgery|the desert surgery]] is "real."

== See also ==
* [[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|the anime]] · [[The Coin Cycle]]
"""

ART["manga-tidal-ward"] = """---
title: The Tidal Ward
strand: manga
kind: Manga volume
aliases: ["The Tidal Ward", "Volume 7"]
editor: tidal_ward
infobox:
  title: The Tidal Ward
  sections:
    - label: Manga volume
      rows:
        - ["Series", "[[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|the manga]]"]
        - ["Volume", "7 of 14"]
        - ["Released", "22 Dec 2011"]
        - ["Preceded by", "[[The Underground Baths (volume)|The Underground Baths]]"]
        - ["Followed by", "[[Crocodiles and the Drone]]"]
categories: ["Manga volumes", "Beach Surgery franchise"]
---
'''The Tidal Ward''' is the seventh volume of the [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|Beach Surgery manga]]. It dramatises the dissolve at the end of [[the cycle|Chapter Three]], in which [[the beach|the beach at dusk]] becomes a desert hospital room and [[Katita]], in scrubs, tells [[Leif]] they must "go for a drive."[ref:guide|''The Official Guidebook'', 2013.]

The volume introduces a hospital-room frame absent from the [[A Complicated Surgery Will Take Place on the Beach Tonight|novel]], igniting the long-running [[the surgery|"is the surgery real?"]] dispute.

{{dialogue|Katita|Honey. I know you have just woken up. But. We need to go for a drive.|closing lines, ''The Tidal Ward''}}

== See also ==
* [[The Wings (volume)]] · [[the glitch]]
"""

ART["anime"] = """---
title: A Complicated Surgery Will Take Place on the Beach Tonight (TV series)
strand: anime
kind: Animated series
aliases: ["the anime", "the TV series", "the animated series", "A Complicated Surgery Will Take Place on the Beach Tonight (anime)"]
editor: karman_line
edited_days_ago: 9
hatnotes:
  - "This article is about the indie animated series. For the manga, see [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)]]."
banners:
  - "The episode count is contested; at least one entry ([[The Anaesthetist Dreams of Tide]]) is [[lost media|widely believed never to have aired]]. [cn]"
infobox:
  title: A Complicated Surgery Will Take Place on the Beach Tonight
  sections:
    - label: Animated series
      rows:
        - ["Format", "Independent web animation"]
        - ["Run", "2012 – present"]
        - ["Episodes", "212 [cn]"]
        - ["Distribution", "online; ((various mirrors))"]
categories: ["Anime", "Web series", "Beach Surgery franchise"]
---
'''A Complicated Surgery Will Take Place on the Beach Tonight''' is a long-running, independently produced online animated series, in production since 2012. Unbound by a publishing schedule, it has grown to a contested '''212''' episodes, expanding [[Beach Surgery (story)|the story]] into side-narratives the [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|manga]] never touched.[ref:wiki|community episode list.]

The series is notorious for episodes that appear and disappear from its mirrors, blurring the line between canon and [[lost media]]. Its best-known and most disputed entry is [[The Anaesthetist Dreams of Tide]].

== See also ==
* [[List of episodes]] · [[the glitch]] · [[lost media]]
"""

ART["anime-ep"] = """---
title: The Anaesthetist Dreams of Tide
strand: anime
kind: Animated episode
aliases: ["The Anaesthetist Dreams of Tide", "Episode 114"]
editor: not_the_ocean
banners:
  - "Some editors hold that this episode '''never aired'''. Three contradictory fan-edits survive; this article describes the most-circulated. [cn]"
infobox:
  title: The Anaesthetist Dreams of Tide
  sections:
    - label: Episode
      rows:
        - ["Series", "[[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|the animated series]]"]
        - ["No.", "114 (disputed)"]
        - ["Runtime", "11:04"]
        - ["Status", "[[lost media|disputed / lost]]"]
categories: ["Anime episodes", "Lost media", "Beach Surgery franchise"]
---
'''The Anaesthetist Dreams of Tide''' is a disputed episode of the [[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|Beach Surgery animated series]]. In the most-circulated of three surviving fan-edits, [[Leif]] — under anaesthetic on [[the surgery|the desert table]] — dreams the entire [[Newcastle]] half from [[Katita]]'s point of view, implying the city chapters are themselves the surgery.[ref:fanedit|"The three edits of 114." community thread #4,201.]

If genuine, the episode would constitute a bridge across [[the glitch]]; sceptics argue it was authored after the fact precisely to seem to do so. See [[the Karman Line hypothesis]].

{{dialogue|Katita|You have done so well. Do not take the bandages off just yet.|from the circulated edit}}

== See also ==
* [[lost media]] · [[the glitch]] · [[The Tidal Ward]]
"""

ART["film-procedimento"] = """---
title: O Procedimento
strand: films
kind: Film (2016)
aliases: ["O Procedimento", "The Procedure (2016 film)"]
editor: dust_garden
infobox:
  title: O Procedimento
  sections:
    - label: Film
      rows:
        - ["Directed by", "((Vera Salgado))"]
        - ["Country", "Brazil"]
        - ["Released", "2016"]
        - ["Runtime", "78 min"]
        - ["Language", "Portuguese"]
categories: ["Films", "Beach Surgery franchise", "Brazilian films"]
---
'''O Procedimento''' (''The Procedure'') is a 2016 low-budget Brazilian film loosely adapting [[Beach Surgery (story)|Beach Surgery]], relocating the action to a coastal town in Bahia. [[Katita]] becomes a community nurse and [[Leif]] a stranded oil-rig engineer; [[the interior|the desert half]] is replaced by the sertão.[ref:fest|festival programme notes, ((██)) 2016.]

The film is celebrated for "solving" [[the glitch]] by simply refusing it: the two halves are shot as two separate films screened back-to-back, with an intermission standing in for the seam. This approach is itself the subject of [[On the unfinishable: recurrence and the outline form|scholarship]].

== See also ==
* [[Karman (film)]] · [[films]] · [[the glitch]]
"""

ART["film-karman"] = """---
title: Karman (film)
strand: films
kind: Film (2019)
aliases: ["Karman", "Karman (2019 film)"]
editor: karman_line
infobox:
  title: Karman
  sections:
    - label: Film
      rows:
        - ["Country", "((Estonia / co-production))"]
        - ["Released", "2019"]
        - ["Runtime", "61 min"]
        - ["Format", "16mm; mostly silent"]
categories: ["Films", "Beach Surgery franchise"]
---
'''Karman''' is a 2019 near-silent film that adapts only the [[Empty World Meditations|empty-world]] sequence of [[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]]: a single figure walking a depopulated desert city toward [[the beach]]. The dialogue is almost entirely absent; the soundtrack is dominated by a sustained low drone identified with [[the sound of the earth rubbing against space]].[ref:prog|press kit, 2019.]

Though [[Katita]] and [[Leif]] never appear, the film is treated as canonical by most editors for its fidelity to the novel's [[the frame|frame]].

== See also ==
* [[O Procedimento]] · [[Empty World Meditations]]
"""

ART["opera"] = """---
title: Satellite Voices
strand: opera
kind: Opera
aliases: ["Satellite Voices"]
editor: not_the_ocean
infobox:
  title: Satellite Voices
  sections:
    - label: Opera
      rows:
        - ["Composer", "((R. Adeyemi))"]
        - ["Premiere", "((██)) 2018"]
        - ["Acts", "two (one per half)"]
        - ["Voices", "satellite recordings (see below)"]
categories: ["Opera", "Beach Surgery franchise"]
---
'''Satellite Voices''' is an opera adapting [[Beach Surgery (story)|Beach Surgery]], realising a proposal made by the narrator within [[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]] itself: that '''instead of singing''', each time a performer opens their mouth the audience hears "live sounds recorded from satellites passing the earth."[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

Structured in two acts mirroring the story's two halves, the work leaves [[the glitch]] audible: between the acts the orchestra falls silent and the house sound system plays only [[the sound of the earth rubbing against space|the drone of the Kármán line]].

== See also ==
* [[Counterclockwise (dance)]] · [[Empty World Meditations]]
"""

ART["dance"] = """---
title: Counterclockwise (dance)
strand: dance
kind: Dance work
aliases: ["Counterclockwise", "Counterclockwise (dance)"]
editor: one_side_of_the_coin
infobox:
  title: Counterclockwise
  sections:
    - label: Dance work
      rows:
        - ["Choreographer", "((M. Halloran))"]
        - ["Premiere", "((██)) 2017"]
        - ["Dancers", "two"]
        - ["Duration", "≈ 50 min, performed in one unbroken loop"]
categories: ["Dance", "Beach Surgery franchise"]
---
'''Counterclockwise''' is a two-dancer work derived from [[the cycle]]. The choreography is built as a single phrase that, danced in reverse, returns the dancers exactly to their starting positions — staging [[Katita]]'s wish to make the world's spin reverse. The piece is performed as an unbroken loop; audiences may enter and leave at any point.[ref:prog|programme note, 2017.]

The dancers' only props are a length of bandage and a coin. See also [[the coin]].

== See also ==
* [[Satellite Voices]] · [[the cycle]]
"""

ART["game"] = """---
title: Coin (One Side)
strand: games
kind: Video game
aliases: ["Coin (One Side)", "Coin: One Side"]
editor: nullify_a_fireball
infobox:
  title: Coin (One Side)
  sections:
    - label: Video game
      rows:
        - ["Developer", "((small studio))"]
        - ["Released", "((██)) 2015"]
        - ["Genre", "side-scrolling escort game"]
        - ["Platforms", "PC; ((various))"]
categories: ["Video games", "Beach Surgery franchise"]
---
'''Coin (One Side)''' is an independent side-scrolling game adapting [[Beach Surgery (story)|Beach Surgery]] as an '''escort''' mechanic: the player controls [[Katita]], pushing [[Leif]] in [[the wheelchair]] from [[Bolton Street car park]] to [[the beach]] while [[Leif]] fires [[the hand cannon]] at threats the player cannot directly aim.[ref:readme|game readme, 2015.]

The game has no win state. On reaching [[the beach]] it resets to the start with the difficulty unchanged, enacting [[the cycle]]; a hidden counter records how many loops the player has completed. The title refers to [[the coin]] with only one side.

== See also ==
* [[the pinball machine]] · [[Half Seven on the Beach]] · [[the cycle]]
"""

ART["pinball"] = """---
title: The pinball machine
strand: pinball
kind: Pinball machine
aliases: ["the pinball machine", "Beach Surgery (pinball)"]
editor: bee_automaton
infobox:
  title: A Complicated Surgery (pinball)
  sections:
    - label: Pinball machine
      rows:
        - ["Manufacturer", "((unknown; Japan))"]
        - ["Produced", "((██)) (small run)"]
        - ["Music", "Bach hymn × Street Fighter melody"]
        - ["Status", "[[lost media|two machines known]]"]
categories: ["Pinball", "Lost media", "Beach Surgery franchise"]
---
'''The pinball machine''' is a rare, possibly apocryphal Beach Surgery pinball table. Its existence is bound up with [[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]], in which the boy narrator composes music for Japanese pinball machines he never hears played — melodies fusing a '''Bach hymn with a Street Fighter stage theme'''.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

Collectors dispute whether any Beach Surgery table was ever produced; the only cited evidence is a scanned photograph in a Japanese "Learn to Speak English" book. The "[[the beach|beach]]" multiball and "[[the wings|wizard mode: WINGS]]" are described in collector lore but unverified.

== See also ==
* [[Coin (One Side)]] · [[lost media]] · [[Street Fighter (tournament)]]
"""

ART["album"] = """---
title: Empty World Meditations
strand: music
kind: Album / meditation tapes
aliases: ["Empty World Meditations"]
editor: dust_garden
infobox:
  title: Empty World Meditations
  sections:
    - label: Album
      rows:
        - ["Format", "guided-meditation tapes; later LP"]
        - ["Released", "((██))"]
        - ["Voice", "second person"]
        - ["Source", "[[Shanbudia]] dome sequence"]
categories: ["Albums", "Audio", "Beach Surgery franchise"]
---
'''Empty World Meditations''' is a series of guided-meditation recordings (later collected on LP) realising the tapes the narrator imagines making in [[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]], after his depopulated last day in [[Shanbudia]].[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.] Each track addresses the listener in the second person, walking them through an emptied city.

{{quote|You are walking down the middle of a highway with one foot in the lane travelling south and one foot in the lane travelling north, and you see a city in the distance that you head towards.|from track one}}

Beneath the narration runs a sustained low tone identified with [[the sound of the earth rubbing against space]].

== See also ==
* [[Karman (film)]] · [[Satellite Voices]]
"""

ART["novels"] = """---
title: The Coin Cycle
strand: tie-in-novels
kind: Tie-in novel series
aliases: ["The Coin Cycle", "the tie-in novels"]
editor: one_side_of_the_coin
infobox:
  title: The Coin Cycle
  sections:
    - label: Novel series
      rows:
        - ["Books", "((41+)) and counting"]
        - ["Numbering", "non-linear"]
        - ["Publisher", "((various licensees))"]
categories: ["Tie-in novels", "Beach Surgery franchise"]
---
'''The Coin Cycle''' is an open-ended series of tie-in novels expanding [[Beach Surgery (story)|Beach Surgery]] in the manner of a long-running media franchise. Individual volumes follow minor figures — [[the mechanic]], [[Mr and Mrs McRae|the McRaes]], a [[Dirtheart]] activist — across loops of [[the cycle]].[ref:cat|publisher catalogue, ((██)).]

The books are deliberately '''un-numbered in sequence''': each is "Book One" of its own thread, so the series can grow forever without a fixed order — a structure critics tie directly to [[the glitch]].

== See also ==
* [[light novels]] · [[A Complicated Surgery Will Take Place on the Beach Tonight (manga)|the manga]]
"""

ART["larp"] = """---
title: Half Seven on the Beach
strand: larp
kind: Live-action role-play
aliases: ["Half Seven on the Beach"]
editor: not_the_ocean
infobox:
  title: Half Seven on the Beach
  sections:
    - label: LARP
      rows:
        - ["First run", "((██))"]
        - ["Duration", "one night (dusk to 7:30)"]
        - ["Players", "two principals + ensemble"]
        - ["Site", "a real coastline"]
categories: ["LARP", "Beach Surgery franchise"]
---
'''Half Seven on the Beach''' is a live-action role-play that stages a single loop of [[Beach Surgery (story)|Beach Surgery]] in real time across one evening, ending precisely at "half seven" — the deadline by which [[Katita]] must deliver [[Leif]] to [[the beach]].[ref:rules|player handbook, ((██)).]

Two players take the principals; an ensemble plays [[Dirtheart]] activists, [[the Mighty Mechas]], and military police. The game's one rule is that the principals may never break character to explain [[the glitch]]. Runs have been reported on coastlines in several countries.

== See also ==
* [[The Bolton Street Walk]] · [[Coin (One Side)]]
"""

ART["tour"] = """---
title: The Bolton Street Walk
strand: tours
kind: Walking tour
aliases: ["The Bolton Street Walk"]
editor: rose_house
infobox:
  title: The Bolton Street Walk
  sections:
    - label: Walking tour
      rows:
        - ["City", "[[Newcastle]]"]
        - ["Length", "≈ 5 km; ends at [[the beach]]"]
        - ["Stops", "12"]
categories: ["City tours", "Beach Surgery franchise"]
---
'''The Bolton Street Walk''' is a self-guided walking tour of the real [[Newcastle]] locations behind the first half of [[Beach Surgery (story)|Beach Surgery]], beginning on the rooftop of [[Bolton Street car park]] and ending at [[the beach]].[ref:map|tour map, ((██)).]

Stops include [[Rose House]], [[the Watt Hotel]], [[Styx Creek]], [[the Dampened Cardboard]] and [[the public baths]]. The tour leans into the city's "ontological incompleteness": several stops are buildings the novel describes as only visible from certain angles.

== See also ==
* [[Half Seven on the Beach]] · [[Places]] · [[Newcastle]]
"""

ART["thesis"] = """---
title: "On the unfinishable: recurrence and the outline form"
strand: theses
kind: Thesis / paper
aliases: ["On the unfinishable: recurrence and the outline form", "the standard thesis"]
editor: karman_line
infobox:
  title: "On the unfinishable"
  sections:
    - label: Paper
      rows:
        - ["Author", "((A. Whitfield))"]
        - ["Year", "((██))"]
        - ["Field", "comparative literature"]
categories: ["Theses & papers", "Beach Surgery franchise"]
---
'''On the unfinishable: recurrence and the outline form''' is a much-cited thesis arguing that [[A Complicated Surgery Will Take Place on the Beach Tonight|the novel]]'s refusal to finish [[Beach Surgery (story)|its embedded story]] is not a failure but its method: the outline form, by withholding "the he-said-she-said rigmarole," compels the reader's mind to "grow long legs" between widely spaced points.[ref:smith2020|Smith, C. W. ''A Complicated Surgery…'', 2020.]

The paper reads [[the glitch]] as a deliberate productive wound and the entire franchise as its "scar tissue." It is frequently set against [[the Karman Line hypothesis]], which it considers "an elegant error."

== Abstract ==
{{quote|Language can only ever talk about language; the outline, alone among forms, admits as much. Beach Surgery does not fail to end. It refuses to, and in refusing, it propagates.|from the abstract}}

== See also ==
* [[the glitch]] · [[fan theories]]
"""

ART["fan-theory"] = """---
title: The Karman Line hypothesis
strand: fan-theories
kind: Fan theory
aliases: ["the Karman Line hypothesis", "the Karman line hypothesis", "Karman Line hypothesis"]
editor: karman_line
banners:
  - "This article documents a '''fan theory''' and is not canon. [cn]"
categories: ["Fan theories", "Beach Surgery franchise"]
---
'''The Karman Line hypothesis''' is a popular fan reading holding that the two halves of [[Beach Surgery (story)|Beach Surgery]] do not connect in space at all but in '''pitch''': the [[Newcastle]] half is the low [[the sound of the earth rubbing against space|drone of the Kármán line]], the [[the interior|desert half]] its high inversion (the spine's resonance), and [[the glitch]] is simply the silent interval between the two tones.[ref:thread|community thread #1,300,041.]

Proponents cite [[The Anaesthetist Dreams of Tide]] as evidence; detractors (see [[On the unfinishable: recurrence and the outline form|the standard thesis]]) call it "an elegant error" that mistakes a metaphor for a mechanism.

== See also ==
* [[the glitch]] · [[the cycle]] · [[lost media]]
"""

ART["lost-media"] = """---
title: Lost media
strand: lost-media
kind: Overview
aliases: ["lost media", "the lost dub"]
editor: tidal_ward
---
This article catalogues '''lost, disputed, or never-confirmed''' Beach Surgery media — a category unusually large for this franchise, owing to its origins in an [[the glitch|unfinishable]] source and its [[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)|web-native]] distribution.

== Confirmed lost ==
* [[The Anaesthetist Dreams of Tide]] — animated episode "believed never to have aired"
* [[the pinball machine]] — possibly never manufactured

== Disputed ==
* '''The Portuguese dub of Volume 0''' — a dub of a manga volume ([[Volume 0: The Outline]]) that may not exist, of episodes that may not exist. [cn]
* '''The cardboard sessions''' — claimed field recordings of [[the Dampened Cardboard]]

== See also ==
* [[the glitch]] · [[the Karman Line hypothesis]] · [[A Complicated Surgery Will Take Place on the Beach Tonight (TV series)]]
"""

for name, text in ART.items():
    open(os.path.join(CONTENT, name + ".md"), "w", encoding="utf-8").write(text)
print(f"wrote {len(ART)} seed articles to {CONTENT}")

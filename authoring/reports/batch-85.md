# batch-85

Made by `qgen batch --media-first` on 2026-11-18 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 49 (q-21084…q-21132)
- Approved: 46
- Needs work: 3
- Dropped by the pipeline: 43
- Reviewed by: claude-opus-5-5
- Claude calls: 877, about $77.40 at list price; $1.68 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-83, batch-84; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-83 | batch-84 | batch-85 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 103 | 94 | 92 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 34 | 31 | 43 |
| drop rate | ≤ 20.0 % | 33.0 % ✗ | 33.0 % ✗ | 46.7 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 1 |
| dropped: hard fail unambiguous |  | 2 | 2 | 2 |
| dropped: hard fail no_giveaway |  | 4 | 6 | 5 |
| dropped: overlap |  | 26 | 21 | 33 |
| dropped: duplicate |  | 2 | 1 | 1 |
| dropped: fact-check wrong |  | 0 | 1 | 1 |
| merged |  | 69 | 63 | 49 |
| approved |  | 50 | 50 | 46 |
| needs_work |  | 19 | 13 | 3 |
| needs_work rate | ≤ 20.0 % | 27.5 % ✗ | 20.6 % ✗ | 6.1 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 14.5 % ✗ | 4.8 % ✓ | 2.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 3.2 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.9 % ✗ | 7.9 % ✗ | 2.0 % ✗ |
| needs_work: media | ≤ 10.0 % | 20.3 % ✗ | 11.1 % ✗ | 4.1 % ✓ |
| media: no pick in review 1 |  | 1 | 2 | 0 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 69 | 63 | 49 |
| needs_work: difficulty | ≤ 10.0 % | 2.9 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 1.6 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 29.1 % ✗ | 28.7 % ✗ | 38.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 35 | 30 | 23 |
| top move | ≤ 25.0 % | n/a | n/a | n/a |
| values move |  | n/a | n/a | n/a |
| top stimulus |  | n/a | n/a | n/a |
| values stimulus |  | n/a | n/a | n/a |
| top clue | ≤ 60.0 % | n/a | n/a | n/a |
| values clue |  | n/a | n/a | n/a |
| top answer_kind | ≤ 40.0 % | n/a | n/a | n/a |
| values answer_kind |  | n/a | n/a | n/a |
| top lens | ≤ 25.0 % | n/a | n/a | n/a |
| values lens |  | n/a | n/a | n/a |
| giveaway-step drop rate |  | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| mechanical-check rate |  | 4.3 % ✓ | 3.2 % ✓ | 0.0 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.50 ✓ | 3.38 ✗ | 3.45 ✓ |
| cost $ |  | $81.95 | $92.45 | $73.99 |
| $ per approved | ≤ $0.35 | $1.64 ✗ | $1.85 ✗ | $1.61 ✗ |
| calls |  | 901 | 1005 | 828 |
| calls per approved |  | 18.02 | 20.10 | 18.00 |
| wall time h |  | 1.42 | 2.51 | 1.76 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 46 (2 %)
- Major among review needs work: 1 of 3 (33 %)
- Problems by kind: giveaway 12 (1 major), fact 1 (0 major), overlap 1 (0 major), media 6 (2 major), difficulty 1 (0 major), style 1 (1 major)
- Mean |audit − final difficulty|: 0.6; ≥ 3 on 0 of 49 (0 %)
- Audit/review agreement (both accept or both not): 46 of 49 (94 %)
- Sample: 49 audited of 49; 49 Claude calls, about $3.41

Major findings on approved questions:

- **q-21095**: media, style — The facts hold up: the Gambia's anthem is "For The Gambia Our Homeland", Howe adapted the Mandinka tune "Foday Kaba Dumbuya", English is the official language, and it is the smallest country on mainland Africa, almost surrounded by Senegal. But the US Navy Band plays it as a Western-style hymn, just like the anthems of Ghana, Liberia and Sierra Leone, so players can't hear which one it is and can only guess (check 1 → media, with no good fix inside the window). There is also a small style problem: "football players" in the description is a word US and UK English use differently and should be reworded. I couldn't open the spectrogram, but the loudness (−19.8 LUFS) and near-zero silence look fine. (http://127.0.0.1:8001/review/q-21095)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 3 | 3 | 3 | 3 | 3 |
| cat:Audio files of national anthems | 30 | 6 | 6 | 6 | 2 | 2 |
| cat:Videos by NASA | 30 | 7 | 7 | 7 | 4 | 3 |
| cat:Videos of animals | 30 | 2 | 2 | 2 | 2 | 2 |
| cat:Videos of nature | 30 | 8 | 8 | 8 | 6 | 6 |
| q:audio:dog bark | 19 | 2 | 2 | 2 | 0 | 0 |
| q:audio:national anthem instrumental | 30 | 7 | 7 | 7 | 4 | 3 |
| q:audio:piano recording | 30 | 5 | 5 | 4 | 1 | 1 |
| q:audio:piano sonata public domain | 24 | 22 | 22 | 10 | 2 | 2 |
| q:video:NASA video launch | 30 | 4 | 4 | 4 | 4 | 4 |
| q:video:animal video wildlife | 1 | 0 | 0 | 0 | 0 | 0 |
| q:video:cooking video | 30 | 8 | 8 | 8 | 7 | 6 |
| q:video:experiment science video | 30 | 7 | 7 | 6 | 3 | 3 |
| q:video:machine working video | 30 | 0 | 0 | 0 | 0 | 0 |
| q:video:space station astronaut video | 30 | 4 | 4 | 4 | 2 | 2 |
| q:video:time-lapse video | 30 | 7 | 7 | 7 | 2 | 2 |
| q:video:traditional dance video | 30 | 11 | 11 | 11 | 5 | 5 |
| q:video:train video | 30 | 2 | 2 | 1 | 0 | 0 |
| q:video:volcano eruption video | 30 | 2 | 2 | 2 | 2 | 2 |
| total | 524 | 107 | 107 | 92 | 49 | 46 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 440 | 72 | 72 | 69 | 41 | 39 |
| pd-music | 84 | 35 | 35 | 23 | 8 | 7 |
| total | 524 | 107 | 107 | 92 | 49 | 46 |

- $ per approved: $1.68

## Needs work

- **q-21090** (drinks) Watch: which fruit is in the glass bowl next to the blender? → Peaches: At 24.04 s (frame 10), a faint caption is already fading in over the blender (you can make out a word ending in “…ened” on the sheet). That is the “1¼ cups peaches” ingredient card starting earlier than the note says. If the player holds the last frame while the family thinks, the text could name the answer. Trim the excerpt end to about 23.8 s, where frames 1–9 are clean, and the question can be approved as written.
- **q-21091** (countries) Listen: this is the national anthem of which country? → Vanuatu: Media-first check 1 fails. Almost no player, not even a trivia specialist, can tell Vanuatu's anthem apart from those of Fiji, Samoa or Tonga by ear. The clip decides nothing, and the answer comes only from hints 2 and 3. There is no other fair question about this instrumental window (for example "which kind of band" would be trivial and off-topic), so the file doesn't fit a question for these players.
- **q-21105** (weather-and-climate) Watch: the colors on this NASA world map are not actual temperatures. What do they show? → Temperature anomaly: This question uses the same NASA video as q-20673 (“Which part of the world turns the deepest red?” → The Arctic). Hint 2 here says the Arctic turns red, which gives away that question's answer. Either drop one of the two questions, or reword hint 2 so it no longer points to the Arctic, for example: “Places that are always cold can still show up red.”

## Question axes

- move: None 49
- stimulus: None 49
- clue: None 49
- answer_kind: None 49
- lens: None 49

## Dropped by the pipeline

- mf-044fca1b62: overlap like q-20824: Watch: what is the name of this type of cloud, which often forms over mountains? → Lenticular cloud: Watch: what type of cloud is the one sitting just above this mountain's snowy peak? → Lenticular cloud
- mf-0e098d2a63: overlap like q-21059: Listen: this is the national anthem of which country? → Czech Republic: Listen: this tune is today the national anthem of which European country? → The Czech Republic
- mf-10aab50870: overlap like q-20673: Watch this NASA map change from the 1880s to the 2010s. Which part of the world turns the deepest red? → The Arctic: Watch: this NASA map turns red as the years pass from 1880 to 2011. What is the name for the pattern at the very top, where the red becomes darkest? → Arctic amplification
- mf-16852f46fe: overlap like q-16727: Cartoon aliens in flying saucers love to visit the planet in this photo. Which planet is it? → Earth: Watch: which planet is spinning in this video? → Earth
- mf-1a42de7853: overlap like q-20820: Listen: from which era of Western music does this solo piano piece come? → Classical era: Listen: from which era of music history does this piano piece come? → The Classical era
- mf-1e2bfabf74: overlap like q-2416: A giant steel arch bridge is nicknamed “the Coathanger”. In which city does it stand? → Sydney: Watch: in which city was this time lapse of a big steel arch bridge over a harbor filmed? → Sydney
- mf-200fb8ae56: overlap like q-20367: Before rugby matches, this team's players chant, slap their thighs and stick out their tongues in a Māori war dance. Which country are they from? → New Zealand: Watch: what is the name of the traditional group dance these workers are performing? → Haka
- mf-308175af04: overlap like q-20939: Listen: this piano piece opens with a tempo marking in Italian. Which one fits what you hear? → Presto: Listen: this piano sonata movement is named after its Italian tempo marking. Which marking is it? → Prestissimo
- mf-3149b2dfe5: overlap like q-11891: Monument Valley's red rock towers sit on the border between Arizona and the state shown on this map. Which state is it? → Utah: Watch: which famous landscape is shown in this time-lapse? → Monument Valley
- mf-31a894125b: fact-check wrong: The answer (Puerto Rico), the wrong answers, the hints and the fun fact are all correct. One detail in the media metadata is wrong: media.work.basis says the composer died in 1905. Félix Astol Artés died on 21 January 1901. The recording is still public domain, because it is a US Navy Band work and the composer died long ago. Authorship is also disputed: some evidence points to Francisco Ramírez's 1860 danza 'La Almojábana'.: Listen: this is the official anthem of which Caribbean island? → Puerto Rico
- mf-3e910c0b29: overlap like q-20636: Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Listen: which composer wrote this fast, fiery piano piece? → Ludwig van Beethoven
- mf-3f00bfcff8: overlap like q-20809: Listen to the very first notes: which nickname does music theory give this quick broken-chord figure? → Mannheim rocket: Listen to the opening: a loud chord, then a fast broken chord that shoots upward. What is this Classical-era musical gesture called? → Mannheim rocket
- mf-427f783996: overlap like q-20693: Watch: in which country is this festival dance performed? → India: Watch: masked dancers in straw skirts perform at a village festival in the mountains. In which country is this? → India
- mf-4845f6f2f5: overlap like q-1510: ¿De qué país es el himno nacional que empieza «Gloria al bravo pueblo»? → Venezuela: Listen: this is the national anthem of which South American country? → Venezuela
- mf-4d90c537b8: duplicate like q-21033: Listen to the sound of this piano-and-orchestra recording. In which decade was it most likely recorded? → The 1930s: Listen to the sound of this piano recording, not just the notes. In which decade was it most likely made? → The 1930s
- mf-539647514f: overlap like q-20982: Watch: what is this huge spacecraft circling high above Earth? → The International Space Station: Watch: where was this footage filmed? → The International Space Station
- mf-5fe8e90d6d: overlap like q-5913: What is this rushing, foamy stretch of a river, full of rocks, called? → Rapids: Watch: which river feature do you see in this video? → Rapids
- mf-61fd587b28: overlap like q-20698: Watch: which kind of spacecraft is lifting off here? → Space Shuttle: Watch: astronauts filmed this giant fuel tank falling away about 8 minutes after launch. Which spacecraft dropped it? → The Space Shuttle
- mf-649cd6d8b8: overlap like q-20705: Listen: this melody is the national anthem of two neighboring countries. Which two? → Finland and Estonia: Listen: this old recording is the national anthem of which country, sung by a choir in that country's own language? → Finland
- mf-74997ef203: overlap like q-20811: Listen: what kind of piece by Mozart is this? → A piano sonata: Listen: what type of piano music is this? → A piano sonata
- mf-7af7574198: overlap like q-20873: Watch: dancers in coral beads and checked wrappers perform to drums. Which country is this traditional dance from? → Nigeria: Watch: men in red caps and wrappers perform a traditional war dance, beating a bundle of sticks. In which country are they? → Nigeria
- mf-82be8b5f29: overlap like q-6826: Tiene un vaso grande con tapa, cuchillas que giran por debajo y en Colombia nunca falta para hacer jugo de mora. ¿Qué es? → La licuadora: Watch: which kitchen machine is the fruit going into? → A blender
- mf-8342bfe049: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: Watch: this masked night-time folk dance is taken from house to house, with the performers receiving gifts. In which Indian state is it at home? → Karnataka
- mf-87762229d1: overlap like q-17450: Esta máscara de viejito sonriente es de la famosa Danza de los Viejitos. ¿Quiénes la bailaron primero? → Los michoacanos: Watch: this masked dancer with a cane is performing a famous traditional dance. Which Mexican state does it come from? → Michoacán
- mf-9fb13366fd: overlap like q-20860: Listen to this choir from a Mass by Mozart. Which musical form is it singing? → Fugue: Listen: this passage from a Beethoven piano sonata is built like which kind of piece? → A fugue
- mf-a006a273ff: overlap like mf-0e098d2a63: Listen: this tune is today the national anthem of which European country? → The Czech Republic: Listen: this former national anthem joins two songs, a slow one followed by a quicker one. Which country used it? → Czechoslovakia
- mf-a2a9770699: overlap like q-9050: What is the job of the people in this photo? → Astronauts: Watch: these people in white suits and helmets are setting off on a trip. Where are they going? → Into space
- mf-aab1db31e9: overlap like q-13350: Escucha: ¿qué pájaro hace este sonido? → La paloma: Listen: which kind of bird is making this soft, rhythmic call? → A dove
- mf-bb3b9b8d1e: overlap like q-20820: Listen: from which era of Western music does this solo piano piece come? → Classical era: Listen: from which period of Western classical music does this piano piece come? → The Classical period
- mf-c23d166210: overlap like q-20826: Listen to this fast, furious piano finale. Which nickname does the sonata it comes from have? → “Moonlight” Sonata: Listen: this light, dance-like middle movement comes from which famous Beethoven piano sonata? → The “Moonlight” Sonata
- mf-c42c17f4f4: overlap like q-19845: Listen: which British animal is making this scream at night in towns and gardens? → A fox: Listen: these short barks were recorded at night in the English countryside. Which wild animal is making them? → A red fox
- mf-c70e5eddaa: hard fail: correct 4, unambiguous 4, no_giveaway 2, no_overlap 5: Watch: this dog's leash is caught around a pole. What does the dog do to get free? → It walks back around the pole
- mf-ce02cfd7b3: overlap like q-20910: Listen: which Italian tempo marking did the composer write at the top of this piano movement? → Allegro vivace: Listen: which Italian tempo marking would a composer write above music played like this? → Allegro
- mf-d30b0f6d79: overlap like q-16981: Hoffmann von Fallersleben dichtete es 1841 auf Helgoland, die Melodie stammt von Joseph Haydn. Was ist es heute? → Die deutsche Nationalhymne: Listen: this melody is a national anthem today. Which composer wrote it? → Joseph Haydn
- mf-dcdd92cf99: overlap like q-20683: Watch: a commuter train heads downtown toward a very tall tower. Which city is this? → Toronto: Watch: this green-and-white double-decker commuter train with the big “GO” logo serves which city's region? → Toronto
- mf-e56479942d: overlap like q-4289: You're reading fables where a slow tortoise beats a hare and a fox calls some grapes sour. Which ancient Greek storyteller are they credited to? → Aesop: Watch what this bird does to reach the water. Scientists named this test after a fable by which storyteller? → Aesop
- mf-f98898d111: overlap like q-3311: What are these huge metal boxes stacked at the port called? → Shipping containers: Watch: from which kind of ship was this time-lapse filmed as it sails into port? → A container ship
- mf-06f352d885: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Listen: which South American country's national anthem is this? → Bolivia
- mf-38ec9b11a7: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Watch: a ship glides between ice cliffs and snowy peaks, with no trees, roads or towns in sight. On which continent is it? → Antarctica
- mf-6770a354ba: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 4: Listen: the piano never stops running in even, rapid notes. What is the musical name for a piece like this? → Perpetuum mobile
- mf-dcb34b74fa: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch the sun and the clock in the corner of this time-lapse. What is this called? → Midnight sun
- mf-eb082c1e07: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: look at the glowing light on the right side of the picture. Why do space gardens use light of this color? → Plants use red and blue light the most
- mf-eec31e6f91: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 4: Watch: in which country is this carnival dancer twirling to the band? → Mexico

# batch-87

Made by `qgen batch --media-first` on 2026-11-18 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 13 (q-21191…q-21203)
- Approved: 12
- Needs work: 1
- Dropped by the pipeline: 15
- Reviewed by: claude-opus-5-5
- Claude calls: 335, about $28.81 at list price; $2.40 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-85, batch-86; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-85 | batch-86 | batch-87 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 92 | 87 | 28 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 43 | 29 | 15 |
| drop rate | ≤ 20.0 % | 46.7 % ✗ | 33.3 % ✗ | 53.6 % ✗ |
| dropped: hard fail correct |  | 1 | 1 | 1 |
| dropped: hard fail unambiguous |  | 2 | 2 | 1 |
| dropped: hard fail no_giveaway |  | 5 | 0 | 2 |
| dropped: overlap |  | 33 | 24 | 10 |
| dropped: duplicate |  | 1 | 2 | 1 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 49 | 58 | 13 |
| approved |  | 46 | 49 | 12 |
| needs_work |  | 3 | 9 | 1 |
| needs_work rate | ≤ 20.0 % | 6.1 % ✓ | 15.5 % ✓ | 7.7 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 2.0 % ✓ | 13.8 % ✗ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.0 % ✗ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 4.1 % ✓ | 8.6 % ✓ | 7.7 % ✓ |
| media: no pick in review 1 |  | 0 | 1 | 0 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 49 | 58 | 13 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 7.7 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 38.0 % ✗ | 29.9 % ✗ | 39.3 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 23 | 26 | 6 |
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
| mechanical-check rate |  | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.45 ✓ | 3.52 ✓ | 3.32 ✗ |
| cost $ |  | $73.99 | $67.05 | $27.75 |
| $ per approved | ≤ $0.35 | $1.61 ✗ | $1.37 ✗ | $2.31 ✗ |
| calls |  | 828 | 725 | 322 |
| calls per approved |  | 18.00 | 14.80 | 26.83 |
| wall time h |  | 1.76 | 1.89 | 1.27 |
| days |  | 2 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 12 (0 %)
- Major among review needs work: 0 of 1 (0 %)
- Problems by kind: giveaway 3 (0 major), fact 1 (0 major), difficulty 1 (0 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 1 of 13 (8 %)
- Audit/review agreement (both accept or both not): 12 of 13 (92 %)
- Sample: 13 audited of 13; 13 Claude calls, about $1.05

Major findings on approved questions:

None.

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 7 | 7 | 7 | 1 | 1 |
| cat:Audio files of national anthems | 15 | 1 | 1 | 1 | 0 | 0 |
| cat:Videos of animals | 22 | 5 | 5 | 5 | 4 | 4 |
| cat:Videos of nature | 30 | 2 | 2 | 2 | 2 | 2 |
| q:audio:piano recording | 30 | 1 | 1 | 1 | 1 | 1 |
| q:video:cooking video | 7 | 0 | 0 | 0 | 0 | 0 |
| q:video:experiment science video | 30 | 2 | 2 | 2 | 1 | 1 |
| q:video:machine working video | 7 | 1 | 1 | 1 | 0 | 0 |
| q:video:traditional dance video | 16 | 6 | 6 | 6 | 3 | 3 |
| q:video:train video | 25 | 3 | 3 | 3 | 1 | 0 |
| q:video:volcano eruption video | 30 | 0 | 0 | 0 | 0 | 0 |
| total | 242 | 28 | 28 | 28 | 13 | 12 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 227 | 27 | 27 | 27 | 13 | 12 |
| pd-music | 15 | 1 | 1 | 1 | 0 | 0 |
| total | 242 | 28 | 28 | 28 | 13 | 12 |

- $ per approved: $2.40

## Needs work

- **q-21198** (trains) Watch: in which country does this green-and-white commuter train run? → Canada: Only people who know Ontario's GO Transit can recognise this train, so a base question breaks the International angle. The clip itself doesn't settle the answer: a snowy platform and a green-and-white diesel with bi-level coaches could just as well be in the US (the same Bombardier BiLevel coaches run on several US lines), so everyone else has to guess between the United States and Canada. The country only becomes clear from the hints that point to Lake Ontario and Toronto, not from what plays on screen.

## Question axes

- move: None 13
- stimulus: None 13
- clue: None 13
- answer_kind: None 13
- lens: None 13

## Dropped by the pipeline

- mf-1401aa2763: overlap like q-9489: Listen: which bird makes this sound in British woods at night? → An owl: Listen: which bird makes these wavering night-time hoots? → Tawny owl
- mf-2977467181: overlap like mf-1401aa2763: Listen: which bird makes these wavering night-time hoots? → Tawny owl: Listen to this bird calling in the woods. At what time of day are you most likely to hear this sound? → In the middle of the night
- mf-442da88204: overlap like q-18836: About how many different song phrases can a male nightingale sing? → About 200: Listen: which bird is singing? → Nightingale
- mf-53007e755b: overlap like q-20287: Listen: British birdwatchers say this great tit's song sounds like it's calling out for someone. Who? → Teacher: Listen: which small European garden bird is singing this repeated two-note song? → Great tit
- mf-5a1e7d5682: overlap like q-9914: Tengo hilos tensos, una lanzadera va y viene por mí y en la Alpujarra se tejen jarapas conmigo. ¿Qué soy? → Un telar: Watch: which machine is at work in this old factory? → Power loom
- mf-6aa0a76bf4: overlap like q-14082: Hör zu: Welcher Vogel singt hier im Garten? → Amsel: Listen: which bird is singing this song on a spring evening in a European city? → Blackbird
- mf-6e230645ca: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: this chick hatched on a tropical Pacific island. Which seabird will it grow up to be? → Red-tailed tropicbird
- mf-7ef3f84345: duplicate like q-20744: Watch: which famous aircraft is taking off here? → SR-71 Blackbird: Watch: this black jet is a close sibling of which famous plane? → SR-71 Blackbird
- mf-9abf19b0d4: overlap like q-20367: Before rugby matches, this team's players chant, slap their thighs and stick out their tongues in a Māori war dance. Which country are they from? → New Zealand: Watch: what is the name of the traditional chant and dance these soldiers are performing? → Haka
- mf-a2dfd75f9a: overlap like q-4028: Listen: which animal is talking like a person? → A parrot: Listen: which animal is whistling, laughing and chattering in this recording? → Parrot
- mf-cc7c09b038: overlap like q-21161: Listen: this jazz version, with its melody played loosely, is based on which country's national anthem? → Japan: Listen: this is the national anthem of which country? → Japan
- mf-e5f6a100dd: overlap like q-20683: Watch: a commuter train heads downtown toward a very tall tower. Which city is this? → Toronto: Watch: this green-and-white double-decker commuter train belongs to a network centered on which city? → Toronto
- mf-33c6ca2d3e: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: this festive metro train runs in which capital city? → Moscow
- mf-5f52b5aef7: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Watch: the tall, leaf-shaped carved figure in the middle of the backdrop is a famous prop from which art form? → Wayang puppet theater
- mf-886c55e0a0: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 5: Watch: this Swedish folk dance, where two men act out a playful fight, is named after which animal? → Ox

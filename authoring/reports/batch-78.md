# batch-78

Made by `qgen batch --media-first` on 2026-11-15 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 13 (q-20634…q-20646)
- Approved: 8
- Needs work: 5
- Dropped by the pipeline: 4
- Reviewed by: claude-opus-5-5
- Claude calls: 143, about $13.42 at list price; $1.68 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-76, batch-77; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-76 | batch-77 | batch-78 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | batch | batch | media-first |
| drafts |  | 131 | 125 | 17 |
| skipped slots |  | 373 | 379 | 0 |
| dropped |  | 55 | 57 | 4 |
| drop rate | ≤ 20.0 % | 42.0 % ✗ | 45.6 % ✗ | 23.5 % ✗ |
| dropped: hard fail correct |  | 0 | 0 | 0 |
| dropped: hard fail unambiguous |  | 0 | 0 | 0 |
| dropped: hard fail no_giveaway |  | 6 | 11 | 1 |
| dropped: overlap |  | 48 | 46 | 3 |
| dropped: duplicate |  | 1 | 0 | 0 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 76 | 68 | 13 |
| approved |  | 72 | 65 | 8 |
| needs_work |  | 4 | 3 | 5 |
| needs_work rate | ≤ 20.0 % | 5.3 % ✓ | 4.4 % ✓ | 38.5 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 2.6 % ✓ | 0.0 % ✓ | 38.5 % ✗ |
| needs_work: fact | ≤ 10.0 % | 1.3 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.3 % ✗ | 2.9 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 1.5 % ✓ | 15.4 % ✗ |
| media: no pick in review 1 |  | 4 | 7 | 1 |
| media: recovered by research |  | 4 | 6 | 0 |
| media: no pick at record |  | 0 | 1 | 13 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 38.2 % ✗ | 38.4 % ✗ | 17.6 % ✓ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 0 | 2 | 6 |
| top move | ≤ 25.0 % | 18.4 % ✓ | 13.2 % ✓ | n/a |
| values move |  | 14 | 13 | n/a |
| top stimulus |  | 81.6 % | 88.2 % | n/a |
| values stimulus |  | 3 | 3 | n/a |
| top clue | ≤ 60.0 % | 34.2 % ✓ | 36.8 % ✓ | n/a |
| values clue |  | 5 | 5 | n/a |
| top answer_kind | ≤ 40.0 % | 27.6 % ✓ | 23.5 % ✓ | n/a |
| values answer_kind |  | 7 | 7 | n/a |
| top lens | ≤ 25.0 % | 18.4 % ✓ | 22.1 % ✓ | n/a |
| values lens |  | 10 | 11 | n/a |
| giveaway-step drop rate |  | n/a | n/a | 0.0 % ✓ |
| mechanical-check rate |  | n/a | n/a | 0.0 % ✓ |
| media share | 15.0 %–50.0 % | 18.4 % ✓ | 11.8 % ✗ | n/a |
| mean fun | ≥ 3.40 | 3.50 ✓ | 3.47 ✓ | 3.47 ✓ |
| cost $ |  | $28.92 | $25.19 | $12.37 |
| $ per approved | ≤ $0.35 | $0.40 ✗ | $0.39 ✗ | $1.55 ✗ |
| calls |  | 205 | 178 | 130 |
| calls per approved |  | 2.85 | 2.74 | 16.25 |
| wall time h |  | 0.96 | 0.86 | 0.90 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 0 of 8 (0 %)
- Major among review needs work: 3 of 5 (60 %)
- Problems by kind: giveaway 6 (3 major), overlap 1 (0 major), media 2 (1 major), difficulty 1 (1 major)
- Mean |audit − final difficulty|: 1.1; ≥ 3 on 1 of 13 (8 %)
- Audit/review agreement (both accept or both not): 11 of 13 (85 %)
- Sample: 13 audited of 13; 13 Claude calls, about $1.06

Major findings on approved questions:

None.

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| q:audio:classical music recording symphony | 30 | 12 | 12 | 12 | 8 | 5 |
| q:audio:opera aria recording | 10 | 5 | 5 | 5 | 5 | 3 |
| total | 40 | 17 | 17 | 17 | 13 | 8 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| pd-music | 40 | 17 | 17 | 17 | 13 | 8 |
| total | 40 | 17 | 17 | 17 | 13 | 8 |

- $ per approved: $1.68

## Needs work

- **q-20636** (classical-music) Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Hints 1 and 2 give the answer away: “born in Bonn, lived in Vienna” and especially “kept writing music after going almost completely deaf” name Beethoven outright among Mozart, Haydn and Schubert. The clip then doesn't matter. Hints 1 and 2 should stay vague and point back to the music, for example the era (around 1800) or a feature you can hear, such as the bold, restless energy that breaks with classical politeness. Only hint 3 may come close to the answer.
- **q-20639** (classical-music) Listen: this soprano aria comes from an opera its composer left unfinished when he died. Who wrote it? → Giacomo Puccini: The description (“a princess who would rather give her suitors an exam”) describes Turandot's riddle plot, which gives away Puccini before any hint. The question text's “opera its composer left unfinished when he died” is Turandot's best-known fact too, so adults at this level can answer from the text alone and the clip isn't needed. Rewrite the description so it plays on opera in general, not on the riddles. Move the clue to what is heard (for example a soprano in a grand early-20th-century Italian style), or drop it.
- **q-20640** (classical-music) Listen: this lively finale closes a composer's last symphony, written in 1788. Who composed it? → Wolfgang Amadeus Mozart: The question text can be answered without the clip. "A composer's last symphony, written in 1788" rules out Schubert (born 1797) and Mendelssohn (born 1809). It also points to Mozart for any well-read adult, since Mozart's last symphonies date from 1788 and Haydn kept writing symphonies until 1795. Move the clue to what can be heard, for example the finale's fugue-like weaving of several themes at once, or cut the year. The distractors should also be composers who were active in 1788.
- **q-20644** (classical-music) Listen: in which language is this opera aria sung? → Italian: Hints 1 and 2 give the answer away: in a question about an opera aria, “the language of most of the famous operas” and “the country of Verdi and Puccini” both clearly point to Italian. The clip may also not carry the answer. The spectrogram shows a loud, flat hiss band up to about 17 kHz over the whole window, and whisper couldn't make out a single word (it produced gibberish and guessed Latin). Players will probably fall back on “opera = Italian” instead of listening to the words, so this window may not work for a language question.
- **q-20646** (classical-music) Listen to the opening: which Beethoven symphony begins like this? → Symphony No. 1: The description ("Vienna, around 1800… a young composer") gives the answer away. It dates the piece to about 1800, which rules out No. 4 (1807) and No. 8 (1814), and points to Beethoven's first symphony before anyone hears the clip. Separately, the clip test itself is a pure ear test: few listeners can tell the slow opening of No. 1 from those of Nos. 2 and 4. Players can only reason towards the answer from the text clues, so consider asking something the 50-second window lets them hear instead.

## Question axes

- move: None 13
- stimulus: None 13
- clue: None 13
- answer_kind: None 13
- lens: None 13

## Dropped by the pipeline

- mf-2e70fd41f8: overlap like q-20636: Listen to this symphony. Its composer first dedicated it to Napoleon, then scratched out his name when Napoleon became emperor. Who was the composer? → Ludwig van Beethoven: Listen: this is the finale of one of Beethoven's symphonies, recorded in 1929. What nickname does that symphony have? → Eroica
- mf-72ebf3131d: overlap like mf-62f02951f0: Listen: this movement from a famous 1808 symphony paints a scene from nature. What does the music depict? → A thunderstorm: Listen: this symphony is known by a nickname that tells you what it paints in sound. What is its nickname? → Pastoral
- mf-c0dad5416d: overlap like q-20634: Listen: who composed this lively piece with its racing flute melody? → Johann Sebastian Bach: Listen: from which era of classical music does this piece come? → Baroque
- mf-51767879cf: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 4: Listen: the steady ticking chords in this movement of Beethoven's Eighth Symphony are often said to imitate which device? → The metronome

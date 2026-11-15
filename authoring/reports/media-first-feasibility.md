# Media-first feasibility: Commons supply and pilot

Findings of `plan 201: Feasibility: Commons supply survey and pilot`: whether Wikimedia Commons holds enough free audio and video to build `milestone 21: add 1000 multimedia questions to the base bundle` around, what a question costs, and which judging aids let an LLM assess media it can't hear or watch. Numbers come from `work/media-survey/` (survey, task 2044) and `work/media-pilot/pilot-1/` (pilot, task 2046; probe aids, task 2045). The developer's look at the pilot (`decision 642: Media-first pilot: how many would you approve?`) is not in yet: every estimate below is before that share.

## Supply
- Count to beat: `decision 641: Milestone 21's count: what makes 1000 additional multimedia questions` (≥ 1058 approved audio/video base sources).
- Survey: 600 API calls, ~58 min; 6632 files kept after filters.
- Kept files by type and class (excerpt = longer than 60 s, up to 600 s):

| type | class | files | ≤ 60 s | needs excerpt |
|---|---|---|---|---|
| audio | general | 2193 | 1007 | 1186 |
| audio | pd-music | 886 | 204 | 682 |
| video | general | 3369 | 1816 | 1553 |
| video | pd-film | 184 | 37 | 147 |

- `audio/midi`: 82 of the audio files (64 pd-music, 18 general); not playable by the game's tools, to drop (`task 2050: Media survey: drop MIDI and unreadable files`).
- Filtered out (counts): audio < 2 s 1619, video < 480p 701, not audio/video 621, video > 600 s 579, duplicate across seeds 303, audio > 600 s 205, licence 75, restriction 54, already in a pool 11.
- Kinds by category (full table in `work/media-survey/tally.md`):
  - audio general: animal (animals 404, pets-and-farm 86, amazon 70, planet-earth 62, plants-and-environment 40), instrument (music 577), machine (transport 356, inventions-and-technology 264), place (architecture-and-landmarks 287, religion-and-philosophy 286, planet-earth 216, plants-and-environment 213)
  - audio pd-music (piece): music 606, world-geography (anthems) 524, history 280, art-and-literature 35
  - video general (scene): planet-earth 779, space 717, plants-and-environment 487, animals 471, transport 333, others 86–229
  - video pd-film: history 174 (newsreels), film-tv-and-superheroes 32
- Thin: history audio (21 general), languages-and-words (16 language, 22 place), video-games (1), pd-film total (184). Several seeds map to many categories (counted under each), so category rows overlap and must not be summed.
- Missing from the survey: no category for celebrities/people, food (audio), science audio; all video categories come from a few seeds mapped to many slugs, so per-category supply is softer than the table.
- Excerpts: 3568 of 6632 files (54 %) need an excerpt to fit `MAX_AUDIO_SECONDS` 60; in the pilot 48 of 60 designed questions carry one. Excerpt bounds are therefore the norm, not the exception: the pipeline and the player (parts 2 and 4 of `plan 200: masterplan`) must support start/end.

## Pilot yield and cost
- Sample: 250 files, seed 201, shares general 64 % / pd-music 18 % / pd-film 18 %, round robin over seeds (so seeds are over-represented against their file counts).
- Probed 247 (3 failures: 2 MIDI, 1 mp3 with an ID3 tag in a RIFF header).

| class | files | worth it | designed | passed giveaway check |
|---|---|---|---|---|
| general | 160 | 36 (22 %) | 36 | 35 |
| pd-music | 45 | 20 (44 %) | 20 | 20 |
| pd-film | 45 | 4 (9 %) | 4 | 3 |
| all | 250 | 60 (24 %) | 60 | 58 (97 %) |

- Audio 39 designed of 144 files (27 %), video 21 of 106 (20 %); video fails the giveaway check more (19 of 21).
- Good seeds: thunder/rain (3 of 3), cat sounds (2 of 2), classical, opera, national anthems (44–56 %), rover/NASA/launch video, bird calls; zero yield: Lingua Libre pronunciation, newsreels (0 of 11), church bells, trains/cars/aircraft audio, rainforest and ocean ambience, bird song search, city names.
- Cost: 557 claude calls, $18.35 (sonnet $12.59, opus $5.76), 2h06m in calls, 59 min wall (probes included). Per designed question $0.31 and 2.1 min; per passed question ≈ $0.32.
- Sketch of expected approved, before the look share (yield per file × kept files; pilot seeds were round robin, so it's an upper-ish estimate; near-duplicates like many files of one species lower it):
  - general: 5562 × 22 % ≈ 1200
  - pd-music: ~820 non-MIDI × 44 % ≈ 360
  - pd-film: 184 × 7 % ≈ 13
  - without `pd-music`/`pd-film`: ≈ 1200; with: ≈ 1570; for 1.3 × 1000 expected approved the look share would have to be ≈ 83 % with both classes and can't be reached with general alone (≈ 1200 before the share); the go/no-go decision (`task 2049: Raise the media-first go/no-go decision`) does the exact arithmetic with the look share.
  - Cost for ~1000 approved at $0.32 designed + review: ≈ $350–500 for design alone at the pilot's yield (more files must be triaged per approved: 250 files cost $18 for 58).

## Which aids worked
Ablation: blind triage (title + description) vs aided triage on the same 247 files. Worth it 53 blind vs 60 aided; 42 yes→yes, 18 no→yes, 11 yes→no; same category on 226, same kind on 215. The aided triage flagged 5 files whose content doesn't match the title. Per aid, files where it changed or confirmed the verdict:

| aid | wrong content | spoken giveaway | written giveaway | quality reject | verdict |
|---|---|---|---|---|---|
| speech (whisper) | 18 | 42 | 0 | 3 | keep: the only aid that finds spoken names; also catches wrong content (e.g. a speech file titled as something else) |
| ocr | 0 | 0 | 41 | 0 | keep for video: only source of written giveaways (captions, titles, watermarks) |
| frame sheet | 1 | 0 | 3 | 7 | keep: needed to recognise the scene at all; 95 confirms |
| spectrogram | 4 | 0 | 0 | 32 | keep: wrong content and silence/noise rejects |
| loudness | 0 | 0 | 0 | 74 | keep, cheap: drives most quality rejects (very quiet files, -37 to -43 LUFS) |
| waveform | 0 | 0 | 0 | 45 | drop or merge into the spectrogram: no effect other than quality rejects loudness already gives |
| silence share | 0 | 0 | 0 | 22 | merge into loudness: 169 of 197 no effect; keep as a number in the prompt, not a picture |

- Caveats: ground truth was Commons categories only; the "subject matches" counts (blind 207, aided 202) don't separate the arms. The aid's value comes mostly from the giveaway and wrong-content rows, not from the match rate. The developer's look will add the real ground truth.
- Recommended aids for review and audit prompts: transcript with language guess, OCR text of the frames, frame sheet, spectrogram, loudness + silence numbers. Drop the waveform picture.

## Giveaways found
- Spoken: 42 files where speech names the subject (announcer says the species, composer or place; speeches with the name in the first words); whisper is the only catch.
- Written: 41 files with on-screen text (titles, captions, intertitles, watermarks, channel logos); OCR finds them. Silent films and newsreels carry them most: the video giveaway pass rate is 90 % against 100 % for audio.
- File name in the picture: not separately counted; the OCR and caption rows include it.
- The model's own giveaway check flagged none; two answer words in speech or OCR slipped past it and were caught only by the mechanical check. Keep the mechanical check (answer word in transcript/OCR) in every run.

## Risks
- Thin categories: history, languages, video-games, film; per-category targets (`app/data/targets.json`) may not be reachable media-first. Most yield sits in animals, music, planet-earth, space, transport.
- Zero-yield seeds: spend nothing on them; the pipeline should triage cheap (sonnet, aids first) and stop per seed on zero yield.
- Licence of the work vs the recording: a CC recording of a public-domain piece, a free film of a work still protected, and films with copyrighted music tracks; the review prompt needs both checks (part 3). `decision 640: Media-first questions: may a question be built around a free recording of a public-domain piece of music or a public-domain film excerpt from Commons?` is open: pd-music is 44 % of the pilot's passed questions (20 of 58) and ~23 % of expected approved, pd-film is negligible; without them the general class alone still reaches ≈ 1200 before the look share.
- Difficulty: music, anthem and instrument questions skew hard or easy; the pilot didn't measure difficulty spread against `targets.json`.
- Loudness spread: aided triage rejected 74 files for loudness alone; the shipped audio needs loudness normalisation (or a per-file gain) so questions don't jump in volume.
- Budget: media size: 54 % of files need an excerpt, so shipped excerpts must be cut (not whole files) to stay in the `app/desktop/media-budget.json` limits (`decision 185: Shipped media: formats, names and where the encode runs (SW-9)`).
- Sample: 250 files of 6632, round-robin by seed; the yield has wide error bars per seed (1–5 files each).
- Look share pending (`decision 642`); the estimates above assume nothing about it.

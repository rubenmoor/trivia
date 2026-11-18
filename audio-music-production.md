# Audio music production from free libraries

Status: draft

## Purpose
Says how one music set gets from "the owner wants calmer apartment music" to loop-ready layer files in the game: brief, search, fetch with its licence record, split, loop, level, export, listen, pick. Music is free library music only (`decision 77: Where does the game's music come from: AI-generated tracks curated by the owner, free library music, or a commissioned composer?`); no music generator is used.

## Where it fits
- Feeds `recipes/audio-music-states.md` (it takes the layer files made here), the processing and storage rules of `recipes/audio-requests-and-storage.md`, the music class of `recipes/audio-mix-and-loudness.md` and the hard checks of `recipes/qc-audio-review.md`.
- Evidence: `spikes/music-library/README.md` (four tracks, numbers, the owner's pick); licences: `recipes/design/audio-sources-and-licences.md` section 3.
- Credits come from the records, not from hand-typed text (`decision 71: Licence and provenance of every asset: REUSE.toml for licences, a sidecar file per generated asset, credits and store disclosure generated from them`).

## Inputs and outputs
- Inputs: a mood sheet from the owner (step 1); the music venv from `spikes/music-library/setup.sh` (`~/.cache/music-spike/demucs`, Demucs 4.1.0, librosa, GPU optional).
- Outputs, per piece `mus_<module>_<piece>` (for example `mus_apartment_carefree`):
  - `sources/audio/<id>/request.toml` and `<id>.meta.toml` (source, licence, credit line, SHA-256 of the download, loop data, exports);
  - layer files `mus_<module>_<piece>_{base,rhythm,melody}.ogg` plus `_full.ogg` (the three added up) in `game/modules/<module>/assets/audio/` (shared: `game/shared/audio/`), each with its `.import` set to `loop=true`, `bpm`, `beat_count`, `bar_beats=4`;
  - one block in `REUSE.toml` (CC-BY-4.0, holder, link);
  - a line on the listening sheet; the original MP3 and raw Demucs output stay in `~/.cache/tdur/music/<id>/`, not in git.

## Tools
| Tool | Source |
|---|---|
| `just audio music fetch\|split\|loop\|export\|run` (`tools/audio/music.py`, `tools/audio/music_loop.py`) | this repo |
| Demucs `htdemucs` 4 sources, run in the music venv | dev-time tool only; weights licence unclear, accepted by `decision 158: Demucs, the tool that splits a song into layers, comes with weights whose licence is unclear: do we use it for music that ships?` |
| `ffmpeg` (Ogg encode, loudness), `just review audio`, `just audio sheet` | dev shell |

## Steps
1. **Brief: the mood sheet.** The owner writes a few lines per set (`apartment_day`, `apartment_night`, `pc_desk`, `street`, `menu`, `collapse`, see `recipes/audio-music-states.md` step 1): mood in words, speed (slow, walking, hurried), instruments liked and disliked, what it must not sound like, which clip is calm and which is stressed. Save it as `sources/audio/<id>/brief.md`. Feedback is iterative: the owner listens (step 10), says "more like this, less like that", and the worker searches again with the new words; keep a round number in `brief.md`. Nothing is the final pick until the owner says so.
2. **Search (allowed libraries only).** Use the licence table of `recipes/design/audio-sources-and-licences.md` section 3:
   - **Kevin MacLeod, incompetech.com**: CC BY 4.0 (some older tracks 3.0). The catalogue `pieces.json` lists title, `bpm`, `feel`, instruments and length for 1 443 pieces; search it by feel and bpm. Command: `python3 -c "import json;[print(p['title'],p['bpm'],p['feel']) for p in json.load(open('$HOME/.cache/tdur/music/pieces.json')) if 'Calming' in p['feel']]"` (the file appears after the first `fetch`).
   - **CC0**: Kenney Music Jingles, OpenGameArt items marked CC0 only; no credit needed, still recorded.
   - **Other CC BY libraries** (Free Music Archive, Scott Buckley): per track page; accept CC0 and CC BY, reject BY-NC, BY-ND, BY-SA and anything with extra clauses.
   - Never: Suno, Udio, any generator, anything non-commercial or share-alike (the forbidden list of `just audio check` catches the named ones).
   - Prefer: a fixed tempo made in a music program (the spike's fits landed on whole numbers); a long steady section with drums, bass and a tune all present; instrumental. A track with a human, drifting tempo makes a weak loop.
3. **Fetch and record.** Command: `just audio music fetch "Carefree" mus_apartment_carefree --use "apartment music, relaxed"`. It downloads the MP3 to the cache, writes `request.toml` and the sidecar with the title, artist, track page, download URL, SHA-256, listed bpm, `spdx = "CC-BY-4.0"`, `attribution_required = true` and the credit line (title, author, link, licence, "adapted"). Then, in a browser, open the track page and read its licence line (the page needs JavaScript, so the tool cannot): if it says 3.0 or something else, edit `spdx` and the credit line (and for anything that is not CC0 or CC BY, stop and drop the track). For another library, `fetch` does not exist yet: write the sidecar by hand from the example in `sources/audio/` of the same shape and download the file into `~/.cache/tdur/music/<id>/original.mp3`. Add the `REUSE.toml` block (copy the Kevin MacLeod block, change holder and licence).
4. **Split into layers, or keep the track whole.** Command: `just audio music split mus_apartment_carefree` (about 10 s on the GPU for a 3.5 minute track; CPU not timed; needs the music venv). Demucs makes drums, bass, other and vocals; the loop step folds vocals into the melody layer. Use the split when the music-state map wants layers (calm to busy by volume). Keep a track **whole** when it splits badly (melody leaks into drums, only one layer is audible); then run `loop` on the whole mix with the layers copied from it, or use only `full` as a single `base` layer (`recipes/audio-music-states.md` step 3). A frequency-band split (no model) is not recommended: only its mid band is audible (`decision 159: Which library songs and which layer splits are good enough for the game's apartment music?`). The result is CC BY music we adapted: the credit line says so; the model is not mentioned in the credits.
5. **Tempo check and loop.** Command: `just audio music loop mus_apartment_carefree` (about 8 s; `--bars 8` is the default, `--bpm` overrides the catalogue's bpm for the search). It finds the tempo from the drums (to 0.001 bpm), the first beat of the bar, the stretch of `--bars` bars that sounds most like the one after it, cuts all layers at the same place and lets the tail ring into the head, so the seam does not click. It prints and writes `info.json`: `bpm`, `comb_score`, `repeat_similarity`, `seam_jump_vs_mean_step`, `loop_s`, `start_s`.
   - **Reject** (pick another track or another section) when: `repeat_similarity` is below 0.8 (the music is not the same after the loop), `seam_jump_vs_mean_step` is above 3 (the limit of `recipes/qc-audio-review.md`), `comb_score` is below about 1.5 (no firm beat), the fitted `bpm` is far from the listed one, or the loop is under 10 s or over 300 s (the music class limits).
   - Known gaps from the spike: a loop cut from the middle repeats naturally only where the music itself repeats; the similarity number makes that likely, not certain: the owner's ears decide.
6. **Level.** The loop step sets one gain for all layers so that the **sum** is at the music class target, -22 LUFS, and its peak at most -1.5 dBTP (`tools/audio/classes.toml`, `decision 85: Sound class targets live in tools/audio/classes.toml, not a second loudness file`). Do not normalise layers one by one: their balance is the music. The final trim per set is set by `task 266: Whole-game loudness measurement and final mix values`.
7. **Export.** Command: `just audio music export mus_apartment_carefree game/modules/apartment/assets/audio`. It encodes Ogg Vorbis (quality 5) for `base` (bass), `rhythm` (drums), `melody` (other plus vocals) and `full`, writes a helper file `mus_<module>_<piece>.import.json` (loop, bpm, beat_count = bars x 4, bar_beats 4, the layer list) for step 8 and fills `exports`, `bpm`, `bars`, `loop_start_s` and `loop_s` in the sidecar.
8. **Import data.** `export` does this itself at its end (also `just audio music run`): it opens the project once headless so the `.import` files exist, writes `loop=true`, `bpm=<fitted>`, `beat_count=<bars x 4>`, `bar_beats=4` into each layer's `.import` (full track included) and deletes the helper file. If it fails, the helper file stays; fix the cause and run `just audio music import <dir>`. With `bpm=0` the engine switches at once and not on the bar; `just audio check` fails such a layer. All layers of a clip carry the same values.
9. **Hard checks.** Command: `just review audio game/modules/apartment/assets/audio/mus_apartment_carefree_full.ogg --class music` and the same for each layer (the layers alone are quieter than the class limit: run `--class music` on `full` only). Expect 10 of 10, loudness -22 +/-0.2. Then `just audio check` (sidecar keys, forbidden sources, `reuse lint`, LFS). No AI review: music is not judged by a model that cannot hear (`decision 37: How does the AI reviewer judge music and sound effects it cannot hear?`); the verdict is written with the queue reason `listen`.
10. **Listening sheet and the owner's pick.** Command: `just audio sheet`. Per piece the owner sees: the `full` loop, each layer, the listed mood, the numbers (bpm, loop length, similarity), the credit line. Ask for: keep, change, drop; and, for a set, which clip is calm and which stressed. The answer goes to `brief.md` (next round) and, when final, to the set's map file (`recipes/audio-music-states.md` step 4). Only then is a track "in": until the owner says so, its files are candidates, kept in `sources/` and not wired into a map. A decision goes through `pm decision add` when the owner's pick changes the plan (for example "no usable library track for the street").
11. **Credits.** Nothing to write by hand: the credits screen is generated from the sidecars and `REUSE.toml` (`just art credits` lists them). CC BY needs title, author, link, licence and "adapted"; keep the credit line in the sidecar in exactly that shape, and the player must be able to reach it (credits screen). Do not write anything that suggests the artist endorses the game.

Run once on this machine (2026-11-17, `just audio music run Carefree mus_apartment_carefree /tmp/out`): fetch, split (6 s of GPU), loop (8 bars at 96.000 bpm, 20.0 s, similarity 0.993, seam 1.06), export; the `full` loop passed 10 of 10 hard checks at -22.0 LUFS; the whole run took 29 s.

## AI review step
- Reviewed: this recipe against `recipes/TEMPLATE.md`; for a piece, its sidecar, `REUSE.toml` block and the output of `just audio check`. The music itself gets no AI review (`decision 37: How does the AI reviewer judge music and sound effects it cannot hear?`).
- Prompt: the checklist at the end of `recipes/TEMPLATE.md`; for a piece: "Does the sidecar name title, artist, link, licence and the change made? Is the licence CC0 or CC BY (not NC, ND, SA)? Do `exports` exist and match the layer names?"
- Pass/fail criteria: sidecar complete; licence allowed; hard checks 10 of 10; loop numbers inside the limits of step 5; `reuse lint` passes; the owner has picked the track.
- Results go to: the Changelog of this recipe; verdicts to `reviews/audio/`.
- Human look: the owner listens to the sheet (step 10) and has the last word on every track and every split.

## Done when
- [ ] `just audio music run <title> <id> <dir>` works from the dev shell and its `full` loop passes the music hard checks.
- [ ] A piece has request, sidecar with credit line, `REUSE.toml` block, `.ogg` layers with loop, bpm and beat count set, and a verdict.
- [ ] The owner has picked the track on the listening sheet.
- [ ] `just audio check` passes.
- [ ] This recipe is in `recipes/README.md`.

## Pitfalls
- The licence line differs per track (3.0 or 4.0, sometimes another licence): read it on the track page every time; the catalogue does not carry it.
- A drifting tempo (live-played music) gives a weak loop and a wrong bpm; `comb_score` shows it. Do not force a bpm.
- Demucs leaks a melody into "vocals" in instrumental tracks (about 20 percent of the energy in two spike tracks); folding it into melody hides it, but a "drums" layer can then carry some tune. Listen to each layer alone.
- Layers must be cut and gained together; never process one layer on its own.
- Original MP3 and raw Demucs output are big: keep them in the cache, not in git; the sidecar's SHA-256 proves which file was used.
- Some artists ask not to register tracks with content-ID systems; the game is not on a video platform, but a trailer might be: keep the credit line with every trailer.
- `fetch` knows only incompetech; other libraries are by hand.

## Decisions this recipe follows
- `decision 77: Where does the game's music come from: AI-generated tracks curated by the owner, free library music, or a commissioned composer?`: only CC0 and CC BY library music.
- `decision 158: Demucs, the tool that splits a song into layers, comes with weights whose licence is unclear: do we use it for music that ships?`: Demucs layers ship; the result is CC BY music we adapted.
- `decision 159: Which library songs and which layer splits are good enough for the game's apartment music?`: the four spike tracks and their Demucs splits are good enough; frequency bands only in the mid band.
- `decision 71: Licence and provenance of every asset: REUSE.toml for licences, a sidecar file per generated asset, credits and store disclosure generated from them`: sidecar and `REUSE.toml` per piece.
- `decision 85: Sound class targets live in tools/audio/classes.toml, not a second loudness file`: -22 LUFS for the layer sum.
- `decision 37: How does the AI reviewer judge music and sound effects it cannot hear?`: hard checks, then the owner.

## Changelog
- 2026-11-17: first version; `tools/audio/music.py` and `music_loop.py` made from the spike's `loopify.py`; run once on "Carefree".
- Review record: 2026-11-17, author self-check against the template checklist only; the separate model review is left to `task 268: Review all audio recipes together and record lasting choices`.

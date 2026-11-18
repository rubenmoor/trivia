# Music from free libraries

This is the how-to for turning one free library track into loop files for the game: one `.m4a` per tension variant, all the same length, levelled, checked and credited. Everything runs through `trivia-music` (dev shell). Music is CC0, public domain or CC BY only, from a library, never from a generator (`decision 733: Reworked game audio: CC0, public domain or CC BY only, no audio generators`). Workers can't hear: the tools print numbers, the developer's ears decide.

## Rules
- Licence: CC0, PD, CC BY 3.0 or 4.0; no BY-SA, NC, ND, extra clauses (`decision 733: Reworked game audio: CC0, public domain or CC BY only, no audio generators`); one `CREDITS.md` row per shipped file, "adapted" where cut, split or remixed
- Demucs `htdemucs` splits are allowed: dev-time only, not shipped, not named in credits (`decision 732: Reworked game music: Demucs layer splits of free library tracks may ship`)
- No Freesound API (`decision 82: Freesound API for a paid Steam release (OQ-45): replace, ask, or family only?`)
- Ported from a sibling project, no import across repos (decision 199); `music.py` and `music_loop.py` headers name the source
- Nothing here ships except the `.m4a` files; `app/` never reads `authoring/`; installing files is the soundtrack task's job
- Loudness: layer sum at -18 LUFS (`app/desktop/loudness.mjs` `TARGET_LUFS`), true peak ≤ -1.5 dBTP

## Files
- `music.py` CLI (standard library only), `music_loop.py` loop finder (numpy, librosa, soundfile), `test_music.py`, `test_music_loop.py`: in `npm test`
- Records (committed): `authoring/data/music/<set>-<piece>.json`: source, licence read on the page, SHA-256, loop numbers, exports
- Work files (gitignored): `work/music/<id>/` original, stems, loop WAVs, `info.json`; `work/music/pieces.json` catalogue; `work/music/venv/` Demucs venv
- Id = `<set>-<piece>`, lower case, e.g. `carefree-try`; output files `musica-<set>-<variant>.m4a`
- Generated credit rows: `app/client/public/audio/CREDITS.md`, between marker comments

## Steps
1. **Brief**
   - Mood in words, speed, instruments liked and disliked, what it must not sound like, which variant is calm and which tense
   - Feedback is iterative: the developer listens, says "more like this, less like that", the next search round uses the new words
   - Nothing is final until the developer says so; picks that change the plan go through `pm decision add`
2. **Search**: `trivia-music search [--feel F] [--bpm LO-HI] [--instrument I] [--min-length S]`
   - incompetech catalogue (Kevin MacLeod, mostly CC BY 4.0), fetched once to `work/music/pieces.json`
   - Other libraries (Free Music Archive, Scott Buckley, Kenney, OpenGameArt CC0): by hand, per track page; accept CC0 and CC BY only
   - Prefer: fixed tempo from a music program, long steady stretch with drums, bass and a tune, instrumental
3. **Fetch and record, licence read on the page**
   - `trivia-music fetch "<title>" <id>`: download, record, credit line, SHA-256; the licence is NOT confirmed yet
   - Read the licence line on the track page and confirm: `trivia-music record <id> --licence <spdx> --read-on-page`; never confirm a licence not read; later steps refuse until then
   - incompetech's track page needs JavaScript: fetched text is empty; the licence line sits in the page's static HTML in the "Attribution Code" block
   - Other libraries: `trivia-music record <id> --file <path> --page <url> --title … --author … --licence …` (then confirm)
4. **Split or keep whole**
   - `trivia-music setup` once (uv venv, torch with CUDA when `/run/opengl-driver/lib` exists, else CPU); `trivia-music split <id>`: drums, bass, other, vocals; vocals fold into `other` later
   - Keep a track whole (`loop --whole`) when it splits badly (melody leaks into drums, one layer audible); variants are then sections: `@<bar>`
5. **Loop**: `trivia-music loop <id> [--bars 8] [--bpm B] [--whole]`
   - Finds the tempo from the drums (0.001 bpm), the downbeat, the most self-similar stretch, cuts all layers at one place, tail rings into head; one gain for all layers, sum at -18 LUFS
   - Rejects (exit 1, reason printed): `repeat_similarity` < 0.8, seam step > 3× the mean step within 10 ms of it, `comb_score` < 1.5, fitted bpm > 3 % off the listed one, loop < 10 s or > 300 s
   - On a reject: another `--bars` (the stretch changes), another section, or another track; don't force a bpm
6. **Variants**: `trivia-music export <id> <out-dir> --variant NAME=RECIPE …`
   - Recipe: layers joined by `+` (`bass+other`), per-layer dB cut after a layer (`bass+other-3`), leading `+` = previous variant plus (`+drums`), `full`; with `--whole`: `full` or `@<bar>`
   - AAC LC 96 kbit/s 44.1 kHz stereo, all variants the same sample length, same gain, never per-layer normalised; exports written into the record
7. **Check**: `trivia-music check <id>`: after AAC decode, fullest variant -18 ±0.5 LUFS, every file ≤ -1.5 dBTP, seam jump ≤ 3, equal length, 10–300 s, licence allowed and read; exit 0/1
8. **Credits**: `trivia-music credits` writes the rows, `credits --check` fails on a row without a record or a record without a row; nothing by hand; no wording that suggests the artist endorses the game
9. **One command**: `trivia-music run <title-or-id> <out-dir> --variant … [--bars N] [--whole] [--id I]`: fetch (a title; stops at the licence gate, confirm, run again with the id), split (skipped when stems exist), loop, export, check, each step timed
10. **The developer listens**: files stay candidates in the work dir until the developer picks; then the soundtrack task installs them and the record is committed

## End-to-end numbers
- 2026-11-18, `trivia-music run carefree-try work/music/try --bars 16 --variant normal=bass+other --variant question=+drums --variant submitted=full`: "Carefree" (Kevin MacLeod, CC BY 4.0), not installed, record not committed
- 96.0 bpm, 16 bars, 40.0 s, similarity 0.965, loop seam 1.29, comb 2.219, gain +1.6 dB
- `normal` -18.3 LUFS, -4.8 dBTP, seam 0.86; `question` and `submitted` -18.1 LUFS, -3.8 dBTP, seam 1.08
- Times: split 10.4 s (GPU, RTX 4060), loop 4.6 s, export 2.4 s, check 0.6 s
- With `--bars 8`, a fresh Demucs split failed the check (seam 6.51 after AAC; an earlier split gave 2.88); with 4 bars the loop was rejected (3.31): the seam metric is fragile at downbeats, `task 2266: Music pipeline: seam metric robust at downbeats`

## Pitfalls
- The licence differs per track (3.0, 4.0, other): read it on the track page every time; the catalogue doesn't carry it
- Drifting tempo (live-played) gives a weak loop and a wrong bpm; `comb_score` shows it
- Demucs leaks melody into vocals/drums on instrumental tracks; folding vocals into `other` hides it, a drums layer may carry some tune; Demucs output differs run to run
- Layers are cut and gained together, never one alone
- Originals and Demucs output are big: they stay in `work/music/`; the record's SHA-256 proves the file
- Some artists ask not to be registered with content-ID systems: keep the credit line with every trailer

# Media-first questions: what makes one fit its file

A question with `media_first` was built around one Commons file: the file is fixed (its type, file, excerpt and `work` stay), only the text and the `background` picture can change. You can't hear or watch it; you judge it from the played window's aids. **Open every path in `media_first.aids.pictures_to_read` with Read** before you decide: the frame sheet (video: numbered frames of the window, times in `frame_times_s`) and the spectrogram (the window's sound over time).

## Input (`media_first`)
- `file`, `license`: the Commons file and its licence; `class`: `general`, `pd-music` (a free recording of a public-domain piece), `pd-film` (public-domain footage); `kind`: what the file is.
- `work`: for `pd-music`/`pd-film`, the work's `title`, `creator`, `year` and `basis` (why it is public domain).
- `excerpt`: the window the game plays (start, end seconds; null: the whole file), `duration`: the file's.
- `commons`: the file's Commons `description` and `categories` (players never see them).
- `aids`: numbers of the window (`integrated_lufs` loudness, `silence_share` 0–1, `true_peak_dbfs`), `speech` (whisper transcript `text`, `language` guess and its probability `language_p`; "[MUSIK]", "[Music]" and the like mean no words), `ocr` (text read in each frame, `<frame>: <text>`).
- `mechanical`: what code found (`kind`, `check`, `note`, `hard`); `hard` ones make the question `needs_work` in code whatever you decide. Judge each against the text: a real one goes into `feedback`, `problems` and the `fix`; a false flag (a title word such as "symphony", or the composer's name when the answer is the piece, that neither answers nor narrows the question) is named as false in `reasons`, and the `fix` doesn't rewrite the text for it. Soft ones (`title-words`, `quiet`, `silent`) are flags or numbers for you to judge.

## Checks
`needs_work` when one of these fails, with the problem kind named:
1. **From the window** (`media`, or `giveaway` when the text alone answers): a player who hears or watches only the window can tell the answer, and the question says unambiguously what to listen or look for ("Listen: which animal makes this call?"), not a thing several parts of the clip could answer (which shape, which colour). Read the question with the four options and without the clip: if players of its difficulty answer from the text alone (a famous fact names it: "the opera set in Nagasaki", "dedicated to Napoleon", "from the same opera as Nessun dorma"), the clip isn't needed: `giveaway`, and the `fix` moves the clue to what is heard or seen (the nickname, the dance form, what the music paints, the instrument, the voice, the era) or cuts it. A text clue that helps but leaves the clip to decide is fine (the composer's name when the question asks which piece or what it paints). The fixed question must stay answerable for its players: never fix it into an ear test only musicians pass ("Listen: which composer wrote this aria?" for a little-known aria); ask about something in the window players can tell instead, and say so in the `fix`. A file a listener can't tell apart from the wrong options (an obscure movement, four similar arias) is `media`, `fix` empty, unless another question about the same window would work: then write that question as the `fix`.
2. **No giveaway in the window** (`giveaway`): the transcript names the answer or an option (a spoken name); a caption, intertitle, title card, watermark, logo or the file name shows in the frames or the OCR text; the `background` picture shows the answer (as for any audio question).
3. **Content matches** (`fact`): the Commons description and categories agree with the answer and with what the question says the clip is. They disagree (another species, another piece, another place): `needs_work`, `fact`.
4. **Licence** (`media`): for `pd-music`/`pd-film`, the work is public domain by its `basis` (creator died 70+ years ago, film before 1930, government work, traditional tune or anthem) and the recording is free (`license`); a film carries no later music track still under copyright (the description names a later soundtrack, a modern score or a restored version with new music). Never a commercial song, a copyrighted film or TV clip, game footage.
5. **Sound and picture quality** (`media`): too quiet (below about −32 LUFS), mostly silent, or the spectrogram shows heavy hiss, crackle or clipping (flat bands across all frequencies, cut-off tops) over the part that carries the answer; a video whose frames are too blurred, small or dark to recognise on a TV.
6. **Speech**: a recording with speech only where the words needn't be understood (which language, which famous voice, which kind of event by its sound); a question about what is said: `needs_work`, `style`, `fix` asks about the language or the voice instead, if the window allows.
7. **The rest of the review** applies as for any question (facts, options, hints, description, overlap, style).

## Media slot
- `media` is kept: no pick, no new search for it; judge it by the aids, not the title. A file unfit for the question (checks 1, 4, 5): `needs_work`, problem `media`; a fix only when another question about the same window would work (check 1).
- `background` (audio): picked and searched again as for any audio question (`new_query` only for it).

## Fixing (reviser)
When you revise a media-first question: keep `media` as it is; the new text must still come from the window (the checks above) and must not name what only the title or description says.

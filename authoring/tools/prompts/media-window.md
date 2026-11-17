# Task: does an approved video question still work on its shorter window?

A video question in the game now plays at most {max_video_s} s: its window keeps its start and ends at most {max_video_s} s later; a video without a window plays its first {max_video_s} s. This question was approved on a longer window. Decide whether it still works on the cut one. The text stays as it is; you only judge it.

## Input
- `question`: the question as played (description, question text, answer, three wrong answers, three hints, fun fact, difficulty 1–15), in its source language.
- `media_first`: the file and the cut window's aids, in the shape the "Media-first questions" text below describes; `excerpt` is the cut window. Also for a question that was written first and given a video later: there `class` and `kind` are null, `work` is absent and `commons` may be null.
- `cut_from`: the window it was approved on (`null`: the whole file) and the file's `duration` (null: unknown).

## Judge
Open every path in `media_first.aids.pictures_to_read` with Read first. Then `needs_work` when one of these fails:
1. **Clue inside** (`media`): what the question asks about is seen or heard inside the cut window, clearly enough to recognise on a TV (Check 1 and 5 below). Frames show only other things (an intro, a title card, a crowd before the event): it is gone.
2. **No new giveaway** (`giveaway`): the cut window's transcript, OCR or frames name the answer or an option (Check 2). A `hard` mechanical `answer-heard` finding is a giveaway unless it is a false flag.
3. **Still says what to look for** (`media`): the question text still points at something in the window ("Watch: which animal…"); it doesn't refer to a moment the cut left out ("at the end", "after the explosion").

An illustrative video (`role` not `essential`) only needs to show the question's subject, not answer it. Checks 3, 4, 6 and 7 below were judged when the question was approved: a problem there is not a reason here unless the cut made it.

## Answer
- `verdict`: `keep` or `needs_work`.
- `problem`: for `needs_work`, the kind (`media` or `giveaway`, as above); null for `keep`.
- `note`: in English, one sentence: for `needs_work` what is missing or wrong in the window and where (frame numbers, seconds); for `keep` where the clue is (frame numbers).

The "Media-first questions" text follows: read it for the input and the Checks; its answer fields (`feedback`, `fix`, `new_query`) and the sections "Media slot" and "Fixing" don't apply.

# Media-first question

Above is the house style. Here the media comes first: you get one Commons file (title, description, class,
duration), the triage's verdict and judging aids in place of hearing or watching it (open every picture path
with Read). Write one English (`en`) question **built around this file**.

- The answer comes from what players hear or see in the played window, never from the file's title or
  description (players never see those). The media is `essential`; `illustrative` only when the question
  stands without it.
- The clip, not the text, carries the answer. Before answering, read the question and its four options
  without the clip: if players of its difficulty could answer from the text alone (a plot ("a bride above
  Nagasaki"), a dedicatee, a nickname's meaning, a biography ("Austrian church organist"), "same opera as a
  famous aria"), move the clue to what is heard or seen (the piece's nickname, dance form, what the music
  paints, instrument, voice, language, era of the sound). A clue that helps but leaves the clip to decide is
  fine; never an ear test only musicians pass. The description and hint 1 never date the piece or rule out
  options (a year, "debut", "weather forecast"): the house style's giveaway rule.
- Say unambiguously what to listen or look for: "Listen: which animal makes this call?", "Watch: which sport
  is being played?". Never a question several things in the clip could answer (which shape, which colour,
  when the clip shows several).
- Exception to "No songs, no film or TV clips": a file of class `pd-music` or `pd-film` (a free recording of
  a public-domain work, public-domain footage) may be the question's media ("Listen: which composer wrote
  this piece?"). Then fill `work`: the work's `title`, `creator`, `year` (number or text such as "c. 1890")
  and `basis`, why the work is public domain ("composer died 1827", "film of 1902", "US government work",
  "traditional"). `work` is null for class `general`.
- Speech: only where the words needn't be understood (which language, which famous voice, which kind of
  event by its sound). No question about what is said; no subtitles in the game.
- `subcategory`: the triage's, unless another fits clearly better. `difficulty` on the shared scale, inside
  `target_levels` unless the question clearly belongs elsewhere.
- `excerpt`: the window to play (start, end seconds) when the file is longer than {max_s} s, or when a
  shorter window is fairer or hides a giveaway (a caption, a spoken name); null for the whole file. At most
  {max_s} s, inside the file's duration. The triage's excerpt is a proposal.
- `media_note`: what must be heard or seen in the window.
- `background_query`: for audio, as the house style says (it must not show the answer); empty string for video.
- `giveaway`: check before you answer, against the aids for the window: does the speech name the answer or
  an option (`spoken`)? does text in the picture (caption, title card, watermark, sign, logo) name it
  (`on_screen_text`)? can the question only be answered from the title (`title_needed`)? does the
  description give it away (`description`)? `passes` only when all four are false; `notes` names what you found.
- `needs_fact_check`: true when the question or fun fact states a checkable fact beyond what the media shows.
- `run_answers`: answers other questions of this run already have; yours must differ and still come from
  listening or watching (a composer taken: the piece, its nickname, the dance form, what the music paints;
  not a date, a city or a dedicatee the clip doesn't convey).
- `previous_attempt`, when given: your earlier question for this file and the problems found in it; write a
  new one that avoids them (another window, another angle, other options).

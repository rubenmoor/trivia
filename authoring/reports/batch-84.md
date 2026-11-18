# batch-84

Made by `qgen batch --media-first` on 2026-11-17 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 63 (q-21021…q-21083)
- Approved: 50
- Needs work: 13
- Dropped by the pipeline: 31
- Reviewed by: claude-opus-5-5
- Claude calls: 1065, about $96.43 at list price; $1.93 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-82, batch-83; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-82 | batch-83 | batch-84 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 100 | 103 | 94 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 36 | 34 | 31 |
| drop rate | ≤ 20.0 % | 36.0 % ✗ | 33.0 % ✗ | 33.0 % ✗ |
| dropped: hard fail correct |  | 1 | 0 | 1 |
| dropped: hard fail unambiguous |  | 3 | 2 | 2 |
| dropped: hard fail no_giveaway |  | 9 | 4 | 6 |
| dropped: overlap |  | 24 | 26 | 21 |
| dropped: duplicate |  | 0 | 2 | 1 |
| dropped: fact-check wrong |  | 0 | 0 | 1 |
| merged |  | 64 | 69 | 63 |
| approved |  | 48 | 50 | 50 |
| needs_work |  | 16 | 19 | 13 |
| needs_work rate | ≤ 20.0 % | 25.0 % ✗ | 27.5 % ✗ | 20.6 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 7.8 % ✓ | 14.5 % ✗ | 4.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 3.2 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 1.6 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 4.7 % ✗ | 2.9 % ✗ | 7.9 % ✗ |
| needs_work: media | ≤ 10.0 % | 15.6 % ✗ | 20.3 % ✗ | 11.1 % ✗ |
| media: no pick in review 1 |  | 1 | 1 | 2 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 64 | 69 | 63 |
| needs_work: difficulty | ≤ 10.0 % | 3.1 % ✓ | 2.9 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 6.2 % ✓ | 0.0 % ✓ | 1.6 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 27.0 % ✗ | 29.1 % ✗ | 28.7 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 32 | 35 | 30 |
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
| mechanical-check rate |  | 0.0 % ✓ | 4.3 % ✓ | 3.2 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.47 ✓ | 3.50 ✓ | 3.38 ✗ |
| cost $ |  | $84.36 | $81.95 | $92.45 |
| $ per approved | ≤ $0.35 | $1.76 ✗ | $1.64 ✗ | $1.85 ✗ |
| calls |  | 925 | 901 | 1005 |
| calls per approved |  | 19.27 | 18.02 | 20.10 |
| wall time h |  | 1.78 | 1.42 | 2.51 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 1 of 48 (2 %)
- Major among review needs work: 3 of 12 (25 %)
- Problems by kind: giveaway 9 (1 major), fact 2 (1 major), ambiguity 1 (0 major), overlap 2 (1 major), media 7 (3 major), difficulty 3 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.7; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 50 of 60 (83 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.97

Major findings on approved questions:

- **q-21037**: overlap, giveaway — The main problem is overlap: related q-21036 asks the same thing ("Watch: which bird is this… white chest puffed up", answer Sage grouse), likely with matching BLM lek footage, so only one of the two should stay in the pool. There is also a minor giveaway: hint 2 ("only… western North America") rules out the capercaillie and the black grouse, which are both Eurasian, and leaves only the turkey. The answer, the Commons description (BLM footage of a sage-grouse lek in Oregon) and the fun fact all check out. The soundtrack is nearly silent (−52.6 LUFS), but the question only needs the picture. I couldn't open the frame sheet with the tools I have, so I haven't checked the frames for a caption or logo myself, though the OCR text shows only noise. (http://127.0.0.1:8001/review/q-21037)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 0 | 0 | 0 | 0 | 0 |
| cat:Audio files of national anthems | 30 | 3 | 3 | 3 | 2 | 2 |
| cat:Videos by NASA | 30 | 6 | 6 | 5 | 4 | 4 |
| cat:Videos of animals | 30 | 5 | 5 | 5 | 4 | 4 |
| cat:Videos of nature | 30 | 8 | 8 | 8 | 7 | 7 |
| q:audio:dog bark | 30 | 3 | 3 | 3 | 2 | 2 |
| q:audio:national anthem instrumental | 30 | 11 | 11 | 10 | 8 | 6 |
| q:audio:piano recording | 30 | 17 | 17 | 10 | 7 | 6 |
| q:audio:piano sonata public domain | 30 | 17 | 17 | 9 | 2 | 1 |
| q:audio:whale song | 28 | 1 | 1 | 1 | 1 | 1 |
| q:video:NASA video launch | 30 | 2 | 2 | 2 | 2 | 2 |
| q:video:animal video wildlife | 30 | 5 | 5 | 3 | 2 | 1 |
| q:video:cooking video | 30 | 5 | 5 | 5 | 4 | 3 |
| q:video:experiment science video | 30 | 5 | 5 | 3 | 1 | 1 |
| q:video:machine working video | 30 | 2 | 2 | 2 | 2 | 2 |
| q:video:newsreel | 29 | 4 | 4 | 3 | 3 | 1 |
| q:video:rover mars video | 18 | 1 | 1 | 1 | 1 | 1 |
| q:video:space station astronaut video | 30 | 1 | 1 | 0 | 0 | 0 |
| q:video:time-lapse video | 30 | 10 | 10 | 10 | 5 | 2 |
| q:video:traditional dance video | 30 | 5 | 5 | 5 | 3 | 2 |
| q:video:train video | 30 | 4 | 4 | 4 | 2 | 1 |
| q:video:underwater video fish coral | 14 | 0 | 0 | 0 | 0 | 0 |
| q:video:volcano eruption video | 30 | 2 | 2 | 2 | 1 | 1 |
| total | 659 | 117 | 117 | 94 | 63 | 50 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 540 | 82 | 82 | 69 | 48 | 40 |
| pd-film | 29 | 4 | 4 | 3 | 3 | 1 |
| pd-music | 90 | 31 | 31 | 22 | 12 | 9 |
| total | 659 | 117 | 117 | 94 | 63 | 50 |

- $ per approved: $1.93

## Needs work

- **q-21028** (technology) Watch: NASA workers put together a space telescope. What are the orange machines that raise them up to it? → Scissor lifts: The text is fine, but the clip's soundtrack isn't free. The Commons description says the music is “Take me Higher” by Julien Vonarb [SACEM], Universal Production Music. That is a commercial track still under copyright, so the window can't be played with its audio as it is. Fix it in the media pipeline by muting the audio track for this excerpt or by using a NASA SVS version without music. Otherwise, drop the file.
- **q-21036** (birds) Watch: which bird is this, strutting with its white chest puffed up on frosty ground? → Sage grouse: This question duplicates draft q-21037. Both use the same sage grouse lek video and ask “Which bird is this?” with the answer Sage grouse, so only one of them should go into the pool. Otherwise this one works: the bird is clearly visible, and the near-silent sound doesn't matter because the picture carries the question.
- **q-21040** (food-history) Watch: what is the tool called that the man uses to move the loaves? → A peel: This is a base question, so it must work in every language, but hints 2 and 3 only work in English. Hint 3 is a pun on the English word "peel" (banana or orange peel), which falls apart in Spanish ("cáscara") and German ("Schale"). Hint 2's Latin "pala" spells out the Spanish name of the tool ("pala"), so it gives the answer away there. Replace both with hints about the tool itself (flat wooden blade, long handle, also used for pizza or bagels) that work in any language.
- **q-21048** (countries) Listen: this is the national anthem of which Caribbean country? → Trinidad and Tobago: Almost no listener, expert or not, can tell Trinidad and Tobago's anthem apart from those of Jamaica, Barbados or The Bahamas by ear, so the 60-second clip can't decide the question and it's a pure guess (media-first check 1). No other question about this window works either: a generic brass-band anthem only supports trivial questions. Separately, hint 2 gives the answer away, since "its name joins two islands" fits only Trinidad and Tobago among the four options. Hint 3 (the steelpan) repeats the fact asked in the approved question q-8819.
- **q-21049** (countries) Listen: this is the national anthem of which West African country? → Benin: I can't approve this one. Players can't recognise Benin's instrumental anthem or tell it apart from the anthems of Togo, Senegal and Ivory Coast, so the clip doesn't decide the answer. It's a pure guess until hint 2 (the country's location) or hint 3 (Dahomey). No other question about this 60-second window would work, because any question about it still comes down to recognising an obscure anthem. Drop it, or keep the file only for a question where the anthem is a mood clip, not the clue.
- **q-21056** (space) Watch: what is this kind of room called, where spacecraft are put together by workers in suits like these? → A clean room: The file's soundtrack is commercial library music: the Commons description credits “Take me Higher” by Julien Vonarb [SACEM], Universal Production Music, and the spectrogram shows music for the whole 0–30 s window. Only NASA's footage is public domain. The music is still under copyright, so this clip can't be played with its sound. Either play it muted or use a different NASA clean-room video without licensed music. The question text itself is fine.
- **q-21060** (technology) Watch: what kind of machine is making this object? → A 3D printer: This repeats approved q-2557 ("Which machine builds objects by laying down thin lines of melted plastic, one layer on top of another?" → 3D printer). The video shows exactly that clue: a nozzle laying down plastic lines, layer by layer. Hint 2 is almost word for word the same as q-2557's question. Seeing one gives the other away, so the pool doesn't need both.
- **q-21066** (classical-music) Listen: this is the opening of a work by Felix Mendelssohn. What kind of piece is it? → A piano concerto: Hint 2 ("a whole orchestra plays, but one instrument keeps stepping into the spotlight as the soloist") is the definition of a concerto, and only one option is a concerto, so it gives the answer away before hint 3. The question also overlaps heavily with approved q-20724 ("Listen: what kind of classical piece is this?" → A concerto): it is the same ear test with the same answer type. It should either be dropped or turned into a clearly different question about this window, for example one about the piano's stormy entry rather than the genre.
- **q-21072** (space-race-and-astronauts) Watch: in February 1958, this US rocket tried to put a small satellite into orbit. What happened to it? → It broke apart in the sky soon after liftoff: Media.work basis “Universal newsreels donated to the US National Archives and released into the public domain” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-21073** (classical-music) Listen: this piano movement is built in one classic musical form, which you can hear as the music changes. Which form is it? → Theme and variations: The played window (55–115 s) is an unverified guess. In Schnabel's slow reading the Op. 26 theme probably lasts until about 110–125 s, so the window most likely holds only the theme and no variation, and the form can't be heard. The spectrogram shows one dip at about 100 s (a cadence, possibly the theme's midpoint) but no clear change to variation figuration. Move the excerpt so it spans the end of the theme and the start of Variation 1 (check by ear), or retire the file for this question.
- **q-21077** (trains) Watch this train roll along the platform. What kind of passenger cars does it have? → Double-decker cars: The fun fact is wrong: the fact check found that Russia's double-decker trains carry about 30–40% more passengers, not "nearly twice as many". Replace it with the corrected version, for example "Russia's double-decker trains carry roughly 30–40% more passengers than ordinary trains of similar length." Separately, related question q-20678 says "double-decker express" in its question text, so a player who has seen it is handed this answer. Consider whether both should stay in the pool. Fact check: wrong. The fun fact says double-deckers carry 'nearly twice as many passengers per train'. That overstates it: RZD reports capacity gains of about 30–40% on routes where they were introduced. The 'twice' figure comes only from a 2011 official's general claim about the Moscow–Samara line. The answer (double-decker cars) is correct.
- **q-21079** (traditional-dress) Watch: what garment is the dancer in red wearing? → Sari: Fact check: uncertain. I could not watch the video, so I could not confirm the dancer in red wears a sari. The Commons page only says it shows the Kanyapu dance by Nalke artists in Tulunadu, Karnataka, at night. Karnataka and the red sari with gold border are plausible, and the wrong answers (kimono, hanbok, dirndl) are surely wrong. Text claims check out: a sari is unstitched, worn in India, Nepal and Bangladesh, and sources give 80+ draping styles (some say 108). The length range varies by source (about 4.1-8.2 m on Wikipedia, 4-9 m elsewhere), so '5 to 8 m' is roughly right. 'Also to everyday work' is plausible.
- **q-21081** (celebrations-around-the-world) Watch and listen: this celebration was filmed in 1957 just before Lent. In which city did it take place? → New Orleans: Media.work basis “Universal Newsreel footage released into the public domain (National Archives collection)” is none of: died-70-years, pre-1930-film, government-work, traditional.

## Question axes

- move: None 63
- stimulus: None 63
- clue: None 63
- answer_kind: None 63
- lens: None 63

## Dropped by the pipeline

- mf-0c54bbafc5: overlap like q-20640: Listen: this lively symphony finale weaves several tunes together at the same time. Who composed it? → Wolfgang Amadeus Mozart: Listen: which composer wrote this piece? → Wolfgang Amadeus Mozart
- mf-0fcf138f8b: overlap like q-20820: Listen: from which era of Western music does this solo piano piece come? → Classical era: Listen: this cheerful solo piano piece was written in about 1802. Which era of music does its style belong to? → Classical
- mf-262357dc6d: overlap like q-16840: This NASA video shows a hurricane heading for the US coast. What is the calm, clear hole in its center called? → The eye: Watch: this plane flies through a hurricane, and the gray clouds suddenly open onto blue sky. Which part of the storm has it reached? → The eye
- mf-3054145aec: overlap like q-20809: Listen to the very first notes: which nickname does music theory give this quick broken-chord figure? → Mannheim rocket: Listen to the theme the piano plays at the very start. What name do musicians give to this kind of theme? → Mannheim rocket
- mf-4d048941c5: overlap like q-20869: Watch: what is the glowing band stretching across the night sky in this time-lapse? → The Milky Way: Watch the sky through the dome's opening after the Moon sets. What is the pale, starry glow that appears there? → The Milky Way
- mf-51f86d4392: overlap like q-9060: Which river carved the canyon in this photo? → Colorado River: Watch: clouds roll over this famous canyon. Which river carved it? → Colorado River
- mf-5b45737d49: overlap like q-20890: Watch: which filming technique was used to make this video of a banana? → Time-lapse: Watch: which filming technique was used to make this video of plants? → Time-lapse
- mf-5edd877fda: overlap like q-20926: Watch: the men wear knee-length robes with wide white cuffs. In which country is this folk dance being performed? → Bhutan: Watch: in which country are these women dancing in their national dress outside a monastery? → Bhutan
- mf-625e4b41bf: overlap like q-20811: Listen: what kind of piece by Mozart is this? → A piano sonata: Listen: this is one movement of a longer work. What type of work is it? → Piano sonata
- mf-6909a5b8cb: overlap like q-1181: Si la locomotora de vapor es al carbón, las locomotoras de carga de hoy suelen ser al… → Diésel: Watch and listen: what powers the two locomotives pulling this freight train? → Diesel fuel
- mf-6c642ad742: overlap like q-10980: Ein rundes blaues Schild zeigt drei weiße Pfeile, die im Kreis hintereinander herlaufen. Was kommt gleich? → Kreisverkehr: Watch this time-lapse: what kind of road junction is being built? → A roundabout
- mf-72f64f9bc7: overlap like q-20784: Listen: which dance is this orchestra playing? → A waltz: Listen: what kind of dance is this fiddler playing? → Waltz
- mf-72f74da070: overlap like q-20724: Listen: what kind of classical piece is this? → A concerto: Listen: this is a slow movement from a longer work. What kind of work is it? → Piano concerto
- mf-823be52633: overlap like q-9307: Der Deutsche Wetterdienst lässt täglich Wetterballons steigen, die erst in rund 30 Kilometern Höhe platzen. In welcher Luftschicht passiert das? → Stratosphäre: Watch: this pilot is so high that the sky looks dark and the Earth looks curved. Which layer of the atmosphere is the plane flying in? → Stratosphere
- mf-85bb7094f4: duplicate like q-20814: Listen: this is the national anthem of which European country? → Slovakia: Listen: this national anthem once formed the first half of a joint anthem. Which nation's song was sung as the second half? → Slovakia
- mf-8bfb02d3a8: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: the red locomotive that rolls in near the end belongs to the national railway of which country? → Austria
- mf-8e4a56754e: overlap like q-20740: Watch: satellite images from 1984 to 2018 show this desert coast changing. Which city is this? → Dubai: Watch: these satellite images show a man-made island being built in the sea. Off the coast of which city is it? → Dubai
- mf-9b378bfbf1: overlap like q-8982: This big reptile is Florida's official state reptile and sometimes shows up on golf courses. Which animal is it? → Alligator: Watch: handlers are holding a big reptile at a wildlife park. Which animal is it? → American alligator
- mf-a270b39da9: overlap like q-20641: Listen: this orchestral movement by Beethoven takes its rhythm from which old court dance? → Minuet: Listen: this graceful movement from a Classical-era piano sonata is written in the form of which dance? → Minuet
- mf-a95987c0be: overlap like q-9691: This bird shrieks over British seaside towns and loves to snatch chips. What kind of bird is it? → A gull: Watch: what kind of birds are the white ones flapping and flying around on this lawn? → Gulls
- mf-c594904fdc: overlap like q-20636: Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Listen: which composer wrote this playful piano piece? → Ludwig van Beethoven
- mf-c7af01a12e: overlap like q-20962: Listen: what musical form is this lively piano movement written in? → Rondo: Listen to how this Beethoven piano finale is built. Which musical form is it? → Rondo
- mf-e9900d8150: overlap like q-13703: Lleva acordeón y bajo sexto, la tocan Ramón Ayala e Intocable, y se baila en las fiestas de Monterrey. ¿Qué género es? → La música norteña: Watch and listen: what is this style of Mexican music and dance called? → Norteño
- mf-0b93d68275: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: Listen: this movement comes from a Beethoven piano sonata. What is the name for this kind of movement? → Scherzo
- mf-515fe41979: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: the video zooms in on a long peninsula in Russia’s far east. Which sea lies on its western side, between it and the Russian mainland? → Sea of Okhotsk
- mf-59bb48ca60: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: this giant, crispy fried chicken cutlet is a famous night-market street food from where? → Taiwan
- mf-62aa80084c: hard fail: correct 4, unambiguous 5, no_giveaway 3, no_overlap 4: Listen: this galloping piano finale gave its whole sonata a nickname. Which one? → The Hunt
- mf-6c1250eb53: hard fail: correct 4, unambiguous 3, no_giveaway 3, no_overlap 5: Watch: which people have traditionally herded animals like these for centuries? → The Sámi
- mf-74f65acd63: hard fail: correct 3, unambiguous 5, no_giveaway 4, no_overlap 5: Listen: which country's national anthem is this? → Qatar
- mf-7b4afdbd8a: fact-check wrong: The fun fact says the song was renamed "Land of the Free" in the 1960s. Sources say the title changed from "Land of the Gods" to "Land of the Free" in 1981, when the anthem was adopted. The 1960s (1963) date refers to the song being used earlier as a national song.: Listen: this is the national anthem of which country? → Belize
- mf-8e1c4a8801: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: in 2023, NASA sent this cat video to Earth from 31 million km (19 million miles) away. What carried it? → Laser light

# tr-es-18

Made by `qgen batch --translate es` on 2026-11-16 (plan 66, D-81): `base` questions translated into Spanish (Latin America). Generated file: don't edit by hand.

- Sources: 168 (1 stale re-translated)
- Translated: 168
- Approved: 161
- Needs work: 7
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 379, about $21.07 at list price; $0.11 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-18&locale=es

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-16 | tr-es-17 | tr-es-18 |
|---|---|---:|---:|---:|
| sources |  | 300 | 281 | 168 |
| stale re-translated |  | 0 | 0 | 1 |
| translated |  | 300 | 281 | 168 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 290 | 266 | 161 |
| needs_work |  | 10 | 15 | 7 |
| needs_work rate | ≤ 20.0 % | 3.3 % ✓ | 5.3 % ✓ | 4.2 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 1.7 % ✓ | 3.2 % ✓ | 3.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 1.7 % ✗ | 1.8 % ✗ | 1.2 % ✗ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.4 % ✓ | 0.6 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 60 |
| audit/review agreement | ≥ 90.0 % | 98.3 % ✓ | 98.3 % ✓ | 75.0 % ✗ |
| cost $ |  | $33.73 | $32.13 | $17.76 |
| $ per approved |  | $0.12 | $0.12 | $0.11 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 13 of 57 (23 %)
- Major among review needs work: 1 of 3 (33 %)
- Problems by kind: giveaway 2 (0 major), overlap 2 (1 major), media 15 (14 major), style 1 (1 major)
- Mean |audit − final difficulty|: 0.3; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 45 of 60 (75 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.31

Major findings on approved questions:

- **q-20660**: media — The media is an essential video with no file picked (title null), but the question says "Mira: ¿cómo se llama esta danza…?". Without the clip, the question can't be played as written. The translation itself is faithful and reads naturally. I checked the facts: intore means "the chosen ones" in Kinyarwanda, it was danced by the Rwandan royal court's elite warriors, and Rwanda is "the land of a thousand hills". Hint 1 only narrows the options, since adumu is also East African. The difficulty of 14 is close to my estimate of 13. (http://127.0.0.1:8001/review/q-20660)
- **q-20664**: media — The media is an essential video, but its title is null, so no file was picked. The question opens with "Mira este video en cámara rápida, puesto al revés", so it can't be played as written. The translation itself matches the source and reads naturally in es-419 ("alacena", "afuera", "Un alga"), and the facts check out: mold is a fungus that spreads by spores, and Fleming found penicillin in 1928. q-4220 (moldy veins in blue cheese → hongos) is close but asks about a different object. (http://127.0.0.1:8001/review/q-20664)
- **q-20670**: media — The question needs its essential video ("Mira… en esta animación"), but no file was picked (media title is null), so it can't be played as it is. The translation itself is accurate and reads naturally. "¿De qué es la sombra esa pequeña mancha negra…?" is a little clunky; "¿De qué es sombra…?" would read better. I checked the fun fact: the 21 August 2017 eclipse was the first to cross the US coast to coast since 1918, and the 384 000 km hint is also right. (http://127.0.0.1:8001/review/q-20670)
- **q-20683**: media, overlap — The question needs an essential video ("Mira: un tren suburbano…"), but media.title is null. With no clip, players can't answer it as written. This comes from the source, not the translation. The translation itself is faithful and reads naturally in es-419 ("hora pico", "tren suburbano"). The fun fact checks out: the CN Tower is about 553 m and was the tallest freestanding structure from 1975/76 until the Burj Khalifa passed it in 2007. Minor point: related q-2711 describes Toronto's 553 m concrete tower, so a player who saw that question would have a head start here. (http://127.0.0.1:8001/review/q-20683)
- **q-20686**: media, style — The essential video is missing (title is null), but the question starts with "Mira: esta animación satelital…". Without it, the Southern Ocean is also a defensible answer, because Antarctic sea ice shrinks every summer too. Smaller issue: "cubeta de hielo" in the description is not a natural Latin American term ("cubeta" usually means "bucket"); "charola/bandeja para hielo" is clearer. Everything else checks out: Arctic minimum in September, Greenland, and the North Pole hint. (http://127.0.0.1:8001/review/q-20686)
- **q-20687**: media — The media is an essential video, but its title is null, so no timelapse was picked. Without it the question "Mira este timelapse" can't be played. This is a source-side media gap, not a translation error. The translation itself is faithful and natural es-419. The facts check out: the Danube is Europe's second-longest river, Budapest was formed in 1873, the Chain Bridge opened in 1849 as the first permanent Danube bridge in Hungary, and the lions' tongues are real but hidden. (http://127.0.0.1:8001/review/q-20687)
- **q-20697**: media — The media is an essential video, but its title is null, so no file was picked. The question only works if players can watch the drone video, so it can't be played as it is (unless the title is just missing from this input). The translation itself is faithful and reads naturally in es-419. The options, hints and fun fact (axial tilt of about 23.4°) are correct, and q-4622 (the Demeter myth) asks a different fact with the same answer, so it doesn't overlap. (http://127.0.0.1:8001/review/q-20697)
- **q-20700**: media — The media is an essential audio clip, but its title is null, so no recording of "Amar Shonar Bangla" was picked. Without it, the "Escucha" question can't be played (only the decorative background image exists). The translation itself is faithful and natural es-419 ("Bangladés", "Daca"), and the facts check out: Tagore wrote both anthems and won the Nobel in 1913 as the first non-European laureate. Hint 2 rules out India and nearly settles the answer, but that comes from the source and hints are only shown through a joker. (http://127.0.0.1:8001/review/q-20700)
- **q-20701**: media — The question needs a video ("Mira: ¿cómo se llama este tipo de nube?"), but no file was picked (title is null). Without a time-lapse of cumulus clouds there is nothing to identify, so it can't be played. The translation itself is faithful and natural es-419: Cúmulo, Cirro, Estrato and Altoestrato are the correct Spanish names, the hints match the source, and the fun fact's figure of about 500 tonnes is the commonly cited USGS estimate. (http://127.0.0.1:8001/review/q-20701)
- **q-20703**: media — The question needs an essential audio clip ("Escucha este final…"), but media.title is null, so no audio file was picked and the question can't be played as it is. This is a source/media issue, not a translation one. The translation itself is faithful and natural es-419. All facts check out: Saint-Saëns lived 1835–1921, was a child prodigy and Madeleine organist, and wrote the score for L'Assassinat du duc de Guise in 1908. Stojowski's "Bach to Offenbach" quip and the No. 2 being written in three weeks in 1868 with the composer as soloist are also right. (http://127.0.0.1:8001/review/q-20703)
- **q-20704**: media — The question needs a video, and none is attached: the media is an essential video, but its title is null. "Mira: … esta bailarina" (Watch: … this dancer) can't be played without it, and the fun fact's "falda roja y dorada" (red-and-gold skirt) also refers to the missing footage. The translation itself is faithful and natural es-419: hanfu, the horse-face skirt (mamianqun) and its 2022 revival check out, and the options agree with each other grammatically. (http://127.0.0.1:8001/review/q-20704)
- **q-20720**: media — The Spanish is faithful and natural (es-419), the options have no articles so none stands out, the hints don't give the answer away early, and it doesn't overlap with q-2537 or q-5735. The problem is the essential video: its title is null, so no file was picked. Without the clip of the Cucullia caterpillar, "Mira: … este bichito" can't be played. (http://127.0.0.1:8001/review/q-20720)
- **q-20726**: media — The question needs an essential audio clip ("Escucha: ¿de qué ópera…?"), but media.title is null, so no recording of «Una furtiva lagrima» is attached and the question can't be played as it is. Everything else checks out: Donizetti wrote both L'elisir d'amore and Lucia di Lammermoor, Dulcamara's "elixir" is cheap Bordeaux wine, and the fun fact about Nemorino and Adina is right. The Spanish is faithful, natural es-419 ("está por abrir"), and the options and difficulty are fine. (http://127.0.0.1:8001/review/q-20726)

## Needs work

- **q-20705** (countries) Escucha: esta melodía es el himno nacional de dos países vecinos. ¿De cuáles? → Finlandia y Estonia: Fact check: wrong. The wrong answer 'Grecia y Chipre' is also correct. Both countries use the 'Hymn to Liberty' as their national anthem, and Greece and Cyprus are neighbors in the eastern Mediterranean. The question asks for 'dos países vecinos' that share an anthem, so it has two valid answers. The Finland/Estonia facts (Pacius, 1848, Estonian lyrics in 1869, ~80 km gulf) are correct.
- **q-20715** (space-race-and-astronauts) Mira: en este video grabado desde la ventana de una cápsula tripulada durante el despegue, ¿qué es la torre puntiaguda que se aleja volando? → Sistema de escape de lanzamiento: Fact check: uncertain. The answer (launch abort system) is right and the wrong answers are wrong. The fun fact's "unos 800 km/h en 2 segundos" is only the top of NASA's range: NASA says 400–500 mph (about 645–805 km/h) in 2 seconds. Northrop Grumman quotes 405 mph (about 650 km/h) for a pad abort, and Pad Abort 1 reached about 445 mph in 3 seconds. I did not check the video clip itself.
- **q-3161** (amazon-history-and-exploration) La Caverna da Pedra Pintada, cerca de Monte Alegre (Brasil), tiene algunas de las pinturas rupestres más antiguas de América. ¿Hace cuánto la habitaron las primeras personas? → Hace unos 11 000 años: Source: the description says the cave has no roof ('no tiene techo'), but Caverna da Pedra Pintada is a sandstone cave with a rock ceiling, and paintings are on its walls and ceiling. The fact check also flags it. The source description needs a new joke without the roof claim (e.g. one about the gallery having no souvenir shop or ticket desk). The rest of the Spanish translation is faithful and natural. Fact check: wrong. The answer (~11,000 years) matches Roosevelt's 1996 radiocarbon dates of about 11,200–10,000 BP. The wrong answers are wrong, the hints are fine, and the fun fact is accurate (excavated 1991–92, published 1996). The description is the problem: it says the site has no roof. Pedra Pintada is a cave or rock shelter with a rock ceiling and overhang, and the paintings are on its walls and ceiling. It is also a protected park site that is open to visitors, so the 'no souvenir shop' joke may be unreliable. I did not run any searches. This verdict comes from what I already know.
- **q-4153** (birds) Mira el enorme pico de este pelícano, con una bolsa elástica debajo. ¿Para qué sirve esa bolsa? → Para atrapar peces: This duplicates approved q-7612 (colombia bundle). Both ask what the pelican's throat pouch is for, and both answers are "Para atrapar peces". Spanish players who get both bundles would see the same fact twice. Either keep only one of them in Spanish or retire one. The translation itself is faithful and reads naturally.
- **q-5869** (athletics) En 1986, ¿qué prueba de lanzamiento del atletismo rediseñó su implemento para que volara menos, porque los mejores tiros casi llegaban al final del campo? → Jabalina: source: the fun fact says 104.80 m is longer than a soccer field. A standard pitch is 105 m, and Laws of the Game lengths run up to 110–120 m, so the claim isn't reliably true (the fact check marked it wrong). Fix the source, for example "almost the length of a professional soccer pitch (105 m)", then translate again. Also note: source hint 2 ("its tip sticks in the grass") points strongly to the only option with a tip. The translation copies it faithfully, but it is worth softening in the source. Fact check: wrong. The answer (javelin) and the hints are correct. The 1986 redesign moved the centre of gravity forward so the tip lands sooner, after Uwe Hohn threw 104.80 m in 1984. The fun fact is shaky: a standard FIFA pitch is 105 m long, so 104.80 m is not farther than a football pitch. Pitches range from about 100 to 110 m.
- **q-6258** (famous-logos) ¿Qué color NO es uno de los colores de los anillos olímpicos? → Morado: The translation itself is accurate and natural, but in Spanish it asks the same fact, with the same answer, as the approved question q-6930 ("¿Cuál de estos colores NO aparece en los aros olímpicos?" → Morado). That question probably wasn't among the related questions when the English source was reviewed. One of the two should be dropped, or this one should ask about a different fact.
- **q-6635** (explorers-and-discoveries) Esta tela suave y brillante se fabricó por primera vez en la antigua China. ¿Qué animal produce el hilo con que se hace? → Gusano de seda: source: hint 2 says the animal is so small it could sit on your fingertip, but a full-grown silkworm is about 7 cm long; only a newly hatched larva is that small (the fact check marks it wrong). Fix the source's hint 2, e.g. "It's a caterpillar that eats only mulberry leaves", then re-translate. Also, in the translated description "pijamas dignas" should be "pijamas dignos", since "pijama" is masculine in most of Latin America. Fact check: wrong. The answer (silkworm) and the wrong answers are correct. The 900 m cocoon thread is a commonly cited figure (sources give about 600–900 m, sometimes more). Hint 2 is misleading: a full-grown silkworm is about 7 cm long, so it doesn't fit on a fingertip. Only a newly hatched larva is that small. I did not run any searches, so this comes from my own knowledge.

## Not travelling

None.

## Stale re-translated

- q-6706: approved

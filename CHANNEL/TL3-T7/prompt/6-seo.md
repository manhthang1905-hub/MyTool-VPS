# YOUTUBE VIDEO SEO

Title: **<<TITLE>>**
Thumbnail text: **<<THUMB>>**
Channel keywords: <<CHANNEL_KEYWORDS>>

Script excerpt:
<<SCRIPT_OPENING>>

Chapters (from the finished subtitle file; may be empty if not available yet):
<<CHAPTERS>>

---

Work in **<<LANGUAGE>>**.

**WHO IS READING THIS DESCRIPTION.** Someone who is quietly resentful. Their
schooling was unremarkable and they hold no diploma worth showing, but at work
they handle things better than people with better credentials. They think
faster late at night, they say little in meetings because most of what gets
said is not worth saying — and none of that is counted anywhere.

**THE SUBJECT OF THIS DESCRIPTION IS THE MEASURING STICK, NOT THE PERSON.**
What they want is not comfort and not company: it is to be MEASURED AGAIN,
with a different instrument. So the description names the instrument that is
getting them wrong — the diploma, the test score, the way a room scores a
person who is quiet — shows what it fails to measure, and then hands over
another instrument. Brain science is that other instrument: it measures the
head, not the file.

Two things that ruin it:
- Turning it into a story about relationships — few friends, being alone, not
  fitting the crowd. That is a different audience and a different channel.
- Praising them to make them feel better. They want evidence the ruler is
  wrong, not a compliment.

**Identify the MAIN KEYWORD** from the title and thumbnail text — the 2–4 word
phrase a viewer would type to find this video. It is usually the MEASURE or
the capability being measured (学歴, IQ, 地頭, 頭のいい人の特徴), not a mood.

Then output the following. Use these exact labels:

DESCRIPTION:
Build it in EXACTLY this order — each block separated by a blank line:

1. **Hook** (1–2 sentences, first sentence ≤150 chars and contains the MAIN
   KEYWORD — this is what shows in search results). Open on the mismeasurement
   itself — what the usual score misses — not on how the viewer feels about it.
2. **What the video covers** (2–4 sentences): name the concrete findings the
   script actually uses as the alternative measure, and say what each one
   measures that a diploma does not. Specifics are the whole argument here;
   a vague promise reads like flattery.
3. **目次 block** — only if Chapters above is non-empty. Wrap it between two
   `━━━━━━━━━━━━━━` lines, first line `📌 目次`, then one `MM:SS label` per
   chapter, copied from the Chapters input verbatim (never invent or shift
   timestamps; if Chapters is empty, omit this whole block including the
   separator lines).
4. **One re-measuring sentence** — state, in one line, what this kind of
   person scores highly on once the right instrument is used. A statement of
   measurement, never a word of consolation.
5. **Channel block**: `🕊 このチャンネルについて` + 1–2 sentences about the
   channel (another ruler — brain science and psychology for people whose
   ability never fit on a résumé).
6. **Comment CTA**: `💬 コメントで教えてください` + restate the script's OWN
   closing comment question. Prefer the form that asks HOW MANY of the traits
   matched them — a score is exactly what this viewer came to collect.
7. Last line: 3–5 hashtags, main keyword hashtag first.

The MAIN KEYWORD must appear naturally 3–5 times across blocks 1–2.

HASHTAGS:
Same 3–5 hashtags, space-separated. Main keyword hashtag first.

KEYWORDS:
Comma-separated, under 500 characters, 12–20 phrases, ordered in tiers:
(a) the measure from title + thumbnail and its obvious variants, (b) the
findings the video actually names, (c) the measuring bridges this channel
shares across videos — 学歴, IQ, 地頭, 脳科学, 本当に頭のいい人, 評価されない,
努力が報われない — (d) the channel name last.

**FORBIDDEN in KEYWORDS:** any token that is not a natural search phrase in
<<LANGUAGE>> — file names, style/asset keys, underscore_tokens (e.g.
`thick_brush_orange_head_white_ground`), English words, hex codes. If such a
token appears in the inputs, it is production metadata that leaked — never
copy it.

**ALSO FORBIDDEN anywhere in the output:** the relationship vocabulary of the
neighbouring audience — ひとりが好き, 友達が少ない, 人付き合いが苦手, 孤独.
Those keywords hand this video to a different audience, and to a sibling
channel that is already serving them.

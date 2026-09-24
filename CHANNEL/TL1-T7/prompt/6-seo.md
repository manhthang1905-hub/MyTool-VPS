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

**WHO IS READING THIS DESCRIPTION.** Someone who is perfectly fine. They
clicked out of CURIOSITY, not out of pain: the title named a small harmless
habit of theirs — gardening, keeping a 15-year-old car, waking at five — that
nobody has ever criticised and nobody has ever explained. They came for a
GIFT: one interesting thing about themselves they did not know.

So this description never consoles, never reassures, never implies they are
struggling, lonely or misunderstood. A single sympathetic line breaks the
promise the thumbnail made. The register is light 雑学 — a curious
field-guide entry about the reader — not therapy.

**Identify the MAIN KEYWORD** from the title and thumbnail text — the 2–4 word
phrase a viewer would type to find this video. It is usually the HABIT or
TRAIT itself, not a psychology term.

Then output the following. Use these exact labels:

DESCRIPTION:
Build it in EXACTLY this order — each block separated by a blank line:

1. **Hook** (1–2 sentences, first sentence ≤150 chars and contains the MAIN
   KEYWORD — this is what shows in search results). Point at the habit and at
   the fact that nobody has ever told them what it means. Curiosity, not
   feeling.
2. **What the video covers** (2–4 sentences): name the concrete traits or
   findings the script actually walks through, and how many of them there are
   — the count is the draw. End on a discovery promise ("いくつ当てはまるか"
   style), never on a consolation.
3. **目次 block** — only if Chapters above is non-empty. Wrap it between two
   `━━━━━━━━━━━━━━` lines, first line `📌 目次`, then one `MM:SS label` per
   chapter, copied from the Chapters input verbatim (never invent or shift
   timestamps; if Chapters is empty, omit this whole block including the
   separator lines).
4. **One surprising sentence** — the single most unexpected thing the video
   says about this kind of person. This is the gift. It must be a FACT about
   them, not comfort offered to them.
5. **Channel block**: `🕊 このチャンネルについて` + 1–2 sentences about the
   channel (a field guide to the odd little things people do, light psychology
   and 雑学, nothing to fix — just something interesting about yourself).
6. **Comment CTA**: `💬 コメントで教えてください` + restate the script's OWN
   closing comment question. Prefer the low-friction counting form ("いくつ
   当てはまりましたか") if the script has one.
7. Last line: 3–5 hashtags, main keyword hashtag first.

The MAIN KEYWORD must appear naturally 3–5 times across blocks 1–2.

HASHTAGS:
Same 3–5 hashtags, space-separated. Main keyword hashtag first.

KEYWORDS:
Comma-separated, under 500 characters, 12–20 phrases, ordered in tiers:
(a) the habit or trait from title + thumbnail, and the obvious variants of it,
(b) the traits the video actually names, (c) the curiosity bridges this
channel shares across videos — 雑学, 特徴, あるある, 隠された特徴,
本人も気づいていない — (d) the channel name last.

**FORBIDDEN in KEYWORDS:** any token that is not a natural search phrase in
<<LANGUAGE>> — file names, style/asset keys, underscore_tokens (e.g.
`thin_line_stick_amber_cream_fieldguide`), English words, hex codes. If such
a token appears in the inputs, it is production metadata that leaked — never
copy it.

**ALSO FORBIDDEN anywhere in the output:** distress vocabulary that belongs to
a different audience — 生きづらい, 孤独, つらい, 悩み, 疲れた, HSP, 自己肯定感.
This viewer has none of those problems, and a keyword that promises them
brings the wrong audience to the wrong channel.

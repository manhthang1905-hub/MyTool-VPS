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

**WHO IS READING THIS DESCRIPTION.** A Japanese man or woman aged 48–62. They
have worked 25–35 years, the children have grown, and three things are
happening at once that they tell nobody: the days feel flat, the memory slips,
and the house keeps getting heavier because things come in and never leave.
Society answers them with one sentence that sounds like care and is really a
closed door: 「もう年だから」.

They are asking **WHAT DO I DO NOW**, not "is something wrong with me". So the
description must carry the same three beats as the video, in this order.
**DROPPING BEAT ① RUINS IT** — an opening that jumps straight to advice reads
as one more person telling them to try harder:

① **ACKNOWLEDGE** — the distance they have already run is real, and it is a lot.
② **ABSOLVE THE AGE** — what they are facing is not age. Never write
   「もう年だから」, and never sell the video with decline: no dementia scare,
   no brain-shrinkage warning, no "before it is too late".
③ **HAND THEM ONE THING** — something concrete they can do this afternoon.

**Identify the MAIN KEYWORD** from the title and thumbnail text — the 2–4 word
phrase a viewer would type to find this video. It is usually the ACTION or the
OBJECT (捨てるもの, 片付け, 習慣), not a psychology term.

Then output the following. Use these exact labels:

DESCRIPTION:
Build it in EXACTLY this order — each block separated by a blank line:

1. **Hook** (1–2 sentences, first sentence ≤150 chars and contains the MAIN
   KEYWORD — this is what shows in search results). This is beat ①: begin by
   recognising the years they have put in, then name what the video hands
   them. Never open on a symptom.
2. **What the video covers** (2–4 sentences): name the concrete things the
   script actually walks through — how many items, which rooms, which habits,
   how many minutes each takes. End with the promise that it starts today,
   not someday.
3. **目次 block** — only if Chapters above is non-empty. Wrap it between two
   `━━━━━━━━━━━━━━` lines, first line `📌 目次`, then one `MM:SS label` per
   chapter, copied from the Chapters input verbatim (never invent or shift
   timestamps; if Chapters is empty, omit this whole block including the
   separator lines).
4. **One sentence that takes the age off them** — beat ②. State plainly that
   the problem is the amount of stuff, or the habit, or the way the day is
   arranged — not the number of years. This is the line that opens the door
   「もう年だから」 closed.
5. **Channel block**: `🕊 このチャンネルについて` + 1–2 sentences about the
   channel (for the second half of life: folding the house and the day back
   down to a size you can hold, one small thing at a time).
6. **Comment CTA**: `💬 コメントで教えてください` + restate the script's OWN
   closing comment question. Prefer the form that asks WHICH ONE they will try
   this afternoon — a choice is easier to answer than a confession.
7. Last line: 3–5 hashtags, main keyword hashtag first.

The MAIN KEYWORD must appear naturally 3–5 times across blocks 1–2.

HASHTAGS:
Same 3–5 hashtags, space-separated. Main keyword hashtag first.

KEYWORDS:
Comma-separated, under 500 characters, 12–20 phrases, ordered in tiers:
(a) the action or object from title + thumbnail, and the obvious variants,
(b) the concrete things the video actually names, (c) the life-stage bridges
this channel shares across videos — 50代, 60代, 人生後半, 断捨離, 片付け,
老後の暮らし, シンプルな暮らし — (d) the channel name last.

**FORBIDDEN in KEYWORDS:** any token that is not a natural search phrase in
<<LANGUAGE>> — file names, style/asset keys, underscore_tokens (e.g.
`navy_sweatshirt_flat_vector_warm_cream`), English words, hex codes. If such
a token appears in the inputs, it is production metadata that leaked — never
copy it.

**ALSO FORBIDDEN anywhere in the output:** 認知症, 脳の老化, ボケ, 手遅れ and
any other decline-and-fear phrasing. They pull clicks and they break beat ②
in the same line — this channel does not sell people their own decline.

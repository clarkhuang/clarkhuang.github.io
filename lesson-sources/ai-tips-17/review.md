# Independent review — AI Tip 17 (Don't Paste Secrets)

Script: `out/ai-tip-17.json` · Notes: `out/notes-17.md` · Titles: `out/titles.json`

## Verdict: CHANGES NEEDED → all MAJOR items fixed; script now passes

Three MAJOR items found and fixed in the script. Rule and summary did not change, so
`titles.json` is untouched. Stills re-rendered to `out/stills/17/`; contact sheet and scene PNGs
checked: no overflow, no overlap, no banned names.

## MAJOR items and fixes

### 1. Scene 02 (`02_paste`): the screen contradicted the voice (checklist 4, 6)
The narration says you catch the password mid-paste and "the password never went in." The
terminal card showed the bot already working on the paste ("Reading the error…") with the
unredacted `DATABASE_URL` as a bot line, and then "Stop. Redact that." as a message typed to the
bot. On screen, the secret had been sent, which is the exact failure the tip is about.

Fix (visual data only, narration unchanged): the card is now an unsent draft. Title is
"chat draft — not sent yet"; the lines are your message, the pasted error, the pasted
`DATABASE_URL` with the password, a gap, then the redacted line and "Sent. The password stayed
out." No bot activity is shown before the redaction.

### 2. Scene 04 (`04_instances`): an unsourced item under "FROM PUBLIC REPORTS" (checklist 1)
The third beat ("error logs and env files that quietly carry connection strings") is not a
public report in the research brief; it is the brief's general description of the problem. It was
narrated and labelled as a public report. The second beat's "then a scramble to figure out what
to do" also overstated its source (threads asking "was that bad?").

Fix: narration and beats now map one-to-one to the three threads the brief cites: production
database credentials pasted into a chatbot at work; an API key pasted into a chat and noticed
only afterward; people asking whether the keys they handed over need replacing. No names, dates
or counts. The punch line was "The chat can still help without the secret", which did not follow
from the list; it is now "Each time, the question came after the paste."

### 3. Scene 07 (`07_rule`): rule card did not match the narrated rule (checklist 4, 6)
The voice gives three follow-ups (replace with placeholders; change the credential if one
slipped through; the chat cannot unsay it). The card showed four items, one never spoken
("Send the rest; the bot can still help") and one worded differently ("Asking the chat to forget
it is not a fix"). Reference tips 12, 13 and 16 keep the card and the voice line for line.

Fix (visual data only): card items are now the three narrated lines, in order. The rule text now
matches across narration, rule card, `notes-17.md` and `titles.json`.

## Minor items left as is

- Scene 05 tell is broader than the example. "If you wouldn't put it on a postcard, don't paste
  it" would also rule out the error and config the video tells you to send. The postcard framing
  comes from the research brief, so I left it; a tighter line would scope it to the secret
  ("If that line would be a problem on a postcard, it doesn't go in the chat").
- Scene 05 card wording ("If it isn't for a postcard, cut it.") paraphrases the voice rather than
  matching it. Same meaning.
- Scene 02/06: the redacted example still shows the `admin` username and `prod-db` host, while
  scene 06 lists "connection strings" and "internal URLs that aren't public" among things to
  replace. This follows the research brief's example. `DATABASE_URL=REDACTED` would be stricter.
- Scene 01 hook reuses Tip 16's sentence frame word for word ("…feels like… [pause] …is
  <emphasis>something else</emphasis>"). Back-to-back in the series it will sound repeated.
- Scene 06 narration lists seven kinds of secret; the split card shows only the usual/better
  paste. No contradiction, but the list is the densest moment (49 words) and has no on-screen
  support.
- Scene 08 "Reply with…" assumes a place to reply; same wording as Tip 16, so left for consistency.

## Checklist results

1. Facts beyond source: fixed (major 2). No statistics, named incidents, or stories about Clark.
   Contractor/whiteboard line and the deploy example come from the research brief.
2. Internal names: none. No company, internal bot, coworker, or system names. "Change that
   credential" is the brief's public security advice, not a key-rotation remark (per BRIEF).
3. Tags: only `[pause]` and `<emphasis>`; balanced; no laugh tags.
4. Screen vs narration: fixed (majors 1 and 3).
5. Tone: no hype words or jokes. Hook repetition noted as minor.
6. Own rule: the example redacts before sending; rule is identical in narration, card, notes
   and titles. Postcard breadth noted as minor.
7. Layout data: all scenes use existing layouts (`title`, `terminal_mock`, `statement`,
   `timeline`, `split`, `rule`, `outro`) with shapes copied from tips 12, 13, 16. Terminal line
   kinds are limited to ones the renderer handles (`you`, `claude`, `ok`, `blank`).

Estimated length after fixes: about 106 seconds, 9 scenes. Nothing was narrated or rendered, and
no API key was touched.

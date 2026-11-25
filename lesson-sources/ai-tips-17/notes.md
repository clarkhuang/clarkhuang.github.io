# AI Tip 17 — Don't Paste Secrets

## Why this tip
Next unused idea from the Nov 21, 2026 user-research brief (`_ref/ai-tips-research.md`, ranked item 6). Tips 12–16 already shipped research items 1–5. This one is not in the existing 16-tip series, and it is not in the OpenBook how-to groupings for chapters 23–27 (those chapters cover tips 1–16 only).

Distinct from:
- Tip 01 (Paste First, Ask Second): show the material; this tip is what *not* to include in that paste.
- Tip 04 (Know What the Bot Can Actually Reach): what the *bot* can reach through connectors; this is what *you* put into the box.
- SE 101 lesson 10 (Strict About Data): building systems that don't risk customer data; this is the everyday chat-paste habit.

## Sources for the instances (public, described generically; no invented statistics)
- LayerX / The Hacker News, 2026: enterprise AI usage and the risk of credentials ending up in prompts. https://thehackernews.com/2026/05/new-ai-usage-report-enterprise-ai-risk.html
- Scene 04 beats map one-to-one to public threads listed in the research brief (item 6), described generically with no names, dates, or counts:
  1. Production database credentials pasted into a chatbot at work (r/Information_Security thread).
  2. An API key pasted into a chat and noticed afterward (r/ChatGPT thread).
  3. Someone asking whether keys given to a chatbot need replacing (r/webdev thread).
  (Review fix: the earlier third beat, "error logs and env files carrying connection strings", was not a public report in the brief, so it no longer sits under the FROM PUBLIC REPORTS label.)
- The research habit: scan before you paste; replace secrets with placeholders; if one went in, treat the paste as a leak.

The deploy-error illustration is clearly generic ("Say a deploy is failing…"). It is not a story about Clark or about any named company.

## Claims and wording notes
- "Change that credential" is general public security hygiene from the research brief, not a remark about this site's narration-key handling or any company's key-rotation process. COMMON.md's "leave out remarks about rotating or exposing API keys" is about not publishing pipeline/keychain practice. This tip does not mention how keys are stored or which services are used.
- No numbers, percentages, or named incidents are asserted.
- No invented stories, quotes, or biography about Clark.
- Allowed tags only: [pause], <emphasis>, <slow>. No laugh tags.

## Review changes (independent review)
- Scene 02 terminal card now shows an unsent chat draft; the bot no longer appears to read the password before the redaction.
- Scene 04 third instance replaced with a sourced one (see above); punch line changed to match.
- Scene 07 rule card items now match the narrated rule line for line.
- Rule and summary are unchanged, so `titles.json` is unchanged.

## Rule
Scan before you paste. Replace secrets with placeholders. If one slipped through, change that credential. The chat cannot unsay it.

## Summary
A chat is not a locked room. Scan a paste for keys, tokens, passwords, and other secrets, replace them with placeholders, and if one slipped through, change that credential — asking the chat to forget it is not a fix.

## After review
Two minor items from the Fable 5.2 review were tightened before narration:
- The hook no longer reuses Tip 16's sentence frame. It is now: "The error belongs in the chat. The password sitting next to it does not."
- The tell is scoped to the secret: "If that line would be a problem on a postcard, it doesn't go in the chat."

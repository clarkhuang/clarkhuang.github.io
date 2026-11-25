# Don't Paste Secrets

_AI Tips · Lesson 17_

HTML page: https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/index.md (plus https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [AI Tips](https://clarkhuang.github.io/ai-tips/index.md)
- Series agents file: [https://clarkhuang.github.io/ai-tips/AGENTS.md](https://clarkhuang.github.io/ai-tips/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/AGENTS.md](https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/ai-tips-17-dont-paste-secrets.mp4
- Duration: 1:33 (93.0 seconds)
- Published: Nov 25, 2026
- Poster: https://clarkhuang.github.io/videos/posters/ai-tips-17-dont-paste-secrets.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/ai-tips-17-dont-paste-secrets.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/ai-tips-17

## Chapters

- [0:00] The problem
- [0:21] Why it happens
- [0:32] Where it shows up
- [0:45] The tell
- [0:51] The habit

## The lesson

A chat is not a locked room. Scan a paste for keys, tokens, passwords, and other secrets, replace them with placeholders, and if one slipped through, change that credential — asking the chat to forget it is not a fix.

## The rule

Scan before you paste. Replace secrets with placeholders. If one slipped through, change that credential. The chat cannot unsay it.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

The error belongs in the chat. The password sitting next to it does not.

### The problem

Say a deploy is failing. You copy the error, and the config, so the bot can see everything. Mid-paste you catch it: a production database password, sitting in the block. You stop, replace it with REDACTED, and send the rest. The bot can still help. The password never went in.

### Why it happens

A chat is closer to emailing a contractor than to writing on a whiteboard in a locked room. Once a secret is in the thread, asking the bot to forget it does not unsay it.

### Where it shows up

This shows up in public reports. Production database credentials pasted into a chatbot at work. An API key pasted into a chat, and noticed only afterward. And people asking whether the keys they handed over now need replacing.

### The tell

Here's the tell. If that line would be a problem on a postcard, it doesn't go in the chat.

### The habit

Before you paste, scan. Keys, tokens, passwords, connection strings, session cookies, customer personal data, internal URLs that aren't public. Replace them with placeholders. If a secret did go in, treat the paste as a leak, and change that credential. Asking the chat to forget it is not a fix.

Scan before you paste. Replace secrets with placeholders. If one slipped through, change that credential. The chat cannot unsay it.

Your turn. Think of the last thing you pasted into a chat. Reply with the one kind of secret you'd now scan for first.

Show the problem. Keep the secrets out.

## Related lessons

- Lesson 1: [Paste First, Ask Second](https://clarkhuang.github.io/ai-tips/01-paste-first-ask-second/index.md) (available)
- Lesson 2: [Ask for Proof, Not “Done”](https://clarkhuang.github.io/ai-tips/02-ask-for-proof/index.md) (available)
- Lesson 3: [Define the Number Before You Ask for It](https://clarkhuang.github.io/ai-tips/03-define-the-number-before-you-ask-for-it/index.md) (available)
- Lesson 4: [Know What the Bot Can Actually Reach](https://clarkhuang.github.io/ai-tips/04-know-what-the-bot-can-actually-reach/index.md) (available)
- Lesson 5: [Don't Trust "I Can't"](https://clarkhuang.github.io/ai-tips/05-dont-trust-i-cant/index.md) (available)
- Lesson 6: [Teach It Once](https://clarkhuang.github.io/ai-tips/06-teach-it-once/index.md) (available)
- Lesson 7: [The Second Message](https://clarkhuang.github.io/ai-tips/07-the-second-message/index.md) (available)
- Lesson 8: [Stop Re-Explaining Yourself](https://clarkhuang.github.io/ai-tips/08-stop-re-explaining-yourself/index.md) (available)
- Lesson 9: [Claude Code Isn't Just for Developers](https://clarkhuang.github.io/ai-tips/09-claude-code-isnt-just-for-developers/index.md) (available)
- Lesson 10: [The Label Is Not the Definition](https://clarkhuang.github.io/ai-tips/10-the-label-is-not-the-definition/index.md) (available)
- Lesson 11: [Your Bot in the Meeting](https://clarkhuang.github.io/ai-tips/11-your-bot-in-the-meeting/index.md) (available)
- Lesson 12: [Brief the Next Chat](https://clarkhuang.github.io/ai-tips/12-brief-the-next-chat/index.md) (available)
- Lesson 13: [Open the Source](https://clarkhuang.github.io/ai-tips/13-open-the-source/index.md) (available)
- Lesson 14: [Ask It to Disagree](https://clarkhuang.github.io/ai-tips/14-ask-it-to-disagree/index.md) (available)
- Lesson 15: [Treat Memory Like Notes](https://clarkhuang.github.io/ai-tips/15-treat-memory-like-notes/index.md) (available)
- Lesson 16: [Don't Fire and Forget](https://clarkhuang.github.io/ai-tips/16-dont-fire-and-forget/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/AGENTS.md) in this folder, [https://clarkhuang.github.io/ai-tips/AGENTS.md](https://clarkhuang.github.io/ai-tips/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

# Ask for Proof, Not “Done”

_AI Tips · Lesson 2_

HTML page: https://clarkhuang.github.io/ai-tips/02-ask-for-proof/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/ai-tips/02-ask-for-proof/index.md (plus https://clarkhuang.github.io/ai-tips/02-ask-for-proof/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [AI Tips](https://clarkhuang.github.io/ai-tips/index.md)
- Series agents file: [https://clarkhuang.github.io/ai-tips/AGENTS.md](https://clarkhuang.github.io/ai-tips/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/ai-tips/02-ask-for-proof/AGENTS.md](https://clarkhuang.github.io/ai-tips/02-ask-for-proof/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/ai-tips-02-ask-for-proof.mp4
- Duration: 2:19 (139.3 seconds)
- Published: Nov 21, 2026. Updated: Nov 22, 2026
- Poster: https://clarkhuang.github.io/videos/posters/ai-tips-02-ask-for-proof.jpg

## Chapters

- [0:00] The problem
- [0:26] Five ways it shows up
- [1:22] The pattern
- [1:34] The habit

## The lesson

When a bot says “done”, it is usually reporting the status of the step it ran, not whether the outcome you wanted is true. Five short examples show the gap, and none of them is a bot misbehaving. The fix is to ask for something only a real result can produce.

## The rule

Ask for the artifact, not the status: the ticket numbers, a screenshot on the actual device, counts per item instead of a job status, a link you can click yourself. No artifact means it hasn't happened yet.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Here's one of the most common ways a bot will quietly waste your week. It tells you something is done. And it isn't.

### The problem

When a bot says done, it usually means one of two things. I posted it. Or, the system I called answered with a success message. Neither one is what you were hoping for.

Both of those are statuses. A report on the step the bot ran. Not on whether the outcome you wanted is actually true.

### Five ways it shows up

Example one. A bot runs a rebill workflow, and reports back: completed, no errors. Accurate. The job did complete. But a large share of the orders inside it had failed. That was the job's status, not the orders'.

Two. A bot reports a page fix is live. Its check read the page's HTML. But that element renders after the page loads. So the check saw a clean page, while anyone on a phone could still see the problem. It took being flagged twice.

Three. A bot sends a screenshot, and it looks correct. It was correct, about test data. The run never touched the real thing.

Four. Tickets have been filed, says the bot. But no ticket numbers. So nobody could open one, and check it existed at all.

And five. A bot says: I'll log that decision in the tracker. It didn't have write access. So the decision never landed anywhere.

### The pattern

Now line them up. No bot misbehaved. Every one reported honestly, on the step it ran. But the step finishing, and the outcome being true, are two different facts.

### The habit

So stop asking whether it did the thing. It'll say yes. It always says yes.

Ask for something only a real result can produce. The ticket numbers. A screenshot on the actual device. Counts per item, not a job status. A link you can click yourself. Each one either exists, or it doesn't.

And if it can't hand you the artifact, the work isn't finished yet. That's fine. It's a normal outcome. You just found out today, instead of a week from now, when somebody else finds it for you.

And none of this is distrust. If a teammate said the tickets were filed, you'd say: great, send me the links. Nobody takes that as an insult.

So that's the habit. Ask for proof, not done.

## Related lessons

- Lesson 1: [Paste First, Ask Second](https://clarkhuang.github.io/ai-tips/01-paste-first-ask-second/index.md) (available)
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
- Lesson 17: [Don't Paste Secrets](https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/ai-tips/02-ask-for-proof/AGENTS.md) in this folder, [https://clarkhuang.github.io/ai-tips/AGENTS.md](https://clarkhuang.github.io/ai-tips/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

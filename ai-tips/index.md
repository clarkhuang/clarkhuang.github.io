# AI Tips

HTML page: https://clarkhuang.github.io/ai-tips/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/ai-tips/index.md (plus https://clarkhuang.github.io/ai-tips/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

Short, practical lessons on working with AI assistants and agents. Each one names a common failure, explains why it happens, and leaves you with one habit to fix it.

16 of 16 lessons available.

## Lessons

### 01. [Paste First, Ask Second](https://clarkhuang.github.io/ai-tips/01-paste-first-ask-second/index.md) (available)

When an AI gives you a useless answer, it is usually not the AI's fault: you described the problem instead of showing it. Without the real material, it can only guess. Paste the screenshot, document, error message, or email thread first, and the same question gets a specific, usable answer.

**Rule:** Paste first, ask second. Hand over the screenshot, document, error message, or email thread before you type a single word of your question.

### 02. [Ask for Proof, Not “Done”](https://clarkhuang.github.io/ai-tips/02-ask-for-proof/index.md) (available)

When a bot says “done”, it is usually reporting the status of the step it ran, not whether the outcome you wanted is true. Five short examples show the gap, and none of them is a bot misbehaving. The fix is to ask for something only a real result can produce.

**Rule:** Ask for the artifact, not the status: the ticket numbers, a screenshot on the actual device, counts per item instead of a job status, a link you can click yourself. No artifact means it hasn't happened yet.

### 03. [Define the Number Before You Ask for It](https://clarkhuang.github.io/ai-tips/03-define-the-number-before-you-ask-for-it/index.md) (available)

Ask a bot for a number with a loose word in it and it will quietly pick a meaning, then hand you a confident, wrong answer. This tip shows how one word like "got" or "orders" can mean several populations, and the one extra sentence that removes the guess.

**Rule:** Before asking any agent or analyst for a number, state three things: the exact metric (which event, which status), the source system your team signs off on, and the as-of date. Where you can, add a number you already know ("this should land near X, tell me if it doesn't") so the answer has to reconcile. If a vague question gets a fast, confident answer, treat that speed as the warning sign and ask what interpretation was used.

### 04. [Know What the Bot Can Actually Reach](https://clarkhuang.github.io/ai-tips/04-know-what-the-bot-can-actually-reach/index.md) (available)

A bot's usefulness is bounded by what it's connected to, and it almost never tells you where that boundary is. Five generic examples show how a missing link, an unread thread reply or a doc it can't write turns into something that sounds like success.

**Rule:** Before handing a bot a task, confirm which bot you're talking to and what it's connected to. Treat any "I'll write / file / run / log it" as a claim about access, not a status, and check it can actually do that. Remember that an approval, a chat request to borrow access, or an untagged thread reply doesn't grant access or reach the bot. Access is granted where the tool is administered.

### 05. [Don't Trust "I Can't"](https://clarkhuang.github.io/ai-tips/05-dont-trust-i-cant/index.md) (available)

A bot's "I can't" is often a prediction, not a test. It hasn't tried, or it guessed at your role. This tip shows how to tell a soft refusal from a real limit, so you push on the right ones and never around a genuine guardrail.

**Rule:** When an agent says it can't, check whether it names the missing piece. A bare refusal: ask it to find another permitted route and try before saying no. A named blocker (a key, an account link, someone's approval): ask it to confirm it actually checked, and if it holds, go get that piece rather than arguing. Ask for the goal, not the method, state your role and access up front, pre-authorise a second attempt, and ask for the exact step that stopped it. "Find a way" never means working around a real limit.

### 06. [Teach It Once](https://clarkhuang.github.io/ai-tips/06-teach-it-once/index.md) (available)

Knowledge is what a bot has picked up. Skills are jobs you've written down for it. This tip shows how to save what a bot works out so nobody repeats it, why a good skill is mostly guardrails, and how saved rules can fence a credential that does more than the job needs.

**Rule:** When you explain the same thing to a bot a second time, or it finally gets something right after getting it wrong, have it save the rule. Write skills mostly as boundaries: when to act, when not to, whose data, where to report, what to do when unsure, and when to stop. Where a credential can do more than the job needs, add an explicit rule (e.g. reads only, no writes without approval), but treat it as a seatbelt, not a vault, and use a narrower credential for anything that genuinely matters.

### 07. [The Second Message](https://clarkhuang.github.io/ai-tips/07-the-second-message/index.md) (available)

Most people read the first answer and stop. Either they settle for it or give up on the tool. One follow-up line in the same chat usually turns a generic draft into a usable one, and asking the A.I. to interview you first is better still.

**Rule:** Treat the first answer as a draft, not a verdict. Reply in the same conversation with one of three follow-ups: say specifically what's wrong, ask for a different shape, or give it something concrete to work from. For anything you'll care about, start by telling it: "Before you write it, ask me what you need to know." Don't open a new chat to fix a draft, because that throws away the context it has built.

### 08. [Stop Re-Explaining Yourself](https://clarkhuang.github.io/ai-tips/08-stop-re-explaining-yourself/index.md) (available)

If every Claude chat starts with you re-explaining your job and re-attaching the same file, a Project fixes it: shared knowledge and instructions in one place. This tip covers what sharing a project hands over (and what stays private), the permission choices, and where Cowork tasks run.

**Rule:** When you find yourself re-uploading the same files or repeating the same instructions, put them in a Claude Project: files in project knowledge, standing rules in project instructions. Share the project with the people who'd benefit. Sharing hands over knowledge and instructions, while each person's chats stay private unless they share one deliberately. Choose org-wide or invite-only, and can-view or can-edit. If a task "can't see" your local folder, check whether it needs the desktop app open.

### 09. [Claude Code Isn't Just for Developers](https://clarkhuang.github.io/ai-tips/09-claude-code-isnt-just-for-developers/index.md) (available)

Claude Code's name keeps most non-developers away, but it works on any folder of ordinary files, driven by plain-English requests. This tip shows what it can do with screenshots, invoices and transcripts, what "it's a terminal" really means, and how to start in five minutes.

**Rule:** For any job that means reading, renaming, or pulling information across many files in one folder, try Claude Code before doing it by hand: install it, point it at the folder, and describe the outcome in plain English. Use Esc to interrupt, /help to see what it can do, and the desktop app if you'd rather not use a terminal. Check the result before relying on it.

### 10. [The Label Is Not the Definition](https://clarkhuang.github.io/ai-tips/10-the-label-is-not-the-definition/index.md) (available)

The most common mistake in six weeks of bots' self-written lessons: trusting what a field is called instead of what it counts. A number with the wrong definition still ties out and reconciles, so nothing looks wrong and it travels.

**Rule:** Before using or explaining a number, find out what it actually counts. Read the definition, not the field name. Treat a surprising number as a likely definition problem before treating it as a story. When the source is unclear, ask the data owner which table holds the number they actually sign off on, and say which dataset every reported number came from.

### 11. [Your Bot in the Meeting](https://clarkhuang.github.io/ai-tips/11-your-bot-in-the-meeting/index.md) (available)

A notetaker records one call and summarises it. A bot that's connected to your team's work can answer questions live, turn action items into real tickets, and remember what was decided last week. This tip shows how to try it on one meeting, and the limit that catches people out.

**Rule:** Try a connected team bot on one recurring meeting, the one where someone always says "I'll check and get back to you." Invite it (or give it the link) and admit it from the waiting room. Afterwards, if you invited it, share the notes yourself, because often only the inviter receives them. Expect a first version: it may not see screen shares or speak aloud yet.

### 12. [Brief the Next Chat](https://clarkhuang.github.io/ai-tips/12-brief-the-next-chat/index.md) (available)

Long chats drift without warning: early decisions count for less and can fall out of view. When a chat gets long, have it write a handoff and carry on in a fresh chat.

**Rule:** When a chat gets long, brief the next one: the goal and the limits, every decision so far, what's still open, and read it before you paste it.

### 13. [Open the Source](https://clarkhuang.github.io/ai-tips/13-open-the-source/index.md) (available)

AI-supplied citations can be perfectly formatted and completely invented, and pushed on a dead link a model may insist the page changed. A reference you haven't opened is a claim, not a source.

**Rule:** Open it before you use it: click the link, check the title and authors, find the sentence you need on the page. Nothing to open? Not a source yet.

### 14. [Ask It to Disagree](https://clarkhuang.github.io/ai-tips/14-ask-it-to-disagree/index.md) (available)

Models lean toward the view already in your question, so a yes to a leading question isn't a second opinion. Ask for the case against before you ask for advice: a review, not a fight.

**Rule:** Ask for the case against: leave your answer out of the question, ask for the strongest case against and how you could be wrong, then ask what it recommends.

### 15. [Treat Memory Like Notes](https://clarkhuang.github.io/ai-tips/15-treat-memory-like-notes/index.md) (available)

AI memory is a small set of saved notes, not a mind. Notes can be never saved, saved wrong, off-topic or stale, and they won't keep up unless you update them.

**Rule:** Treat memory like notes: say what matters in the prompt, don't assume a new chat knows, read your memory now and then, and fix or delete what's wrong.

### 16. [Don't Fire and Forget](https://clarkhuang.github.io/ai-tips/16-dont-fire-and-forget/index.md) (available)

Agents act on real systems, and a rule typed into a prompt is not a lock. Put the lock in access and approval settings, and keep the judgment for steps you can't undo.

**Rule:** Set the stop before you start: say what done looks like, limit what it can touch, require approval before delete, reset, push or send, and watch the first few steps.

## For agents

- This series: https://clarkhuang.github.io/ai-tips/index.md
- This series’ agents file: https://clarkhuang.github.io/ai-tips/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.

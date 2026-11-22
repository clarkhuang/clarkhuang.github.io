# Understand Before You Change

_Software Engineering 101 · Lesson 5_

HTML page: https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md (plus https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-05-understand-before-you-change.mp4
- Duration: 2:14 (134.0 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se101-05-understand-before-you-change.jpg

## Chapters

- [0:00] The worst fix
- [0:28] The one job
- [0:48] The old habit
- [1:04] Today’s version
- [1:25] The split
- [1:46] The rule
- [2:03] Your turn

## The lesson

A perfect fix for the wrong problem is still wrong. Own the problem, restate it, reproduce and trace it, then fix the cause.

## The rule

Before planning, restate the problem in plain words, and confirm it with the person who gave you the task. They own the problem. Before fixing, reproduce it if you can, and trace what actually happens. Then fix the cause, not the symptom.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering one oh one. Lesson five. Understand before you change.

### The worst fix

Here's the most dangerous kind of fix. One that works perfectly. On the wrong problem.

Watch how it happens. Misunderstand the problem, and the spec is wrong. The agent builds the wrong thing, flawlessly. A reviewing agent checks it against the same wrong spec, and says, looks good. Every step passes. And nothing in that chain is built to catch it.

### The one job

In lesson one, I had agents fix mobile app code I couldn't read. And there was one job I didn't hand over. Understanding the problem. I made sure I understood what had actually been reported. For me, that was not negotiable.

In plain words, that means two things. What's happening. And what should happen instead.

### The old habit

There's an older habit that teaches this. Set a breakpoint, and step through the code. Line by line. Into every function. Hardly anyone does it now. It was slow. But when you finished, you knew what the code actually did. Not what you assumed it did.

### Today’s version

Here's the version for today. Before the agent changes anything, have it restate the problem. Reproduce it, if it can. And trace what actually happens, step by step. If the trace doesn't explain the symptom, you haven't found it yet.

Then fix the cause, not the symptom. A symptom fix makes the report go away. The cause is still in there.

### The split

So here's the split. If you hand out the task, you own the problem. The agents work the solution. In lesson one, I didn't need to read that code line by line. I needed to know what fixed meant.

And here's a quick test. Can you say the problem in one sentence? Would the person who reported it agree? If not, you're not ready to hand it off.

### The rule

Rule five, for your agents. Before planning, restate the problem in plain words, and confirm it with the person who gave you the task. They own the problem. Before fixing, reproduce it if you can, and trace what actually happens. Then fix the cause, not the symptom.

### Your turn

Your turn. Take the last bug you were handed, and write it down in one sentence. Would the person who reported it agree?

See you in lesson six.

## Related lessons

- Lesson 1: [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)
- Lesson 2: [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 4: [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)
- Lesson 6: [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)
- Lesson 7: [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)
- Lesson 10: [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

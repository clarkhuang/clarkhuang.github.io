# Say What, Not How

_Software Engineering 101 · Lesson 6_

HTML page: https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md (plus https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-06-say-what-not-how.mp4
- Duration: 2:29 (149.7 seconds)
- Published: Nov 21, 2026
- Poster: https://clarkhuang.github.io/videos/posters/se101-06-say-what-not-how.jpg

## Chapters

- [0:00] A slow query
- [0:32] The idea
- [1:01] The dial
- [1:32] In practice
- [2:05] The rule
- [2:19] Your turn

## The lesson

Like a database optimizer, an agent does its best work when you state the outcome and the limits, not the steps. Too tight and too loose both cost you.

## The rule

A spec states the outcome, and what must not break. It doesn't dictate steps, unless a step is itself a requirement. And before you start the work, give a cost forecast.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering one oh one. Lesson six. Say what, not how.

### A slow query

Quick question. A database query is slow. What's the most likely cause? The server's too small? An index is missing? Or the database is just slow? Usually, a missing index.

And there's an order to it. First, look at what the database is actually doing. Usually, an index is missing. Sometimes a better query fixes it, and that can be the easiest fix of all. And once it's fast enough, you stop.

### The idea

Here's the idea underneath. A query is like ordering at a restaurant. You say what you want. You don't walk into the kitchen and tell the chef which pan to use.

The database has an optimizer, and it picks the plan. These days, it's very good. It keeps statistics on your data that you don't carry in your head. So when you force its hand, you can easily make things worse.

Over-engineering can hurt you. That's true of databases. And it's just as true of agents.

### The dial

Picture a dial. Turn it all the way one way, and you dictate every step. Use this file. Write this function. Name it this. Now the agent can't find a better answer. You already chose for it.

Turn it all the way the other way. Build me something good. Now it wanders. It explores things you never needed, and you pay for every step in usage.

The useful spot is the middle. Say exactly what done looks like. Say what must not break. Ask what it'll cost. And leave the how alone.

### In practice

Here it is in one example. Too tight sounds like this. Add an index, on this column, in this file, with this name. Better sounds like this. This report must load in under two seconds. The numbers stay exactly the same. Show me the cost before you start. The second one might get you that index. Or something smarter.

One exception. Sometimes the how is the requirement. Use the library the project already has. Don't add a new dependency. Write those down. That's a constraint, not micromanagement.

### The rule

Rule six, for your agents. A spec states the outcome, and what must not break. It doesn't dictate steps, unless a step is itself a requirement. And before you start the work, give a cost forecast.

### Your turn

Your turn. Find the last instruction you gave an agent, and read it again. Is it a what? Or a how?

See you in lesson seven.

## Related lessons

- Lesson 1: [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)
- Lesson 2: [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 4: [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)
- Lesson 5: [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)
- Lesson 7: [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)
- Lesson 10: [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

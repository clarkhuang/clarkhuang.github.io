# The Abstraction Ladder

_Software Engineering 101 · Lesson 4_

HTML page: https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md (plus https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-04-abstraction-ladder.mp4
- Duration: 2:52 (173.0 seconds)
- Published: Nov 21, 2026
- Poster: https://clarkhuang.github.io/videos/posters/se101-04-abstraction-ladder.jpg

## Chapters

- [0:00] The ladder
- [0:54] The idea
- [1:17] The catch
- [1:44] The skill
- [2:01] The rule
- [2:12] Your turn

## The lesson

AI coding is one more rung on a ladder that runs from logic gates up. Stay at the top, and know when to send your agent down a rung.

## The rule

Break a task into small pieces that each do one thing. And when something on one layer doesn't add up, look at the layer below, before you change anything.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering one oh one. Lesson four. The abstraction ladder.

### The ladder

A.I. coding can feel like the moment everything about software changed. I see something else. One more rung, on a ladder I've been climbing for thirty years.

Start at the bottom. Logic gates. AND, OR, NOT. Wires and switches, nothing more.

Wire enough gates together, and you get a chip that runs machine code. Ones and zeros. Then assembly. The same instructions, with names a person can read.

Then programming languages. Procedural: do this, then this. Then object oriented: bundle the data with the things you can do to it.

Then libraries and frameworks. Somebody already solved the problem. You call their solution, and you don't look inside.

And now, agents. You describe what you want, in plain words, and the agent writes the layer below. One more rung.

### The idea

Notice that every rung does the same job. It hides the one below it, so you can think about a bigger problem. That's abstraction.

Abstraction has a partner. Breaking things down. At Berkeley, they loved teaching this with small functions. A large problem is a series of small ones. Solve each one. Combine them. A planner agent does the same thing to a feature request.

### The catch

Here's the catch. Every abstraction leaks. Sooner or later, the layer below shows through.

A query is slow, and the answer is one rung down: is there an index to use? An agent reports the work is done, and the code underneath says otherwise. In lesson one, the reviewing agent went one rung down. It read the real code, not the builder's summary. And in round four, it found a fix that had created two new problems.

### The skill

So when something doesn't add up, the move is one rung down. Look below, before you change anything.

And look at what today's A.I. tools stand on. Linux. Apache. Open source building blocks, and ideas that are decades old. The top rung is new. The ladder isn't.

### The rule

Rule four, for your agents. Break a task into small pieces that each do one thing. And when something on one layer doesn't add up, look at the layer below, before you change anything.

### Your turn

Now, a question for you. Which rung should you be working on, most days? Think about it for a second.

It's a trick question. You should always stay at the top of your A.I. tools ladder. But you have to know how, and when, to ask your A.I. tool to climb down that ladder, to understand the problem and the solutions better. And to direct it down, or back up, depending on where you are with the solution, the feature, or the bug fix. That's the art. That's the experience. Understand these fundamentals, and it's a piece of cake.

So, your turn. Think of the last time you sent your agent down a rung. What did it find there?

See you in lesson five.

## Related lessons

- Lesson 1: [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)
- Lesson 2: [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 5: [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)
- Lesson 6: [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)
- Lesson 7: [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)
- Lesson 10: [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

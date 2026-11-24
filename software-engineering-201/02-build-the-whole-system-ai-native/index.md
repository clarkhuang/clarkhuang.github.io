# Build the Whole System, AI-Native

_Software Engineering 201 · Lesson 2_

HTML page: https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md (plus https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-02-build-the-whole-system-ai-native.mp4
- Duration: 3:58 (238.9 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-02-build-the-whole-system-ai-native.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-02-build-the-whole-system-ai-native.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-02

## Chapters

- [0:00] The question
- [0:33] One loop to a system
- [0:51] What AI-native means
- [1:38] A worked example
- [2:18] At enterprise scale
- [3:00] The path
- [3:30] The rule
- [3:48] Your turn

## The lesson

After the four eras, the first step from one loop to enterprise systems: what changes when you build a whole app or system with AI instead of one fix. A system is AI-native when agents and people can both read it, navigate it, contribute to it, and rebuild it. That takes four things: a Markdown twin, an index, and an AGENTS.md for every part; specs and briefs as the source; tests and checks as the contract; and staging plus a person's approval before anything reaches production. The worked example is this site, and the same four things matter even more at enterprise scale.

## The rule

Before you build anything bigger than one fix, make it readable to agents and people: a Markdown twin for every page, an index of the whole system, and an AGENTS.md that says how to work there. Treat specs and briefs as the source and tests and checks as the contract, and send every change through staging for a person to approve before it reaches production.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. From loop, to enterprise systems. Lesson two. Build the whole system, AI native.

### The question

Quick question to start. You're asking agents to build a whole app, not just one fix. What matters most? The smartest model? The longest prompt? Or a system the agents can read, check, and rebuild on their own? The system they can read. A smarter model still guesses when the project lives in someone's head. A long prompt is gone after one chat. What's written into the system is there for every run, and every agent.

### One loop to a system

In 101, the unit of work was one loop. Plan, build, verify. One fix. One feature. In 201, the unit of work is the system. Many parts. Many people. Years of history. And now, agents working in it right alongside the people.

### What AI-native means

So what does AI native actually mean? Here's the definition this series uses. A system is AI native when agents and people can both read it, find their way around it, contribute to it, and rebuild it. Not only the person who wrote it. Not only whoever knows the history.

That takes four things. One. Every page people read has a twin an agent can read: plain Markdown, an index of the whole system, and an agents file that says how to work there. Two. Specs and briefs are the source. Change the brief, and the build follows. Three. Tests and checks are the contract. An agent is done when the checks pass, not when it says it's done. And four. Every change goes to staging first, and a person approves it before it reaches production.

### A worked example

And this isn't hypothetical. The site you're on right now is built exactly this way.

Every page has an index.md twin, and every folder has an AGENTS.md file. There's an llms.txt that indexes the whole site, a machine-readable lesson catalog, and a read-only connector AI tools can plug into. The pages are generated from one content file, and the rebuild steps are written down, so an agent can regenerate every page.

And here's the part that matters most. Agents open pull requests into a staging branch. Staging is a full preview of the site, hidden from search. And only I merge into production.

### At enterprise scale

Think of a kitchen with one great cook. The recipes are in their head. Only they know where everything is. And every plate waits on them.

Now picture a big restaurant kitchen. The recipes are written down. Every station is labeled. A cook on a brand new shift can work from the cards. And nothing leaves the pass until the head chef looks at it. That's what lets a kitchen grow past one great cook.

Now scale that up. An enterprise system isn't one repo. It's dozens of services, data that has to stay private, and people who need to know who changed what, and why. The same four things still hold. They just matter more. Without them, every agent starts from zero, and every person becomes the bottleneck.

### The path

That's the path for this series. Today: build the whole system, AI native. Then, decompose it into a graph. Run agents in parallel, and bring the work back together. Put people where the decisions matter. Measure quality, and watch it run. Turn repeated work into skills. Wire it into routines and pipelines. Then, agents that operate enterprise systems, with real permissions, and a full audit trail. And last, a capstone: one feature, built end to end.

### The rule

Which gives us rule two, for your agents. Before you build anything bigger than one fix, make it readable: a Markdown twin, an index, and an agents file. Keep the specs as the source, and the checks as the contract. And send every change through staging, for a person to approve before production.

### Your turn

Now, your turn. Pick a system you work on. If a brand new agent showed up tomorrow, what could it read? And what would it have to guess?

See you in lesson three.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)
- Lesson 10: [Capstone: One Feature, End to End](https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

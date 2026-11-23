# Four Eras of Building Systems

_Software Engineering 201 · Lesson 1_

HTML page: https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md (plus https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-01-four-eras-of-building-systems.mp4
- Duration: 4:20 (260.8 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-01-four-eras-of-building-systems.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-01-four-eras-of-building-systems.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-01

## Chapters

- [0:00] The question
- [0:28] A lens
- [1:02] Four eras
- [2:26] Building now
- [3:03] What never changes
- [3:18] The path
- [3:34] Recap
- [3:44] The rule
- [4:01] Your turn

## The lesson

How we build big systems has changed from thirty, twenty and ten years ago to now, with agents doing much of the building. One useful lens is that architecture bends around whatever is scarcest. Machines were scarce in the mid-1990s, coordination in the 2000s, and seeing the whole system in the 2010s. Now the scarce things are knowing the work is right and how much of the system an agent can see at once. So design for checking: clear module boundaries, one repository an agent can read, tests and specs it can run, and decisions written down. This is where the thinking is heading, not a settled answer. Four things never changed: the data model outlives the code, money has to add up, you depend on things you don't control, and someone has to understand the layer below.

## The rule

Before you design a system, write down four things: where the boundaries are, what the data model is, what you depend on but don't control, and how you'll know it's right. Put that note in the repository, where every agent and person working on the system can read it, and keep it current as the design changes.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. From loop, to enterprise systems. Lesson one. Four eras of building systems.

### The question

Quick question. An agent can now write a working piece of a billing system in an afternoon. So in a big system today, what's scarce? Code? Servers? Or knowing that what got built is right? Knowing it's right. Code got cheap. Checking it didn't. Thirty years ago, the answer was very different.

### A lens

I've been building systems for about thirty years. Systems built around money: electronic rent payments, a card-issuing platform, an investment adviser for nonprofits. And systems that sell: retail e-commerce and E.D.I., subscription billing, and today, e-commerce again. And the way you build a big system keeps changing.

Here's a useful way to see why. Architecture bends around whatever is scarcest. Whatever is expensive, or slow, the design works around it. So for each of four eras, ask: what was scarce?

### Four eras

Thirty years ago, the commercial web was brand new. You bought servers and racked them yourself, and more capacity was weeks away. So, typically, you built one big program, on one big database, and shipped a few times a year. Companies traded orders as overnight batch files, through E.D.I., and much of that still runs. What was scarce? The machines.

Twenty years ago. The web was the front door. Browser, application, database: three tiers, on rented racks. And the first big public cloud services had just launched. Agile teams shipped every few weeks. What was scarce? Coordination. Getting a growing team to change one codebase without colliding.

Ten years ago. The cloud, by default, for new systems. Many small services, in containers, owned by small teams. The best teams deployed many times a day. And parts they once built themselves became a service, behind an API What was scarce? Seeing the whole. No one person could hold it all in their head, so we built dashboards and tracing to see it.

And now. Agents can write much of the code. Building a piece is fast, and cheap. So what's scarce? Knowing that it's right. That, and context: how much of the system an agent can see, and understand, at once.

### Building now

Now a made-up example: a subscription-billing system, built today, the kind of platform I ran as C.T.O. at sticky dot I O. Clear modules, with boundaries an agent can work inside. One repository, where it can find anything. Tests and specs it can check itself against. And decisions written down, because the agent wasn't in the meeting. My own team keeps its code that way: one repository, with instruction files for the agents.

I'll be straight about that list. It's where the thinking is heading, not a settled answer. The evidence for it is still thin, and indirect. Every era had a confident answer, then found its costs.

### What never changes

And here's what never changed, in any era. The data model outlives the code. Money has to add up. Every system depends on things you don't control: a bank, a card network, a partner's system. And somebody has to understand the layer below.

### The path

Here's the path. Today, the four eras. Then, build a whole system AI native, decompose it, and run agents in parallel. Then governance, quality, skills, and pipelines. And finally, agents that operate enterprise systems.

### Recap

So, to recap. Architecture bends around what's scarce. Today, that's knowing the work is right, and context. So design for checking. And the four constants still hold.

### The rule

Which gives us rule one, for your agents. Before you design a system, write down four things. Where the boundaries are. What the data model is. What you depend on, and don't control. And how you'll know it's right. Then put it in the repository, where every agent can read it.

### Your turn

Now, your turn. Pick the oldest system you still depend on. When was it built, and what was scarce back then? Then ask your AI which era's thinking is hiding inside it.

Next: build a whole system, AI native, so agents and people can both read it, and rebuild it. See you in lesson two.

## Related lessons

- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

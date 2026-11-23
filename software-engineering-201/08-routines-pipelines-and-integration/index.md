# Routines, Pipelines, and Integration

_Software Engineering 201 · Lesson 8_

HTML page: https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md (plus https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-08-routines-pipelines-and-integration.mp4
- Duration: 4:15 (255.5 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-08-routines-pipelines-and-integration.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-08-routines-pipelines-and-integration.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-08

## Chapters

- [0:00] The question
- [0:32] The oldest problem
- [0:50] Work that starts itself
- [1:10] A worked example
- [2:51] What you don’t control
- [3:11] Recap
- [3:24] The rule
- [3:41] Your turn

## The lesson

A job charges a card, the answer is lost, and the job tries again: unless someone designed that retry to be safe, the customer can be charged twice. Connecting systems is the oldest problem in this series, from overnight batch files and EDI, to web services, to an API for everything, to agents calling tools, and all of them are still running somewhere. Some work should start on its own: call a skill plus a trigger a routine, and routines chained together a pipeline. The worked example is the nightly billing run of a made-up subscription-billing system: a clear format at every hand-off, a record from every step whose counts add up, a retry made safe with an idempotency key, and a reconcile step that tells a person when the numbers don't match. The same thinking covers a partner's file that arrives late, twice, or broken: design for at least once, and make twice harmless.

## The rule

Before any work runs on its own, write down four things: what starts it, what crosses at each hand-off, what record each step leaves, and what happens when a step fails, or runs twice. No answer? It isn't ready to run unattended. In full: give every hand-off a clear, written format. Make every step leave a record that adds up, and make every step safe to run twice. When the numbers don't match, don't guess and don't fix them quietly: keep every record and tell a person. Keep that note where the agents and people who run the work can read it.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. Lesson eight. Routines, pipelines, and integration.

### The question

Quick question. It's two in the morning. A job charges a customer's card. The payment goes through, but the connection drops before the answer comes back. So the job tries again. What happens? Nothing? The customer is charged twice? Or the processor catches it on its own? Quite possibly, charged twice. Some processors catch a quick duplicate, but don't count on it. Design the retry to be safe. That design is this lesson.

### The oldest problem

Connecting systems is the oldest problem in this series. Thirty years ago: overnight batch files, and EDI. Then web services. Then an API for everything. Now, agents calling tools. And every one of those is still running somewhere, often inside the same enterprise.

### Work that starts itself

A skill is one job, written down and tested, that runs when someone asks. But some work should start on its own. On a schedule: every night at two. On an event: a payment fails, or a file arrives. Or when the step before it finishes. Call a skill plus a trigger a routine. And routines, chained, make a pipeline.

### A worked example

Here's one, in our made-up subscription-billing system: the nightly billing run. On a schedule, find the renewals due. Charge each one, through the payment processor. Write the invoices. Send the export to the accounting system. And last, reconcile: does our ledger match what the processor says it charged?

Between every two steps, something crosses: the renewals due, the charge results, the invoices, the export file. Give each a clear, written format. Then any step can be rebuilt, or rerun, without touching the others.

And every step leaves a record: what came in, what went out, what failed. A thousand renewals due. Nine hundred eighty-eight charged, twelve declined. Nine hundred eighty-eight invoices, and as many rows sent. The numbers are made up, but they have to add up. When they don't, the run stops there, and you know which step to open.

Back to two A.M. Partway through the charge step, the connection drops. One charge went out, and no answer came back. Did it go through? We don't know. So the retry has to be safe to run twice. Renewals already recorded as charged, it skips. Every other one, it sends with a key that never changes: this subscription, this billing period. If the processor has already seen that key, it returns the first result, instead of charging again. That's an idempotency key, and many payment processors support one.

Last, reconcile compares our ledger with the processor's record. If they don't match, the pipeline doesn't guess, and doesn't fix the numbers itself. It keeps every record, and tells a person. Most of these steps are plain code. An agent earns its place where a step needs judgment, like working out why they don't match.

### What you don’t control

The same thinking covers everything you don't control. Take a partner's nightly file. Check it first. Late: wait, then alert. Twice: recognize it, and skip it. Broken: set it aside, and tell a person. You can't count on anything arriving exactly once. So design for at least once, and make twice harmless.

### Recap

So, to recap. Give every hand-off a clear format. Make every step leave a record that adds up. Make every step safe to run twice. And when the numbers don't match, stop, and tell a person.

### The rule

Which gives us rule eight, for your agents. Before any work runs on its own, write down four things. What starts it. What crosses at each hand-off. What record each step leaves. And what happens when a step fails, or runs twice. No answer? It isn't ready to run unattended.

### Your turn

Now, your turn. Pick one job that already runs on its own: a nightly report, or a sync. Describe its steps to your AI, and ask, for each step: what happens if it runs twice? And what record would prove it ran? The steps with no good answer are where to start.

A pipeline that runs on its own is already operating the system. So whose name does it run under? What is it allowed to touch? And who can see what it did? That's the last lesson: agents that operate enterprise systems. See you in lesson nine.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

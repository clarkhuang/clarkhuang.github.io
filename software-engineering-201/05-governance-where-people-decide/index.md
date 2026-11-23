# Governance: Where People Decide

_Software Engineering 201 · Lesson 5_

HTML page: https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md (plus https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-05-governance-where-people-decide.mp4
- Duration: 4:13 (253.0 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-05-governance-where-people-decide.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-05-governance-where-people-decide.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-05

## Chapters

- [0:00] The question
- [0:29] Every era had a yes
- [1:01] Four questions
- [1:19] A worked example
- [2:05] Make the stop quick
- [2:28] Write it down
- [2:53] What it costs
- [3:16] Recap
- [3:25] The rule
- [3:48] Your turn

## The lesson

Every era had a place where a person said yes: a change board signing off a whole release, then a teammate reviewing the code, then an approval on a pull request. Each was sized for people writing the code, so when agents write changes faster than anyone can read them all, that place has to be designed, not inherited. A good rule of thumb is four questions: does it move money, touch customer data, is it hard to undo, or is it a judgment call no check can make? One yes and a named person decides; four no's and that kind of change can ship on its checks. The worked example is a made-up subscription-billing system, where six pieces of an agent's work lead to four stops and two changes that never wait, and where the agent prepares each decision: what changes, why, the evidence, the risk, and the way back. Write down who approves what in the repository, let the pipeline enforce it, and start strict, releasing one kind of change at a time as its checks earn trust.

## The rule

Before a change ships, find out who decides. Money, customer data, hard to undo, or a judgment call that no check can make: stop for the person named in the repo, and bring the change, the evidence, the risk, and the way back. Not on the list? Stop and ask. Ship on checks alone only what a person has released. In full: bring the decision ready to make (what changes, why, the evidence, the risk, and the way back), and don't classify or approve your own change.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. Lesson five. Governance: where people decide.

### The question

Picture this. Overnight, your agents wrote forty changes to a billing system. All pass their tests. One changes what customers are charged. Who catches it? The tests? A person, reading all forty? Or a person, at a stop built for it? A stop built for it. Tests can't say whether you wanted the change. And nobody reads forty carefully.

### Every era had a yes

Every era had a place where a person said yes. Thirty years ago, typically, a change board, signing off a whole release, a few times a year.

Twenty years ago, more and more, a teammate, reviewing the code before it went in.

Ten years ago, an approval step in an automated pipeline: a pull request a reviewer approves, before it merges.

Each was sized for people writing the code. Now agents write changes faster than anyone can read them all. So that place can't just be inherited. It has to be designed.

### Four questions

So where does a person decide? A good rule of thumb is four questions. Does it move money? Does it touch customer data? Is it hard to undo? Is it a judgment call that no check can make? One yes, and a person decides. Four no's, and that kind of change can ship on its checks.

### A worked example

Take our made-up example: the subscription-billing system from lesson one. Overnight, an agent drafts six things. Fix a typo on an internal admin screen. Add a missing test for renewals. Four no's, both times. They ship on their checks, and nobody waits.

Change how a late fee is calculated. That moves money: the finance owner decides. Migrate the ledger. Money again, and hard to undo: the ledger's owner decides. Send customer emails to a new partner. Customer data: the data owner decides.

And it isn't only code. A refund over the limit: the agent prepares it, a support lead approves it. Under the limit, a person already decided, when they set it. Six pieces of work. Four stops. Two never waited.

### Make the stop quick

A stop only works if a person can clear it quickly. So the agent doesn't hand over a wall of diff and ask, okay? It prepares the decision. What changes. Why. The evidence, from the pipeline: last month's invoices, recomputed, old against new. The risk. And the way back. Now the finance owner decides about the fee. And an engineer still reviews the code that moves money.

### Write it down

Then write it down: who approves what, in a file in the repository. Fees and prices: the finance owner. The ledger: its owner. The checks, the pipeline, and this file itself: always a person. Anything the list doesn't cover: stop and ask. And the pipeline enforces it, by what a change touches. The agent that wrote a change doesn't classify it, or approve it. An old idea from accounting: whoever prepares a payment doesn't approve it.

### What it costs

Stops cost something. A person on everything: people become the bottleneck, and yes turns into a rubber stamp.

A person on nothing: fast, until money moves unapproved.

So start strict, like lesson two: a person on every change. Then release one kind at a time, as its checks earn trust. And where an audit requires a review, that review stays.

### Recap

So, to recap. Design where people decide. Make every stop quick to clear. And let the rest ship on its checks, one released kind at a time.

### The rule

Which gives us rule five, for your agents. Before a change ships, find out who decides. Money, customer data, hard to undo, or a judgment call: stop for the person named in the repo, and bring the change, the evidence, the risk, and the way back. Not on the list: stop and ask. Ship on checks alone only what a person has released.

### Your turn

Now, your turn. Give your AI the last ten changes to a system you run, and the four questions. Ask it: which of these needed a person? Which could have shipped on checks alone? Then see where you disagree.

Ships on its checks. That phrase is carrying a lot. So how good are your checks, really? That's next: quality, feedback, and observability. See you in lesson six.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

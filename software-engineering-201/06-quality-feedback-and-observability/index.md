# Quality, Feedback, and Observability

_Software Engineering 201 · Lesson 6_

HTML page: https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md (plus https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-06-quality-feedback-and-observability.mp4
- Duration: 4:08 (248.6 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-06-quality-feedback-and-observability.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-06-quality-feedback-and-observability.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-06

## Chapters

- [0:00] The question
- [0:31] A lens
- [0:59] The real check
- [1:48] Run it twice
- [2:15] Watch every run
- [2:38] Feed it back
- [3:11] Recap
- [3:24] The rule
- [3:44] Your turn

## The lesson

A green build says the code did what its tests asked; it says nothing about what happened last night. Ten years ago the scarce thing was seeing the whole system, and logs, metrics and traces answered "what happened?". Now the scarce thing is knowing it's right, and no dashboard can answer that until someone has written down what right means. The worked example is a made-up subscription-billing system: "every renewal charged the right amount, exactly once" becomes three checks, and running them on last night's renewals finds three wrong ones inside totals that match exactly. Write the check once and run it twice, before a change ships and after every run; make every step leave a record that people and agents can both read; and feed every miss back into the brief and the checks, while a person still reads a sample, because a check only catches what somebody thought to ask.

## The rule

Before you build, write down what right means, as checks you can run, in the business's words. Run them before a change ships, and after every run. Leave a record at every step. When a check fails, stop and tell a person. Feed every miss back into the brief and the checks. In full: run the checks on samples before a change ships and on the real data after every run, leave each record in a shape people and agents can both read, and let every miss make the next run better.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. Lesson six. Quality, feedback, and observability.

### The question

Picture a made-up billing system. Last night, it renewed its subscriptions. This morning the build is green, and every test passed. Was every customer charged the right amount, exactly once? Yes, the tests passed? Probably, coverage is high? Or: you can't tell from that? You can't tell from that. Green says the code did what its tests asked. It says nothing about what happened last night.

### A lens

Back to the lens from lesson one: architecture bends around what's scarce. Ten years ago, the scarce thing was seeing the whole system. The answer was observability: logs, metrics, traces. They answer: what happened?

Now the scarce thing is knowing it's right. That's a different question. And no dashboard can answer it, until somebody has written down what right means. So: define right, up front. Watch every run. And feed back what you learn.

### The real check

Take our made-up example: the subscription-billing system from lesson one. Here are last night's renewals. And the build is green. But no test ever looked at this table. So was last night right? The green can't say.

So before the work starts, write down what right means, in the business's words. Every renewal charged the right amount, exactly once. Then split that into checks an agent can run. One: none was charged twice. Two: each charge equals the plan's price. Three: every renewal that was due was attempted.

Now run them, on last night's real renewals. One was charged twice. One, the wrong amount. One was never attempted. And look at the totals: they match. Three wrong renewals, inside a sum that's exactly right. So check every renewal, not just the total.

### Run it twice

That one sentence does double duty. You write the check once, and run it twice. Before a change ships, on sample renewals, in the pipeline. And after every nightly run, on the real ones. Add a target for time, too. A service level objective, an SLO: say, ninety-nine point nine percent of renewals due today, attempted by six A.M. Now an agent can run all of it, without asking anyone what good looks like.

### Watch every run

The checks say that something is wrong. The record says why. So every step of every run leaves a line, in a shape that people and agents can both read. Here's the double charge. Attempt one: a timeout. Attempt two, with a new key: charged. Then reconcile, against the processor's own report: two charges. The first attempt had gone through. Nobody has to guess.

### Feed it back

First, put last night right, with a person approving, as in lesson five. Then close the loop. Every miss goes back into the brief, and the checks. The double charge becomes a new line in the brief: a retry must reuse the same key. That's an idempotency key; more in lesson eight. And a new test: the processor times out. So each run makes the next one better.

And be honest about the limit. A check only catches what somebody thought to ask. So a person still reads a sample of real invoices. And whatever they find becomes the next check.

### Recap

So, to recap. Green doesn't mean right. Define right first, in the business's words. Check before you ship, and after every run. Make every step leave a record. And feed every miss back in.

### The rule

Which gives us rule six, for your agents. Before you build, write down what right means, as checks you can run, in the business's words. Run them before a change ships, and after every run. Leave a record at every step. When a check fails, stop and tell a person. And feed every miss back into the brief and the checks.

### Your turn

Now, your turn. Pick one job your system runs every day. Ask your AI: what would have to be true for last night's run to be right? Write it as three read-only checks I can run on the real data. Then run one.

Once a job has a brief, its checks, and a record of every run, it's ready to be reused. That's next: skills as building blocks. See you in lesson seven.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (available)
- Lesson 10: [Capstone: One Feature, End to End](https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

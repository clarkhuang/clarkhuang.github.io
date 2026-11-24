# Parallel Agents, One Integration

_Software Engineering 201 · Lesson 4_

HTML page: https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md (plus https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-04-parallel-agents-one-integration.mp4
- Duration: 3:42 (222.5 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-04-parallel-agents-one-integration.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-04-parallel-agents-one-integration.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-04

## Chapters

- [0:00] The question
- [0:26] What goes wrong
- [0:49] Plan the integration first
- [1:51] A worked example
- [2:36] The honest math
- [2:54] Recap
- [3:05] The rule
- [3:23] Your turn

## The lesson

Three agents can each pass their own check while the system is still broken, because no check has seen the parts together. Parallel work is only fast if it comes back together cleanly, so plan the integration first: a shared contract written before the work starts, one merge point used early, and tests on the whole system. The worked example is Software Engineering 101, lessons 3 to 5: built at the same time, then brought together through one shared script format, one content file, and one generator, and shipped in one change. Today the same path adds a whole-site check and a pull request to staging that a person approves.

## The rule

Before you run agents in parallel, plan how the work comes back together. Write the shared contract first: the interfaces, the formats, the names, and who owns which files; when it has to change, change it in one place. Give each agent its own brief, its own finish line, and its own check, and make matching the contract part of that check. Merge early, in one place, and test the whole system, not just each part. If two parts keep needing each other's answers, they are not parallel work: go back to the graph.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. Lesson four. Parallel agents, one integration.

### The question

Quick question. Three agents each build one part of a system. All three say, done. All three pass their own checks. Is the system done? Yes? Almost? Or does nobody know yet? Nobody knows yet. Each check proves one part works alone. Not one of them has seen the parts together.

### What goes wrong

Picture a team that splits one feature across three agents. One builds the screen. One builds the service behind it. One changes the database. Each part gets finished, and each part is correct on its own. Then the parts meet. The screen asks for a field the service never sends. Two of the agents edited the same file. And nobody finds out until the very end, when it costs the most to fix.

### Plan the integration first

Parallel work is only fast if it comes back together cleanly. So plan the integration first. Before any agent starts.

Three things. First, a shared contract. Write down what crosses between the parts: the interfaces, the formats, the names, and who owns which files. At enterprise scale, that's an API, or a schema. It can be one page. But it has to exist before the work starts. And when it has to change, change it in one place, where every agent sees it.

Then every agent gets its own brief, its own finish line, and its own check. And part of that check is: does it match the contract?

Second, one merge point. One place where the parts come together. So when something doesn't fit, there's exactly one place to look. And use it early. Join rough versions of the parts on day one. Don't let the first meeting be the last step.

Third, test the whole system. Not just each part. The assembled thing, running as one. That's the check no single agent could run alone.

### A worked example

Here's a real one. Lessons three, four and five of software engineering 101 were built at the same time. Three scripts, three renders, running side by side. The three finished videos landed within forty seconds of each other.

And they came back together in one place. The contract already existed: the same script format the first two lessons used, and the same page fields. One merge point: one content file, read by one generator that builds every page. And they shipped together, in one change. Today that path has two more gates. One check that walks the whole site: every link, and every file a page points to. And a pull request to staging, for me to approve. This lesson and the one before it were drafted in parallel, too.

### The honest math

Parallel isn't free. You pay for it at the merge. With the integration planned first, three agents finish sooner than one working down a list. Without a plan, the time you saved comes back as rework. And if two parts keep needing each other's answers, they aren't parallel work. Go back to the graph.

### Recap

So, to recap. Split only where nothing crosses. Agree the contract before anyone starts. Merge early, in one place. And test the whole, not just the parts.

### The rule

Which gives us rule four, for your agents. Before you run agents in parallel, plan how the work comes back together. Write the shared contract first. Give each agent its own brief, its own finish line, and its own check. Merge early, in one place. And test the whole system, not just each part.

### Your turn

Now, your turn. Think of the last time work was split, across agents, or across people. Where did the parts first meet? And who checked the whole thing?

At that merge point, someone still has to say yes. That's next. Governance: where people decide. See you in lesson five.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (available)
- Lesson 10: [Capstone: One Feature, End to End](https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

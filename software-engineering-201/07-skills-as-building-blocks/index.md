# Skills as Building Blocks

_Software Engineering 201 · Lesson 7_

HTML page: https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md (plus https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-07-skills-as-building-blocks.mp4
- Duration: 4:00 (240.7 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-07-skills-as-building-blocks.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-07-skills-as-building-blocks.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-07

## Chapters

- [0:00] One job, three results
- [0:34] A new unit of reuse
- [0:54] Anatomy of a skill
- [1:56] Is this just a runbook?
- [2:18] Treat it like code
- [2:33] Fix it in one place
- [2:54] When to write one
- [3:09] Recap
- [3:20] The rule
- [3:37] Your turn

## The lesson

Three capable agents can do the same job three different ways when nobody wrote down how. Software has had several units of reuse: libraries, frameworks, then services behind an API. A skill reuses something different: how a job gets done. The worked example is a made-up subscription-billing system and the job of adding a plan or a price: the skill is one page saying when to use it, the inputs, the steps, the checks, and the traps. It is a runbook; what has changed is the reader, an agent that reads it on every run and guesses wherever the page is silent. So keep it in the repository, test it with a fresh agent, and when a run goes wrong, fix the skill so every later run gets the fix.

## The rule

When a job comes back a third time, write it as a skill: when to use it, inputs, steps, checks, and traps. Keep it in the repo, and test it with a fresh agent. When a run goes wrong, fix the skill, not just the run. In full: write it sooner if a mistake costs money. If an input is missing, ask instead of guessing, and if a check fails, stop and say so. Make any step that needs no judgment a script the skill calls. Keep the skill versioned and reviewed like code, and test it by handing it to a fresh agent that has never seen the job.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 201. Lesson seven. Skills as building blocks.

### One job, three results

Why would three capable agents do the same job three different ways? Take our made-up subscription-billing system. Now and then, someone asks for a new plan, or a new price. The first time, an agent works out the four steps, and gets it right. The second time, a different agent starts from zero, and skips the tax setup. The third time, another one edits the old price in place, and every existing subscriber is on the new price. Same job. Three results. Nobody wrote down how.

### A new unit of reuse

Software keeps finding new units of reuse. Libraries: shared code. Frameworks: an application's structure. Services: something running, behind an API. All three reuse software. A skill reuses something different: how a job gets done. One recurring job, written down, tested, and shared.

### Anatomy of a skill

Several agent tools now share a format for this: a folder, with an instruction file. It starts with when to use it: someone asks for a new plan, or a new price. That line is how an agent finds the skill. Then the inputs: name, price, billing period, start date. If one is missing, the agent asks. It doesn't guess.

Then the steps, in order. Add the plan, with its price as a new version. Set its tax category. Map it in the accounting export. Then open a pull request, because a price is money, and a person approves it.

Then the checks: how the agent knows the job worked. A test renewal on staging charges the right amount, tax included, exactly once. The ledger still adds up. And existing subscribers still renew at their old price. If one fails, the agent stops, and says so.

And the traps: what went wrong before. Never edit a price in place. Add a new version. That's the mistake from the third run, written down, so nobody repeats it.

### Is this just a runbook?

If that sounds like a runbook, it is. Engineers have written those for decades. What's changed is the reader. A person reads a runbook now and then, and fills the gaps from memory. An agent reads the skill on every run, with no memory of the last. Where the page is silent, it guesses. And when a step needs no judgment, make it a script the skill calls.

### Treat it like code

So treat a skill like code. Keep it in the repository, versioned, and reviewed when it changes. And test it. Hand it to a fresh agent that has never seen the job, and let it run on staging. If it can't finish from the page alone, the skill isn't done.

### Fix it in one place

Now run those three jobs again, from the skill. Same steps. Same checks. No guarantee: agents still vary. That's what the checks are for. And when a run goes wrong, don't just fix the run. Fix the skill. One change, in one place, and every later run gets it. That's a building block: reliable enough to build on.

### When to write one

So when is a job worth a skill? The first time? The third? Or never, because agents can work it out? A good rule of thumb: the third time. Once, you're learning. Twice, you see the pattern. The third time, write it down. Sooner, if a mistake costs money.

### Recap

So, to recap. One recurring job, written down, with its checks and its traps. In the repo, tested by a fresh agent. And when a run goes wrong, fix the skill.

### The rule

Which gives us rule seven, for your agents. When a job comes back a third time, write it as a skill: when to use it, inputs, steps, checks, and traps. Keep it in the repo, and test it with a fresh agent. And when a run goes wrong, fix the skill, not just the run.

### Your turn

Now, your turn. Pick a job you've explained to your AI more than twice. Ask it to draft the skill. Then open a fresh chat, give it only that page, and see if the job gets done.

One skill does one job. But real work is a chain of jobs, and some of it should start on its own. That's next: routines, pipelines, and integration. See you in lesson eight.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)
- Lesson 10: [Capstone: One Feature, End to End](https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

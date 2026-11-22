# Software Engineering 201: From Loop to Enterprise Systems

HTML page: https://clarkhuang.github.io/software-engineering-201/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/index.md (plus https://clarkhuang.github.io/software-engineering-201/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

101 was about one piece of work: one fix or one feature, done right with an AI loop of plan, build, and verify. 201 goes from that loop to enterprise systems: whole apps and systems, built AI-native, so agents and people can both read them, change them, and rebuild them. It starts with what AI-native building means for anything bigger than one fix. Then it climbs: decompose the system into a graph, run agents in parallel and bring the work back together, put people where the decisions matter, measure quality and watch the system run, turn repeated work into skills, and wire those skills into routines and pipelines. It ends with agents that operate enterprise systems, with real permissions, security, and an audit trail. That is the move from one loop to enterprise systems.

1 of 8 lessons available.

## Lessons

### 01. [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/01-build-the-whole-system-ai-native/index.md) (available)

What changes when you build a whole app or system with AI instead of one fix. A system is AI-native when agents and people can both read it, navigate it, contribute to it, and rebuild it. That takes four things: a Markdown twin, an index, and an AGENTS.md for every part; specs and briefs as the source; tests and checks as the contract; and staging plus a person's approval before anything reaches production. The worked example is this site, and the same four things matter even more at enterprise scale.

**Rule:** Before you build anything bigger than one fix, make it readable to agents and people: a Markdown twin for every page, an index of the whole system, and an AGENTS.md that says how to work there. Treat specs and briefs as the source and tests and checks as the contract, and send every change through staging for a person to approve before it reaches production.

### 02. [From Loop to Graph: Decompose the System](https://clarkhuang.github.io/software-engineering-201/02-from-loop-to-graph/index.md) (outline only)

An enterprise system is too big for one loop. Draw it as a graph: split the system into parts with clear boundaries and owners, then find the real dependencies. “And then” is not a dependency; if nothing crosses between two parts, they don't need to wait for each other. The graph decides which loops exist and which can run at the same time, and every part still gets its own plan, build, and verify loop. An earlier recording of this material, made when it was lesson 1, is at https://clarkhuang.github.io/videos/se201-01-from-loop-to-graph.mp4.

### 03. [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/03-parallel-agents-one-integration/index.md) (outline only)

Once the parts are independent, run agents on them at the same time, each with its own brief, its own finish line, and its own check. Parallel work is only fast if it comes back together cleanly, so plan the integration first: shared contracts and interfaces, one place where the pieces merge, and tests that run on the whole system, not just on each part.

### 04. [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/04-governance-where-people-decide/index.md) (outline only)

At enterprise scale, governance means designing where people decide. Put a person at the points where judgment, risk, money, customer data, or production are on the line, make those stops easy to review, and let everything else run without waiting. Write down who can approve what, so agents know when to stop and ask.

### 05. [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/05-quality-feedback-and-observability/index.md) (outline only)

A system you can't see is a system you can't trust. Define quality up front with tests, checks, and service levels; watch every run with logs and metrics that agents and people can both read; and feed what went wrong, what a reviewer fixed, and what it cost back into the briefs, the checks, and the plan, so each run improves the next.

### 06. [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/06-skills-as-building-blocks/index.md) (outline only)

The third time you explain the same job, write it down once: the steps, the checks, the inputs and outputs, and the traps. Skills are the reusable building blocks of an AI-native system. Version them, test them, and share them, so any person or agent across the organization can run the job the same way.

### 07. [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/07-routines-pipelines-and-integration/index.md) (outline only)

Some work should start on its own: on a schedule, when something changes, or when the last step finishes. Chain skills into routines and pipelines, connect them to the systems the business already runs on through clear interfaces, and make every step leave a record you can check and replay.

### 08. [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/08-agents-that-operate-enterprise-systems/index.md) (outline only)

The end of the path: agents that operate enterprise systems, not just build them. Give each agent a clear job, its own identity, and the least access it needs, so every action is permitted, logged, and auditable. Keep people at the decision points and keep secrets and customer data out of reach. You still own the outcome, from one loop to the whole enterprise system.

## For agents

- This series: https://clarkhuang.github.io/software-engineering-201/index.md
- This series’ agents file: https://clarkhuang.github.io/software-engineering-201/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.

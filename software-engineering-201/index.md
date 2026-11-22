# Software Engineering 201: From Loop to Enterprise Systems

HTML page: https://clarkhuang.github.io/software-engineering-201/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/index.md (plus https://clarkhuang.github.io/software-engineering-201/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

101 was about one piece of work: one fix or one feature, done right with an AI loop of plan, build, and verify. 201 goes from that loop to enterprise systems: whole apps and systems, built AI-native, so agents and people can both read them, change them, and rebuild them. It starts with what AI-native building means for anything bigger than one fix. Then it climbs: decompose the system into a graph, run agents in parallel and bring the work back together, put people where the decisions matter, measure quality and watch the system run, turn repeated work into skills, and wire those skills into routines and pipelines. It ends with agents that operate enterprise systems, with real permissions, security, and an audit trail. That is the move from one loop to enterprise systems.

3 of 8 lessons available.

## Lessons

### 01. [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/01-build-the-whole-system-ai-native/index.md) (available)

The first step from one loop to enterprise systems: what changes when you build a whole app or system with AI instead of one fix. A system is AI-native when agents and people can both read it, navigate it, contribute to it, and rebuild it. That takes four things: a Markdown twin, an index, and an AGENTS.md for every part; specs and briefs as the source; tests and checks as the contract; and staging plus a person's approval before anything reaches production. The worked example is this site, and the same four things matter even more at enterprise scale.

**Rule:** Before you build anything bigger than one fix, make it readable to agents and people: a Markdown twin for every page, an index of the whole system, and an AGENTS.md that says how to work there. Treat specs and briefs as the source and tests and checks as the contract, and send every change through staging for a person to approve before it reaches production.

### 02. [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/index.md) (available)

An enterprise system is too big for one loop, so draw it as a graph. A numbered plan only shows the order someone wrote the steps in; the test for any two steps is what crosses between them, and “and then” is not a dependency. The worked example is this site: four parts that share one generator, and one lesson's build, a strict chain that forks after the render. The graph decides which loops exist and which can run at the same time, and every part still gets its own plan, build, and verify loop. An earlier recording of this material, made when it was lesson 1, is at https://clarkhuang.github.io/videos/se201-01-from-loop-to-graph.mp4.

**Rule:** Before any job with more than one part, draw the graph. Name the parts, and give each one a boundary and an owner. Draw an arrow only where something crosses from one part to another; “and then” is not a dependency. Anything two parts share becomes its own node, with one owner. Run the parts with no arrow between them at the same time, and give every part its own plan, build, and verify loop, with its own finish line and its own check.

### 03. [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/03-parallel-agents-one-integration/index.md) (available)

Three agents can each pass their own check while the system is still broken, because no check has seen the parts together. Parallel work is only fast if it comes back together cleanly, so plan the integration first: a shared contract written before the work starts, one merge point used early, and tests on the whole system. The worked example is Software Engineering 101, lessons 3 to 5: built at the same time, then brought together through one shared script format, one content file, and one generator, and shipped in one change. Today the same path adds a whole-site check and a pull request to staging that a person approves.

**Rule:** Before you run agents in parallel, plan how the work comes back together. Write the shared contract first: the interfaces, the formats, the names, and who owns which files; when it has to change, change it in one place. Give each agent its own brief, its own finish line, and its own check, and make matching the contract part of that check. Merge early, in one place, and test the whole system, not just each part. If two parts keep needing each other's answers, they are not parallel work: go back to the graph.

### 04. [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/04-governance-where-people-decide/index.md) (outline only)

At enterprise scale, governance means designing where people decide. Put a person at the points where judgment, risk, money, customer data, or production are on the line, make those stops easy to review, and let everything else run without waiting. Write down who can approve what, so agents know when to stop and ask.

### 05. [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/05-quality-feedback-and-observability/index.md) (outline only)

A system you can't see is a system you can't trust. Define quality up front with tests, checks, and service levels; watch every run with logs and metrics that agents and people can both read; and feed what went wrong, what a reviewer fixed, and what it cost back into the briefs, the checks, and the plan, so each run improves the next.

### 06. [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/06-skills-as-building-blocks/index.md) (outline only)

At enterprise scale, the same jobs come up again and again. The third time you explain one, write it down once: the steps, the checks, the inputs and outputs, and the traps. Skills are the reusable building blocks of an AI-native system. Version them, test them, and share them, so any person or agent across the organization can run the job the same way.

### 07. [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/07-routines-pipelines-and-integration/index.md) (outline only)

A skill still waits for someone to start it. Some work should start on its own: on a schedule, when something changes, or when the last step finishes. Chain skills into routines and pipelines, connect them to the systems the business already runs on through clear interfaces, and make every step leave a record you can check and replay.

### 08. [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/08-agents-that-operate-enterprise-systems/index.md) (outline only)

The end of the path: agents that operate enterprise systems, not just build them. Give each agent a clear job, its own identity, and the least access it needs, so every action is permitted, logged, and auditable. Keep people at the decision points and keep secrets and customer data out of reach. You still own the outcome, from one loop to the whole enterprise system.

## For agents

- This series: https://clarkhuang.github.io/software-engineering-201/index.md
- This series’ agents file: https://clarkhuang.github.io/software-engineering-201/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.

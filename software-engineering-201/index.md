# Software Engineering 201: From Loop to Enterprise Systems

HTML page: https://clarkhuang.github.io/software-engineering-201/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/index.md (plus https://clarkhuang.github.io/software-engineering-201/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

101 was about one piece of work: one fix or one feature, done right with an AI loop of plan, build, and verify. 201 is about whole systems: how you design one, how the parts fit together, and how that has changed from thirty, twenty and ten years ago to now, with agents doing much of the building. It starts with the four eras of building systems, and what never changed. Then it builds the whole system AI-native, so agents and people can both read it, change it, and rebuild it. Then it climbs: decompose the system into a graph, run agents in parallel and bring the work back together, put people where the decisions matter, design quality in and watch every run, turn repeated work into skills, and wire those skills into routines and pipelines. It ends with agents that operate enterprise systems, with real permissions, security, and an audit trail. That is the move from one loop to enterprise systems.

4 of 9 lessons available.

## Lessons

### 01. [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)

How we build big systems has changed from thirty, twenty and ten years ago to now, with agents doing much of the building. One useful lens is that architecture bends around whatever is scarcest. Machines were scarce in the mid-1990s, coordination in the 2000s, and seeing the whole system in the 2010s. Now the scarce things are knowing the work is right and how much of the system an agent can see at once. So design for checking: clear module boundaries, one repository an agent can read, tests and specs it can run, and decisions written down. This is where the thinking is heading, not a settled answer. Four things never changed: the data model outlives the code, money has to add up, you depend on things you don't control, and someone has to understand the layer below.

**Rule:** Before you design a system, write down four things: where the boundaries are, what the data model is, what you depend on but don't control, and how you'll know it's right. Put that note in the repository, where every agent and person working on the system can read it, and keep it current as the design changes.

### 02. [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)

After the four eras, the first step from one loop to enterprise systems: what changes when you build a whole app or system with AI instead of one fix. A system is AI-native when agents and people can both read it, navigate it, contribute to it, and rebuild it. That takes four things: a Markdown twin, an index, and an AGENTS.md for every part; specs and briefs as the source; tests and checks as the contract; and staging plus a person's approval before anything reaches production. The worked example is this site, and the same four things matter even more at enterprise scale.

**Rule:** Before you build anything bigger than one fix, make it readable to agents and people: a Markdown twin for every page, an index of the whole system, and an AGENTS.md that says how to work there. Treat specs and briefs as the source and tests and checks as the contract, and send every change through staging for a person to approve before it reaches production.

### 03. [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)

An enterprise system is too big for one loop, so draw it as a graph. A numbered plan only shows the order someone wrote the steps in; the test for any two steps is what crosses between them, and “and then” is not a dependency. The worked example is this site: four parts that share one generator, and one lesson's build, a strict chain that forks after the render. The graph decides which loops exist and which can run at the same time, and every part still gets its own plan, build, and verify loop. An earlier recording of this material, made when it was lesson 1, is at https://clarkhuang.github.io/videos/se201-01-from-loop-to-graph.mp4.

**Rule:** Before any job with more than one part, draw the graph. Name the parts, and give each one a boundary and an owner. Draw an arrow only where something crosses from one part to another; “and then” is not a dependency. Anything two parts share becomes its own node, with one owner. Run the parts with no arrow between them at the same time, and give every part its own plan, build, and verify loop, with its own finish line and its own check.

### 04. [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)

Three agents can each pass their own check while the system is still broken, because no check has seen the parts together. Parallel work is only fast if it comes back together cleanly, so plan the integration first: a shared contract written before the work starts, one merge point used early, and tests on the whole system. The worked example is Software Engineering 101, lessons 3 to 5: built at the same time, then brought together through one shared script format, one content file, and one generator, and shipped in one change. Today the same path adds a whole-site check and a pull request to staging that a person approves.

**Rule:** Before you run agents in parallel, plan how the work comes back together. Write the shared contract first: the interfaces, the formats, the names, and who owns which files; when it has to change, change it in one place. Give each agent its own brief, its own finish line, and its own check, and make matching the contract part of that check. Merge early, in one place, and test the whole system, not just each part. If two parts keep needing each other's answers, they are not parallel work: go back to the graph.

### 05. [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (outline only)

Design where people decide, so agents run fast everywhere else. Every era had a place where a person said yes: a release board a few times a year, then code review, then an approval step in an automated pipeline. When agents produce changes faster than anyone can read them all, that place has to be designed, not inherited. Put a person where judgment, risk, money, customer data or production are on the line, make those stops quick to review, and let everything else run without waiting. Picture a payments system: an agent can draft a change to how a fee is calculated, but a person approves anything that changes how money moves. Write down who can approve what, so agents know when to stop and ask.

### 06. [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (outline only)

When knowing it's right is the scarce thing, design quality in and watch every run. Ten years ago the scarce thing was seeing the whole system, and logs, metrics and tracing were the answer. Now that knowing the work is right is scarce, quality has to be defined before the work starts: tests, checks, and service levels that agents can run themselves. Picture a subscription-billing system: the real check is not “the build passed” but “every renewal charged the right amount, exactly once”. Watch every run with signals that agents and people can both read, and feed what went wrong, what a reviewer fixed, and what it cost back into the briefs and checks, so each run improves the next.

### 07. [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (outline only)

Turn the jobs that keep coming back into written, tested, shared skills. Every era found its unit of reuse: shared libraries, then frameworks, then services behind an API. In a system agents help build and run, the reusable unit is also a written skill: the steps, the checks, the inputs and outputs, and the traps of a job that keeps coming up. Picture retail e-commerce: bringing on a new supplier's product data is nearly the same job every time, so write it down once, test it, and version it. Then any person or agent can run that job the same way, and improve it in one place.

### 08. [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (outline only)

Chain skills into work that starts on its own, connected to the systems the business already runs. Integration is the oldest problem in this series: thirty years ago it was overnight batch files and EDI between retailers and suppliers, then web services, then an API for everything, and all three are still running somewhere today. Some work should start on its own: on a schedule, when something changes, or when the last step finishes. Chain skills into routines and pipelines, connect them through clear interfaces, and make every step leave a record you can check and replay. And remember the constant: you depend on systems you don't control, so design every hand-off to fail safely and be retried.

### 09. [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline only)

Agents that run the system, not just build it, with identity, least access, and an audit trail. The end of the path: agents that operate enterprise systems day to day. Give each agent a clear job, its own identity, and the least access it needs, so every action is permitted, logged, and auditable. Picture a payments or investment system where an agent reconciles accounts overnight and flags anything that doesn't add up, while a person approves anything that moves money. Keep secrets and customer data out of reach, keep people at the decision points, and remember that you still own the outcome, from one loop to the whole enterprise system.

## For agents

- This series: https://clarkhuang.github.io/software-engineering-201/index.md
- This series’ agents file: https://clarkhuang.github.io/software-engineering-201/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.

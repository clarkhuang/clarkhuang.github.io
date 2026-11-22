# Software Engineering 201: From Loops to Building Systems

HTML page: https://clarkhuang.github.io/software-engineering-201/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/index.md (plus https://clarkhuang.github.io/software-engineering-201/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

101 was about one piece of work: one fix or one feature, done right with an AI loop of plan, build, and verify. 201 is about everything around that loop. Real work is never just one loop. It is many of them: split into pieces, some waiting on others, some running side by side, with a person deciding at the moments that matter, and feedback that makes each run better than the last. And once you have run the same loop a few times, you stop running it by hand. You write it down and build it into a system that keeps working: a skill, a routine, a pipeline, or an agent. That is the move from loops to building systems.

1 of 8 lessons available.

## Lessons

### 01. [From Loop to Graph](https://clarkhuang.github.io/software-engineering-201/01-from-loop-to-graph/index.md) (available)

The first step from a loop to a system: before a job with more than one part, draw the work as a graph. A loop makes one piece of work correct. The graph decides which pieces exist and which can run at the same time. Built around how three Software Engineering 101 lessons were made side by side, each with its own review.

**Rule:** Before any job with more than one part, write down the pieces, and which can run at the same time. Then run each piece as its own loop, checked on its own.

### 02. [Find the Real Dependencies](https://clarkhuang.github.io/software-engineering-201/02-find-the-real-dependencies/index.md) (outline only)

“And then” is not a dependency. If nothing crosses between two steps, they don't need to wait for each other. Find what really has to come first, and everything else can start now.

### 03. [Run Loops in Parallel](https://clarkhuang.github.io/software-engineering-201/03-run-loops-in-parallel/index.md) (outline only)

Once the pieces are independent, run them at the same time, each as its own loop with its own check. Give every run a clear brief and a clear finish line, and plan the moment the pieces come back together.

### 04. [Where a Person Decides](https://clarkhuang.github.io/software-engineering-201/04-where-a-person-decides/index.md) (outline only)

A system still needs people, just not everywhere. Put a person at the few points where judgment, risk, or taste matter, make those stops easy to review, and let the rest run without waiting.

### 05. [Feedback That Improves Every Run](https://clarkhuang.github.io/software-engineering-201/05-feedback-that-improves-every-run/index.md) (outline only)

A system gets better only if each run teaches the next one. Keep what went wrong, what a reviewer fixed, and what it cost, and feed it back into the brief, the checks, and the plan.

### 06. [Turn a Repeated Loop into a Skill](https://clarkhuang.github.io/software-engineering-201/06-turn-a-loop-into-a-skill/index.md) (outline only)

The third time you explain the same job, write it down once: the steps, the checks, and the traps. A good skill lets any person or agent run the loop the same way, without starting from scratch.

### 07. [Routines and Pipelines](https://clarkhuang.github.io/software-engineering-201/07-routines-and-pipelines/index.md) (outline only)

Some work should start on its own: on a schedule, when something changes, or when the last step finishes. Chain skills into routines and pipelines, and make every step leave a record you can check.

### 08. [Agents That Run the System](https://clarkhuang.github.io/software-engineering-201/08-agents-that-run-the-system/index.md) (outline only)

The last step is handing a whole system to an agent: the graph, the skills, the routines, and the points where a person decides. Give it a clear job, clear limits, and a way to show its work, and you own the outcome.

## For agents

- This series: https://clarkhuang.github.io/software-engineering-201/index.md
- This series’ agents file: https://clarkhuang.github.io/software-engineering-201/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.

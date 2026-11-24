# Software Engineering 101

HTML page: https://clarkhuang.github.io/software-engineering-101/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/index.md (plus https://clarkhuang.github.io/software-engineering-101/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

Ten short lessons on building software when AI agents do much of the building. Each lesson ends with one rule, written so your agents can follow it too.

10 of 10 lessons available.

## Lessons

### 01. [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)

How do you fix code you don't understand when you only get one shot? Split the work into four roles: a person who owns the problem, a planner, a builder, and a verifier on a different model that can only read and report. Loop until the verifier runs out of serious things to say. Then: what that costs, and when a lighter path is good enough.

Published: Nov 21, 2026. Updated: Nov 22, 2026

**Rule:** If a change can't be rolled back, and the person asking can't check it themselves, it gets an independent review, on a different model, before it ships. That's the floor. The longer list, of when to use the full pattern, is judgment.

### 02. [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)

A patch in ten minutes or the root cause in two days? Redeploy speed is only half the question: a redeploy fixes the code, but it doesn't undo what the code did. Product shape is uncertain and easy to change, so ship it rough behind a flag. Correctness you can't undo, meaning money, customer data, and messages, gets the root cause.

Published: Nov 21, 2026. Updated: Nov 22, 2026

**Rule:** Rough is fine for product shape. It is never fine for money, customer data, or anything that can't be undone. If a piece of work is both, the stricter standard wins. For that kind of work: stop any live damage first, then find the root cause, and give the estimate in usage, not in days.

### 03. [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)

Why a computer science education built on ideas, not languages, still pays off, and why it matters more now that agents write the syntax.

Published: Nov 21, 2026

**Rule:** When you make a design choice, explain the principle behind it, in plain words. Not just the framework feature you used.

### 04. [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)

AI coding is one more rung on a ladder that runs from logic gates up. Stay at the top, and know when to send your agent down a rung.

Published: Nov 21, 2026

**Rule:** Break a task into small pieces that each do one thing. And when something on one layer doesn't add up, look at the layer below, before you change anything.

### 05. [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)

A perfect fix for the wrong problem is still wrong. Own the problem, restate it, reproduce and trace it, then fix the cause.

Published: Nov 21, 2026

**Rule:** Before planning, restate the problem in plain words, and confirm it with the person who gave you the task. They own the problem. Before fixing, reproduce it if you can, and trace what actually happens. Then fix the cause, not the symptom.

### 06. [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)

Like a database optimizer, an agent does its best work when you state the outcome and the limits, not the steps. Too tight and too loose both cost you.

Published: Nov 21, 2026

**Rule:** A spec states the outcome, and what must not break. It doesn't dictate steps, unless a step is itself a requirement. And before you start the work, give a cost forecast.

### 07. [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)

Pair programming, test-first and code review still work with agents in the seats. Cheaper tests change the trade, and three anti-patterns to watch for.

Published: Nov 21, 2026

**Rule:** Write the failing test before the fix. No bug fix merges without a test that would have caught the bug. And the agent that wrote the code never approves it.

### 08. [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)

Keep every scrum ceremony, but run the loop daily. Deploy continuously, ship features switched off behind a flag, and write down what you learned.

Published: Nov 21, 2026

**Rule:** Ship small changes continuously, once the automated checks pass. New features ship switched off, behind a flag. A person decides when each one turns on, for one client or a small group first. And end every session with a short written note on what was learned.

### 09. [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)

AI usage is the new currency of software. See the spend, the limit and a priced forecast before you start, and remember that owning software costs more than building it.

Published: Nov 21, 2026

**Rule:** Before any sizable task, show the spend so far, the limit, and a forecast for each path. If you can't see a number, say so, and label an estimate as an estimate. Afterward, record what it actually cost. And before you build something new, check what already exists.

### 10. [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

Be uncompromising about customer personal data and card data, pragmatic about where internal apps live, and see the whole series on one screen.

Published: Nov 21, 2026. Updated: Nov 23, 2026

**Rule:** Never store, log, or send raw card data. Customer personal data stays out of logs, errors, test data, and your own working notes. Internal apps sit behind company sign-in, on every route. And any change that touches personal data or payments gets an independent review.

## For agents

- This series: https://clarkhuang.github.io/software-engineering-101/index.md
- This series’ agents file: https://clarkhuang.github.io/software-engineering-101/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.

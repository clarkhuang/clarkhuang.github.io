# Capstone: One Feature, End to End

_Software Engineering 201 · Lesson 10_

HTML page: https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/index.md (plus https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-10-capstone-one-feature-end-to-end.mp4
- Duration: 5:09 (309.2 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-10-capstone-one-feature-end-to-end.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-10-capstone-one-feature-end-to-end.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-10

## Chapters

- [0:00] The question
- [0:29] One small feature
- [0:40] Plan it
- [2:35] Build it
- [2:54] Run it
- [3:19] Operate it
- [3:47] What still holds
- [4:07] Recap
- [4:22] The rule
- [4:41] Your turn

## The lesson

The capstone builds one small feature of a made-up subscription-billing system end to end, using every lesson in the series in order: a customer on a $30 monthly plan switches to a $300 annual plan ten days into the month. What to charge depends on a rule nobody has written down, so the plan comes first: say what right means and let a person set the rule; put it in a spec in the repository; draw the graph and find the one new thing that crosses, the quote; make the quote's format the shared contract for three agents and one merge point; name who decides; turn "right" into three checks that run before the change ships and every night after; and notice that adding a plan is already a skill. Then the plan is carried out: the parts are built at the same time, the finance owner says yes, the feature runs as a pipeline with an idempotency key on the charge, and an agent with its own identity and read-only access works the nightly reconcile, flags a double charge for a person to refund, and the miss becomes a fourth check. Under all of it, the four constants from lesson 1 still hold.

## The rule

Before you build a feature with more than one part, write the plan in the repository, show it to a person, and wait for a yes. The plan says: what right means, as checks you can run before the change ships and after every run; the graph of the parts, the contract they share, and the one place they merge; who decides, by name or role, and what you will bring them; which parts are already a skill; and what will run on its own, what starts it, what happens when a step fails or runs twice, and under whose identity and access it runs. If you cannot fill in a line, do not guess: stop, and ask.

This rule is written so an AI agent can follow it as a standing instruction.

## What the video simplifies

- The numbers are made up and leave tax out. In the spec on screen the quote is "new price - credit, plus tax", and check 2 compares each quote with the rule and each charge with its quote, so the checks still hold once tax is added.
- The rule shown (credit the days paid for and not used) is one policy among several. Others charge the full price, or switch at the next renewal. The lesson's point is that a person has to pick one and write it down.
- A declined charge leaves the subscription on the monthly plan; the plan switches only after the charge succeeds.
- An idempotency key only helps if the payment processor supports one; many do, and they keep keys for a limited time. Lesson 8 covers this.
- The double charge in the lesson gets past the key because two browser tabs produced two quotes, and so two keys. The fix is the fourth check, one open quote per subscription. A key built as in lesson 8 (this subscription, this billing period) would also have stopped it.
- Most pipeline steps are plain code, as lesson 8 says. The agent earns its place at the nightly reconcile, where working out why something doesn't match takes judgment.
- Lesson 9 is an outline, not a video. The capstone uses its ideas: an agent's own identity, the least access the job needs, a log of every action, and a person at any decision that moves money.

## Transcript

Software engineering 201. Lesson ten. Capstone: one feature, end to end.

### The question

Picture a made-up billing system. A customer pays thirty dollars a month. Ten days in, they click: switch to annual. Three hundred a year. What do you charge them, today? Three hundred? Two eighty? Or: it depends? It depends. On a rule nobody has written down. And an agent will build either answer, without asking.

### One small feature

So this last lesson builds that one feature, end to end, in our made-up subscription-billing system from lesson one. Here's the map we'll fill in. Each number is the lesson it comes from.

### Plan it

What's scarce, lesson one said, is knowing it's right. So, say what right means: every upgrade is charged the right amount, exactly once. The amount is a person's call, so the agent asks. The finance owner's rule: credit the days paid for, and not used. Twenty days, twenty dollars. So, before tax, charge two eighty.

Now make it readable. The rule goes into a spec, in the repository, with an agents file, for how to work there, and an index, so an agent can find it. The spec is the source. Change it, and the build follows.

Next, the graph. Four parts. Add the annual plan. Calculate the credit. Show the amount, and get a yes. Charge it, and switch the plan. What crosses? One new thing: the quote. Its ID, old plan, new plan, credit, amount due. Three parts share it, so it's its own node, with one owner.

Then plan the integration, before anyone starts. The quote's format is the shared contract. Three parts are new work: three agents, each with its own brief, finish line, and check. And one merge point, on staging, where the whole feature is tested.

Who decides? It moves money, so a person does. The repository already says who: fees and prices, the finance owner. The agent that writes the change doesn't classify it, or approve it. It brings the change, the evidence, the risk, and the way back.

Now turn right into checks an agent can run. No upgrade is charged twice. Each quote follows the rule, and each charge equals its quote. And the old monthly plan doesn't renew again. Write them once, run them twice: before it ships, on sample upgrades. And every night after, on the real ones.

One part isn't new. Adding a plan has come back often enough to be a skill: written down, and tested. So that part needs no new brief. An agent runs the skill.

### Build it

The plan is written, and a person has read it. Now, build. Four parts, at the same time. They meet early, at the merge point, and the whole feature runs on staging. The three checks pass, on sample upgrades. An engineer reviews the code. The finance owner says yes. And it ships.

### Run it

Now it runs on its own: a pipeline. The trigger is an event: the customer confirms the quote. Charge, switch the plan, invoice and ledger, email. Every step leaves a record. And the charge carries an idempotency key that never changes: this quote's ID. So a double-click, or a retry, doesn't charge twice. A second trigger, every night: reconcile our ledger against the processor's record, and run the three checks.

### Operate it

Lesson nine's question: who operates it? An agent works that nightly reconcile. It gets its own identity, and the least access the job needs: it reads the ledger, and the processor's report. It can't move money, or change the ledger. Every action is logged. One night, an upgrade shows two charges: two browser tabs, two quotes, two keys. The agent flags it. A person refunds it. And the miss becomes a fourth check: one open quote per subscription.

### What still holds

Under all of it, the four constants from lesson one. The data model outlives the code: the plan, and the quote. Money has to add up: the invoice, the ledger, and the processor all say two eighty. You depend on things you don't control: the processor. And somebody understands the layer below: someone who can work that credit out by hand.

### Recap

So that's the series, in one feature. Say what right means. Write it down. Draw the graph. Merge in one place. Put a person where it matters. Check it. Reuse what recurs. Let it run. And know who's running it.

### The rule

Which gives us rule ten, for your agents. Before you build a whole feature, write the plan in the repo, and show a person. What right means, as checks. The graph, and the shared contract. Who decides. What's already a skill. What runs on its own, and under whose identity. A blank line? Stop, and ask.

### Your turn

Now, your turn. Pick one small feature in a system you work on. Before any code, ask your AI to write that plan. Then find the line it guessed, when it should have asked.

Every box on that map is still one loop: plan, build, verify. Agents do more of the building now. You still own the outcome. That's software engineering 201: from one loop, to enterprise systems. Thanks for watching.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Decompose the System into a Graph](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (available)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (available)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (available)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (available)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

# Rigor Follows Risk

_Software Engineering 101 · Lesson 2_

HTML page: https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md (plus https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-02-rigor-follows-risk.mp4
- Duration: 3:28 (208.3 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se101-02-rigor-follows-risk.jpg

## Chapters

- [0:00] The choice
- [0:17] Half the question
- [0:49] Two kinds of work
- [1:24] Ship it rough
- [1:39] Get it right
- [2:21] The sort
- [2:52] The rule
- [3:15] Your turn

## The lesson

A patch in ten minutes or the root cause in two days? Redeploy speed is only half the question: a redeploy fixes the code, but it doesn't undo what the code did. Product shape is uncertain and easy to change, so ship it rough behind a flag. Correctness you can't undo, meaning money, customer data, and messages, gets the root cause.

## The rule

Rough is fine for product shape. It is never fine for money, customer data, or anything that can't be undone. If a piece of work is both, the stricter standard wins. For that kind of work: stop any live damage first, then find the root cause, and give the estimate in usage, not in days.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering one oh one. Lesson two. Rigor follows risk.

### The choice

Picture this. Something's broken, and your agent offers you a choice. I can patch this in ten minutes. Or find the root cause, in two days. Which one do you pick?

### Half the question

It depends. But on what? Most of us ask: how fast can I redeploy? If it's minutes, a patch feels safe.

Here's the catch. Say a bad fix is live for ten minutes, then I ship a good one. The code is fixed. But a customer charged twice is still charged twice. A sent message is still sent. Bad data is still sitting there.

So redeploy speed is only half the question. The other half: what does a wrong answer damage, before anyone notices?

### Two kinds of work

So I sort work into two kinds. Kind one: product shape. Features, screens, wording, what's in and what's out. Uncertain, because you don't know what people want until they use it. And easy to change.

Kind two: correctness you can't undo. Money. Customer data. Messages to customers. And releases you can't roll back, like the mobile app in lesson one.

Mix them up, and it costs you both ways. Too careful with product shape, and you polish something nobody wanted. Too rough with money or data, and a fast fix leaves real damage behind.

### Ship it rough

For product shape, ship it rough. But not reckless. Put it behind a feature flag. One client. One small group. Watch. Then everyone. I'd rather a real user sees it half finished and early, than polished and late.

### Get it right

For kind two, I go the other way. I want the root cause, not the patch. A patch hides the symptom, and the cause can keep doing damage where you can't see it.

Here's what changed. Two days is an old estimate, from when a person did the digging. In my experience, it's a few hours of agent time, plus some A.I. usage. It isn't free. So ask for the estimate in usage, not days.

Back to the choice. A display glitch on an internal dashboard? Take the patch. A service that handles money, customer messages, or customer data? Root cause. And if the damage is happening right now, stop it first. The patch buys you time. Then find the root cause.

### The sort

Here's the sort. Ship it rough when it's easy to change once someone sees it. A new dashboard layout. Wording on a page. A prototype for one team.

Get it right when a wrong answer does lasting damage. A refund or a charge. An email to every subscriber. A change to stored customer data. A mobile release.

Most real projects have both. A new checkout page is product shape outside, and money inside. Rough with the look, exact with the charge. Can't split them? The stricter standard wins.

### The rule

Rule two, for your agents. Rough is fine for product shape. It is never fine for money, customer data, or anything that can't be undone. If a piece of work is both, the stricter standard wins. And for that kind of work: stop any live damage first, then find the root cause, and give the estimate in usage, not in days.

### Your turn

Your turn. Pick one thing on your plate this week, and sort it. Product shape, or can't undo? Can't tell? The stricter standard wins.

See you in lesson three.

## Related lessons

- Lesson 1: [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 4: [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)
- Lesson 5: [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)
- Lesson 6: [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)
- Lesson 7: [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)
- Lesson 10: [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

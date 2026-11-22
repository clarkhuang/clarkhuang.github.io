# Old Patterns, New Clothes

_Software Engineering 101 · Lesson 7_

HTML page: https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md (plus https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-07-old-patterns-new-clothes.mp4
- Duration: 2:19 (139.3 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se101-07-old-patterns-new-clothes.jpg

## Chapters

- [0:00] Nothing new
- [0:58] I changed my mind
- [1:24] Anti-patterns
- [1:58] The rule
- [2:10] Your turn

## The lesson

Pair programming, test-first and code review still work with agents in the seats. Cheaper tests change the trade, and three anti-patterns to watch for.

## The rule

Write the failing test before the fix. No bug fix merges without a test that would have caught the bug. And the agent that wrote the code never approves it.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering one oh one. Lesson seven. Old patterns, new clothes.

### Nothing new

Here's some good news, if you've been doing this a while. The new way of working with A.I. agents? You've done it before. You just did it with people.

Pair programming. One person drives and writes the code. The other navigates. Watches. Questions. Catches the mistake before it lands. In lesson one, one agent built the fix, and a second agent checked every round of it. Same idea. Nobody works alone.

Test driven development. Write the test first. Watch it fail. Then write just enough code to make it pass. With an agent, that test is the spec. Here's what passing looks like. Go. And the reviewer checks the tests too, so nobody bends a test to fit the code.

And code review. A second pair of eyes. With agents, the key word is different. A different model, with different blind spots.

### I changed my mind

Now, a confession. I used to be a pragmatist about unit tests. I've changed my tune. With agents, a test costs very little to write. It still has to be maintained. But now it just makes sense to have more tests than fewer.

And that's the bigger lesson. A practice is a trade. When the price changes, you're allowed to change your answer. So ask yourself. What else have you skipped, because it used to be too expensive?

### Anti-patterns

Now the flip side. Quick question. Which of these is the anti-pattern? The agent that wrote the code approves it? A different model reviews it? Or the tests run before the review? The first one. That's grading your own exam.

At Berkeley, we had whole courses on design patterns, and on their twin. Anti-patterns. Things that look fine, and go wrong. With agents, three to watch for. The author approves its own work. The reviewer reads the summary, not the code. And the loop that never ends, because nobody set a cap.

### The rule

Rule seven, for your agents. Write the failing test before the fix. No bug fix merges without a test that would have caught the bug. And the agent that wrote the code never approves it.

### Your turn

Your turn. Name one practice you skipped because it was too expensive. Is it still?

See you in lesson eight.

## Related lessons

- Lesson 1: [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)
- Lesson 2: [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 4: [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)
- Lesson 5: [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)
- Lesson 6: [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)
- Lesson 10: [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

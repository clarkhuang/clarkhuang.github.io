# Plan, Build, Verify (and When to Skip It)

_Software Engineering 101 · Lesson 1_

HTML page: https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md (plus https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-01-plan-build-verify.mp4
- Duration: 3:35 (215.9 seconds)
- Published: Nov 21, 2026. Updated: Nov 22, 2026
- Poster: https://clarkhuang.github.io/videos/posters/se101-01-plan-build-verify.jpg

## Chapters

- [0:00] One shot
- [0:28] Why this one
- [0:57] Four roles
- [1:34] The loop
- [2:18] The cost
- [2:32] When to use it
- [3:05] The rule
- [3:23] Your turn

## The lesson

How do you fix code you don't understand when you only get one shot? Split the work into four roles: a person who owns the problem, a planner, a builder, and a verifier on a different model that can only read and report. Loop until the verifier runs out of serious things to say. Then: what that costs, and when a lighter path is good enough.

## The rule

If a change can't be rolled back, and the person asking can't check it themselves, it gets an independent review, on a different model, before it ships. That's the floor. The longer list, of when to use the full pattern, is judgment.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering one oh one. Lesson one. Plan, build, verify. And when to skip it.

### One shot

Friday afternoon. A hard deadline, one week out. A mobile app has a push notification problem, and I've decided to fix it myself.

One small issue. I have never built a mobile app. More than thirty years of building software, and I'd never seen this code. So how do you fix code you don't understand, in one shot?

### Why this one

Three things made this one different. First, you can't just roll it back. A web fix gets replaced in minutes. A mobile fix waits on store review, and then on every customer to update.

Second, one week. Little room for a second try. And third, the honest one: I couldn't read this code and tell you if it was right.

The tempting instinct: I don't know this, so I'll trust the A.I. I went the other way. I don't know this, so I need more checking. Not less.

### Four roles

So I split the work into four roles. The first is mine, and I don't hand it off. Not the code. The problem. What does fixed look like, to the person who reported it?

Then three agents. A planner writes the spec, with acceptance criteria, and a list of things we must not break. A builder writes the code, and the tests.

And a verifier, on a different model, with different blind spots. It reads the real code, says what's wrong, and changes nothing.

Then they loop. Build, verify, fix, verify again, until the verifier runs out of serious things to say.

### The loop

Round one: real problems in both changes, and one change blocked outright. Round two: fixed, and a new problem. Round three: from a cold start, one tap could still open the same screen twice.

Round four. The fix for round three created two new problems. A fix is new code, and new code can be wrong. So in this loop, every fix gets checked.

Round five. Clean. About seventy minutes, start to finish. Passing tests: thirty-five to forty-one on one change, fifty-nine to sixty-five on the other.

Clean means the verifier found nothing serious in the code. A person still tests it on a real iPhone and a real Android phone before it ships.

### The cost

So, run this on everything? No. A plan, a build, and five full reviews cost several times a quick fix, and some of that is A.I. usage now. So know what you're spending, and spend it on purpose.

### When to use it

Use the full pattern when a mistake is hard to undo. Money, checkout, customer data. A mobile release. Anything that crosses several systems, already failed once, or nobody fully understands.

Everywhere else, be pragmatic. Wording and styling. A config change. An internal tool. A prototype. One plan, one build, tests, one review. Good enough is good enough.

And in between, a middle path. One independent review, on a different model. Loop only if it finds something serious.

### The rule

Rule one, for your agents. If a change can't be rolled back, and the person asking can't check it themselves, it gets an independent review, on a different model, before it ships. That's the floor. The longer list, of when to use the full pattern, is judgment.

### Your turn

Your turn. One change from this month that deserved this pattern. And one where it would have been overkill. Knowing the difference? That's the skill.

See you in lesson two.

## Related lessons

- Lesson 2: [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 4: [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)
- Lesson 5: [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)
- Lesson 6: [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)
- Lesson 7: [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)
- Lesson 10: [Strict About Data, Relaxed About the Perimeter](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

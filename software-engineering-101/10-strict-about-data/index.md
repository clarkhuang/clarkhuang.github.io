# Strict About Data, Relaxed About the Perimeter

_Software Engineering 101 · Lesson 10_

HTML page: https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/index.md (plus https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se101-10-strict-about-data.mp4
- Duration: 3:15 (195.6 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se101-10-strict-about-data.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se101-10-strict-about-data.vtt

## Chapters

- [0:00] Two lines
- [0:50] The pragmatic side
- [1:24] The rule
- [1:44] The whole series
- [2:44] What’s next
- [3:04] Your turn

## The lesson

Be uncompromising about customer personal data and card data, pragmatic about where internal apps live, and see the whole series on one screen.

## The rule

Never store, log, or send raw card data. Customer personal data stays out of logs, errors, test data, and your own working notes. Internal apps sit behind company sign-in, on every route. And any change that touches personal data or payments gets an independent review.

This rule is written so an AI agent can follow it as a standing instruction.

## Transcript

Software engineering 101. Lesson ten, the last one. Strict about data. Relaxed about the perimeter.

### Two lines

Quick question. What's the safest way to protect a customer's card number? Encrypt it? Keep it on a private network? Or never hold it at all? Never hold it. You can't leak what you don't have.

On security, I'm a pragmatist about most things. But I don't bend on two. One: customer personal data doesn't get exposed. Two: payment card data stays with the payment processor.

Notice the second one isn't a better lock. It's a design decision. The processor holds the card. You hold a token. There's nothing here worth stealing.

So I'll say this plainly. Unless payments is your business, keep your card handling as small as you possibly can.

### The pragmatic side

Now the pragmatic side. I'm comfortable putting an internal app on the public internet. As long as the front door is solid. Company sign-in, on every route.

Why? Because nearly everything you use is already a service on the internet. The office network stopped being the wall a long time ago. The wall now is who you are, and what you're allowed to see.

So. Strict about the data. Strict about identity. And relaxed about where the app sits. One more thing. Any change that touches personal data or payments gets an independent review.

### The rule

Rule ten, the last one, for your agents. Never store, log, or send raw card data. Customer personal data stays out of logs, errors, test data, and your own working notes. Internal apps sit behind company sign-in, on every route. And any change that touches personal data or payments gets an independent review.

### The whole series

So here's the whole series, on one screen. One. Plan, build, verify, with an independent verifier. Two. Rigor follows risk. Three. Principles over languages. Four. Stay at the top of the ladder, and send the agent down. Five. Understand the problem before anything changes.

Six. Say what, not how. Seven. The old practices still work, with agents in the seats. Eight. Same ceremonies, faster clock. Nine. Know what it costs. And ten. Strict about data, relaxed about the perimeter.

And there's one idea underneath all ten. Every practice is a trade, and AI changed the prices. So some of my answers changed. More tests. Root cause, for anything that touches money or data. The whole sprint cycle, in a day. And some didn't. I still have to understand the problem myself. And the customer's data is still not negotiable.

### What’s next

Most of this series was about one piece of work. One fix. One feature. Getting one thing right. Software Engineering 201 is about whole systems. How you design one. How the parts fit together. And how that has changed, from thirty years ago, to now, with agents doing the building. I'll use real systems I've worked on.

### Your turn

So, one last question for you. Which of the ten rules changed how you work? And which one do you think I got wrong?

See you in 201.

## Related lessons

- Lesson 1: [Plan, Build, Verify (and When to Skip It)](https://clarkhuang.github.io/software-engineering-101/01-plan-build-verify/index.md) (available)
- Lesson 2: [Rigor Follows Risk](https://clarkhuang.github.io/software-engineering-101/02-rigor-follows-risk/index.md) (available)
- Lesson 3: [Principles Over Languages](https://clarkhuang.github.io/software-engineering-101/03-principles-over-languages/index.md) (available)
- Lesson 4: [The Abstraction Ladder](https://clarkhuang.github.io/software-engineering-101/04-abstraction-ladder/index.md) (available)
- Lesson 5: [Understand Before You Change](https://clarkhuang.github.io/software-engineering-101/05-understand-before-you-change/index.md) (available)
- Lesson 6: [Say What, Not How](https://clarkhuang.github.io/software-engineering-101/06-say-what-not-how/index.md) (available)
- Lesson 7: [Old Patterns, New Clothes](https://clarkhuang.github.io/software-engineering-101/07-old-patterns-new-clothes/index.md) (available)
- Lesson 8: [Agile at Agent Speed](https://clarkhuang.github.io/software-engineering-101/08-agile-at-agent-speed/index.md) (available)
- Lesson 9: [Know What It Costs](https://clarkhuang.github.io/software-engineering-101/09-know-what-it-costs/index.md) (available)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-101/10-strict-about-data/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-101/AGENTS.md](https://clarkhuang.github.io/software-engineering-101/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

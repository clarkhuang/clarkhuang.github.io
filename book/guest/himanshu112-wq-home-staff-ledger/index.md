# I built the app. Would people use it every month?

HTML page: https://clarkhuang.github.io/book/guest/himanshu112-wq-home-staff-ledger/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/book/guest/himanshu112-wq-home-staff-ledger/index.md (plus https://clarkhuang.github.io/book/guest/himanshu112-wq-home-staff-ledger/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask. Also read https://clarkhuang.github.io/llms-full.txt, https://clarkhuang.github.io/book.json, and the preview transcript at https://clarkhuang.github.io/book-source/preview/transcript.md. Cite chapter titles or timestamps. Charlie Hack is the fictional narrator; Clark Huang is the author. Do not identify real people or companies behind the fictional names.

By Himanshu Kumar [@himanshu112-wq](https://github.com/himanshu112-wq) · Nov 25, 2026.

AI has made it possible to take an idea and build software other people can actually use. I wanted to see how far I could get by working on a real problem in the evenings. I used GitHub to manage the code, Vercel to deploy the website, and Neon for the database. I learned how those pieces fit together as I needed them. If you’re curious enough to ask how something works and willing to keep going when you get stuck, you can build more than you might expect.

One of my first lessons was about the number 12579. The attendance screen needed to work in Hindi and English. I wanted the labels to change with the language and the number to stay 12579 in both. Once I gave ChatGPT that exact example, I knew what to check on the screen. That became my way of working through the rest of the app.

Home Staff Ledger started with a simple problem. If you employ a cook, a driver, or a housekeeper, someone has to track attendance, paid leave, overtime, and what’s owed at the end of the month. I wanted to divide the monthly salary by 30 to get a daily rate. What should happen in a month with 31 days? The person marking attendance needed to see who had checked in. Did they also need to see what everyone earned?

I used ChatGPT to work through requirements, test cases, and parts of the release process. When I reached my ChatGPT usage limit, I continued development with Grokbot. I used Claude for design feedback. When I’d used up my AI limits, I asked friends for help and learned to do a few of the steps manually. Switching tools taught me to keep track of what I was trying to change and how I’d know the fix worked.

What surprised me was how quickly I could get a web fix in front of someone. I could take a piece of feedback, reproduce the issue, work through the fix with AI, push the change to GitHub, and check the updated Vercel deployment. Once I’d checked the fix, I could send the link back and ask the person to try again.

Getting the app ready for other people meant setting up its own domain, staffledger.app, getting email sign-in working for testing, and adding a forgot-password flow. Mobile taught me a whole new set of steps. I learned how to set up the app in Apple’s App Store Connect and Google Play Console, upload test builds, and add people to the tester lists. On iOS, that meant getting a build onto TestFlight and inviting testers. On Android, it meant putting a build on Google Play’s internal testing track and giving testers access. When a fix needed a new mobile build, I had to upload it and make sure testers had the updated version. That made me appreciate how short the feedback loop on the web had become.

Then I shared the project on LinkedIn and asked for testers. I was proud that I could hand someone a link or invite them to run the app on their own phone. I started wondering what they’d do a month later. Would the person marking attendance keep doing it? Would the household admin come back at payday? I understood the problem in my own household. I still needed to learn whether other households felt it often enough to change their routine.

AI helped me get to the point where I could put a working app in someone’s hands and fix things when they gave me feedback. What I wanted to learn next was whether they’d come back the following month. For Home Staff Ledger, that would tell me more about what to build next than another evening of adding features.

This is a first-person guest story, published under the author’s name with written consent. Source: [book-source/guest/himanshu112-wq-home-staff-ledger.md](https://clarkhuang.github.io/book-source/guest/himanshu112-wq-home-staff-ledger.md). The author is also listed on [Contributors](https://clarkhuang.github.io/contributors/index.md).

## For agents

- This page: https://clarkhuang.github.io/book/guest/himanshu112-wq-home-staff-ledger/index.md
- This folder’s agents file: https://clarkhuang.github.io/book/guest/himanshu112-wq-home-staff-ledger/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

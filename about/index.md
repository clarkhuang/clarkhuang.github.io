# About this project

The mission of this project is to put good software engineering within reach of anyone who wants to build with AI. The training is public. You can study how a change works, try it yourself and show someone else how to verify the result. Clark Huang intends to establish a nonprofit foundation and help fund it himself, alongside donors who share that mission.

The proposed foundation would support two kinds of work. It would help produce and maintain courses, captioned lessons and hands-on labs that anyone can use. For approved projects, it would also provide mentorship and cover a defined amount of hosting so builders can put an application in someone’s hands. The courses are available now. The shared hosting service and awards are proposals.

## Who gets to build?

An individual learning AI engineering can ask an agent to fix one bug and prove the fix works. A nonprofit with a small staff might tackle a weekly delivery list. A sole proprietor might turn a customer request into a draft estimate they can check. A small business might help its team catch duplicate orders before they ship. Each builder brings a problem they know firsthand and a way to tell whether the software helped.

Pick one case to work through. If a customer submits the same order twice, what should staff see? Write that down, give the example to your agent and test the result. A laptop and a free lesson are enough to start. The proposed SE 401 platform would help when you want someone else to use what you built.

<!-- BEGIN generated project state -->
## What you can use today

Study the public courses in the format that works for you. Watch a video, follow the captions in SE 201, read a lesson transcript, or give the Markdown page to your assistant. The published courses are [AI Tips](/ai-tips/) (17 available), [Software Engineering 101](/software-engineering-101/) (10 available), [Software Engineering 201](/software-engineering-201/) (10 available).

The [OpenBook](/book/) is listed as a preview. Its first complete edition is targeted for 2027. The chapter catalog links to [Building Blocks](/book/chapters/17b-building-blocks/), [Sick, Well, Fit](/book/chapters/36-sick-well-fit/). The [story arc](/book/story-arc/) follows the career stories into the engineering lessons and the making of this site.

The [Change Log](/change-log/) records what reached production. Its [full archive](/change-log/archive/) links each update to the public commit.

## Hands-on training in SE 301

[SE 301](/software-engineering-301/) is the playbook for running this workflow on local compute. The planned February 2027 Studio build will test it against a real site change. Readers can already try the laptop path and share what they measure.

## A possible first cohort with a nonprofit

The [SE 401 proposal](/software-engineering-401/) asks whether a team can build an affordable application that another organization can operate. One candidate is work a nonprofit and its advisor could explore with eCIO. Staff would trace a gift from receipt to allocation. Staff could count the follow-ups on real cases, then see whether a second nonprofit can repeat the process with a standard file import.

A nonprofit would help choose the problem and decide which results to share. A possible ending for the book is a first funded cohort showing its work to the staff who use it. That scene depends on what the cohort actually builds.
<!-- END generated project state -->

## Eat your own dogfood

Clark says, “I’m not a fan of typical sales and marketing tactics.” That view shapes both the book and the site. When you depend on the same thing you offer someone else, you can tell them where it helped, where it failed, and what it cost. They can try it and reach their own conclusion.

Take this site. SE 101 teaches readers to verify a change. When we added SE 301 to the navigation, we had to open the deployed homepage and follow the link ourselves. A successful merge alone would have told us nothing about what a reader could actually see. The February Mac Studio build will put the SE 301 playbook through the same test: start at first login, follow the published instructions, and correct the steps that fail.

That is the public purpose behind the proposed foundation. A first-time builder should be able to read the same instructions, inspect the same code, see the running costs, and take their work elsewhere. If the shared infrastructure makes a lab affordable, publish what the subsidy buys. If a reader on a cheaper laptop finds a better way, give them credit and change the lesson.

This site hosts its courses, book and videos on GitHub Pages. Its optional reader service calls an external backend to save a signed-in learner’s progress. Readers can inspect both parts, and a guest can still take the courses. SE 401 would build on that experience to help others run applications of their own.

## How the project will improve itself

Our technical goal is recursive self-improvement (RSI). The first system we want to improve is this one. For example, when three learners get stuck on the same lab step, an agent could replay the exercise, propose a clearer instruction and test it with a fresh checkout. After review, we would publish the change and check whether learners can finish that step. The next round starts with that evidence.

SE 301 starts this work on a laptop. The planned 512 GB Mac Studio would run the project’s inference locally and let members use the same models in SE 401 applications. Smaller models could handle routine tasks while more capable open-weight models handle harder ones. The February build will measure which models and workloads the hardware can actually support.

## A proposed hosting service for builders

[Explore the SE 401 goals and ten-lab outline](/software-engineering-401/).

Imagine a product owner and a new engineer working together on a small application for a community organization. They start with a GitHub account, a real user and a written definition of success. Every pull request gets a preview. Before they invite the first user, they can explain who can see each record, how to undo a release, and what one more user will cost. After launch, they hand the service to another team that can actually operate it. That handoff would be their final exam.

The proposed platform would offer a Vercel-style deployment flow. You would sign in with GitHub and give your agent the course URL. With your approval, the agent would publish the educational frontend on your own GitHub Pages site. The platform would supply an isolated backend on Render and a project database on MongoDB from shared provider accounts. The goal is one signup for the builder. The platform operator would manage the provider accounts, credentials and usage limits.

Communication would be a later part of the curriculum. A team could receive email at its own address on a teaching domain, use SendGrid to reply, or add a Twilio number for voice and SMS. WhatsApp, Instagram, Facebook and LinkedIn would be separate, opt-in integrations. Each project would operate under its own identity, permissions and spending limit. In a first lab, sending a message to a test inbox and showing what happens when delivery fails would be a successful outcome.

### Give an agent the course URL

A learner should be able to tell a fresh agent, “Read SE 401 and set up the first lab in my GitHub account.” The course would publish a discovery link in llms.txt, a Markdown guide for the learner, and a versioned, machine-readable recipe for each lab. The recipe would name the owner, required accounts and permissions, supported free tier, expected resources, and the checks that prove the app works. The recipes would live on GitHub Pages. The learner’s authorized agent would execute them in the learner’s environment.

For a first lab, the agent would show which repository it needs, what it intends to publish and how much sponsored usage the project has. After the owner approves, it would create a preview and call the platform to provision that project’s backend and database. Runtime secrets would stay with the service. The owner could see what the agent created, export the application and revoke access.

The test would start with a fresh GitHub account. The agent must return a working preview URL, write and read a sample record, retrieve that record through the authorized tool, and demonstrate that a second user cannot read it. Running the recipe again must reuse existing resources. The handoff would record resource IDs, versions, verified checks, cost limits, and steps to export or remove the lab. A second agent should be able to pick up that record and operate the app without the original conversation.

## How the proposed foundation would fund learning

A learner should be able to see what it costs to run a lab and who paid for it. One proposal is to accept gifts through a qualified educational charity or fiscal sponsor. The recipient would own the money and issue donor acknowledgments. Subject to the recipient’s approval and Schwab’s account requirements, longer-term assets could be held at Charles Schwab with eCIO as investment adviser. Clark’s role at eCIO, any fees and the adviser selection would be disclosed.

Operating gifts could cover current hosting, databases and communication credits. A long-term fund could support future cohorts under a documented spending policy. The project would report contributions, fees, program spending and the cost per completed learner project. A donation page would follow selection of a recipient, custody arrangements and gift terms.

### Who pays for the lab?

The curriculum is free. For a hosted lab, the proposal is to meter each project’s compute, database storage and paid messages. A builder could see the allowance, usage to date and estimated cost of the next run. At the limit, they could pause, request additional credit, move the app to their own hosting or explicitly agree to cover further usage.

Clark’s initial contribution and future fundraising could support teaching, mentorship and operating credits for selected projects. The proposed foundation would publish which projects it supports, what the awards cover and what the builders learned. Selection criteria and award amounts remain open.

### Clark’s work at eCIO and the idea for an education endowment

Clark Huang is the co-founder and CTO of eCIO, where he leads investment technology and technical operations. He helped build a firm that manages long-term funds for nonprofits. Its education clients include Redwood City Education Foundation, Bloomington Montessori School and Genesys Works. [Meet the eCIO team](https://www.getecio.com/about-ecio-investment-advisor-for-nonprofits) · [See the schools and educational organizations eCIO serves](https://www.getecio.com/nonprofits/schools).

Clark wants to bring that experience to this project. A free course can teach someone how to deploy an app today. A learner who keeps that app running next semester still needs a database, hosting and someone to turn to when it breaks. Clark’s vision is an education endowment whose distributions could pay for lab credits and shared infrastructure across successive cohorts. He would like eCIO to manage that endowment if the project establishes one. The fund and advisory appointment are proposals. If they go ahead, this page should identify who oversees the fund, what the adviser is paid, and how much reaches learners each year.

[Explore SE 301](https://clarkhuang.github.io/software-engineering-301/) · [Contribute to the project](https://clarkhuang.github.io/contribute/)

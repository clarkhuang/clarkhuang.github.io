# About this project

Clark Huang started this public learning site around a question: what should an engineer still know how to do when an AI can write the code? The lessons follow the work from one change in SE 101, through whole systems in SE 201, to running the models and tools yourself in SE 301. The free OpenBook, *Silicon Valley C Players*, explores the same interest in fundamentals through stories and practical lessons.

<!-- BEGIN generated project state -->
## What you can use today

Watch a lesson, read its transcript, or give the Markdown page to your assistant. The published video courses are [AI Tips](/ai-tips/) (17 available), [Software Engineering 101](/software-engineering-101/) (10 available), [Software Engineering 201](/software-engineering-201/) (10 available).

The [OpenBook](/book/) is listed as a preview. Its first complete edition is targeted for 2027. The chapter catalog links to [Building Blocks](/book/chapters/17b-building-blocks/), [Sick, Well, Fit](/book/chapters/36-sick-well-fit/). The [story arc](/book/story-arc/) follows the career stories into the engineering lessons and the making of this site.

The [Change Log](/change-log/) records what reached production. Its [full archive](/change-log/archive/) links each update to the public commit.

## The next experiment

[SE 301](/software-engineering-301/) is the playbook for running this workflow on local compute. The planned February 2027 Studio build will test it against a real site change. Readers can already try the laptop path and share what they measure.

## What a first cohort could prove

The [SE 401 proposal](/software-engineering-401/) asks whether a team can build an affordable application that another organization can operate. One candidate comes from the work a nonprofit and an advisor may share: identifying a gift and reconciling its allocation. Staff could count the follow-ups on real cases, then see whether a second nonprofit can repeat the process with a standard file import.

That pilot, an education foundation and an eCIO advisory role are ideas to test. A possible ending for the book is a funded cohort showing what it built. That scene depends on a cohort actually doing the work and its partners agreeing to share the result.
<!-- END generated project state -->

## Who gets to build?

Today, anyone can take a free lesson, inspect its source, and apply it to work they care about. A volunteer tracking food deliveries and a founder tracking customer orders can use the same first exercise. Pick one order, describe what should happen when it arrives twice, and show another person that the software handles it. Neither learner needs a credential or a foundation award to begin.

The next test is whether someone else can reproduce our work. SE 301 puts the site’s own development workflow on local hardware. The February 2027 build is where we expect to learn which instructions survive first contact with a new machine. Readers working on smaller machines can contribute their results along the way.

Longer term, Clark envisions a foundation that funds learning opportunities through mentorship and access to infrastructure. His role as eCIO’s co-founder and CTO gives him a place to look for real problems that nonprofits and their advisors share. A potential partner would help choose a problem, try the result and decide what evidence could be shared. The partnership, awards and funding model are proposals. The public curriculum would also serve people building for-profit ventures and internal systems. Anyone could take the code and run it elsewhere.

## Eat your own dogfood

Clark puts it plainly: “I despise marketing and sales.” That conviction shapes both the book and the site. When you depend on the same thing you offer someone else, you can tell them where it helped, where it failed, and what it cost. They can try it and reach their own conclusion.

Take this site. SE 101 teaches readers to verify a change. When we added SE 301 to the navigation, we had to open the deployed homepage and follow the link ourselves. A successful merge alone would have told us nothing about what a reader could actually see. The February Mac Studio build will put the SE 301 playbook through the same test: start at first login, follow the published instructions, and correct the steps that fail.

That is the public purpose behind the proposed foundation. A first-time builder should be able to read the same instructions, inspect the same code, see the running costs, and take their work elsewhere. If the shared infrastructure makes a lab affordable, publish what the subsidy buys. If a reader on a cheaper laptop finds a better way, give them credit and change the lesson.

The long-term goal is an AI-native cloud platform for small businesses. A small team could give its agent a business requirement and a budget, then use shared infrastructure to deploy a web app, connect its data, handle incoming messages and recover from a failed release. Those are capabilities a large company can staff internally. Here, each business would own its accounts and data and could export its application. The proposed funding model combines donated learning credits with transparent, minimal cost-recovery fees for ongoing business use.

GitHub Pages at clarkhuang.github.io is the hosting infrastructure for this site. The courses, book, videos and public navigation work as static files. Optional features such as reader sync can call an external HTTPS service while the learning materials remain available to guests. SE 401 would evaluate other hosts for student applications only when a free tier is available. Each lab would document its free limits, what happens when they are reached, and how to export the project.

## A possible SE 401: build something someone else can depend on

[Explore the SE 401 goals and ten-lab outline](/software-engineering-401/).

Imagine a product owner and a new engineer working together on a small application for a community organization. They start with a GitHub account, a real user and a written definition of success. Every pull request gets a preview. Before they invite the first user, they can explain who can see each record, how to undo a release, and what one more user will cost. After launch, they hand the service to another team that can actually operate it. That handoff would be their final exam.

The proposed next step is a shared teaching platform. A project would get a web app, a preview environment, a budget and a named owner. Teams could expose a narrowly scoped MCP tool for agents and choose Postgres or MongoDB for persistence. A search lab could add vector retrieval once a team has examples that let it measure whether retrieval improves the answer.

Communication would be a later part of the curriculum. A team could receive email at its own address on a teaching domain, use SendGrid to reply, or add a Twilio number for voice and SMS. WhatsApp, Instagram, Facebook and LinkedIn would be separate, opt-in integrations. Each project would operate under its own identity, permissions and spending limit. In a first lab, sending a message to a test inbox and showing what happens when delivery fails would be a successful outcome.

## Give an agent the course URL

A learner should be able to tell a fresh agent, “Read SE 401 and set up the first lab in my GitHub account.” The course would publish a discovery link in llms.txt, a Markdown guide for the learner, and a versioned, machine-readable recipe for each lab. The recipe would name the owner, required accounts and permissions, supported free tier, expected resources, and the checks that prove the app works. The recipes would live on GitHub Pages. The learner’s authorized agent would execute them in the learner’s environment.

For a first lab, the agent would inspect the learner’s existing setup and show a plan. With approval, it would create the repository from a template, configure a preview deployment, provision the selected database, put scoped credentials in the runtime’s secret store, and wire up a read-only MCP tool. Provider adapters would use documented APIs or CLIs and identify any required browser step. If a provider asks the owner to verify an identity, accept terms, approve access or authorize a charge, the agent would save its place, explain exactly what is needed, and resume after confirmation.

The test would start with a fresh GitHub account. The agent must return a working preview URL, write and read a sample record, retrieve that record through the authorized tool, and demonstrate that a second user cannot read it. Running the recipe again must reuse existing resources. The handoff would record resource IDs, versions, verified checks, cost limits, and steps to export or remove the lab. A second agent should be able to pick up that record and operate the app without the original conversation.

## Clark’s work at eCIO and the idea for an education endowment

Clark Huang is the co-founder and CTO of eCIO, where he leads investment technology and technical operations. He helped build a firm that manages long-term funds for nonprofits. Its education clients include Redwood City Education Foundation, Bloomington Montessori School and Genesys Works. [Meet the eCIO team](https://www.getecio.com/about-ecio-investment-advisor-for-nonprofits) · [See the schools and educational organizations eCIO serves](https://www.getecio.com/nonprofits/schools).

Clark wants to bring that experience to this project. A free course can teach someone how to deploy an app today. A learner who keeps that app running next semester still needs a database, hosting and someone to turn to when it breaks. Clark’s vision is an education endowment whose distributions could pay for lab credits and shared infrastructure across successive cohorts. He would like eCIO to manage that endowment if the project establishes one. The fund and advisory appointment are proposals. If they go ahead, this page should identify who oversees the fund, what the adviser is paid, and how much reaches learners each year.

## Who pays for the lab?

The goal is free access to the core learning experience. One idea is to sponsor a fixed amount of compute, storage and messaging per team. A team approaching its allowance could stop, apply for more sponsored credit or explicitly pay the published cost of continuing. A successful student project should have a clear path to its own hosting and provider accounts.

An educational nonprofit and a long-term fund for learner access are possibilities. Decisions about governance, funding, partners and service availability are ahead of us. The work readers can use today is the published curriculum. The proposed platform gives us a specific question to test: can a new team build something useful, operate it within a budget, and teach the next team to do the same?

## A proposed fund for free learner access

A learner should be able to see what it costs to run a lab and who paid for it. One proposal is to accept gifts through a qualified educational charity or fiscal sponsor. The recipient would own the money and issue donor acknowledgments. Subject to the recipient’s approval and Schwab’s account requirements, longer-term assets could be held at Charles Schwab with eCIO as investment adviser. Clark’s role at eCIO, any fees and the adviser selection would be disclosed.

Operating gifts could pay current bills for hosting, databases and capped communication credits. A separate long-term fund could support future cohorts through a documented spending policy. We would publish annual contributions, investment and administrative fees, amounts released for programs, and the cost per completed learner project. This is a funding proposal. A giving page would open only after a recipient, custody arrangements and gift terms are established.

[Explore SE 301](https://clarkhuang.github.io/software-engineering-301/) · [Contribute to the project](https://clarkhuang.github.io/contribute/)

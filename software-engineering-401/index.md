# Software Engineering 401 • Build it, run it, hand it off

**Course in development.** This is the public design and lab outline. The shared hosting platform, provider adapters and lab videos are planned. Start today with the [SE 301 playbook](/software-engineering-301/).

SE 401 is for the individual learning AI engineering, the nonprofit stretching a small budget, the sole proprietor handling work alone and the small business with a team to support. A sole proprietor could start with a tool that turns a customer inquiry into a draft estimate. A builder and a nonprofit coordinator could plan tomorrow’s deliveries. Each team would choose one recurring job, test the app with the person doing it and show what it costs to run.

The proposed platform would give those builders a Vercel-style experience through an agent. Start with a GitHub account, give your agent the SE 401 URL and review its plan. With your authorization, it would publish the lab frontend under your own github.io address and request an isolated Render backend and MongoDB database from the shared platform. The platform operator would hold the provider accounts and keep each project’s credentials and data separate. The builder would sign up only with GitHub.

The project’s own reader service gives the class a working example to study. A useful acceptance test is whether one reader can stop a lesson on a laptop and resume on a phone while a second reader’s bookmarks stay private. The shared provisioning service for student projects is a future build.

## One possible first cohort

A nonprofit and eCIO could bring one recent gift that staff had trouble identifying. A learner would replay the handoff with information staff already collect, record where someone had to ask a question, and compare a proposed destination fund or split with the actual subaccounting entry. The exercise could run alongside existing operations without changing the donor’s Giving Page or posting to a live account.

If staff find the replay useful, they could test it over a defined period and count follow-up requests per eligible gift across both partners. A second nonprofit could try the workflow from a standard file import. Those experiments would tell us what travels beyond eCIO. A cohort might share an open-source release and, with both partners’ permission, a redacted walkthrough. These are starting hypotheses for the people doing the work to revise.

## What a learner should be able to do

| Goal | Evidence we want to see |
|---|---|
| Start with a GitHub account and a course URL | A fresh agent discovers a versioned recipe, explains its resource plan and identifies every step requiring the owner. |
| Ship a useful first feature | The product owner names a user and an observable outcome. The user can try it at a preview URL. |
| Give people and agents appropriate access | Two users can save their own data. An agent with a read grant can retrieve approved data, and revoking its grant ends access. |
| Keep the service affordable | The team publishes a unit cost, a free allowance, and the behavior when that allowance runs out. |
| Hand the application to another team | A second team can deploy, recover, export and retire it using the repository and its own accounts. |

## Proposed lab sequence

| Lab | What the team builds | How it earns a pass |
|---|---|---|
| 1. Find the first user | A one-page brief, a real constraint and an acceptance test | The user can say what would make the feature worth keeping. |
| 2. Teach an agent to provision | A discoverable recipe with prerequisites, versions and owner prompts | Interrupt setup and rerun it without duplicating paid or free resources. |
| 3. Put a preview behind a pull request | A static frontend and an optional free-tier app runtime | Follow the preview link on a phone and roll back one change. |
| 4. Own the data model | A Postgres or MongoDB implementation and an export format | Restore a clean copy and explain which records each user may access. |
| 5. Give an agent one useful tool | A narrowly scoped MCP tool | Demonstrate authorization, isolation and revocation using two test identities. |
| 6. Evaluate search | A small benchmark for keyword and vector retrieval | Publish which approach answered real questions accurately enough for the app. |
| 7. Handle an email end to end | An inbound address on a teaching subdomain and a SendGrid test reply | Replaying a delivery event creates one reply. A failed delivery is visible. |
| 8. Add a communication channel | One opt-in voice, SMS or WhatsApp use case through Twilio. Instagram, LinkedIn and Facebook are optional extensions subject to provider access. | Demonstrate consent, opt-out and a spending limit with test users. |
| 9. Operate a shared lab | Project ownership, quotas, recovery instructions and cost reporting | One team reaching its limit leaves another team’s work available. |
| 10. Hand it off | A live app, an operating record and an agent-readable rebuild recipe | A second team reproduces the app without the original chat and reports the steps that failed. |

## What stays on GitHub Pages

Clark’s courses, book and public playbooks stay on clarkhuang.github.io. For an educational project, a learner could own the repository and publish its frontend at an address such as your-name.github.io/delivery-lab/. An agent would request permission for that repository and a separate project grant for its backend. For a business moving on to online transactions or commercial software as a service, the handoff would include moving the frontend to a host that permits that use. [GitHub Pages usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## How we will teach it

The platform would meter each project’s use of Render, MongoDB and any paid integrations. Clark hopes to sponsor approved projects with money he intends to contribute to a private foundation and with future fundraising. A lab would show the grant, the amount used and the options when it runs out. A business that wants to keep an app running could later opt into a published cost-recovery arrangement or take the app elsewhere. The [About page](/about/) explains the proposed funding model and eCIO’s possible role.

Have you already built a shared teaching environment? [Contribute an experience](/contribute/): tell us who used it, what they built, the actual cost, and one thing the next cohort should do differently.

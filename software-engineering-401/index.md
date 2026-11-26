# Software Engineering 401 • Build it, run it, hand it off

**Course in development.** This is the public design and lab outline. The shared hosting platform, provider adapters and lab videos are planned. Start today with the [SE 301 playbook](/software-engineering-301/).

SE 401 pairs a new engineer with a product owner. Together they will build one small application for a real user and leave it in a state another team can operate. Our first customer will be this project itself. Reader progress, for example, gives us a concrete test: can someone stop a lesson on a laptop and resume it on a phone, while another reader’s progress stays private?

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

This site, its public playbooks and their machine-readable instructions stay on clarkhuang.github.io. The learner’s agent will provision external resources in an authorized environment. Each proposed runtime must offer a free tier. Metered services need an explicit allowance, sponsored credit or an owner-approved budget. The handoff will identify who owns each resource and how to remove it.

## How we will teach it

We will use our own workflows first and publish what survives contact with real users. The proposed foundation’s goal is to make that information and infrastructure accessible to the next generation of builders. The [About page](/about/) explains Clark’s role at eCIO and his vision for funding learner access.

Have you already built a shared teaching environment? [Contribute an experience](/contribute/): tell us who used it, what they built, the actual cost, and one thing the next cohort should do differently.

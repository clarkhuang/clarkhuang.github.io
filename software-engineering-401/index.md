# Software Engineering 401 • Build it, run it, hand it off

**Course in development.** This is the public design and lab outline. The shared hosting platform, provider adapters and lab videos are planned. Start today with the [SE 301 playbook](/software-engineering-301/).

The aim of SE 401 is to teach people how to build an application others can rely on, then give approved projects a way to keep it running. The proposed foundation would help fund both the public labs and a shared hosting service. Anyone could study the recipes and take the code to a host of their choice.

Choose someone with a weekly task. A sole proprietor might turn a customer inquiry into a draft estimate. A nonprofit coordinator might plan tomorrow’s deliveries. An individual learning to code can take either example through the labs. A small business can bring a workflow of its own and judge the result with its staff.

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

## Build SE 401 with hosted models first

Start before the SE 301 Studio is ready. Follow one volunteer coordinator from a page of fictional shift notes to a handoff they can approve. Claude, ChatGPT or Grok can help the builder write code and review results from day one. For the running app, the operator would connect one approved server-side API from Anthropic, OpenAI or xAI, with its own credentials and spending limit. A learner can rehearse the flow with saved sample responses before anyone turns on billing.

### 1. Establish the baseline (course lab 1)

Ask the coordinator to write one handoff by hand. Save the input, their draft, time taken and a rubric covering owners, deadlines and unsupported claims. Reserve unseen cases, including incomplete and contradictory notes. Pass when the coordinator can use the rubric to accept or reject a draft.

### 2. Deploy a thin slice (labs 2–4)

Publish a member-owned frontend, a Render web service and project-scoped MongoDB records. First return a saved example. Record a preview URL, a clean deployment, a rollback and a successful restore. Repeat setup after an interruption and check that it creates no duplicate resources.

### 3. Run one real model job (labs 4–5)

Send a job ID, project ID, task version and approved input to a queue. A worker uses one hosted provider to return a structured draft with links to the supporting notes. Record provider, model version, usage, elapsed time and errors. The coordinator approves or edits the draft. Pass when a timeout and retry produce one saved handoff and one member charge; record any duplicate provider cost separately.

### 4. Compare with evidence (lab 6)

Replay the same redacted cases through a second available provider. Keep the rubric, inputs and output budget fixed. Have the coordinator score drafts without seeing model names. Publish acceptance rate, unsupported claims, time to approved handoff and cost per accepted result. Keep the simplest provider that meets the agreed threshold, and document one case it missed.

### 5. Operate two member apps (labs 7–9)

Give a second team a separate app, credentials and allowance. Deliver an approved handoff through one opt-in test channel. Exhaust one project’s quota, replay a delivery and interrupt a worker. Verify the other team can still work, each sees only its own jobs, and one approval produces one delivery. Save the usage ledger and recovery times.

### 6. Rehearse site improvement (labs 6 and 9)

Use a hosted model to propose one improvement to the foundation site’s lesson-link answers. Compare the current version and the proposed change on held-out questions. Record regressions as well as gains. A maintainer reviews the diff and staging results, then accepts or rejects the PR. Keep this experiment on a separate budget from member requests.

### 7. Swap in the Studio and hand it off (SE 301 and lab 10)

Once SE 301 can serve a pinned local model, have the Studio claim the same job format over an authenticated outbound connection. Replay the hosted baseline alongside a site-improvement run. Measure queue wait, 95th-percentile completion time, quality and cost per accepted result, including local operating costs. Disconnect and reconnect the Studio. Pass when queued jobs recover and a second team can reproduce the comparison and switch back using the written recipe.

Publish each lab as a field report after the build. Include the starting hypothesis, dated PR and deployment, redacted test inputs, observed results, one failure or surprise, and the decision it changed. Invite another team to rerun the recipe. Mark untested steps as planned and record an unsuccessful experiment when that is what happened.

## Give an application a local AI task

Imagine a volunteer coordinator who wants a weekly handoff from shift notes. In the proposed platform, their agent publishes the interface on their own GitHub Pages site. A project-scoped Render web service receives the request, queues a summarization task on the shared SE 301 inference service, and saves the draft in that project’s MongoDB data. The coordinator reviews it before sharing. The browser never needs a model-service credential.

Each job would record its project, model, input and output tokens, compute time, result and funding source. A retry must reuse the job identifier so it cannot spend the same credit twice. A builder could inspect the usage, see how much the foundation or donors covered, and set a limit before enabling a recurring task. If the Studio is offline or a project reaches its cap, show the queued or paused state. Paid overages would require an explicit choice. The first shared deployment would have to demonstrate project isolation, accurate metering and recovery before opening it to members.

## Test shared hosting and foundation-sponsored inference

The pilot goal is to help two members build and deploy independent apps on a foundation-managed Render account. Each app would have its own service, credentials, data access and spending limit. A Render web service would accept requests and queue jobs. The foundation’s 512 GB Mac Studio would make an authenticated outbound connection to claim each job, run the model locally and return the result to the requesting app. An approved project could offer this AI feature free to its users within its grant. The foundation would budget for hosting, electricity and operating the machine.

The Studio would also run a recursive self-improvement (RSI) experiment on the foundation’s own site. Start with a repeatable task, such as answering a learner’s question with the right lesson link. Save the current answers, let the agent propose an improvement, and compare both versions on held-out questions. A maintainer would review the results and approve a staging PR before a change reaches readers.

Before inviting more members, have both apps request summaries while the site experiment runs. Measure answer quality, the wait for 95% of requests, completed jobs per hour and cost per completed job. Pause the Studio mid-job, bring it back, and show that each app receives its own result and is charged once. Use those results to set each project’s allowance and decide when the Studio can spare time for experiments.

## What stays on GitHub Pages

Clark’s courses, book and public playbooks stay on clarkhuang.github.io. For an educational project, a learner could own the repository and publish its frontend at an address such as your-name.github.io/delivery-lab/. An agent would request permission for that repository and a separate project grant for its backend. For a business moving on to online transactions or commercial software as a service, the handoff would include moving the frontend to a host that permits that use. [GitHub Pages usage limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## How we will teach it

A proposed nonprofit foundation, funded by Clark alongside other donors, would support course production, hands-on training and mentorship. Hosting would be a separate award with a project budget. Builders could see their Render, MongoDB and integration usage, check how much credit remains and export the app. If a project outgrows the award, its owner could move it or opt into a published cost-recovery arrangement. The [About page](/about/) explains the funding proposal and eCIO’s possible role.

Have you already built a shared teaching environment? [Contribute an experience](/contribute/): tell us who used it, what they built, the actual cost, and one thing the next cohort should do differently.

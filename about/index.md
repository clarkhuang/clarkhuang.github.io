# About this project

Clark Huang started this public learning site around a question: what should an engineer still know how to do when an AI can write the code? The lessons follow the work from one change in SE 101, through whole systems in SE 201, to running the models and tools yourself in SE 301. The free OpenBook, *Silicon Valley C Players*, explores the same interest in fundamentals through stories and practical lessons.

GitHub Pages at clarkhuang.github.io is the hosting infrastructure for this site. The courses, book, videos and public navigation work as static files. Optional features such as reader sync can call an external HTTPS service while the learning materials remain available to guests. SE 401 would evaluate other hosts for student applications only when a free tier is available. Each lab would document its free limits, what happens when they are reached, and how to export the project.

## A possible SE 401: build something someone else can depend on

Imagine a product owner and a new engineer working together on a small application for a community organization. They start with a GitHub account, a real user and a written definition of success. Every pull request gets a preview. Before they invite the first user, they can explain who can see each record, how to undo a release, and what one more user will cost. After launch, they hand the service to another team that can actually operate it. That handoff would be their final exam.

The proposed next step is a shared teaching platform. A project would get a web app, a preview environment, a budget and a named owner. Teams could expose a narrowly scoped MCP tool for agents and choose Postgres or MongoDB for persistence. A search lab could add vector retrieval once a team has examples that let it measure whether retrieval improves the answer.

Communication would be a later part of the curriculum. A team could receive email at its own address on a teaching domain, use SendGrid to reply, or add a Twilio number for voice and SMS. WhatsApp, Instagram, Facebook and LinkedIn would be separate, opt-in integrations. Each project would operate under its own identity, permissions and spending limit. In a first lab, sending a message to a test inbox and showing what happens when delivery fails would be a successful outcome.

## Give an agent the course URL

A learner should be able to tell a fresh agent, “Read SE 401 and set up the first lab in my GitHub account.” The course would publish a discovery link in llms.txt, a Markdown guide for the learner, and a versioned, machine-readable recipe for each lab. The recipe would name the owner, required accounts and permissions, supported free tier, expected resources, and the checks that prove the app works. The recipes would live on GitHub Pages. The learner’s authorized agent would execute them in the learner’s environment.

For a first lab, the agent would inspect the learner’s existing setup and show a plan. With approval, it would create the repository from a template, configure a preview deployment, provision the selected database, put scoped credentials in the runtime’s secret store, and wire up a read-only MCP tool. Provider adapters would use documented APIs or CLIs and identify any required browser step. If a provider asks the owner to verify an identity, accept terms, approve access or authorize a charge, the agent would save its place, explain exactly what is needed, and resume after confirmation.

The test would start with a fresh GitHub account. The agent must return a working preview URL, write and read a sample record, retrieve that record through the authorized tool, and demonstrate that a second user cannot read it. Running the recipe again must reuse existing resources. The handoff would record resource IDs, versions, verified checks, cost limits, and steps to export or remove the lab. A second agent should be able to pick up that record and operate the app without the original conversation.

## Who pays for the lab?

The goal is free access to the core learning experience. One idea is to sponsor a fixed amount of compute, storage and messaging per team. A team approaching its allowance could stop, apply for more sponsored credit or explicitly pay the published cost of continuing. A successful student project should have a clear path to its own hosting and provider accounts.

An educational nonprofit and a long-term fund for learner access are possibilities. Decisions about governance, funding, partners and service availability are ahead of us. The work readers can use today is the published curriculum. The proposed platform gives us a specific question to test: can a new team build something useful, operate it within a budget, and teach the next team to do the same?

[Explore SE 301](https://clarkhuang.github.io/software-engineering-301/) · [Contribute to the project](https://clarkhuang.github.io/contribute/)

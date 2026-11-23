# Claims toned down or removed: SE201 Lesson 5, Governance: Where People Decide

What was softened or cut between the outline, the round-1 draft (`make_se201_05_governance.round1.py`) and the recorded script, and why.
Round 2 changed nothing.

| Earlier wording (scene) | What happened | Why |
|---|---|---|
| Outline: "Picture a payments system: ... a person approves anything that changes how money moves." | Replaced by "our made-up example: the subscription-billing system from lesson one", labelled made-up aloud and on screen. | The brief asks for one running example across lessons 5 to 8, and it must never read as a claim about a real company. |
| Outline: "a release board a few times a year, then code review, then an approval step in an automated pipeline" stated flatly | Kept, with "typically" (1996) and "more and more" (2006). | History has to stay approximate; many teams had no change board, and review spread gradually. |
| 03c "a pull request to approve, before production" | Changed to "a pull request a reviewer approves, before it merges". | It conflated a code review with a deploy approval. |
| 03 eras card, 2016: "HOW OFTEN: Every change" | Changed to "Most changes". | "Every" overclaims. |
| 04 "Four no's, and it ships on its checks" | Changed to "that kind of change can ship on its checks"; rule and recap now say only what a person has released. | The flat version contradicted lesson 2's rule (a person approves every change) and claimed more than the lesson supports. |
| 04 on-screen examples under each question ("A fee, a price, a refund" ...) | Removed. | They were on screen but never spoken. |
| 05a "Fix a typo in an email template" as a change that needs nobody | Changed to "a typo on an internal admin screen". | A customer email is customer-facing and can't be unsent; calling it risk-free was wrong. |
| 05b "The ledger's owner decides, after a rehearsal on a copy" | "After a rehearsal on a copy" cut. | Spoken but not shown; an invented process detail the lesson did not need. |
| 05 "Five pieces of work. Three stops." | Now six pieces and four stops, adding "Send customer emails to a new partner" for the data owner. | The customer-data question had no example. |
| 05c refund example with no word on refunds under the limit | Added "Under the limit, a person already decided, when they set it." | Otherwise small refunds appeared to move money with no person deciding, against question 1. |
| 06 "The evidence: the checks that ran, and last month's invoices..." | Now "The evidence, from the pipeline". | The agent should not author its own evidence. |
| 06 "Now the finance owner is deciding about a fee, not proofreading code." | Changed to "Now the finance owner decides about the fee. And an engineer still reviews the code that moves money." | The first version implied the decision card replaces code review on a money path. |
| 06 card: risk "Some customers pay a larger fee than before"; way back "One setting restores the flat fee" | Now "Some customers pay more; they must be told first" and "Restore the flat fee; credit anyone already charged". | Flipping a setting does not undo fees already charged, and the draft ignored telling customers. |
| 07 "If you keep a code owners file, you've already started." | Cut. | Cut for time, and it named a specific host feature as if it were the whole answer. The facts file notes the feature exists. |
| 07 "in a file in the repository, where every agent reads it" and "whoever wrote a change never approves it" | Now "the pipeline enforces it, by what a change touches. The agent that wrote a change doesn't classify it, or approve it." | An agent reading a file is not enforcement, and the draft let the author classify its own change. |
| 07 table row "Wording, tests, internal tools" on checks alone | Now "Internal screens, docs, added tests", plus a row "The checks, the pipeline, this file: always a person". | The first version let an agent weaken a test or edit the approvals file without a person. |
| 08 chapter "THE HONEST PART"; "Be honest about the cost... Worse, they stop reading" | Chapter renamed "WHAT IT COSTS"; lines cut to one sentence each. | "They stop reading" is an unsourced claim about how people behave; "honest" was becoming a tic. |
| 08c "So aim for the few that matter... you can start strict" | Now "So start strict, like lesson two... And where an audit requires a review, that review stays." | Separation of duties was cited and then seemed to be dropped; audited systems keep required reviews. |
| 10 rule "check who decides ... Everything else ships on its checks." | Now "find out who decides ... Ship on checks alone only what a person has released." | Same reasons as 04 and 07. |
| 11 "which of these needed a person, and who?" | "And who" dropped; the exercise now hands the AI the four questions. | An AI can't know who without the file. |

Nothing about Clark or any company was claimed in any draft, so nothing of that kind was removed.

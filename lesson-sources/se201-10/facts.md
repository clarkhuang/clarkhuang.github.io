# Facts and sources: SE201 Lesson 10, Capstone: One Feature, End to End

Script as generated: `scripts/se201-10-capstone.json` (18 scenes, 852 spoken words). Each claim, where it is made, and where it comes from.

## About the presenter and real companies
None. The lesson makes no statement about Clark, his career, his team, or any company. The only real-world references are to this series' own earlier lessons.

## The worked example (all made up, and labelled so)
| Claim | Scene | Source or status |
|---|---|---|
| "a made-up billing system" / "our made-up subscription-billing system from lesson one" | 02, 03; label on every map frame | Lesson 1, scene 09 ("a made-up example: a subscription-billing system"). Called made up in the first sentence of the example. |
| $30 a month, day 10 of a 30-day month, annual plan $300 | 02, 04 | Invented for the lesson; on screen "MADE-UP NUMBERS". |
| 20 days unused = $20 credit; $300 - $20 = $280 before tax | 04, 06, 12, 14 | Arithmetic: $30 / 30 days = $1 a day; 20 x $1 = $20; 300 - 20 = 280. Same figures on every frame. |
| "The finance owner's rule: credit the days paid for, and not used" | 04 | An illustration. Day-based proration with a credit for unused time is a common policy, not the only one; the page notes say so. "Fees and prices: the finance owner" is lesson 5, scene 07. |
| The quote: ID, old plan, new plan, credit, amount due (Q-1, monthly, annual, $20, $280) | 06 | Invented data shape for the example. |
| Four parts; three agents; `billing/upgrade/SPEC.md`, `AGENTS.md`, `index.md`; `billing-ops-agent` | 05-13 | Invented names for the example. |
| "One night, an upgrade shows two charges: two browser tabs, two quotes, two keys" | 13 | A made-up failure inside the made-up example, not an incident. Mechanism is sound: two quotes have two IDs, so two idempotency keys, so the processor sees two distinct charges. |

## Ideas taken from the recorded lessons (wording checked against each script)
| Capstone | Lesson and scene it matches |
|---|---|
| "What's scarce, lesson one said, is knowing it's right" | L1 08_now: "So what's scarce? Knowing that it's right." |
| Spec in the repository, agents file, index; "The spec is the source. Change it, and the build follows." | L2 05_four: twin, index, agents file; "Specs and briefs are the source. Change the brief, and the build follows." |
| "What crosses?"; shared thing "its own node, with one owner"; "An arrow only where something crosses" | L3 03_test, 05b_shared, 10_rule. |
| Shared contract before anyone starts; own brief, finish line, check; one merge point; whole feature tested; "They meet early" | L4 05a-05d, 10_rule ("Merge early, in one place"). |
| "It moves money, so a person does"; named in the repository; "doesn't classify it, or approve it"; "the change, the evidence, the risk, and the way back"; "An engineer reviews the code" | L5 04_tests, 06_packet, 07_written, 10_rule. |
| "charged the right amount, exactly once"; checks an agent can run; "Write them once, run them twice"; "the miss becomes a fourth check" | L6 04b_define, 05_twice, 07a_loop ("Every miss goes back into the brief, and the checks"). |
| Adding a plan is a skill, "written down, and tested"; "come back often enough" | L7 02_hook, 03_reuse ("written down, tested, and shared"), 08_when ("the third time"). |
| A pipeline; a trigger that is an event; a second trigger on a schedule; "Every step leaves a record"; idempotency key that never changes; reconcile the ledger against the processor's record | L8 04_triggers, 05c_records, 05d_retry, 05e_stop. |
| Own identity, least access, every action logged, a person decides anything that moves money | Lesson 9 outline text (not a recording); referred to as "Lesson nine's question". |
| The four constants | L1 11_constants, word for word except "somebody understands" for "somebody has to understand". |
| "one loop: plan, build, verify" | L3 04_loop_graph; SE101. |
| "You still own the outcome"; "from one loop, to enterprise systems" | Lesson 9 outline; the series title. |

## Technical claims
| Claim | Scene | Basis |
|---|---|---|
| "an agent will build either answer, without asking" | 02 | A statement about the risk the rule addresses, framed as what happens when nothing is written down; consistent with L1/L2/L7 ("Where the page is silent, it guesses"). Not a statistic. |
| An idempotency key that never changes means "a double-click, or a retry, doesn't charge twice" | 12 | Standard behaviour where the processor supports idempotency keys (L8 05d: "many payment processors support one"). Stated as the outcome (no second charge), not as "returns the first result". The dependence on processor support is in the page notes. |
| Reconcile compares our ledger with the processor's record | 12 | Standard practice; L8 05e. |
| Read-only access cannot move money or change the ledger | 13 | Least privilege, as in the lesson 9 outline. |
| "the invoice, the ledger, and the processor all say two eighty" | 14 | Internal consistency of the example: charged $280 (12), "$280 in the ledger" (12). |

## Runtime
852 spoken words. Estimate at 2.6 words/second: 328 s (5:28), inside the 5:30 cap. Lessons 5 to 8 ran about 2.8 words/second as recorded, so the measured length should be a little shorter; measure after narration.

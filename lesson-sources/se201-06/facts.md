# Facts: SE201 Lesson 6, Quality, Feedback, and Observability

Every factual claim in the lesson (spoken or on screen), with its source. Script: `scripts/se201-06-quality.json`.
- **BRIEF** means the owner's brief for lessons 5 to 8 (`briefA.md`): the facts about Clark, the series path and the running example.
- **L1 / L5 / L8** means a lesson of this series (`sitegen/content.json`, `lesson-sources/`, `scripts/se201-08-pipelines.json`).
- **GH** means general industry knowledge, with a well-known reference.
- **LENS** marks a teaching idea written by the scriptwriter. It is presented as a lens or rule of thumb, not as fact or as Clark's quote.
- **MADE-UP** marks an invented illustration, labelled as made-up aloud and on screen.

## About Clark
No claim about Clark, his career or any company is made in this lesson. No company is named.

## Industry terms and history
| Claim | Scene | Source |
|---|---|---|
| A green build says the code did what its tests asked; it says nothing about last night's run | 02_quiz | GH: tests exercise code against test inputs before release; they do not observe production runs. |
| Ten years ago the scarce thing was seeing the whole system | 03a_then | L1's lens (2016 card: "Seeing the whole"). Recalled as "the lens from lesson one". |
| The answer was observability: logs, metrics, traces; they answer "what happened?" | 03a_then | GH: the usual three signals of observability (for example the report "Distributed Systems Observability", 2018; OpenTelemetry's signals). |
| Now the scarce thing is knowing it's right | 03b_now | L1's lens. |
| A service level objective (S.L.O.) is a written target, for example 99.9% of renewals due today attempted by 6 a.m. | 05_twice | GH: SLOs as defined in Google's "Site Reliability Engineering" (2016). The figure is an example, said as "say" and shown as "for example". |
| A charge that times out may still have gone through; a retry with a new key can then charge twice | 06_record | GH: a well-known failure mode of payment APIs; the reason processors offer idempotency keys. |
| "A retry must reuse the same key. That's an idempotency key" | 07a_loop | GH: idempotency keys in payment APIs (for example Stripe's and Adyen's API documentation). L8 covers it ("more in lesson eight"). |
| Reconciling against the processor's own report shows what was really charged | 06_record | GH: standard payment reconciliation against processor settlement reports. |

## Teaching ideas (LENS)
| Claim | Scene | Source |
|---|---|---|
| Architecture bends around what's scarce | 03a_then | L1's lens, framed there as a lens. |
| No dashboard can answer "was it right?" until somebody has written down what right means | 03b_now | LENS. |
| Write right in the business's words, then split it into checks an agent can run | 04b_define | LENS (series outline: "every renewal charged the right amount, exactly once"). |
| Check every renewal, not just the total | 04c_run | LENS, demonstrated by the arithmetic below. |
| Write the check once, run it twice: before a change ships on samples, after every run on the real data | 05_twice | LENS. |
| The checks say something is wrong; the record says why. Every step leaves a line people and agents can read | 06_record | LENS. |
| Every miss goes back into the brief and the checks, so each run improves the next | 07a_loop | LENS (series outline). |
| A check only catches what somebody thought to ask, so a person still reads a sample | 07b_limit | LENS. |

## The worked example (MADE-UP), with the arithmetic
| Claim | Scene | Source |
|---|---|---|
| "A made-up billing system" / "our made-up example: the subscription-billing system from lesson one" | 02_quiz, 04a_green; on-screen labels in 04 and 06 | BRIEF; L1. |
| Six renewals with prices $29, $99, $29, $49, $99, $49: DUE $354.00 | 04a-04c | MADE-UP. 29 + 99 + 29 + 49 + 99 + 49 = 354. |
| CHARGED $354.00: "the totals match" | 04c_run | MADE-UP. 29 + 99 + (2 x 29) + 49 + 119 + 0 = 354. The errors are +29, +20 and -49, which sum to 0. |
| One charged twice (R-1043), one wrong amount (R-1045, $119 against $99), one never attempted (R-1046); each check fails once | 04c_run | MADE-UP; consistent with the table. |
| The record for R-1043: schedule 02:00:03, attempt 1 (key A, timeout) 02:00:04, attempt 2 (key B, charged) 02:00:36, invoice 02:00:37, reconcile 06:10:00 (processor: 2 charges) | 06_record | MADE-UP; times and values invented. |
| "Put last night right, with a person approving, as in lesson five" | 07a_loop | L5 (a refund is a stop for a person). |

## Cross-references
| Claim | Scene | Source |
|---|---|---|
| Next: skills as building blocks, lesson seven | 11_close | BRIEF series path. |

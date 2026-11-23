# Claims toned down or removed: SE201 Lesson 6, Quality, Feedback, and Observability

What was softened or cut between the outline, the round-1 draft (`make_se201_06_quality.round1.py`) and the recorded script, and why.
Round 2 changed nothing in the script (one stale comment in the generator was corrected; the JSON is unchanged).

| Earlier wording (scene) | What happened | Why |
|---|---|---|
| Outline: "logs, metrics and tracing were the answer", stated as history | Recalled as "the lens from lesson one: architecture bends around what's scarce", spoken and on screen. | It is lesson 1's teaching lens, not a settled fact about the industry. |
| Outline: "Picture a subscription-billing system" | Now "Picture a made-up billing system" in the quiz and "our made-up example" in the worked example. | The system has to be called made-up the first time it is heard. |
| Outline: feed back "what it cost" | Cut; the record card reads "what happened, step by step". | The lesson never showed a cost, so the claim had no example. |
| 02 quiz option "Probably" | Now "Probably: coverage is high". | The bare option was a strawman. |
| 04a "The table looks fine... From here, you can't say." | Now "no test ever looked at this table. So was last night right? The green can't say." | The table on screen plainly showed a 2, a wrong amount and a 0, so the narration contradicted it. |
| 04b check "every renewal that was due got charged" | Now "every renewal that was due was attempted"; the flag is "Never attempted". | Declined cards are normal in billing; "charged" was naive. |
| 04c "the totals: only thirty dollars apart... a sum that looks close" | R-1045 is now charged $119.00, so both totals are $354.00: "they match. Three wrong renewals, inside a sum that's exactly right." | A $30 gap is a failed reconciliation, so the total would have caught it and the point backfired. |
| 05 "Here's what makes that sentence powerful." | Now "That one sentence does double duty." | Overselling. |
| 05 S.L.O. "every renewal due today, charged by six A.M." | Now "say, ninety-nine point nine percent of renewals due today, attempted by six A.M.", shown as "for example". | A 100% deadline is not how an S.L.O. is written, and "charged" had the same problem as check 3. |
| 06 "Attempt two: charged. But the first attempt had gone through." | The steps now carry key A and key B, and reconcile reads "processor: 2 charges": "Then reconcile, against the processor's own report: two charges." | "The record says why" was overclaimed; nothing in the record showed the first attempt had gone through. |
| 06 "An agent can read that, and so can you." | Cut. | Repeats the line before it. |
| 07a "a retry must reuse the same request key. And check two stays, for good." | Now "a retry must reuse the same key. That's an idempotency key; more in lesson eight. And a new test: the processor times out." | "Request key" is not the usual term, and nothing said why the green build had missed the bug. |
| 07a began at "Then close the loop" | Now opens "First, put last night right, with a person approving, as in lesson five." | Nobody had corrected the three wrong renewals. |
| 09 rule "after every run, on the real data ... when something goes wrong, add it to the brief" | Now adds "When a check fails, stop and tell a person." | The rule said nothing about what an agent does when a check fails. |
| 10 "three checks I can run on the real data" | Now "three read-only checks". | An exercise that runs on real data should say it must not change anything. |
| Loop caption and lens label on screen | Now the spoken lines themselves. | On-screen text has to match what is said. |

Nothing about Clark or any company was claimed in any draft, so nothing of that kind was removed.

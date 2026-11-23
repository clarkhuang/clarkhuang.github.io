# Facts in SE201 Lesson 8, "Routines, Pipelines, and Integration", and where each comes from

Script: `pipeline/scripts/se201-08-pipelines.json` (generator `pipeline/make_se201_08_pipelines.py`). 14 scenes, 696 spoken words, 246.1 s of narration audio.

The lesson makes no claim about the narrator, about sticky.io, or about any real company, person, incident or number. It contains no statistics; the only numbers are the made-up counts in scene 05c, called made up aloud and on screen. The web sources below are public documentation pages named from general knowledge; they were not re-fetched during round 2, so check the links before publishing them.

## Claims about the world

| Scene | Claim | Basis |
|---|---|---|
| 02 | A charge goes through, the answer is lost, the job retries: "Quite possibly, charged twice. Some processors catch a quick duplicate, but don't count on it. Design the retry to be safe." | A second create-charge request with no idempotency key is a new charge on the widely used payment APIs. A few gateways apply a short duplicate-transaction window by default (for example Authorize.Net's duplicate window), so the retry is not always a double charge; the recorded line now says so ("Some processors catch a quick duplicate, but don't count on it"). The lesson's working claim is that you cannot rely on that. The line was softened after the round-2 review ("Owner's call"); see `BUILD.md`. |
| 03 | "Thirty years ago: overnight batch files, and E.D.I. Then web services. Then an A.P.I. for everything. Now, agents calling tools." On screen: 30 / 20 / 10 YEARS AGO / NOW; "XML over HTTP"; "REST and JSON" | Approximate industry history, the same thirty/twenty/ten-year steps as lesson 1. EDI and batch files are older than thirty years and were the normal way to connect companies in the mid-1990s; XML web services (SOAP) were at their height in the mid-2000s; REST and JSON APIs were the default by the mid-2010s. |
| 03 | "Every one of those is still running somewhere, often inside the same enterprise." | Common knowledge: EDI remains standard in retail supply chains, and overnight files remain normal in banking and payments. "Somewhere" and "often" are the hedges. |
| 04 | Work can start on a schedule, on an event, or when the step before finishes | Standard triggers in schedulers and workflow tools. |
| 04 | "Call a skill plus a trigger a routine. And routines, chained, make a pipeline." | The lesson's own vocabulary, introduced with "call", not presented as an industry definition. |
| 05b | A written format at each hand-off lets a step be rebuilt or rerun without touching the others | Standard interface-contract reasoning (lessons 3 and 4 of this series). |
| 05d | "If the processor has already seen that key, it returns the first result, instead of charging again. That's an idempotency key, and many payment processors support one." | Documented by several processors: Stripe (https://docs.stripe.com/api/idempotent_requests), Adyen (https://docs.adyen.com/development-resources/api-idempotency), Square (https://developer.squareup.com/docs/build-basics/common-api-patterns/idempotency), PayPal (the `PayPal-Request-Id` header). Not universal, hence "many". |
| 05d | A key built from "this subscription, this billing period" never changes between tries | Design advice. A key derived from the business facts survives a crashed job, where a random key made per attempt would not. |
| 05d | Skip renewals already recorded as charged; send every other one with its key | Design advice. The two layers cover each other: a charge that succeeded but was never recorded is sent again and gets the first result back. |
| 05e | Reconcile compares our ledger with the processor's record; on a mismatch, keep every record and tell a person | Standard reconciliation practice. |
| 05e | "Most of these steps are plain code. An agent earns its place where a step needs judgment." | A position, stated as one. |
| 06 | "You can't count on anything arriving exactly once. So design for at least once, and make twice harmless." | Standard distributed-systems reasoning: across a network a sender cannot know whether a lost reply means the message was lost, so reliable delivery means at-least-once delivery plus a receiver that tolerates duplicates. |
| 06 | A partner's file can be late, arrive twice, or be broken | Common experience with file hand-offs; no specific partner or incident is described. |

## Not said in the video; for the lesson page if wanted

- Idempotency keys are kept by the processor for a limited time (Stripe's documentation says keys can be removed once they are at least 24 hours old), so a retry days later needs the local record, which is why the skip step exists.
- Reusing a key with different request details is an error at most processors, and the "first result" returned can be a decline.
- A real retry after a decline is a new attempt and needs a new key (for example, add an attempt number).
- The 12 declined renewals in the example would go to a retry-later and customer-email path, outside this pipeline.

## The worked example (made up)

| Scene | Content | Status |
|---|---|---|
| 05a | The nightly billing run of "our made-up subscription-billing system": find renewals due, charge, invoice, accounting export, reconcile; starts every night at 2:00 | Invented illustration; called made up aloud at first mention; "A MADE-UP EXAMPLE" on all five frames. |
| 05b | Hand-offs: renewals due, charge results, invoices, export file | Invented illustration. |
| 05c | 1,000 due; 988 charged, 12 declined; 988 invoices; 988 rows sent | Invented numbers. "The numbers are made up" aloud; "MADE-UP NUMBERS" on screen. 988 + 12 = 1,000. |
| 05d | Ten blocks standing for renewals: six charged, one unknown, three not reached; on retry six skipped and four sent with keys | Invented illustration. |
| 06 | A partner's nightly file | Part of the series' shared made-up example; no real partner. |

## Threads to other lessons (checked against the brief)

| Scene | Thread |
|---|---|
| 04 | "A skill is one job, written down and tested": lesson 7 |
| 05c | "they have to add up": lesson 1's constant, money has to add up |
| 06 | Chapter title "What you don't control": lesson 1's constant |
| 05e | "tells a person": lesson 5, governance |
| 10 | Bridge: "agents that operate enterprise systems. See you in lesson nine." |

## Production facts

| Item | Value |
|---|---|
| Voice, language, speed | `4lbl0krw73vf`, `en`, 1.05 |
| Speech tags used | `[pause]`, `<emphasis>` only |
| Spelled for speech | "two oh one", "E.D.I.", "A.P.I.", "A.I.", "two A.M." |
| Speech-to-text check | All 14 clips match the script (`asr-check.txt`, lines for `se201-08-pipelines`); "item potency key" and "sink" are the recogniser's spellings of "idempotency key" and "sync" |
| New layout | `pipeline` in `pipeline/se201_layouts_58b.py` |

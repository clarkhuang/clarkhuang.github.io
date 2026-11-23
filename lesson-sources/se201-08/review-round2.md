# SE201 Lesson 8, "Routines, Pipelines, and Integration": critique, round 2 (after narration and render)

Reviewed: `scripts/se201-08-pipelines.json` as narrated and rendered (14 scenes, 696 spoken words, 246.1 s of narration audio, about 4:06 before scene padding), all 14 stills in `stills-08/`, the rendered-video still `/workspace/se201-l5to8-stills/08-pipelines.png`, and the speech-to-text lines for the 14 clips in `asr-check.txt`. The generator `make_se201_08_pipelines.py` was rerun in a scratch copy and its output is byte-identical to the JSON that was narrated.

## Verdict

**No major problem. Nothing changed. No re-narration and no re-render needed.**

One item (the quiz answer, below) is the closest thing to a factual objection in either lesson. It is defensible as recorded and is left for the owner to decide; it is not applied.

## Checks against the four "major" tests

| Test | Result |
|---|---|
| Anything wrong | None found. Closest call: 02 quiz, see "Owner's call". |
| A claim beyond the facts | None. Idempotency keys are "many payment processors support one", not "all". History is approximate and correct. |
| Rule inconsistent with its own examples | Consistent. See "Rule vs examples". |
| On-screen text contradicting narration | None in any of the 14 scenes. Screen-only additions are listed under minor. |

## Owner's call (not applied)

**02 quiz: "Charged twice. Unless someone designed that retry to be safe."** For a plain retried charge request with no key this is the right default, and it is what the dominant payment APIs do. But a few gateways apply a short duplicate-transaction window by default, so option C ("the processor catches it on its own") is sometimes true in the real world, and a payments engineer could say so. Why it is not major: the narration's own qualifier ("unless someone designed that retry to be safe") and 05d's "many payment processors support one" keep the lesson's actual claim to "you cannot rely on it". If scene `02_quiz` is ever re-recorded for another reason, the safer line is: "Quite possibly, charged twice. Unless someone designed that retry to be safe." That is one narration scene and no screen change.

## Claims

- **Idempotency key (05d).** "If the processor has already seen that key, it returns the first result, instead of charging again... many payment processors support one." Correct and hedged. Round 1's "the processor has seen that key" is now "if". Building the key from subscription plus billing period is sound and survives a crashed job.
- **Skip what is recorded as charged; send every other renewal with its key (05d).** Sound, and the screen shows it: six skipped, the uncertain one and the three never attempted all sent with keys. The caption says the same thing.
- **"You can't count on anything arriving exactly once. So design for at least once, and make twice harmless" (06).** Standard and correctly stated.
- **History (03).** Batch files and EDI thirty years ago; web services (XML over HTTP); an API for everything (REST and JSON); agents calling tools; "every one of those is still running somewhere, often inside the same enterprise". Approximate and correct. Round 1's "talks to all four" is gone.
- **Reconcile (05e).** "Doesn't guess, and doesn't fix the numbers itself. It keeps every record, and tells a person." Right. "Most of these steps are plain code. An agent earns its place where a step needs judgment" is the line an experienced engineer wants to hear.
- **Counts (05c).** 1,000 due = 988 charged + 12 declined; 988 invoices; 988 rows sent. They add up; called made up aloud and on screen.
- **Worked example.** "our made-up subscription-billing system" aloud at first mention (05a); "A MADE-UP EXAMPLE" on all five pipeline frames. The quiz scenario in 02 comes before that label but names no company and is plainly hypothetical. No narrator claims.
- **Speech.** Only `[pause]` and `<emphasis>`; "E.D.I.", "A.P.I.", "A.I.", "A.M." spelled out. ASR of all 14 clips matches the script; "item potency key" and "sink" are the recogniser's spellings of "idempotency key" and "sync", so the audio is right.

## Rule vs examples

Rule 8: before any work runs on its own, write down what starts it, what crosses at each hand-off, what record each step leaves, and what happens when a step fails or runs twice.

| Rule part | Where the lesson shows it |
|---|---|
| What starts it | 04 (three triggers); 05a ("EVERY NIGHT AT 2:00") |
| What crosses at each hand-off | 05b (four labelled hand-offs, "a clear, written format") |
| What record each step leaves | 05c (a record under each step; counts that add up) |
| Fails, or runs twice | 05d (dropped connection, safe retry), 05e (mismatch: tell a person), 06 (file late, twice, broken) |

The recap's four lines are the same four in the same order. The quiz in 02 is answered in 05d ("Back to two A.M."). Your-turn asks the rule's last two questions of a real job. Consistent.

## Is it better than lessons 1 to 4?

Yes: the strongest hook of the eight (a question with money on it, answered later by the lesson itself), one pipeline diagram held across five scenes with a different layer lit each time, and the only lesson so far where the diagram shows a failure and its recovery step by step. It is the densest lesson; 05d at 88 words is the limit of what one scene should carry.

## Minor issues: NOT applied (not worth a re-record)

1. **02 quiz answer**: see "Owner's call".
2. **04 vs 05e vocabulary.** 04 defines a routine as "a skill plus a trigger" and a pipeline as routines chained; 05e then says most steps are plain code. Lesson 7 covers the gap ("when a step needs no judgment, make it a script the skill calls"), but lesson 8 alone does not say it. One clause in 04 would fix it. Narration change; not applied.
3. **05b hand-off into Reconcile is labelled "export file"**, while 05e reconciles the ledger against the processor's record. The four labels follow the linear chain as narrated; a purist would draw a second arrow from Charge to Reconcile. Screen-only; not applied because the frames are a held group of five rendered scenes.
4. **05c does not say where the 12 declined go** (retry later, email the customer). Out of scope for the scene; belongs on the lesson page.
5. **05d omits real-world limits of idempotency keys**: keys are retained for a limited time, the same key with a different request is an error, the "first result" can be a decline. None belongs in narration; noted in the facts file for the lesson page.
6. **Screen-only text not spoken** (additions, not contradictions): 03 tags "20 YEARS AGO" and "10 YEARS AGO" and subs "XML over HTTP", "REST and JSON", "On top of those APIs"; 06 "As expected: load it"; 05a tags "CALLS THE PROCESSOR", "LEAVES OUR SYSTEM". Leave.
7. **03 "the oldest problem in this series"** is a slightly odd superlative for a first-time viewer. Leave.
8. **10 close** asks three questions before the bridge; it runs 46 words. Could lose one. Leave.

## What changed between round 1 and round 2

Round 1 to the recorded script: quiz option C reworded to "The processor catches it on its own"; "often inside the same enterprise" replaces "talks to all four"; "Call a skill plus a trigger a routine"; "accounting system", "charged" and "rows sent" wording; "the run stops there" added to 05c; 05d rewritten (every unrecorded renewal is sent with its key; "if the processor has already seen that key"); 05e no longer says the pipeline "stops" after the export has gone, and the alert reads "Don't guess. Keep every record. Tell a person."; 06 rewritten around "You can't count on anything arriving exactly once"; recap drops the vocabulary line; the rule's last line is spoken; close asks "whose name does it run under?".

Round 2 to now: nothing.

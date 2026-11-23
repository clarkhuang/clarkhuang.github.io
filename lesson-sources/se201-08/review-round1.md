# SE201 Lesson 8, "Routines, Pipelines, and Integration": critique, round 1

Draft reviewed: `make_se201_08_pipelines.py` (14 scenes, 738 spoken words, est. 284 s at 2.6 w/s, before the 12 `[pause]` tags) and the 14 stills in `stills-08/`. Compared against Lesson 1 (`make_se201_01_four_eras.py`) and Lesson 4 (`make_se201_04_parallel.py`).

Limits of this review: I saw one late frame per scene, so animation timing is inferred from the `at` values, not watched. I did not hear audio. The processor-specific details under Facts are from my own knowledge of the public API docs, not re-fetched here; they must be sourced in the facts file (see problem 3).

Verdict: the best worked example in the series so far, with one real technical flaw in the retry scene, one logical flaw in the reconcile scene, a quiz option that is the lesson's own answer, and 38+ words too long. None of it needs a restructure.

## What already beats lessons 1-4

- **Hook with stakes.** A customer charged twice at 2 a.m. is more concrete than lesson 1's "what's scarce?" and lesson 4's "is the system done?". It starts about 5 seconds in, and scene 05d returns to it by name. Lessons 1 and 4 never close their own quiz that explicitly.
- **One diagram carried through five scenes, and it grows.** Stages, then hand-off labels, then records, then a zoom inside one stage, then the last stage lit. Lesson 4 reuses `lanes`; this one accumulates. 05d (first try / retry blocks, the key callout) is the best single frame in the series.
- **Numbers that do work.** 1,000 = 988 + 12; 988 invoices; 988 rows. The numbers are the argument ("they have to add up"), not decoration. Lesson 1 has no numbers; lesson 4's are timestamps.
- **The exercise uses the AI.** "Describe its steps to your AI and ask, for each step..." is a real task. Lesson 4's your-turn never involves an AI.
- **Honest about agents.** "Most of these steps are plain code. An agent earns its place where a step needs judgment" is the line an experienced engineer will trust the lesson for.
- **The close is a question, not an announcement.** Three questions that are exactly lesson 9's outline (identity, access, audit).

## Where it is not better than lessons 1 and 4

- Lesson 4 had a real example with real timestamps; everything here is made up. Acceptable under the constraints, but it is why the technical claims must be airtight.
- Lesson 1 has a caveat scene ("not settled"). This lesson states idempotency as if it closes the problem; the limits (problem 2, 5) are not acknowledged anywhere.
- There is no first-person voice at all. Lesson 1 has the career scene, lesson 4 has "for me to approve". A payments lesson narrated by someone with a payments background never says "I". See Tone.
- Scene 04 teaches vocabulary by equation; it is the flattest scene and weaker than lesson 4's `03_broken`.
- It is over length; lessons 1 and 4 are not.

## Problems

1. **Major. Quiz option C is the lesson's own answer.** "The processor catches it" is what an idempotency key makes true (05d: "the processor has seen that key, so it returns the first result"). Also, some gateways do have a short built-in duplicate-transaction window, so a payments engineer will say C is sometimes right with no design at all. The spoken answer ("charged twice, unless someone designed that retry to be safe") is correct as a default: a plain retry is a new charge request. The option is what is unfair. **Fix:** make C "The processor catches it on its own", spoken "Or the processor catches it on its own?". Then B-with-the-caveat is clearly the answer and C is clearly the thing you cannot count on. Record the duplicate-window point in the facts file.

2. **Major. 05d describes the retry less correctly than the picture shows it.** Three issues in three sentences:
   - "For the one we're not sure about, it sends the same request, with the same key." The job generally cannot tell "sent, no answer" from "never sent" unless it recorded intent first, and it does not need to. The sound design, and what the still shows (blocks 7 to 10 all go out on the retry), is: skip what is recorded as charged; send *every other* renewal with its key.
   - "The processor has seen that key, so it returns the first result." Two sentences earlier: "Did it go through? We don't know." The narration then asserts it did. The point of the key is that it is right either way: seen, you get the first result; not seen, it charges, once. Say "if".
   - Caption: "resend the rest with the same key" reads as one key for everything.
   
   **Replacement narration (88 words, was 95):** "Back to two A.M. Partway through the charge step, the connection drops. One charge went out, and no answer came back. Did it go through? We don't know. [pause] So the retry has to be safe to run twice. Renewals already recorded as charged, it skips. Every other one, it sends with a key that never changes: this subscription, this billing period. If the processor has already seen that key, it returns the first result, instead of charging again. That's an idempotency key, and many payment processors support one."
   **Replacement caption:** "Safe to run twice: skip what’s recorded as done; send the rest, each with its own unchanging key."

3. **Major. `se201-08-facts.md` does not exist.** The generator's docstring says "every factual claim and its source is in se201-08-facts.md". I could not find that file anywhere under `/workspace/legacy`. The idempotency claims need public sources (the idempotency sections of at least two processors' API docs) and the two known limits written down (problem 5). Lesson 4's review had a facts file to check against; this one has nothing.

4. **Major. "It stops" at the last step stops nothing, and the export has already left.** Reconcile is step five. By then the accounting export (tagged "GOES TO A PARTNER") has been sent. "The pipeline ... stops, keeps every record, and tells a person" is the right instinct in the wrong place: an experienced engineer will ask "stops what?". The lesson already has the right place: 05c says the counts must add up from step to step. Put the stop there, where it prevents something (988 charged but 950 invoices: do not export), and let reconcile be the independent last check that reports. **Fix, 05c ending:** "The numbers are made up, but they have to add up. When they don't, the run stops there, and you know which step to open." **Fix, 05e opening (was "And the last step is the safety net ... tells a person"):** "Last, reconcile compares our ledger with the processor's record. If they don't match, the pipeline doesn't guess, and doesn't fix the numbers itself. It keeps every record, and tells a person." **Alert box:** "Doesn’t match?\nDon’t guess. Keep every record.\nTell a person."

5. **Minor (narration), required (facts file / lesson page). Two limits of idempotency keys the lesson implies away.** (a) Keys expire: processors keep them for a limited window (on the order of a day to a week, depending on the processor). A retry that runs the next night can be past it. The lesson's own design covers this, because it skips on its own record first and reconciles last; say so on the lesson page. (b) "Returns the first result" includes a first *decline*. A key of "subscription + billing period" would replay that decline for a later legitimate retry of the 12 declined cards in the same period; real keys usually include the attempt. Do not add this to the narration; put one line on the lesson page so the payments reader sees it was considered.

6. **Major (cheap). 06: "expect it at least once" is wrong for the example on screen.** The same scene says the file can be late, which includes never. At-least-once is something you arrange (retry until acknowledged), not something you can expect from a partner. And "exactly once is hard to guarantee" blurs delivery with effect: lesson 6's outline promises "charged ... exactly once" as the check, and 05d has just achieved it. **Replacement:** "You can't count on anything arriving exactly once. So design for at least once, and make twice harmless." **Caption:** "Design for at least once. Make twice harmless."

7. **Major. The recap leaves out failure and repeats vocabulary.** "Skill plus trigger is a routine" is said in 04, captioned in 04, and takes the first recap line, while "when it doesn't match, stop and tell a person" (05e, 06, and the rule's fourth clause) is not in the recap at all. Recap and rule disagree: recap says "every step is safe to run twice"; the rule says "what happens when a step fails, or runs twice". **Replacement narration (36 words):** "So, to recap. Give every hand-off a clear format. Make every step leave a record that adds up. Make every step safe to run twice. And when the numbers don't match, stop, and tell a person." **Items:** "A clear format at every hand-off" / "Every step leaves a record that adds up" / "Every step is safe to run twice" / "Doesn’t match? Stop, and tell a person".

8. **Minor. "GOES TO A PARTNER" contradicts "send the export to accounting".** Accounting is normally your own department or ledger system. Either tag it "LEAVES OUR SYSTEM" and say "to the accounting system", or drop the tag. (Preferred: the first; both amber stages are then "where we touch something we don't control", which sets up scene 06.)

9. **Minor. "what the processor says it collected".** At 2 a.m. the processor has authorized and captured, not settled or funded. A payments engineer hears "collected" as money in the bank. Say "charged". (Real reconciliation also has a later leg against settlement and the bank; one line on the lesson page is enough.)

10. **Minor. 03: "A real enterprise system talks to all of them" / on screen "it talks to all four" is an overclaim.** Many talk to two or three. **Replacement for the last two sentences:** "And every one of those is still running somewhere, often inside the same enterprise." **System box:** "One enterprise, today: often several of these at once". Also note for the facts file: EDI is far older than thirty years; "30 YEARS AGO" is fine as "what integration looked like then", which is how lesson 1 used it. No wince.

11. **Minor. On-screen text that is not spoken, or differs from what is spoken** (the stated constraint):
    - 04: box says "When the last step finishes"; narration says "the step before it". "Last step" also reads as "final step". Change the box to "When the step before finishes".
    - 05a: caption "Five routines, chained. The first starts on a schedule; each of the others, when the one before finishes." is 19 unspoken words at near full width (ends about x=1775 of 1920; it fits, barely). Replace with "Five steps, chained. The first starts on a schedule." and size it up.
    - 05c: spoken "rows exported", screen "988 rows sent". Say "rows sent".
    - 05d: "subscription 1042" is never spoken. Acceptable under the "MADE-UP EXAMPLE" label; or change to "key = this subscription + this billing period".
    - 06: "Check it first / Complete? Seen before?" and "On time, complete: load it" are unspoken. Add "Check it first." to the narration (done in the cut list); the fourth outcome can stay as diagram completeness.
    - 08: screen "No answer?" vs spoken "If there's no answer to that last one". Different meaning. Speak the screen version: "No answer? It isn't ready to run unattended." (saves 6 words, and "any of the four" is the better rule).
    - 03: "XML over HTTP", "REST and JSON", "On top of those APIs" are unspoken subs. Same practice as lesson 1's era cards; leave.

12. **Minor. 04 presents the series' vocabulary as if it were the industry's.** Engineers call this a scheduled job, a workflow, a DAG. "A skill plus a trigger is a routine" stated flat invites "says who?". Frame it as naming: "Call a skill plus a trigger a routine." Also "A skill is one job ... and run when someone asks" is clumsy; "that runs when someone asks".

13. **Minor. "Five routines" versus "most of these steps are plain code".** 04 defines a pipeline as chained skills; 05e says most steps are plain code. Not a contradiction (a skill is a written, tested job, whoever runs it) but the caption "Five routines, chained" sharpens it for no gain. "Five steps, chained" (see 11) removes it.

14. **Minor. Hand-off labels are the smallest text in the lesson and the subject of 05b.** "renewals due", "charge results", "invoices", "export file" render at roughly 20 px, and dimmer still in 05e. Enlarge by about half in 05b.

15. **Minor. 05a and 05b frames are empty below y=700** (40% of the frame) because the layout reserves room for records and the retry panel. 05a lasts about 18 s on that frame. Either move the caption down and size it up in those two scenes, or accept it; it is not a defect, it is just thin.

16. **Minor. 05e still shows a green tick on "Ledger matches the processor" and an amber "Doesn’t match?" box hanging from the same record.** Readable as "if not", but confirm in motion that the alert arrives on "If they don't match" (alert `at` 0.3 looks right for the new wording) and consider a dashed arrow.

17. **Minor. Spelling and TTS.** "recognise" (06 narration and box) is British; the other generators use "labeled". Use "recognize". "A.P.I.s" in 05d is a TTS risk (may be read "A P I S"); the replacement in problem 2 says "payment processors" and removes it. Listen to "idempotency" in the rendered clip before accepting it.

18. **Minor. Close.** "So who is it?" is abrupt when heard once. **Replacement:** "So whose name does it run under?" Outro sub is "Software Engineering 201" on a half-empty frame; lesson 4 used the next lesson's title. Use "Next: agents that operate enterprise systems" (it is spoken).

19. **Minor. The 12 declined go nowhere.** An engineer will ask. No narration; if anything, one line on the lesson page ("declined renewals go to a separate retry schedule").

20. **Note, no change. Charge before invoice.** Many billing systems raise the invoice first and collect against it. The order is fixed by the series brief and is defensible for a made-up system (the invoice here is a receipt). Leave.

## Facts

- **Quiz: "charged twice, unless the retry was designed to be safe."** Correct as a default for a plain retried charge request. Unfair only because option C describes the designed fix and, on some gateways, a built-in duplicate window. Fix in problem 1.
- **Idempotency keys; "many payment APIs support this".** Correct and properly hedged. Widely documented by major processors (a client-supplied key or request ID on create-payment calls). Not universal; some gateways rely on a duplicate window instead. "Many" is the right word. Needs sources in the missing facts file.
- **"The processor returns the first result instead of charging again."** Correct in substance for a repeated key within the key's retention window and with the same request parameters. Not stated: retention is limited; a changed request body with the same key is an error; a request still in flight may return a conflict; the "first result" can be a decline or an error. None need narration; see problem 5.
- **"The processor has seen that key."** Unsupported by the scene's own premise ("we don't know"). Must be "if". Problem 2.
- **Deriving the key from subscription + billing period.** Sound, and better than a random key because it survives a crashed job. Naive about attempts after a decline. Problem 5.
- **Skip "recorded as charged", resend the rest with the key.** Sound design, and the two layers cover each other: a charge that succeeded but was never recorded locally is resent and returns the first result. Only sound if *every* unrecorded renewal carries its key, which is why the "the one we're not sure about" wording has to go.
- **"Exactly once is hard to guarantee between systems; expect at least once and make twice harmless."** First half true and suitably hedged (exactly-once delivery cannot be relied on across a network; exactly-once effect is built from at-least-once plus idempotent handling). "Expect" is wrong for a partner file that may never arrive. Problem 6.
- **History: batch files and EDI, web services, APIs, agents calling tools; "every one is still running somewhere".** Approximate and correct. EDI and batch predate the thirty-year mark and are still heavy in retail and in payments (overnight files remain normal). XML web services peaked around twenty years ago. REST and JSON "for everything" about ten years ago is fair. "Talks to all four" is the overclaim. Problem 10.
- **Reconciliation last; "stop and tell a person".** Reconciling ledger against the processor is standard and "don't guess, tell a person" is right. "Stop" at the final step, after the export has gone, is not. Problem 4. "Collected" should be "charged". Problem 9.
- **Counts.** 1,000 due = 988 charged + 12 declined; 988 invoices; 988 rows. They add up. Labelled made up on screen in 05c and aloud ("The numbers are made up").
- **Worked-example constraint.** "our made-up subscription-billing system" is said aloud on first mention (05a); every pipeline frame is labelled "A MADE-UP EXAMPLE". No company named. Pass.
- **Narrator constraint.** No personal facts, anecdotes, names or company details appear. Pass (see Tone for the cost).
- **Statistics.** None. Pass.
- **Speech tags.** Only `[pause]` and `<emphasis>`. "E.D.I.", "A.P.I.", "A.I." spelled out. Pass, with the "A.P.I.s" risk in problem 17.
- **Overflow / overlap / clipping.** None in any of the 14 stills. Tightest: 05a caption (right edge about x=1775), rule card line 5 (about x=1647), 05d caption under the panel (clear by about 20 px).

## Tone

A calm, competent professor; nothing jokey, forced or condescending. "Did it go through? We don't know." is the best beat. "The steps with no good answer are where to start" is a good last line for the exercise.

Two notes. First, it is impersonal: no "I" anywhere, in the one lesson that sits on the narrator's own ground. (A suggested first-person line was removed from this public copy; it was never recorded.) Second, "Notice, too:" and "And the last step is the safety net" are filler in the densest scene; both go in the cut list.

Ideas are framed as rules of thumb, not as the narrator's beliefs. Pass.

## Rule vs examples

Rule: before work runs on its own, write down what starts it, what crosses at each hand-off, what record each step leaves, and what happens when a step fails or runs twice.

- What starts it: 04 (three triggers), 05a (the 2:00 pill). Shown.
- What crosses: 05b. Shown.
- What record: 05c. Shown.
- Fails or runs twice: 05d (twice), 05e and 06 (fails). Shown, with the "stop" flaw in problem 4.

Consistent. Three gaps: the recap does not match the rule (problem 7); the spoken last line narrows "no answer" to the fourth item while the card does not (problem 11); and nothing in the rule is specific to agents or says where the note lives (rule 1 said "in the repository"). The card's foot, "THE FULL RULE IS ON THE LESSON PAGE", can carry that: the page version should add "and keep it where the agent that runs the job can read it". No narration change.

Stands alone without lessons 1-7: yes. "Skill" is defined in one clause, the made-up system is introduced as made up, and the only series reference ("the oldest problem in this series") does not need the earlier lessons.

## Specific cuts to reach <= 700 words

Per-scene now: title 11, quiz 63, oldest 47, triggers 66, run 46, hand-offs 38, records 66, retry 95, stop 60, partner 57, recap 37, rule 56, ask 53, close 43 = 738.

Proposed, including every wording fix above (target just under 700):

| Scene | Now | After | Change |
|---|---|---|---|
| 02_quiz | 63 | 62 | "A job charges a customer's card." (drop "for a renewal"); "What happens? Nothing? The customer is charged twice? Or the processor catches it on its own?" |
| 03_oldest | 47 | 43 | Last two sentences become "And every one of those is still running somewhere, often inside the same enterprise." |
| 04_triggers | 66 | 60 | "A skill is one job, written down and tested, that runs when someone asks. But some work should start on its own. On a schedule: every night at two. On an event: a payment fails, or a file arrives. Or when the step before it finishes. [pause] Call a skill plus a trigger a routine. And routines, chained, make a pipeline." |
| 05a_run | 46 | 48 | "...Send the export to the accounting system. And last, reconcile: does our ledger match what the processor says it charged?" |
| 05b_handoffs | 38 | 36 | "Give each a clear, written format." (drop "of those") |
| 05c_records | 66 | 58 | "...Nine hundred eighty-eight invoices, and as many rows sent. The numbers are made up, but they have to add up. When they don't, the run stops there, and you know which step to open." (drops "but notice what they do", "from one step to the next", "exactly") |
| 05d_retry | 95 | 88 | Full replacement in problem 2. |
| 05e_stop | 60 | 55 | "Last, reconcile compares our ledger with the processor's record. If they don't match, the pipeline doesn't guess, and doesn't fix the numbers itself. It keeps every record, and tells a person. [pause] Most of these steps are plain code. An agent earns its place where a step needs judgment, like working out why they don't match." |
| 06_partner | 57 | 52 | "The same thinking covers everything you don't control. Take a partner's nightly file. Check it first. Late: wait, then alert. Twice: recognize it, and skip it. Broken: set it aside, and tell a person. [pause] You can't count on anything arriving exactly once. So design for at least once, and make twice harmless." |
| 07_recap | 37 | 36 | Replacement in problem 7. |
| 08_rule | 56 | 50 | Last sentence becomes "No answer? It isn't ready to run unattended." |
| 09_ask | 53 | 52 | "a nightly report, or a sync" (drop "a deploy") |
| 10_close | 43 | 46 | "So whose name does it run under?" |
| 01_title | 11 | 11 | none |

Total: about 697 words, about 268 s at 2.6 w/s before pauses. With 12 pauses that is close to the 4:30 ceiling, so if the render exceeds it, cut next, in this order: (1) 05b "Then any one step can be rebuilt, or rerun, without touching the others." down to "Then any step can be rebuilt without touching the others." (-4); (2) 09 "a nightly report, or a sync" (-6); (3) two of the twelve `[pause]` tags (the ones in 04 and 06). Do not cut the agent sentence in 05e or "Did it go through? We don't know."

## Changes to make

- Write `se201-08-facts.md` with public sources for idempotency keys, the duplicate-window point, key retention, and the decline-replay limit.
- 02: option C "The processor catches it on its own" (screen and speech).
- 03: soften "talks to all four" (speech and system box).
- 04: "Call a skill plus a trigger a routine"; box 3 "When the step before finishes".
- 05a: "accounting system", "charged" not "collected"; caption "Five steps, chained. The first starts on a schedule."; tag "LEAVES OUR SYSTEM".
- 05b: larger hand-off labels.
- 05c: "rows sent"; add "the run stops there".
- 05d: replacement narration and caption (every unrecorded renewal goes with its key; "if the processor has already seen that key").
- 05e: drop "stops"; alert box "Don’t guess. Keep every record. Tell a person."
- 06: "recognize"; "Check it first."; "You can't count on anything arriving exactly once. So design for at least once"; caption to match.
- 07: recap drops the vocabulary line, adds "Doesn’t match? Stop, and tell a person".
- 08: speak "No answer? It isn't ready to run unattended."
- 10: "whose name does it run under?"; outro sub "Next: agents that operate enterprise systems".
- Lesson page only: key expiry, attempt number in the key, where the 12 declined go, settlement as the later reconciliation leg, and "keep the note where the agent can read it".
- After re-render: check the 05d key callout lands on "a key that never changes", the 05e alert lands on "If they don't match", listen to "idempotency", and confirm runtime is at or under 4:30.

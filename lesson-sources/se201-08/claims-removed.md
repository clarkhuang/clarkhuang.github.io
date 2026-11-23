# SE201 Lesson 8: claims softened or removed, and why

All of these were changed between the first draft and the recorded script (round 1). Round 2 changed nothing. The "first draft" column quotes or summarises the wording recorded in the round-1 review (`se201-08-review-round1.md`); the first-draft script itself was overwritten by the revision.

| Scene | First draft | Recorded | Why |
|---|---|---|---|
| 03_oldest | One enterprise "talks to all four" | "Every one of those is still running somewhere, often inside the same enterprise." On screen: "often several of these at once". | Not every enterprise runs all four. "Somewhere" and "often" are what can be defended. |
| 05d_retry | "The processor has seen that key" | "If the processor has already seen that key, it returns the first result, instead of charging again." | The scene's premise is that we don't know whether the charge went through, so it has to be "if". |
| 05d_retry | The retry resent only "the one we're not sure about" with a key | "Renewals already recorded as charged, it skips. Every other one, it sends with a key that never changes." | The design is only safe if every unrecorded renewal carries its key, not just the doubtful one. |
| 05d_retry | "many payment APIs support this" | "That's an idempotency key, and many payment processors support one." | The hedge "many" was already there and was kept: common, not universal. Some gateways use a duplicate-transaction window instead. |
| 05e_stop | The pipeline "stops" on a mismatch | "the pipeline doesn't guess, and doesn't fix the numbers itself. It keeps every record, and tells a person." | Reconcile is the last step; the export has already gone, so "stops" claimed something the diagram could not do. |
| 05a_run | "what the processor collected" | "what the processor says it charged" | Charged and collected (settled) are different events; the pipeline only knows the first. |
| 06_partner | "Exactly once is hard to guarantee... expect at least once" | "You can't count on anything arriving exactly once. So design for at least once, and make twice harmless." | A partner's file may never arrive, so "expect at least once" was wrong. "Design for" is the accurate verb. |
| 04_triggers | "A routine is a skill plus a trigger" (as a definition) | "Call a skill plus a trigger a routine." | It is this series' vocabulary, not an industry definition. |
| 02_quiz | Option C described the designed fix | Option C: "The processor catches it on its own" | The wrong options must be wrong for a reason the lesson explains. |
| 05c_records | Ended on an aside after the counts | "The numbers are made up, but they have to add up. When they don't, the run stops there, and you know which step to open." | The counts were already labelled made up aloud and on screen; the new ending says what a mismatch does, instead of leaving "add up" as a slogan. |
| 07_recap | A line restating the routine/pipeline vocabulary | Replaced with "when the numbers don't match, stop, and tell a person" | The recap should carry the practice, not the terms. |

## Kept out from the start

- No statement that the narrator, sticky.io, or any real company ran this pipeline, had a double charge, or received a bad partner file. The example is called made up aloud and on screen.
- No named processors, gateways, schedulers or workflow tools.
- No statistics (for example, no failure rates or decline rates; "12 declined" is a labelled made-up count).
- No claim that agents should run the pipeline's steps: "Most of these steps are plain code."

## Flagged in round 2

- 02_quiz: "Charged twice." was said flatly. A few gateways catch an immediate duplicate by default, so the third option is sometimes true. After round 2 the answer was softened and that one scene re-narrated: "Quite possibly, charged twice. Some processors catch a quick duplicate, but don't count on it. Design the retry to be safe." The lesson was re-rendered with it. 05d's "many payment processors support one" is unchanged.
- 05d: the limits of idempotency keys (limited retention, same key with a different request, a replayed decline) are not spoken. They are listed in `se201-08-facts.md` for the lesson page.

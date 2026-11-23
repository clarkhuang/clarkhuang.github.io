# SE201 Lesson 7, "Skills as Building Blocks": critique, round 2 (after narration and render)

Reviewed: `scripts/se201-07-skills.json` as narrated and rendered (15 scenes, 696 spoken words, 233.7 s of narration audio, about 3:54 before scene padding), all 15 stills in `stills-07/`, the rendered-video still `/workspace/se201-l5to8-stills/07-skills.png`, and the speech-to-text lines for the 15 clips in `asr-check.txt`. The generator `make_se201_07_skills.py` was rerun in a scratch copy and its output is byte-identical to the JSON that was narrated.

## Verdict

**No major problem. Nothing changed. No re-narration and no re-render needed.**

Every round-1 "change to make" is present in the recorded script. The remaining issues below are polish; none is wrong, beyond the facts, inconsistent with the rule, or a screen/narration contradiction.

## Checks against the four "major" tests

| Test | Result |
|---|---|
| Anything wrong | None found. See "Claims" below. |
| A claim beyond the facts | None. The "same result, whoever runs it" overclaim from round 1 is gone; 07 now says "No guarantee: agents still vary. That's what the checks are for." |
| Rule inconsistent with its own examples | Consistent. See "Rule vs examples". |
| On-screen text contradicting narration | None in any of the 15 scenes. Screen-only additions are listed under minor. |

## Claims

- **"Several agent tools now share a format for this: a folder, with an instruction file."** True: the Agent Skills format (a folder with `SKILL.md`) is an open format read by tools from several vendors. "Several" is the right size of claim.
- **"It starts with when to use it... That line is how an agent finds the skill."** True of the real format (the description is what an agent sees before it loads the rest). The card's five sections are the lesson's own structure and the frame says "A MADE-UP EXAMPLE".
- **Libraries, frameworks, services, "roughly in the order they became common".** Hedged on screen; correct as hedged. "All three reuse software" is accurate for services too (round 1's "packages code" is gone).
- **"If that sounds like a runbook, it is. Engineers have written those for decades."** True, and it is the line that stops an experienced engineer from objecting.
- **"An agent reads the skill on every run, with no memory of the last. Where the page is silent, it guesses."** True of a fresh session, which is the case the lesson set up in the hook ("a different agent starts from zero"). See minor 1.
- **"The third time"**: labelled a rule of thumb aloud and on screen. Correct framing.
- **Worked example**: called "our made-up subscription-billing system" aloud at first mention (02) and "A MADE-UP EXAMPLE" on screen in 02 and 04a to 04d. No company, person, number or incident. No narrator claims at all.
- **Speech**: only `[pause]` and `<emphasis>`; "A.P.I." and "A.I." spelled out; ASR of all 15 clips matches the script (differences are punctuation and "eight"/"8").

## Rule vs examples

Rule 7: third time, write it as a skill (when to use it, inputs, steps, checks, traps); keep it in the repo; test with a fresh agent; when a run goes wrong, fix the skill, not just the run.

- The five parts named in the rule are exactly the five headings on the card, in the same order (04a to 04d).
- The hook's two failures are both caught by the card: the skipped tax setup by step 2 and the check "tax included"; the in-place price edit by step 1 ("as a new version"), the check "existing subscribers renew at their old price", and the trap.
- "Fix the skill" is shown (07: `v1` becomes `v2`, "Fixed once, here").
- "Third time" and the hook: the hook's three unscripted runs are the cost of not having the skill by the third time, and 08 adds "Sooner, if a mistake costs money", which is this very job. Consistent, though the lesson never says so out loud (minor 2).
- Your-turn ("a job you've explained more than twice", "give only that page to a fresh chat") is the rule in miniature.

## Is it better than lessons 1 to 4?

Yes on hook (a question in the first sentence and a concrete three-run failure inside 30 seconds), on the worked example (one job carried from failure, to page, to rerun), and on visuals (the skill card that fills in over four scenes; the before/after drift grid). The recap and rule are shorter than lesson 4's. Weakest stretch: 03 (units of reuse) is the one scene that is a history aside rather than the example.

## Minor issues: NOT applied (not worth a re-record)

1. **05, "with no memory of the last".** Some agent tools keep memory between sessions. The sentence is true for the fresh agent the lesson is about; "often with no memory of the last" would be safer. Narration change; not applied.
2. **08 does not connect the rule of thumb to the hook.** One clause ("our price job should have been written sooner") would close the loop. Narration change; not applied.
3. **04d, "so nobody repeats it"** is a shade stronger than 07's "No guarantee: agents still vary". The check in 04c is what actually backs it. Not applied.
4. **Rule card omits "sooner, if a mistake costs money"**, which 08 says aloud. The card's foot says "THE FULL RULE IS ON THE LESSON PAGE"; the clause is in the full rule in `se201-07-page.md`. No video change.
5. **Screen-only text not spoken** (additions, not contradictions): 03 tag "NOW, ALSO" on Skills; 06 tag "REVIEWED WHEN IT CHANGES" is spoken, but the node sub "Never seen the job" is paraphrased; 07 "ONE SKILL, ONE PLACE" and "Fixed once, here". Leave.
6. **04b step 4 "Open a pull request"** assumes plans and prices live in the repository. Reasonable for the made-up system and consistent with "keep it in the repo"; not explained. Leave.
7. **03 is the least concrete scene.** It could be eight seconds shorter. Leave.
8. **Real `SKILL.md` files carry a name and description header** that the card does not draw. Covered by "A MADE-UP EXAMPLE"; mention on the lesson page if wanted.

## What changed between round 1 and round 2

Round 1 to the recorded script: removed "Same result, whoever runs it" and added the no-guarantee line; `v1` to `v2` swap in 07; "no memory of the last / where the page is silent, it guesses" in 05; "tax included" and "if one fails, the agent stops, and says so" in 04c; "a new plan, or a new price" and "four steps" in 02; "with its price as a new version" in 04b; "that line is how an agent finds the skill" in 04a; OUTPUT section dropped; "Sooner, if a mistake costs money" in 08; "All three reuse software" in 03; shorter recap and your-turn.

Round 2 to now: nothing.

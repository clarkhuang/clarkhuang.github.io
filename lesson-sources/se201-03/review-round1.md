# SE201 Lesson 3, "Parallel Agents, One Integration": critique, round 1

Draft reviewed: `make_se201_03.py` as first rendered to stills (14 scenes, 559 words, est. 215 s). Compared against Lesson 1 (`make_se201_01.py`, 15 scenes, 234 s).

## What already beats Lesson 1

- **Hook.** "Three agents, three parts, every part passes its own check. Is the system done?" is a real tension, and the answer ("nobody knows yet") sets up the whole lesson. It starts about 5 seconds in.
- **One diagram carried through.** The same `lanes` picture appears broken (no contract, parts don't fit), then planned (contract, merge point, whole-system test lit one at a time), then with the real lessons in it. Lesson 1 changes layout every scene and never returns to a picture.
- **Real numbers on screen.** The three finish times (8:46:32, 8:46:36, 8:47:10 pm) are the files' actual timestamps.

## Problems

1. **"One merge point" reads as one big merge at the end.** That is the classic integration mistake, and the draft's own failure scene blames finding out "at the very end". Nothing in the fix says to merge early. An experienced engineer would call this out first. **Major. Say it: join rough versions early; don't let the first meeting be the last step. Put "early" in the recap and the rule.**
2. **The contract is treated as fixed.** Contracts change mid-work. One sentence: change it in one place, and every agent hears about it.
3. **Each agent's check doesn't mention the contract.** "Its own check" should include "does it match the contract?", or the contract is only a document.
4. **No enterprise scale.** Same gap as Lesson 2. One clause is enough here: at enterprise scale the contract is an API or a schema.
5. **"The contract was set before they started" is a claim about timing I can't check directly.** What is checkable: lessons 1 and 2 already used the same script format and page fields. Say that instead.
6. **"Far sooner" in the bars scene** overstates an illustration. Use "sooner".
7. **The failure scene's amber box arrives early.** At 45% through the scene the "parts don't fit" box is already up while the narration is still on "each part is correct on its own". Time it to "then the parts meet".
8. **Runtime is at the bottom of the range** (3:35). The additions above bring it to about 4 minutes.
9. **Six of fourteen scenes use `lanes`.** Deliberate, see above, and each differs (ghost contract, focus on one stage, real timestamps, files underneath). The quiz, statement, bars, list, rule card and outro break it up. Leave as is.

## Facts

Checked against the build machine and the repo (see `se201-03-facts.md`).

- Confirmed: the three scripts were written in the same second; the first narration clips of all three landed in the same second; the three final MP4s were written 37.6 s apart on Nov 21, 2026.
- Confirmed: all three lessons are entries in the one `sitegen/content.json`, built by `sitegen/gen.py`; `sitegen/check_site.py` exists and checks internal links and referenced files across the whole site.
- **Not confirmed here:** that the three reviews ran in parallel. `review.sh` runs one independent review per lesson per call, but no review output or log survives on the build machine. The draft therefore says "each with its own independent review" and does not say the reviews ran in parallel.
- **Not confirmed here:** that `check_site.py` was run on that build, and that lessons 3 to 5 reached staging in one pull request. `git log` is blocked in this sandbox, and the deploy workflow does not call `check_site.py`. The draft describes them in the present tense as how work comes together on this site, which the repo supports.

The "picture a team" scene is labelled as such on screen and in the narration.

## Tone

Matches Lesson 1. "Parallel isn't free. You pay for it at the merge" is the most pointed line and is fair. The aside about lessons 2 and 3 being drafted in parallel is one sentence.

## Rule vs examples

Rule: contract first, own brief and check per agent, one merge place, test the whole. The worked example shows each: script format and page fields, one script and review per lesson, one content file and generator, one site check. Consistent, apart from "early" (problem 1).

## Changes to make

- 5a: add the API/schema clause and "does it match the contract?".
- 5b: add "and use it early".
- Bars scene: "sooner"; add the contract-change sentence.
- 7: "the contract already existed: the script format the first two lessons used".
- 3: time the amber box to the narration.
- Recap and rule: "merge early, in one place".

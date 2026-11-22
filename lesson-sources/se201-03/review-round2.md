# SE201 Lesson 3, "Parallel Agents, One Integration": critique, round 2

Draft reviewed: `make_se201_03.py` after the round 1 revision (15 scenes, 613 words). All 15 stills re-rendered and looked at.

## Round 1 problems: status

| # | Problem | Status |
|---|---|---|
| 1 | "One merge point" read as one big merge at the end | Fixed. Scene 5c: "use it early; join rough versions of the parts on day one; don't let the first meeting be the last step." "Early" is in the caption, the recap and the rule. |
| 2 | Contract treated as fixed | Fixed in scene 5a: "when it has to change, change it in one place, where every agent sees it." |
| 3 | Agent's check didn't mention the contract | Fixed in scene 5b: "part of that check is: does it match the contract?" |
| 4 | No enterprise scale | Fixed with one clause in 5a: "at enterprise scale, that's an API, or a schema." |
| 5 | "The contract was set before they started" | Reworded to what is checkable: "the contract already existed: the same script format the first two lessons used, and the same page fields." Confirmed by comparing the keys of the five script files and the five page entries. |
| 6 | "Far sooner" | Now "sooner". |
| 7 | Amber box arrived early in the failure scene | Fixed: timed to "then the parts meet". Checked on the mid-scene still. |
| 8 | Runtime at the bottom of the range | Now 613 words, 236 s by the script's estimate. On Lesson 1's actual pace (674 words in 234 s) expect about 3:35. In range, at the short end. |

## New problems found this round

1. **The round 1 fixes overloaded two scenes.** Scene 5a had grown to about 75 words on one unchanging picture, and the bars scene carried three ideas, one of them (contracts change) with nothing on screen. **Major, fixed:** 5a is split into two beats. The first lights the contract while the lanes sit idle; the second lights the three agents and runs their lanes. The contract-change sentence moved to the contract beat. The bars scene is back to two ideas, both on screen. This needed two small options in the `lanes` layout (`idle`, `hold_stages`).
2. **Lanes finished during the contract beat.** Before the split, the three progress bars completed while the narration was still on the contract. With `idle` they now wait. **Fixed.**

## Would an experienced engineer call anything wrong or naive?

- **Whole-system tests are hard to write.** The lesson says to run them, not how. Lesson 5 (quality, feedback, observability) is where that goes.
- **"One merge point" in a large organization** is usually a main branch plus a pipeline, not one person. The lesson says "one place", not "one person", and the bridge to Lesson 4 picks up who approves.
- **The worked example is three video lessons, not three services.** The contract there is a file format and a set of page fields. That is a real interface (the renderer and the generator both read it), and the lesson does not present it as more than it is.
- **The worked example does not show an early merge.** The narration does not claim it does.

## Facts

See `se201-03-facts.md`. Two claims rest on the brief, not on something I could check in this sandbox:

- "Each with its own independent review." `review.sh` does run one independent review per lesson per call, but no review output survives on the build machine. The script does not say the reviews ran in parallel.
- That `check_site.py` and a single pull request were used for lessons 3 to 5. The script describes them in the present tense, as how work comes together on this site. `git log` is blocked here, so the pull request history is unchecked.

If either is not true, change scene 6 ("each with its own independent review") or scene 7 before recording.

One thing found while checking: `lesson-sources/se201-01/facts.md` lists `sitegen/check_site.py` under "checks run on every deploy", but `.github/workflows/deploy-pages.yml` does not call it. That is in Lesson 1's sources, not in these scripts.

## Compared with Lesson 1

- Hook: stronger, and five seconds earlier.
- Example: real timestamps on screen.
- Visuals: one diagram returns in three states. Two plain statements of fifteen scenes (Lesson 1: four of fifteen).
- Tone: same register. No jokes.
- Weaker than Lesson 1 in one respect: no everyday analogy. The generic team scene does that job.

## Verdict

One major problem found and fixed this round. Two facts flagged for the owner to confirm.

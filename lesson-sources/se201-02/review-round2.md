# SE201 Lesson 2, "Decompose the System into a Graph": critique, round 2

Draft reviewed: `make_se201_02.py` after the round 1 revision (14 scenes, 697 words). All 14 stills re-rendered and looked at.

## Round 1 problems: status

| # | Problem | Status |
|---|---|---|
| 1 | "No arrow, so run at once" ignored shared things | Fixed. The site example now says the shared node needs one clear owner; the recap asks "what crosses? what do they share?"; the rule adds "anything two parts share becomes its own node, with one owner". |
| 2 | No enterprise scale | Fixed. New scene 8, labelled "picture an enterprise system": orders, billing, shipping, support over a shared customer-data node. |
| 3 | "Owner" appeared from nowhere | Fixed in scene 5b. |
| 4 | "The chain sets the minimum" | Fixed: "the longest chain sets the minimum", spoken and on screen. |
| 5 | Arrow labels never spoken | Fixed: "script", "audio", "timeline", "video", "PR", each matching a spoken phrase. |
| 6 | Warning with no picture | Fixed: moved to scene 8, where the shared node is on screen. |
| 7 | Scene 5a lopsided | Not fixed. Folder names were added under each part, so the frame carries more, but the left third is still empty until 5b. Minor. |
| 8 | Recap filled half the frame | Fixed with the `rule` layout. |

## New problems found this round

1. **Length.** The revision reached 721 words, 277 s by the script's estimate, over the 4.5-minute limit. Trimmed to 697 words, 268 s. Lesson 1 is a useful calibration: 674 words, estimated 259 s, actually recorded at 234 s. On that pace this lesson should land near 4:02. **Fixed.**
2. **Scene 8 arrows landed before they were spoken.** "order" and "payment" appeared with their boxes, about ten seconds ahead of "a few real arrows". Added an `at` time for edges in the `graph` layout and set them to the narration. **Fixed.**
3. **"payment" label touched both boxes.** Reduced its size. **Fixed.**

## Would an experienced engineer call anything wrong or naive?

- **Cycles.** Two parts that each need something from the other are not covered. Lesson 3 covers them in one line ("if two parts keep needing each other's answers, they aren't parallel work; go back to the graph"). Acceptable for a four-minute lesson; not fixed here.
- **Cost of the shared node.** The lesson says a shared node needs one owner and that changing it moves everything. It does not say how to change one safely. That belongs to Lessons 3 and 4.
- **The bars.** "A third of the time" is never said; the label reads "an illustration" and the fine print states the assumption (three equal parts, nothing crossing).
- **"More agents won't make it shorter."** True of a strict chain. Correct as stated.

## Facts

Every claim about the site and the pipeline is in `se201-02-facts.md` with the file to check. None are unverified. The enterprise scene is generic and says "picture".

## Compared with Lesson 1

- Hook: sharper. The quiz answer is the thesis.
- Example: drawn, not listed, and it contains a small real finding (the build script runs two independent steps in sequence).
- Visuals: eight diagram scenes of fourteen, one plain statement. Lesson 1: four of fifteen, four plain statements.
- Tone: same register as Lesson 1.
- Weaker than Lesson 1 in one respect: no everyday analogy as developed as the kitchen. Dinner gets one scene. That is a deliberate trade for the two real graphs.

## Verdict

No major problems left. One minor one (scene 5a) left as is.

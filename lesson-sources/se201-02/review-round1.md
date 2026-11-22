# SE201 Lesson 2, "Decompose the System into a Graph": critique, round 1

Draft reviewed: `make_se201_02.py` as first rendered to stills (13 scenes, 639 words, est. 246 s). Compared against Lesson 1 (`make_se201_01.py`, 15 scenes, 234 s).

## What already beats Lesson 1

- **Hook.** Lesson 1 asks "what matters most?", which has an answer you can guess from the title. This one asks how many of ten numbered steps must wait, and the answer ("you can't tell from the list") is the lesson's whole point. It lands about 12 seconds in, after a 5-second title.
- **Visuals.** Lesson 1 has four plain statement scenes and three lists. This draft has one statement (the "your turn" ask) and seven diagram scenes, three of them on new layouts (`crossing`, `graph`).
- **Worked example.** Lesson 1 lists files. Here the site is drawn twice: as four parts with a shared node, and as one lesson's build chain with a fork.

## Problems

1. **"No arrow, so run at once" is naive as stated.** The test "what crosses?" only finds data that flows from one step to another. It misses two steps that both touch the same thing: the same file, the same database, the same generator. An experienced engineer would object within a minute. The draft shows a shared node in the site example and mentions parts that "secretly share something", but the test, the recap and the rule all ignore it. **Major. Fix in the test wording, the recap and the rule.**
2. **No enterprise scale.** The series is "From Loop to Enterprise Systems" and the outline for this lesson opens with "an enterprise system is too big for one loop". The draft never leaves dinner and this site. Lesson 1 has an "at enterprise scale" chapter. **Major. Add one generic, clearly hypothetical scene.**
3. **"Owner" appears from nowhere.** The recap says "a boundary and an owner for each", but no earlier scene mentions owners. The shared node is the natural place to introduce one.
4. **"The chain sets the minimum" is loose.** It is the *longest* chain that sets the minimum. Say so.
5. **On-screen labels that are never spoken.** The chain diagram labels arrows "text" and "audio"; the narration says "script" and "narration". Change the labels to "script" and "clips" and say "narration clips".
6. **The "opposite mistake" line has no picture.** In the bars scene the narration warns about running two parts that share something, while the screen shows only the two bars. Move the warning to the scene that shows a shared node.
7. **Scene 5a is lopsided.** Four boxes in the middle, a caption on the right, nothing on the left for 21 seconds. Tolerable because 5b fills the left side without a cut, but it is the weakest frame.
8. **The recap used the `recap` layout with four rows, which fills only the top half of the frame.** Already switched to the `rule` layout during the still check.

## Facts

Checked each claim about the site against the repo and pipeline (see `se201-02-facts.md`). Two corrections to the brief's list were needed before drafting, and the draft already reflects them:

- The book is not in `sitegen/content.json`. The generator builds it from text in `gen.py`. So the draft says the four parts share "one generator, with one stylesheet" and does not say they share one content file.
- Captions do not need the rendered video, only the script and the render's timeline log. Sound level and poster need only the video. That is what makes the fork real.

Nothing in the draft is presented as an anecdote. The line about the build script running the fork "one after the other" is checkable in `finish_se201_01.sh`.

## Tone

Reads like Lesson 1: short declaratives, no jokes. The quiz could feel like a trick question; the reveal explains itself in one sentence, which is enough. "And then, is not a dependency" is the only slowed line and earns it.

## Rule vs examples

The rule says parts with no arrow run at the same time; the fork (captions beside sound and poster) is exactly that. The rule says every part gets its own loop; scene 4 shows it. The gap is problem 1: the site example has a shared node and the rule doesn't mention shared things.

## Changes to make

- Test, recap and rule: add "and what do they share?" / "anything shared becomes its own node, with one owner".
- 5b: the shared node gets one clear owner.
- 6a: labels "script", "clips"; say "narration clips".
- 6b: "the longest chain sets the minimum".
- Bars scene: cut the warning, keep it to the two bars.
- New scene after the bars: a generic enterprise graph (orders, billing, shipping, support, with customer data and sign-in as the shared node), labelled "picture an enterprise system", carrying the warning about a missed shared node and pointing at Lesson 3.

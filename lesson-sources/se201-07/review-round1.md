# SE201 Lesson 7, "Skills as Building Blocks": critique, round 1

Draft reviewed: `make_se201_07_skills.py` (15 scenes, 752 spoken words, est. 289 s = 4:49) and the 15 stills in `stills-07/`. Compared against Lesson 1 (`make_se201_01_four_eras.py`) and Lesson 4 (`make_se201_04_parallel.py`). Nothing was edited, rendered or sent to a speech API for this review.

Limits of this review: one late frame per scene, so reveal timing against the narration could not be checked. `se201-07-facts.md`, which the generator's docstring cites as the source for every claim, was not found anywhere under `/workspace/legacy`.

Verdict: the best worked example in the series so far, and not yet recordable. It is 52 words over, it oversells what a skill guarantees, and the skill on screen does not catch one of the two failures the hook shows.

## What already beats lessons 1-4

- **The artifact is copyable.** The skill page built up over 04a to 04d is the most concrete thing any lesson has shown. A viewer could pause and write their own from it. Lesson 1's billing graph and lesson 4's lanes are pictures of ideas; this is a picture of the thing.
- **The hook's picture comes back repaired.** The `drift` grid appears broken (02), then again from the skill (07). Lesson 1 never returns to a picture. Lesson 4 does it with lanes; this is at least as clear.
- **It answers the engineer's objection before it is raised.** "If that sounds like a runbook, it is" is honest and well placed. "Make it a script the skill calls" answers "why not just automate it?".
- **The exercise is a real exercise.** Draft the skill, then test it in a fresh chat with only the page. Lesson 4's your-turn asks two reflective questions and never involves the AI.
- **The trap line is the best single idea.** "That's the mistake from the third run, written down" ties the hook to the page in one sentence.
- **Hook lands in time.** The title is 11 words (about 5 s), so the question is heard by about second 9.

## Problems

1. **"Same result, whoever runs it" is false, and nothing in the lesson says what a skill does not do.** Agents vary between runs even with the same page. Scene 07 shows three rows of "Right" and says so flatly. Lesson 1 has a whole caveat scene and lesson 4 has "Parallel isn't free"; this lesson has no honest limit anywhere. An experienced engineer stops trusting it here. **Major.** Replace in 07: "Same steps. Same checks. Same result, whoever runs it." with "Same steps. Same checks. [pause] No guarantee: agents still vary. That's what the checks are for."

2. **"An agent ... follows the page closely. So a gap in the page becomes a gap in the work" contradicts the hook.** In the hook the agents did not leave gaps; they filled them with guesses (one improvised an in-place edit). That is the real failure mode, and "follows the page closely" is not reliably true of any current agent. **Major.** Replace in 05: "An agent runs the skill every time, and follows the page closely. So a gap in the page becomes a gap in the work." with "An agent reads the skill on every run, with no memory of the last. Where the page is silent, it guesses." On screen: `s1` "Read on every run, no memory of the last"; `s2` "Where the page is silent, it guesses".

3. **The skill does not catch the hook's second failure.** Run two skipped tax, yet its "Test a renewal" cell is ticked. The skill's three checks never mention tax, so the same run would pass again. Each hook failure must map to a check. **Major.** 04c on screen: "A test renewal on staging: right amount, tax included, exactly once". Narration: "charges the right amount, tax included, exactly once."

4. **The third failure does not fit the stated job.** The label says the job is "add a new plan". Nobody adding a new plan edits an old price. The failure only makes sense for a price change, which the skill's own WHEN TO USE line admits ("a new plan, or a new price"). **Major, cheap to fix.** Hook: "Now and then, someone asks for a new plan, or a new price." Label: "THE JOB: ADD A PLAN, OR A NEW PRICE".

5. **The second half of 07 has no picture, and `v1` never pays off.** "Fix the skill. One change, in one place, and every later run gets it" is the lesson's main operational idea (the outline's "improve it in one place"). The frame shows three clean runs on `v1` and a caption. Nothing goes wrong and nothing gets fixed. **Major.** At "Fix the skill", flip the header to `skills/add-a-plan · v2` with a tag such as "+1 TRAP", and re-fire the four arrows. Otherwise remove the `v1` badge from every card; it is on-screen text nobody speaks.

6. **Recap, rule and your-turn say the same list three times in about 45 seconds.** "When to use it, inputs, steps, checks, traps" is spoken in 09, 10 and 11, and "keep it in the repo, test it with a fresh agent, fix the skill" in 09 and 10 word for word. Lessons 1 and 4 word the recap differently from the rule. **Major for pacing; it is also the easiest cut.** See Specific cuts for 09 and 11.

7. **The rule says "third time"; the example is a job where waiting cost two mistakes with money.** By its own rule the skill is written after the run that repriced every subscriber. An engineer will say a pricing change needs the page on day one. **Major (rule vs example).** Add to 08: "Sooner, if a mistake costs money." Add the same line to the quiz `why`. Rename the hook rows "First time / Second time / Third time" so the callback to "the third time" is visible ("Time after" is also awkward English).

8. **The hook grid shows twelve cells of text the narration never speaks.** "Export mapping", "On staging" and the four column heads are not said in 02; the four steps are not named until 04b. This breaks the on-screen-matches-spoken rule and makes the frame busier than the idea. **Minor.** Drop the text from the ticked cells (tick only), keep text on the two failures, and say "works out the four steps".

9. **"Add the plan as a new price version" muddles the model.** A plan is not a version of a price. **Minor, but an engineer will wince.** Step 1 on screen and spoken: "Add the plan, with its price as a new version". Hook cells follow suit, or become ticks (problem 8).

10. **The page never says what the agent does when a check fails.** The hook's failures were silent. "Ask, don't guess" covers inputs only. **Minor.** Replace in 04c: "This is the part most write-ups leave out: how do you know the job worked?" with "how the agent knows the job worked", and end the scene with "If one fails, the agent stops, and says so." This also removes "most write-ups", an unsourced claim about the world.

11. **The lesson never says how an agent finds a skill.** WHEN TO USE is presented as one section among six. In the real formats that line is what the agent reads to decide whether to load the page at all. **Minor; one sentence.** Add to 04a: "That line is how an agent finds the skill."

12. **Six sections on the card, five in the recap and rule.** OUTPUT is on the card and spoken in 04d, then dropped. **Minor.** Remove the OUTPUT block and its sentence (saves 14 words). If the author wants to keep it, add "output" to the recap and rule instead; do not leave the mismatch.

13. **"Each of those packages code" is loose for services.** A service is reused as something running that someone else operates; that is the point of it. **Minor.** "All three reuse software. A skill reuses something different." Band label: "THESE REUSE SOFTWARE". The arrows between the four boxes also read as "replaced by"; the "NOW, ALSO" tag saves it, so keep that tag.

14. **05's right-hand band says "RUN BY A PERSON OR AN AGENT" under a headline that says the reader changed.** The picture argues against its own label. **Minor.** "A SKILL · READ BY AN AGENT, EVERY RUN".

15. **"With nobody watching" in the close contradicts lesson 6** ("watch every run"). **Minor.** End the sentence at "start on its own".

16. **The outro does not name lesson 8 on screen.** Lesson 4's outro sub reads "Next: governance, where people decide"; this one reads "Software Engineering 201". **Minor.** Sub: "Next: routines, pipelines, and integration".

17. **"Next to the system it changes" does not match the path shown** (`skills/add-a-plan/` is a top-level folder). **Minor.** Cut the phrase (also saves 6 words).

18. **Published outline disagrees with the draft.** `software-engineering-201/index.md` describes lesson 7's example as retail e-commerce supplier data and says "every era found its unit of reuse". The draft's billing example and softer "keeps finding" are better, but the index must be updated before this ships. **Minor, outside the script.**

19. **06 states "treat it like code" three times** (chapter, label, caption) and leaves the lower right empty. One test run is also not a test of something that varies. **Minor.** Change the label to "TEST IT WITH A FRESH AGENT"; optional on-screen sub under "Runs it on staging": "more than once".

20. **Four card scenes open "Then ... Then ... Then ... And last".** Flat. **Minor.** The 04c and 04d rewrites below vary it enough.

Stills, one by one: 01 fine. 02 readable but busy (problem 8); "MAP TO ACCOUNTING" sits about 26 px from "TEST A RENEWAL", tight but not touching. 03 clean. 04a is two-thirds placeholder bars for about 25 s; acceptable because it fills. 04b, 04c, 04d readable, nothing clipped. 05 readable; label problem 14. 06 lopsided, problem 19. 07 problem 5. 08, 09, 10, 11, 12 clean. No overflow, overlap or clipping in any of the fifteen frames.

Hard-constraint check: "made-up" is spoken at first mention and labelled on 02 and 04a-d. No sticky.io or other company, no narrator facts beyond the allowed list (none are used at all), no names, no numbers. Tags are only `[pause]` and `<emphasis>`; "A.P.I." and "A.I." are spelled out. All required elements are present. Violations found: on-screen text not spoken (problems 5, 8, 12, 14), one unsourced generalisation (problem 10), and the missing facts file.

## Facts

- **"Several agent tools now have a format for this: a folder, with an instruction file."** Defensible. The Agent Skills format (a folder containing `SKILL.md`) was published as an open standard in December 2025 and is read by tools from several vendors, including Codex, GitHub Copilot, Cursor and VS Code. Checked by one web search during this review; sources below. Record it in the facts file. The on-screen `SKILL.md` is the real filename, which is fine, but real files carry a name and description header that the card does not show; "A MADE-UP EXAMPLE" covers that.
- **"Libraries ... Frameworks ... Services", "roughly in the order they became common."** Defensible as labelled. Subroutine libraries date from the 1950s, application frameworks from the 1980s and 1990s, services behind an API from the 2000s onward. The hedge on screen is needed; keep it.
- **"Each of those packages code."** Loose for services. See problem 13.
- **"A skill packages something different: how a job gets done."** Not new, as 05 itself admits: runbooks, checklists and scripts did this. Acceptable because 05 says so within a minute.
- **"Engineers have written runbooks for decades."** Defensible. Operator run books go back to mainframe operations.
- **"A person reads a runbook now and then, and fills the gaps from memory."** Fair generalisation, framed as a contrast.
- **"An agent runs the skill every time, and follows the page closely."** Not defensible as stated. See problem 2.
- **"A different agent starts from zero."** Correct: a new session has no memory of the last unless something is written down.
- **Editing a price in place moves every existing subscriber to the new price.** Plausible for the made-up system and consistent with why billing systems commonly treat prices as immutable. No real system is named. Fine.
- **"This is the part most write-ups leave out."** Unsourced. Cut (problem 10).
- **"Same result, whoever runs it."** Not defensible. See problem 1.
- **"The third time."** This is the old refactoring "rule of three" reused for skills. Labelled a rule of thumb on screen and aloud, which is correct framing. No attribution is needed, and none should be added by name.
- **"One change, in one place, and every later run gets it."** True provided runs read the page from the repo each time, which 06 establishes.
- **Statistics:** none. **Narrator claims:** none.
- **Not confirmed here:** `se201-07-facts.md` does not exist on this machine. Write it before recording.

Sources for the first item: [Anthropic: donating Agent Skills to the Agentic AI Foundation](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation).

## Tone

Plain and professorial. Nothing jokey, forced or condescending. "It doesn't guess" and "because a price is money, and a person approves it" are the right register.

Two weaknesses. It is the least personal lesson so far: there is no "I" anywhere, where lesson 1 has "I'll be straight about that list" and lesson 4 has "for me to approve". Do not fix this with a story; the allowed facts do not include his team using skills. The honest-limit line in problem 1 does the same job. Second, the last four scenes read as a list being recited (problem 6).

## Rule vs examples

Rule: third time, write it as a skill (when to use, inputs, steps, checks, traps); keep it in the repo; test with a fresh agent; fix the skill, not just the run.

- When to use, inputs, steps, checks, traps: all shown on the card. Consistent, apart from OUTPUT (problem 12).
- Checks: the card's checks miss the tax failure (problem 3).
- In the repo, tested by a fresh agent: shown in 06. Consistent.
- Fix the skill: said, not shown (problem 5).
- Third time: the example is a money job that went wrong on runs two and three (problem 7).

## Is it better than lessons 1 and 4?

Better: concreteness, the bookend picture, the exercise, anticipating the runbook objection.

Not better: no honest limit (lesson 1 scene 10, lesson 4 scene 08); nothing real or checkable (lesson 4 has file timestamps); the quiz comes at 08, after the answer has been implied for three minutes, where lessons 1 and 4 open with it; the title's promise of "building blocks" gets one sentence and no picture of blocks combining; the ending repeats itself; it is 19 seconds over the range.

Standing alone: it works without lessons 1-6. "Our made-up subscription-billing system" is enough. "Pull request", "staging" and "ledger" go unexplained, as in lessons 2 and 4.

## Specific cuts to reach <= 700 words

Full replacement narration, counted the same way the generator counts. Total 699 words, est. 269 s. Changes fold in the fixes above.

| Scene | Now | After | Replacement narration |
|---|---|---|---|
| 01 | 11 | 11 | unchanged |
| 02 | 84 | 86 | "Why would three capable agents do the same job three different ways? [pause] Take our made-up subscription-billing system. Now and then, someone asks for a new plan, or a new price. The first time, an agent works out the four steps, and gets it right. The second time, a different agent starts from zero, and skips the tax setup. The third time, another one edits the old price in place, and every existing subscriber is on the new price. [pause] Same job. Three results. Nobody wrote down how." |
| 03 | 47 | 42 | "Software keeps finding new units of reuse. Libraries: shared code. Frameworks: an application's structure. Services: something running, behind an A.P.I. [pause] All three reuse software. A skill reuses something different: <emphasis>how a job gets done.</emphasis> One recurring job, written down, tested, and shared." |
| 04a | 64 | 63 | "Several agent tools now share a format for this: a folder, with an instruction file. Let's write one. It starts with when to use it: someone asks for a new plan, or a new price. That line is how an agent finds the skill. Then the inputs: name, price, billing period, start date. If one is missing, the agent asks. It doesn't guess." |
| 04b | 42 | 40 | "Then the steps, in order. Add the plan, with its price as a new version. Set its tax category. Map it in the accounting export. Then open a pull request, because a price is money, and a person approves it." |
| 04c | 43 | 46 | "Then the checks: how the agent knows the job worked. A test renewal on staging charges the right amount, tax included, exactly once. The ledger still adds up. And existing subscribers still renew at their old price. If one fails, the agent stops, and says so." |
| 04d | 47 | 30 | "And the traps: what went wrong before. Never edit a price in place. Add a new version. That's the mistake from the third run, written down, so nobody repeats it." |
| 05 | 73 | 68 | "If that sounds like a runbook, it is. Engineers have written those for decades. What's changed is the reader. A person reads a runbook now and then, and fills the gaps from memory. An agent reads the skill on every run, with no memory of the last. Where the page is silent, it guesses. [pause] And when a step needs no judgment, make it a script the skill calls." |
| 06 | 56 | 50 | "So treat a skill like code. Keep it in the repository, versioned, and reviewed when it changes. [pause] And test it. Hand it to a fresh agent that has never seen the job, and let it run on staging. If it can't finish from the page alone, the skill isn't done." |
| 07 | 59 | 58 | "Now run those three jobs again, from the skill. Same steps. Same checks. [pause] No guarantee: agents still vary. That's what the checks are for. And when a run goes wrong, don't just fix the run. Fix the skill. One change, in one place, and every later run gets it. That's a building block: reliable enough to build on." |
| 08 | 49 | 49 | "So when is a job worth a skill? The first time? The third? Or never, because agents can work it out? [pause] A good rule of thumb: <emphasis>the third time.</emphasis> Once, you're learning. Twice, you see the pattern. The third time, write it down. Sooner, if a mistake costs money." |
| 09 | 41 | 31 | "So, to recap. One recurring job, written down, with its checks and its traps. In the repo, tested by a fresh agent. And when a run goes wrong, fix the skill." |
| 10 | 55 | 55 | unchanged |
| 11 | 45 | 37 | "Now, your turn. Pick a job you've explained to your A.I. more than twice. Ask it to draft the skill. [pause] Then open a fresh chat, give it only that page, and see if the job gets done." |
| 12 | 36 | 33 | "One skill does one job. But real work is a chain of jobs, and some of it should start on its own. That's next: routines, pipelines, and integration. See you in lesson eight." |
| **Total** | **752** | **699** | |

699 is one word under the limit and the pauses are not counted, so take at least one reserve cut:

- 05: drop "Engineers have written those for decades." (6 words; also removes one fact to source.)
- 04a: drop "Let's write one." (3 words.)
- 12: drop "One skill does one job." (5 words.)

With the first two the script is 690 words, est. 265 s.

On-screen text that must change with these cuts: 03 node subs ("Shared code", "An app's structure", "Running, behind an API") and band label; 04b step 1 and step 2 ("Set its tax category"); 04c check 1; remove OUTPUT block; 05 nodes and band label; 08 `why` gains "Sooner if a\nmistake costs\nmoney."; 09 item 2 becomes "With its checks and its traps".

## Changes to make

- 07: remove "Same result, whoever runs it"; add the no-guarantee line; show `v1` becoming `v2` at "Fix the skill".
- 05: "with no memory of the last. Where the page is silent, it guesses"; fix the right-hand band label.
- 04c: "tax included"; add "If one fails, the agent stops, and says so"; cut "most write-ups".
- 02: "a new plan, or a new price"; rows "First / Second / Third time"; ticks only in passing cells; say "four steps".
- 04b: "Add the plan, with its price as a new version".
- 04a: "That line is how an agent finds the skill".
- 04d: drop OUTPUT from card and narration.
- 08: add "Sooner, if a mistake costs money" aloud and on screen.
- 09 and 11: shortened wording above, so the five-part list is spoken once, in the rule.
- 12: cut "with nobody watching"; outro sub "Next: routines, pipelines, and integration".
- 03: "All three reuse software"; update subs and band label.
- 06: cut "next to the system it changes"; new label.
- Write `se201-07-facts.md`; update lesson 7's entry in the series `index.md` to the billing example.
- Re-render stills and check 02, 05 and 07 again after the layout changes.

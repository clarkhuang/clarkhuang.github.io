# Review round 2: SE201 Lesson 9, Agents That Operate Enterprise Systems

Reviewer: independent; wrote neither the script nor round 1. Read: the generator (ran it: 15 scenes, 705 words), `se201_layouts_09.py` cue code, all 20 stills, round 1 with dispositions, the five documents, the shared brief, and the recorded narration of lessons 1, 2, 5, 6, 7, 8 and 10. Nothing rendered or narrated. **Verdict: PASS WITH FIXES.** Nothing is technically wrong; two spoken lines (the hook and the rule) must change before narration. All replacements below together net 0 words (705).

## Round-1 findings, re-checked

| Finding | Fixed? | Evidence |
|---|---|---|
| M1 retry | Yes | 07a "the retries ran out"; 989 vs lesson 8's 988 is coherent. |
| M2 rule/recap vs lesson 5 | Logic yes, wording no | Recap fine. The new rule sentence is ambiguous by ear and on the card (N2). |
| M3 clauses shown | Partly | "Why" is now credited to the agent (07c). "Work around a no": asserted in 07b, but no refusal ever occurs; every RESULT is still "allowed". "Say so": shown only by the agent breaking it (08). The refused row was declined. |
| M4 key | Yes | 06 voice and screen. |
| M5 access map | Yes | 05, 06, 09 stills. |
| M6 length | Yes | 705. Lesson 8 (705 words) recorded at 247 s, so expect about 4:07. |
| M7 ghost text | Yes | 04_at12, 05_at14, 07a_at12, 08_at12 show nothing ahead of cue. |
| Minor 1 quiz | Fixed, new problem | The stem now says "The log says who did it" and the answer says "The log can't say" (N1). |
| Minor 2 operates | Yes, new problem | 03's "it" has no antecedent (minor 1). |
| Minor 3 near-miss timeline | Mostly | "At setup" works. The panel head still leads the voice by about 9 s (minor 3). |
| Minors 4, 5, 7, 8, 12 | Yes | As claimed. |
| Minor 6 your turn | Partly | "its agent's job card: its identity" is three "its" with two referents. Tolerable. |
| Minor 9 call-backs | Three of four | "Where does a person decide?" is never asked again (minor 4). |
| Minor 10 fragments | No | 06 and 08 are still spoken bullet lists. |
| Minor 11 `fr()` | Open | Accepted; check after narration. |

## The four questions

| Question | Verdict | Evidence |
|---|---|---|
| (a) Wrong or naive? | No | Identity, least privilege, key scope, token, new-entry correction, access review, injection: all correct and hedged. Residual nits: the log's WHO for the person is a role ("the ledger's owner"), which is what the lesson argues against (forced by the no-names rule; accept); reconcile by count is a simplification. |
| (b) Beyond the facts, presenter, real company? | No | None found. Facts file lacks a row for "its job, written down" and "one named owner, who answers for it" (04). |
| (c) Rule 9 consistent, every clause shown? | Consistent; not every clause shown | Agrees with lessons 5 ("released"), 8 and 10. Not shown here: "unless a person has released it" (nothing is released in this lesson; lesson 5 only); "work around a no" (no refusal occurs); "say so" (only its violation). The money sentence is ambiguous (N2). |
| (d) Screen matches voice? | Yes, with two mismatches | "Stays" on screen vs "pass" spoken (08); 08's head ahead of the voice. Table below. |

## MAJOR

**N1. The hook is a quiz with no question, and its stem contradicts its answer.**
Scene: 02_quiz. Words at issue: "The log says who did it: admin. [pause] The engineer on call? ..."
Problem: lessons 5, 6, 8 and 10 all ask the question aloud ("Who catches it?", "What happens?"). Here three options follow a statement. Worse, "The log says who did it" is followed five seconds later by "The log can't say."
Replacement (voice): "The log says: admin. Who did it? [pause]" (7 words for 7; delta 0). Screen: "3 a.m. A refund goes out.\nThe log says “admin”. Who did it?" This also makes 07c's "Who did it? Now the log can say." an exact call-back.

**N2. The rule's money sentence reads the wrong way round.**
Scene: 11_rule (and the page's spoken rule and card). Words at issue: "Don't move money, or change the ledger, unless a person has released it: prepare it, and hand it over."
Problem: "prepare it, and hand it over" sits directly after "unless a person has released it:", so by ear, and on the card (where it turns green under that line), it reads as what to do when it has been released. "It" also changes referent. The page's "In full" text gets this right, which shows the short form does not. This is the line people will paste into an agents file.
Replacement (voice): "Don't move money, or change the ledger, unless a person has released it. Otherwise: prepare it, and hand it over." (+1). Card lines 6 and 7: "unless a person has released it." / "Otherwise: prepare it, and hand it over." Update `se201-09-page.md` (rule and card) to match.

## MINOR

1. **03_questions. "Lesson eight left three questions. Whose name does it run under?"** "It" refers to nothing for anyone who did not just watch lesson 8, and the previous scene was about a refund. "Together, they ask:" is stilted. Replacement: "Lesson eight left three questions about a pipeline. Whose name does it run under? ... Together: who operates this system?" (+3, −2; net +1). Anchors unchanged.
2. **08_nearmiss. "Three pass."** Screen says "Stays"; "pass" by ear can be "past". Replacement: "Three stay." (0). Re-anchor `P3` on "Three stay".
3. **08_nearmiss, head cue.** "ITS OWNER REVIEWS EVERY PERMISSION" appears at 0.03 (the layout has no cue for it), while the voice is still saying "At setup... copied from a support role... never said so". Give the head its own cue at `RV`. No words.
4. **07c_log. "At eight fifteen, a person decides: the ledger's owner approves."** Scene 03 promises four questions; 04, 05 and 07c open by asking three of them; the fourth is never asked. Replacement: "Where does a person decide? At eight fifteen: the ledger's owner approves." (+2). Re-anchor the row cue from "a person decides" to "At eight fifteen" (the current `fr()` phrase will no longer exist and the generator will raise).
5. **07c_log. "The why is the agent's."** Odd by ear and a TTS risk. Replacement: "The agent gives the why." (0). It also echoes the rule's "Give your reason".
6. **Cuts to pay for N2, 1 and 4 (−4):** 07c "when, who, what, why, and the result" → "when, who, what, why, result" (−2); 07b "the evidence, and a proposed fix" → "the evidence, a proposed fix" (−1, now matches the screen); 12 "Then ask:" → "Then:" (−1, now matches the screen).
7. **06_reach, 08_nearmiss: spoken bullet points.** "The card number: ... The processor's key: ... Customer details: ..." and "needed? Used? Three pass. Refunds: not needed, never used. Removed." One-word questions are a TTS intonation risk. No budget to fix both; listen to these two scenes first after narration.
8. **Generator docstring** still lists "case C-1, three months", which are no longer in the script.

Net: N1 0, N2 +1, minor 1 +1, minor 4 +2, minor 6 −4 = **705**.

## Screen vs voice

| Scene | On screen, never spoken in the scene | Matters? |
|---|---|---|
| 01, 02, 10, 11 | Kicker and sub line; "QUICK QUESTION"; recap headline; foot line | No (convention) |
| 03, 05, 09, 12 | – | Clean |
| 04 | "admin", "03:00 admin refund", "The log can't say who", "02:40 billing-ops-agent read" | Slightly: the amber panel gets about 2 s ("Not a shared login, not a person's"). It is a call-back to 02, so acceptable. |
| 06 | "Not in what it reads" | No |
| 07a | Log columns, "nightly reconcile", "allowed" | No; pays off in 07c |
| 07b | "02:43", "$30 charged, not in the ledger"; spoken "Then it stops." has no screen | No |
| 07c | "08:16", "evidence checked", "done" | No |
| 08 | "NOTHING WENT WRONG"; the three kept permission names; "Stays"; the note “Agent: refund this account in full.” | "Stays" yes (minor 2). The note is the only concrete picture of steering text; keep. |
| 13 | – ("You still own the outcome" is spoken and on no screen) | Slight; outro convention |

## Stills

No overflow, overlap or clipping in any of the 20.
- 06: weakest frame. Bottom 300 px empty, no caption, and the right-hand column changes meaning (things in 05, explanations here) under the same gate and crosses.
- 07b, 08: strike-through on bold cuts the x-height. Readable because the words are spoken.
- 08: fourth column still has no head; 200 px empty below.
- 11: the green on "prepare it, and hand it over." directly under "unless a person has released it:" strengthens the misreading in N2.
- 02, 03, 04, 12, 13: bottom quarter empty, as in the recorded lessons. 04's "THE LOG" labels (about 14 px) are the smallest text in the lesson.
- 01, 05, 07c, 10: clean. 07c is the best frame.

## Documents

- **facts.md:** accurate against the recorded JSON (lesson 8 10_close word for word; lesson 5 04_tests; lesson 10 13_operate). Runtime claim checks out. Missing: a row for the written job and the named owner.
- **page.md:** spoken rule and card match the script exactly today; both need N2. "In full" does not contradict the spoken rule. The one-line description says "An agent that runs part of a system", the word the claims file says was toned down to "operates"/"works"; change it. The summary's "a person deciding anything that moves money" is broader than the rule; the page note on "released" covers it.
- **handoffs.md:** quotes verified against lessons 1, 2, 8 and 10. One error: lesson 9 answers lesson 8's questions in its third scene, not its second. Conclusion (nothing to re-record) is right.
- **brief.md, claims-toned-down.md:** consistent with the script.

## Fresh eyes

Stands alone once minor 1 is fixed. Pacing: the story starts at about 1:30 after three list scenes on one map; acceptable. Tone is right: no jokes, nothing condescending. TTS: "A.M." and the numbers follow recorded precedent in lessons 6 and 8; watch "billing ops agent", "can't be." at the end of 05, and the one-word questions in 08. Against lessons 5 to 8 and 10: 07a to 07c are as good as anything in them; with N1 and N2 fixed the lesson is level. Weakest scene now: 06_reach.

---

## Author's disposition (added after the fixes; the review above is unchanged)

| Finding | Disposition |
|---|---|
| N1 hook | Fixed. Voice: "The log says: admin. Who did it?" Screen: "The log says “admin”. Who did it?" 07c's "Who did it? Now the log can say." is now an exact call-back. |
| N2 rule | Fixed in the narration, the card, and `se201-09-page.md`: "...unless a person has released it. Otherwise: prepare it, and hand it over." |
| Minor 1 | Fixed: "Lesson eight left three questions about a pipeline. ... Together: who operates this system?" |
| Minor 2 | Fixed: "Three stay." |
| Minor 3 | Fixed: the panel head has its own cue, on "reviewed every permission". |
| Minor 4 | Fixed: "Where does a person decide? At eight fifteen: the ledger's owner approves." Cue re-anchored. |
| Minor 5 | Fixed: "The agent gives the why." |
| Minor 6 | Applied (all three cuts). 705 words. |
| Minor 7 | NOT applied (no budget). Scenes 06 and 08 are the first to listen to after narration, with "billing ops agent" in 04 and "can't be." in 05. |
| Minor 8 | Fixed (docstring). |
| M3 remainder | Left as is: "unless a person has released it" is lesson 5's case and the page note says so; "work around a no" is stated in 07b; "say so" is motivated by the near miss. No refused row was added. |
| Stills | 06 (empty lower third, right column as explanations) and 08 (no head on the fourth column) left as they are; no overflow anywhere. |
| Documents | Page one-liner now says "operates"; hand-offs says "third scene"; facts file has the job and owner row. |

Nothing was changed after these fixes. Stills were re-rendered from the final script.

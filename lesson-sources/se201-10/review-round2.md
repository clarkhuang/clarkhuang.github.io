# SE201 Lesson 10, "Capstone: One Feature, End to End": review, round 2

**Verdict: PASS WITH FIXES.** Two majors, both small: one on-screen heading is cut by a divider line (04_right), and after round 1's
fix none of the three checks tests the amount the whole lesson is about (09_checks). Neither needs a new scene; together they add six
spoken words. Everything else from round 1 is fixed or acceptably fixed in part.

Reviewer: an independent agent that wrote neither the script nor round 1. Checked: `scripts/se201-10-capstone.json` (18 scenes; the
preview copy used for the stills has byte-identical scenes and the stills are newer than the JSON), all 18 stills (plus zoomed crops of
04, 08, 11, 12, 13), `se201_layouts_10.py`, round 1 and its draft, both briefs, the narration of recorded lessons 1-8, the lesson 9
outline, and the round-2 reviews of lessons 6 and 8. No file other than this one was changed. Not available to check: `se201-10-page.md`,
`-facts.md`, `-claims-toned-down.md` (they do not exist yet), so every round-1 item that was to go "on the lesson page" is unverified.

Arithmetic: $30 / 30 days = $1 a day; 20 unused days = $20; $300 - $20 = $280. The day row in 04 has 10 grey and 20 green cells. Every
figure on every still ($30, $300, $20, $280, day 10 of 30, 10 days used, 20 days, Q-1) agrees with every other. One loose end: tax (minor 3).

Length: **849 spoken words** (cap 858). At the brief's 2.6 words/second that is 5:27. Recorded lessons 5-8 actually ran at 2.84 to 2.98
words/second including pauses (measured from their audio files), which puts this at about 4:45 to 5:00. Under the cap either way; nine
words of headroom. 13 `[pause]` tags; only `[pause]` and `<emphasis>` are used.

---

## Status of round 1's findings

### Majors

| # | Round 1 finding | Status | Evidence |
|---|---|---|---|
| M1 | Nothing switches the subscription | **Fixed** | Part 4 is "Charge it, switch the plan" (spoken in 06, box on the map). 12: "Charge, switch the plan, invoice and ledger, email"; stage "Switch the plan" with notes "now annual / monthly renewal off". The declined-charge note was for the page: unverified. |
| M2 | Run-time diagram wrong in three places | **Fixed in part** | (a) Fixed: "Quote" stage gone; chain starts at Charge under "WHEN THE CUSTOMER CONFIRMS". (b) Fixed: Reconcile sits apart behind a dashed divider with its own tag "EVERY NIGHT", no arrow from Email. (c) Part: "pipeline", "trigger" and "idempotency key" are now spoken and shown; "routine" is still never said, and by lesson 8's own definitions the nightly reconcile is a second routine, not part of the event pipeline it shares a panel tag with. Minor. |
| M3 | Idempotency claim absolute; "this quote" not a key | **Fixed in part** | "this quote's I.D."; "doesn't charge twice"; caption "Safe to run twice: same key, no second charge."; the quote now has an ID on screen ("ID · Old plan · ..." / "Q-1 · ..."). Not done: no expiry on the quote, and lesson 8's hedge ("many payment processors support one") is not in the script. The two-tab hole is now the failure beat in 13, which is the right use of it. |
| M4 | Check 2 breaks once tax is added | **Fixed as proposed, and the fix opened a new hole** | "Each charge equals its quote." / "2   Each charge = its quote"; SPEC line "Quote = new price - credit, plus tax." See new major N2. |
| M5 | Seven "Lesson N:" beats in a row | **Fixed** | Openers are now "Now make it readable." / "Next, the graph." / "Then plan the integration..." / "Who decides?" / "Now turn right into checks..." / "One part isn't new." / "Now it runs on its own". Lesson numbers are spoken only in 03, 04, 13, 14. 03 says "Each number is the lesson it comes from." The beats are still 32 to 55 words each and similar in shape, but it no longer reads as a contents list. |
| M6 | "Three parts are new work" / "the fourth part" | **Fixed** | 07 shows "NOT NEW" under "Add the annual plan" and "AGENT A/B/C" under the other three; 10 opens "One part isn't new", the label becomes "7 A SKILL", panel head "THAT PART". |
| M7 | "Show a person" and "Stop, and ask" never demonstrated | **Fixed in part** | 04: "The amount is a person's call, so the agent asks." (also the panel head). 11: "The plan is written, and a person has read it." (also the first log row). 17: "Then find the line it guessed, when it should have asked." Both are asserted in a clause, not shown: no person appears on the map before the build, and the reader of the plan is nobody in particular. Acceptable. |
| M8 | Example used before it is called made up | **Fixed** | 02 opens "Picture a made-up billing system." |
| M9 | Over length (875) | **Fixed** | 849. |
| M10 | Arrows and "the quote" blur a format with a value | **Fixed** | 06 "One new thing: the quote."; 07 "The quote's format is the shared contract." with sub-label "its format: the shared contract" and panel "The quote's format, written before anyone starts"; arrows now run up from Calculate into the quote and down into Show and Charge. Residue in minor 5. |

### Minors

| # | Round 1 finding | Status | Evidence |
|---|---|---|---|
| 1 | Quiz answer is the series' stock trick | Fixed | "Or: it depends? ... It depends. On a rule nobody has written down." Options now carry their policies. |
| 2 | "in an afternoon" | Fixed | "And an agent will build either answer, without asking." |
| 3 | Agent classifies its own change | Fixed | "It moves money, so a person does... The agent that writes the change doesn't classify it, or approve it." |
| 4 | "FIRST OF THE FOUR QUESTIONS" | Fixed | Head is "DOES IT MOVE MONEY?", lines "Yes. / So a person decides". |
| 5 | "it never sees a card" | Fixed | Now "It can't move money, or change the ledger." |
| 6 | "An agent runs that reconcile" | Fixed | "An agent works that nightly reconcile." |
| 7 | 09 caption overclaims | Fixed | Caption is "Write them once, run them twice." |
| 8 | 10 caption "Seven lessons in..." | Fixed | Caption is "Reuse what recurs." |
| 9 | "Billing period: one year. The price: a new version." | Fixed | Cut, with its two greyed lines. |
| 10 | "never renews again" | Fixed | "doesn't renew again", spoken and shown. |
| 11 | "any agent"; "Markdown twin" missing | Fixed in part | "so an agent can find it". "Twin" still absent and `index.md` still stands in for the index of the system. Leave. |
| 12 | "KNOWS" vs "understands" | Fixed | Card head "Somebody understands the layer below". |
| 13 | "Money has to add up" restated the subtraction | Fixed | "the invoice, the ledger, and the processor all say two eighty"; card "Invoice = ledger = processor: $280". |
| 14 | Same list three times in 55 seconds | Fixed in part | Cut from 17. Still said in 15 and again in 16, back to back. |
| 15 | "a whole feature" is not a testable threshold; no "wait for a yes" | Left | Card unchanged. Round 1 allowed that if the page carries the full wording; the page does not exist yet. |
| 16 | "Every step leaves a record" not shown | Fixed | Stage notes: "charged $280", "now annual / monthly renewal off", "invoice written / $280 in the ledger", "receipt sent". |
| 17 | Lesson 9 is not a video | Nothing to change in narration | "Lesson nine's question: who operates it?" is traceable to lesson 8's close and the outline. |
| 18 | Nothing goes wrong | Fixed | 13 failure beat. See minors 1 and 2 below. |
| 19 | Close | No change needed | Unchanged. |

---

## MAJOR (fresh review)

**N1. 04_right: the panel heading is cut by the column divider and runs into the right-hand column.** (layout defect, still
`04_right.png`)
The revision lengthened the head to "THE AMOUNT IS A PERSON’S CALL, SO THE AGENT ASKS  ·  HERE: $30 A MONTH, DAY 10 OF 30". It now ends at
about x = 1148; the vertical divider is at x = 1074 and starts above the heading's baseline, so the line passes through the "0" of "10"
(it reads "DAY 1|0 OF 30") and "OF 30" sits over the sum column, directly above "Annual plan".
Fix (data only): shorten the head to **"A PERSON’S CALL, SO THE AGENT ASKS  ·  $30 A MONTH, DAY 10 OF 30"** (64 characters; at the
measured 12 px a character that ends near x = 910, clear of the divider). Or, in `_lower_days`, start the divider below the heading
(`LY + 50` instead of `LY + 22`) and still shorten the head so it does not sit over the sum.

**N2. 09_checks: after the round-1 fix, no check tests the right amount.** (rule inconsistent with the lesson's own example)
Words: "Now turn right into checks an agent can run. No upgrade is charged twice. Each charge equals its quote. And the old monthly plan
doesn't renew again." On screen: "RIGHT, AS THREE CHECKS AN AGENT CAN RUN / 2   Each charge = its quote".
Why: "right" is "Every upgrade is charged the right amount, exactly once", and the quiz, the day row and the finance owner's rule are all
about the amount. Check 2 now only compares the charge with the quote. If the quote is built wrong (the full $300, a $19 credit, a stale
quote confirmed the next day), all three checks pass. Lesson 6's own check 2 was an independent recomputation ("each charge equals the
plan's price"); this one compares the system with itself. Rule 10 says "what right means, as checks", and the one thing a person had to
decide is the thing no check looks at.
Fix, keeping three checks (plus 6 words, 09 goes 47 to 53, total 855):
Spoken: "No upgrade is charged twice. **Each quote follows the rule, and each charge equals its quote.** And the old monthly plan doesn't
renew again."
On screen: **"2   Each quote = the rule; each charge = its quote"** (49 characters; line 3 is 43 and fills about three quarters of the
column, so this fits at the same size).

---

## MINOR

1. **13_operate, the failure beat is sound but says less than it could, and the screen credits the wrong step.** Two tabs give two quotes,
   so two IDs, so two keys, so two charges: that is exactly the boundary of the idempotency claim in 12, and it does not contradict it.
   But the script never says why the key did not help, so a viewer hears "doesn't charge twice" and, 25 seconds later, "two charges". Add
   two words: "two browser tabs, two quotes, **two keys**." (13 goes 80 to 82; with N2 the total is 857.) Also note that reconcile cannot
   find this (ledger and processor both show two charges and agree); check 1 does. The screen's green "the three checks" under Reconcile
   covers it, so no narration change. **Worth applying before narration** (two words).
2. **13 to 15, "the three checks" stays on screen after "a fourth check".** The note under Reconcile reads "the three checks" in 13
   (beside the caption "The miss becomes a fourth check"), and still in 14 and 15. Not a contradiction in 13 (three, then four), stale in
   14 and 15. Change the note to "the checks" in all three scenes, or to "the four checks" in 14 and 15. Data only. **Worth applying.**
   Related, leave: "one open quote per subscription" is a rule the system must enforce, and lesson 6 fed a miss back as "a new line in the
   brief... and a new test"; calling it "a fourth check" is close enough. Lesson 8's key ("this subscription, this billing period") would
   have prevented the double charge outright; the capstone chose a narrower key and never says so. Put one line on the lesson page.
3. **Tax.** 04 says "before tax, charge two eighty" and the SPEC on screen says "Quote = new price - credit, plus tax", yet the quote's
   amount due, "charged $280", "$280 in the ledger" and "all say two eighty" are the pre-tax figure. Harmless if the example has no tax.
   Say so on the lesson page ("no tax in this example"). **Leave** in the video.
4. **12_run, the idempotency claim has lost lesson 8's hedge.** "So a double-click, or a retry, doesn't charge twice" is true only where
   the processor honours the key ("many payment processors support one", lesson 8). In a made-up system this is a design statement, and
   13 then shows a limit, so it is not a claim beyond the facts. Put the hedge on the page. **Leave.**
5. **06_graph, the annual plan has no arrow though the quote names it.** The caption is "An arrow only where something crosses", the
   quote's fields include "New plan", and the new plan's price feeds the credit sum. "One new thing" covers the narration; the picture
   still shows the first part touching nothing. A fourth arrow would break "Three parts share it". **Leave.** The three arrowheads are
   about 18 px tall and their direction is hard to read at phone size; enlarge them if the layout is touched for N1.
6. **08_decide, the third column head is shrunk to about 13 px** ("THE AGENT DOESN’T CLASSIFY OR APPROVE. IT BRINGS") against 16 px for
   every other head. It fits (ends 29 px inside the panel). Shorter: head "THE AGENT DOESN’T CLASSIFY OR APPROVE", lines "It brings the
   change, the evidence, / the risk, the way back". **Worth applying** if the stills are regenerated anyway.
7. **12_run, slot 9 is an empty dashed box for the whole of the second-longest scene** (about a fifth of the panel, 27 s). Round 1 raised
   it; unchanged. The left note "idempotency key = quote ID" is wider than its Charge box and starts 12 px from the panel edge; not
   clipped. **Leave.**
8. **11_go, the "SHIPS" stub has no arrowhead in the late still** (it has one in 12). The still is taken 0.55 s before the end and the
   ship step lands at 94% of the scene, so the arrow has about 1.5 s to draw. Check it in the rendered video. **Leave.**
9. **14_constants, "somebody understands the layer below: someone who can work that credit out by hand".** Doing the sum by hand is
   knowing the business rule, not the layer below. Closer to lesson 1: "someone who knows what the processor does with that key". Same
   length. **Leave** unless 14 is touched.
10. **15 and 16 give the same list twice in 35 seconds.** Under the cap now, and the map pulse earns 15 its place. **Leave.**
11. **02_quiz opens with lesson 6's first sentence, word for word** ("Picture a made-up billing system."), and "It depends" is the
    weakest correct answer in the series: true of almost any question. The reveal line ("On a rule nobody has written down") rescues it.
    **Leave.**
12. **"Routine" is never said** (round 1 M2c), and the event chain and the nightly reconcile share one tag, "A PIPELINE". **Leave.**
13. **Rule card, "a whole feature" and "show a person"** still need "more than one part" and "wait for a yes" in the page's full rule
    (round 1 minor 15). The page does not exist yet. **Do it when the page is written.**

---

## Screen vs voice, scene by scene

Words are spoken words with tags and `[pause]` stripped.

| Scene | Words | On screen, never spoken in the scene | Spoken, not shown | Contradiction? |
|---|---|---|---|---|
| 01_title | 13 | "From loop to enterprise systems • clarkhuang.github.io" (same sub as lessons 5-8) | none | No |
| 02_quiz | 55 | "the full annual price"; "credit the unused days" | "Picture a made-up billing system"; "an agent will build either answer, without asking" | No |
| 03_feature | 33 | "MADE-UP NUMBERS"; "MID-MONTH"; "switch to annual, mid-month" | "from lesson one" | No. Skeleton shows slots 1-7; 8 and 9 arrive with the pipeline panel |
| 04_right | 55 | caption "Until a person decides the rule, there is no right answer to build."; "DAY 10 OF 30"; "10 DAYS USED"; "Annual plan $300" | "What's scarce, lesson one said" | No. Layout defect N1 |
| 05_readable | 43 | "billing/upgrade/"; SPEC lines 2-3 ("Quote = new price - credit, plus tax." / "Charge the quote, exactly once."); "READABLE" | "in the repository" | No. "plus tax" against $280 everywhere else: minor 3 |
| 06_graph | 53 | caption "An arrow only where something crosses."; sample row "Q-1 · Monthly · Annual · $20 · $280" | none | No. Missing plan arrow: minor 5 |
| 07_parallel | 42 | caption "Plan how the work comes back together, before it splits."; "NOT NEW"; "AGENT A/B/C"; "written before anyone starts" (spoken as "before anyone starts") | none | No |
| 08_decide | 44 | "Named in the repo"; caption "Money moves, so a named person decides." | none | No |
| 09_checks | 47 | "AS CHECKS"; "CHECKS, BEFORE" | none | No. Content gap N2 |
| 10_skill | 32 | caption "Reuse what recurs." (spoken in 15) | none | No |
| 11_go | 52 | "THE BUILD, AS IT RUNS"; "SHIPS"; "Says yes" | none; all eight log rows are the narration | No |
| 12_run | 70 | "charged $280"; "now annual"; "monthly renewal off"; "invoice written"; "$280 in the ledger"; "receipt sent"; "ledger = processor"; caption "Safe to run twice: same key, no second charge." | "double-click"; "a retry"; "Every step leaves a record" (shown as the notes) | No |
| 13_operate | 80 | "id: billing-ops-agent"; "THE OPERATOR"; "the three checks" (beside "a fourth check") | "the least access the job needs"; "two browser tabs, two quotes"; "One night" | No; stale label, minor 2 |
| 14_constants | 61 | "Things you don't control" (spoken "You depend on things you don't control"); "the three checks" | "someone who" | No; minor 2 |
| 15_recap | 40 | nothing new | all nine recap phrases (each is a pulse on its map element) | No |
| 16_rule | 56 | "THE FULL RULE IS ON THE LESSON PAGE" | none; card is the narration | No |
| 17_ask | 34 | none | none ("A.I." shown as "AI") | No |
| 18_close | 39 | none | "plan, build, verify"; "You still own the outcome"; "Thanks for watching" | No |

Stills: one defect (N1). No other overflow, overlap, clipping or empty frame. Smallest text: 08's third head (about 13 px) and the note
"charged $280" (about 18 px). The frame below y = 920 is empty in 03-13, as in round 1; acceptable.

---

## The new text, point by point

| Added in the revision | Verdict |
|---|---|
| Quiz "It depends" | Correct, and consistent with $280 twenty seconds later because the reveal is about the unwritten rule. Weak as a quiz answer (minor 11). |
| "so the agent asks" | Fine; it is the only demonstration of the rule's last line. Its on-screen head causes N1. |
| Quote "Its I.D."; "the quote's format is the shared contract" | Correct. Fixes round 1's format-versus-value point. |
| Arrow directions | Correct: Calculate writes the quote, Show and Charge read it. Small (minor 5). |
| "NOT NEW" then "A SKILL" | Clear in the stills; the label swaps in 10 in the same place. |
| "Each charge equals its quote" | Survives tax, but stops testing the amount: N2. |
| "a person has read it" | Acceptable; asserted, not shown. |
| Two triggers; "an idempotency key that never changes: this quote's I.D." | Sound. Event chain and nightly run are visibly separate. "Never changes" holds for one quote; 13 shows what happens with two. |
| Failure beat, "two browser tabs, two quotes... a fourth check: one open quote per subscription" | Technically sound: two quotes mean two keys, check 2 passes for both, check 1 fails, a person refunds (the operator cannot move money). Consistent with the idempotency claim once "two keys" is said (minor 1). "Three checks" on screen goes stale afterwards (minor 2). |
| Four-constants cards, "Invoice = ledger = processor: $280" | Matches the narration and the stage notes. Pre-tax figure (minor 3). |
| Shortened your-turn | Good. It now tests "A blank line? Stop, and ask." |

## Against lessons 1-8

No contradiction found. Lesson 1: "knowing it's right" and the four constants are worded as recorded (the card shortens the third).
Lesson 2: spec as source, agents file, index. Lesson 3: "its own node, with one owner"; arrows only where something crosses (minor 5).
Lesson 4: contract first; brief, finish line, check; one merge point; "They meet early"; whole feature tested on staging. Lesson 5:
"doesn't classify it, or approve it"; "the change, the evidence, the risk, and the way back"; "An engineer reviews the code. The finance
owner says yes." Lesson 6: "Write them once, run them twice"; sample then real; the miss fed back (as a check, not a brief line). Lesson 7:
"written down, and tested". Lesson 8: trigger, event and schedule, every step leaves a record, idempotency key, reconcile against the
processor's record, "an agent works" the step that needs judgment, a person acts on a mismatch. Lesson 9: identity, least access, logged
actions, a person at the decision, all from the outline and presented as a question, not as recorded content. No presenter claim, no real
company, no statistic.

## Is it at least as good as lessons 5-8?

Yes, once N1 and N2 are fixed. It is more ambitious than any of them and the single map that fills in, dims for the run and pulses in the
recap is the best visual in the series. It is still weaker in four places:

- **The failure is told, not shown.** Lesson 6 puts the three wrong renewals on screen and lesson 8 draws the 2 a.m. retry. Here the double
  charge is three short sentences and one green line in the operator box.
- **Density at the end.** 13 carries lesson 9, the failure and the fix in 80 words, and 14-15 put the map, the pipeline, the operator and
  four cards on one frame with 18 to 21 px text. Lessons 5-8 never ask the eye to hold that much.
- **Technical loose ends per minute.** Tax, the quote's expiry, a declined charge and the processor hedge are all deferred to a lesson page
  that is not written yet. Lesson 8 after its round 2 had none.
- **The hook.** "It depends" is a softer open than lesson 8's "charged twice" or lesson 5's forty changes.

## Word counts

| Scene | Words | Scene | Words |
|---|---|---|---|
| 01_title | 13 | 10_skill | 32 |
| 02_quiz | 55 | 11_go | 52 |
| 03_feature | 33 | 12_run | 70 |
| 04_right | 55 | 13_operate | 80 |
| 05_readable | 43 | 14_constants | 61 |
| 06_graph | 53 | 15_recap | 40 |
| 07_parallel | 42 | 16_rule | 56 |
| 08_decide | 44 | 17_ask | 34 |
| 09_checks | 47 | 18_close | 39 |

**Total 849** (cap 858). With N2 (+6) and minor 1 (+2): **857**, 5:30 at 2.6 words/second, about 4:50 to 5:02 at the rate lessons 5-8
were actually recorded.

---

## Author's disposition (added after the fixes; the review above is unchanged)

| Finding | Disposition |
|---|---|
| N1 `04_right` heading cut by the divider | Fixed: "A PERSON'S CALL, SO THE AGENT ASKS · $30 A MONTH, DAY 10 OF 30". Still re-rendered and checked. |
| N2 `09_checks` no check tests the amount | Fixed: spoken "Each quote follows the rule, and each charge equals its quote."; on screen "2   Each quote = the rule; each charge = its quote". |
| `13_operate` "two keys" | Applied: "two browser tabs, two quotes, two keys." |
| Reconcile note after the fourth check | Applied: the note reads "the checks" in 12 to 15. |
| `08_decide` shrunk column head | Applied: head "THE AGENT BRINGS"; "It doesn't classify, or approve" moved into the body. |
| Page notes | Written in `se201-10-page.md`. |
| Failure told, not shown | Left. The caption and the operator's last line show it; a drawn failure would need another scene and the lesson is at the length cap. |
| Dense frames 13 to 15 | Left. The map is the point of those frames; smallest body text is about 19 px, the same as lesson 8's records. |

To stay under the cap after these additions, "not a borrowed login" was cut from 13 (and from the operator card) and one clause in 05 was shortened. Final count: 852 spoken words, 5:28 by the estimate.

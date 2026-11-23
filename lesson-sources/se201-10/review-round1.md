# SE201 Lesson 10, "Capstone: One Feature, End to End": review, round 1

Reviewer: an independent agent that did not write the script. Read: `scripts/se201-10-capstone.json`, all 18 stills, `briefA.md`,
`brief-common.md`, the narration of recorded lessons 1-8, the lesson 9 outline, and the round-1 reviews of lessons 5-8.

**Verdict: CHANGES NEEDED.** The through-line map is the best visual in the series and the arithmetic is right, but the feature as drawn
never switches the subscription, the run-time diagram is wrong in three places, check 2 breaks on the first taxed upgrade, the plan act is
seven same-shaped "Lesson N:" beats, and the script is 875 spoken words against a cap of 858.

Arithmetic checked: $30 / 30 days x 20 unused days = $20; $300 - $20 = $280; $20 + $280 = $300. Consistent on every still.
No presenter claim, real-company claim, statistic or banned speech tag found. `se201-10-facts.md`, `-brief.md`, `-page.md` and
`-claims-toned-down.md` do not exist in the work folder yet.

---

## MAJOR

**M1. Nothing in the feature switches the subscription, yet check 3 tests for it.** (06_graph, 09_checks, 12_run)
Words at issue: the four parts "Add the annual plan. Calculate the credit. Show the amount, and get a yes. Charge it, and record it."; the
run "Quote, charge, invoice and ledger, email."; check 3 "the old monthly plan never renews again."
Problem: no part and no pipeline step moves the subscription from monthly to annual, stops the monthly renewal, or sets the renewal a
year out. A billing engineer will see that the feature takes $280 and leaves the customer on monthly. Check 3 tests work that nobody was
briefed to build. Nothing says what happens when the card is declined either.
Replacement: part 4, spoken "Charge it, and switch the plan." and box "Charge it,\nswitch the plan". In 12_run, speak "Charge, switch the
plan, invoice and ledger, email." and rename the third stage "Switch plan,\ninvoice, ledger". Put on the lesson page: "a declined charge
leaves the subscription on monthly".

**M2. The run-time diagram in 12_run is wrong in three places.** (12_run, held through 13-15)
(a) Under the tag "STARTS WHEN THE CUSTOMER CONFIRMS" the first stage is "Quote". The customer confirmed a quote they were already shown
("Show it, get a yes"). A quote made after the yes can differ from the one shown (at midnight the credit becomes $19).
(b) "Email -> Reconcile" is drawn as one chain under that same event tag, but reconcile is nightly. Lesson 8 keeps those as different
triggers ("On a schedule... On an event... Or when the step before it finishes").
(c) Lesson 8's own vocabulary is absent. "Routine", "pipeline" and "idempotency key" are never spoken or shown in the capstone.
Replacement narration (76 words): "Now it runs on its own. The trigger is an event: the customer confirms the quote. Charge, switch the
plan, invoice and ledger, email. Every step leaves a record. And the charge carries an idempotency key that never changes: this quote's
I.D. So a double-click, or a retry after a dropped connection, doesn't charge twice. [pause] A second trigger, every night: reconcile our
ledger against the processor's record, and run the three checks on the real upgrades."
Screen: drop the "Quote" stage, or retitle it "The confirmed quote" and put it left of the trigger tag. Remove the Email -> Reconcile
arrow and give Reconcile its own amber tag "EVERY NIGHT". Change the panel tag to "A PIPELINE · RUNS ON ITS OWN".

**M3. The idempotency claim is stated as an absolute, and "key = this quote" is under-specified.** (12_run)
Words at issue: "a key that never changes: this quote. So a double-click, or a retry after a dropped connection, gets the first result
back. One charge." Caption: "Safe to run twice: the same key gets the first result back."
Problem: lesson 8 hedged this twice ("Some processors catch a quick duplicate, but don't count on it"; "many payment processors support
one"). The capstone drops the hedge. A double-click is also two requests in flight at once, and a processor may reject the second one as a
conflict instead of returning the first result. The outcome that can be promised is "no second charge". The quote as listed ("Old plan,
new plan, credit, amount due") has no identity and no expiry, so "this quote" cannot be a key, and two browser tabs give two quotes and
two charges.
Replacement: narration as in M2 ("this quote's I.D." and "doesn't charge twice"). Caption: "Safe to run twice: same key, no second
charge." Add a third greyed line to the 06_graph quote panel: "Quote ID · good until midnight". Lesson page: "one open quote per
subscription; many processors support idempotency keys, and keys expire".

**M4. Check 2 contradicts the lesson's own "before tax".** (04_right, 09_checks, 12_run)
Words at issue: 04 "So, before tax, charge two eighty." 09 "Each charge equals the new price, minus the credit." On screen "2   Each
charge = the new price − the credit".
Problem: once tax is added, every charge fails check 2 as written. Lesson 7's check says "charges the right amount, tax included". Check 2
also re-derives the amount instead of comparing against the contract the lesson has just set up.
Replacement: spoken "Each charge equals its quote." On screen "2   Each charge = its quote". Change the spec line in 05_readable to
"Quote = new price − credit, plus tax. Charge the quote, exactly once."

**M5. The plan act is a recap list in disguise: seven consecutive scenes with the same opener and shape.** (05_readable to 10_skill, 12, 13)
Words at issue: "Lesson two: make it readable." "Lesson three: draw the graph." "Lesson four: plan the integration first." "Lesson five:
who decides?" "Lesson six: turn right into checks..." "Lesson seven: what's already a skill?" "Lesson eight: now it runs on its own."
"Lesson nine's idea: who operates it?"
Problem: the brief says "must not be a list-y recap". The map already carries the lesson number in a circle on every element, so the
spoken "Lesson N:" is redundant and makes each scene a recap bullet. Each beat is 43-52 words, each in the pattern heading, then
application. It reads as a table of contents with examples.
Replacement: say once in 03_feature "Each number is the lesson it comes from", then let the feature's need drive each opener:
05 "Now make it readable." 06 "Next, the graph." 07 "Then plan the integration, before anyone starts." 08 "Who decides?" 09 "Now turn
right into checks an agent can run." 10 "One part isn't new." 12 "Now it runs on its own." 13 "Lesson nine's question: who operates it?"
Keep the spoken lesson number only in 04 ("lesson one said"), 13 and 14. Full text is in the proposed cuts below.

**M6. "Three parts are new work" and "the fourth part" refer to something the viewer has not been told, and the count is wrong on
screen.** (07_parallel, 10_skill)
Words at issue: 07 "Three parts are new work, so: three agents". 10 "So the fourth part needs no new brief." On screen "THE FOURTH PART".
Problem: in 07 the viewer has just heard "Four parts" and now hears three, with no reason until three scenes later. In 10 "the fourth
part" is the first box on the map ("Add the annual plan" is leftmost and lit). Following lesson order forces lesson 7 after lesson 4,
though in a real plan you notice the reusable part while drawing the graph.
Replacement: 07 "Three parts are new work: three agents, each with its own brief, finish line, and check." is acceptable only if 10
opens "One part isn't new. Adding a plan has come back often enough to be a skill: written down, and tested. So that part needs no new
brief. An agent runs the skill." Panel head "THAT PART" in place of "THE FOURTH PART". Better still, dim the "Add the annual plan" box in
07 with a small "7 →" so the eye sees why it has no agent label.

**M7. Rule 10 says "show a person", and the lesson never does; "A blank line? Stop, and ask" is never demonstrated.** (16_rule, 11_go,
04_right)
Words at issue: rule "write the plan in the repo, and show a person"; 11 "The plan is written. Now, build."; 04 "And the amount is a
person's call. Here, the rule is:"
Problem: in the lesson a person appears only at the end (the finance owner's yes). Nobody reads the plan before the build, so the rule's
main verb is undemonstrated. The quiz is exactly a blank line, but the lesson never shows the agent stopping on it. The narrator supplies
the rule. Lines 2-6 of the rule are demonstrated; the first and last are not.
Replacement: 04 "The amount is a person's call, so the agent asks. The finance owner's rule: credit the days paid for, and not used."
11 "The plan is written, and a person has read it. Now, build." Add a first log row in 11: "The plan: read by a person".
Also 17_ask: "Then find the line it guessed, when it should have asked." (now it tests the rule's last line).

**M8. The example is used before it is called made up.** (02_quiz)
Words at issue: "Quick question. A customer pays thirty dollars a month."
Problem: the shared brief says "ALWAYS call it made up... aloud the first time in each lesson". "Made-up" is first spoken in 03. The
lesson 6 round-1 review rated this same slip major and fixed it with "Picture a made-up billing system."
Replacement: "Picture a made-up billing system. A customer pays thirty dollars a month."

**M9. Over length.** 875 spoken words = 5:37 at 2.6 words/second before twelve [pause]s; the cap is 5:30 (858 words). See the proposed
cuts: 835 words, with a further option at 792.

**M10. The graph's arrows and "the quote" blur a format with a value.** (06_graph, 07_parallel)
Words at issue: "What crosses? One thing: the quote." "That quote is the shared contract, written before anyone starts." On screen, three
identical arrows run down from "The quote" to Calculate, Show and Charge; the panel shows an instance ("Monthly · Annual · $20 · $280").
Problem: what is written before anyone starts is the quote's format. A $280 quote cannot be written first. Calculate produces the quote
and the other two consume it, yet all three arrows point the same way. "One thing" is also untrue as stated: the customer's yes crosses
from Show to Charge, and the plan's price feeds the quote. An experienced engineer will ask which graph this is, build order or data flow.
Replacement: 06 "What crosses? One new thing: the quote." (plans and prices already exist in this system). 07 "The quote's format is the
shared contract." Quote sub-label in 07: "its format: the shared contract, written first". Draw the Calculate arrow pointing up into the
quote and the other two pointing down.

---

## MINOR

1. **02_quiz, the answer is the series' stock trick, word for word.** Lesson 4's quiz: "Or does nobody know yet? Nobody knows yet."
   Lesson 3: "impossible to tell". Lesson 6: "you can't tell from that". A returning viewer picks C before the options finish. The two
   real options also omit the commonest policy (charge nothing today, switch at renewal). Preferred: options "$300: the full annual
   price" / "$280: credit the unused days" / "It depends on a rule nobody wrote down", reveal "It depends. Nobody has written down what
   right means." Twenty seconds later the lesson says $280, so the "why" must stay about the rule, as it does.
2. **02_quiz, "And an agent can build either answer in an afternoon."** Reuses lesson 1's hook phrase and misses the risk. Replace: "And
   an agent will build either answer, without asking." (sets up the rule's last line).
3. **08_decide, the agent classifies its own change.** "Does it move money? Yes." is answered by nobody; lesson 5 says "The agent that
   wrote a change doesn't classify it, or approve it" and the capstone keeps only "doesn't approve it". Replace: "Who decides? It moves
   money, so a person does. The repository already says who: fees and prices, the finance owner. The agent that writes the change doesn't
   classify it, or approve it. It brings the change, the evidence, the risk, and the way back."
4. **08_decide, "FIRST OF THE FOUR QUESTIONS" is on screen; "four questions" is never spoken.** Change the head to "DOES IT MOVE MONEY?"
   and the lines to "Yes. So a person decides".
5. **13_operate, "it never sees a card."** In this system nobody does: the brief says the processor holds the card and we hold a token.
   The line implies other parts do see cards. Cut it; keep "It can't move money." On screen: "Can't move money. Can't edit the ledger."
6. **13_operate, "An agent runs that reconcile."** Lesson 8: "Most of these steps are plain code. An agent earns its place where a step
   needs judgment, like working out why they don't match." Replace "runs" with "works": "An agent works that nightly reconcile."
7. **09_checks caption (16 words, never spoken): "Green only says the code did what its tests asked. These say what right is."** The
   second sentence overclaims against lesson 6 ("A check only catches what somebody thought to ask"). Replace the caption with the spoken
   line: "Write them once, run them twice."
8. **10_skill caption "Seven lessons in, and nothing is built yet. The plan is."** Never spoken, and "seven lessons in" is odd two
   minutes into one video. Replace with "The plan is written." and let 11 speak it.
9. **10_skill, "Billing period: one year. The price: a new version."** Cryptic without lesson 7 (a new plan has no old version), and the
   lesson 7 review already flagged "plan as a new price version" as muddled. Cut both sentences and both greyed lines (11 words).
10. **09_checks, "never renews again".** As a check it is unbounded. Say "doesn't renew again"; on screen "3   The old monthly plan
    doesn't renew".
11. **05_readable, "so any agent can find it".** Say "so an agent can find it". Lesson 2's own term "Markdown twin" is missing, and in
    lesson 2 `index.md` is the page twin while the index of the whole system is a separate file. Either label the third file "the index"
    or leave it; do not claim more.
12. **14_constants, screen and voice disagree.** Screen "SOMEBODY KNOWS THE LAYER BELOW"; voice and lesson 1 say "understands". Use
    "SOMEBODY UNDERSTANDS THE LAYER BELOW".
13. **14_constants, "Money has to add up: twenty in credit, plus two eighty charged, is three hundred."** It restates the subtraction
    from 04, so it proves nothing. Lesson 8's sense was step records agreeing. If a word can be spared: "the invoice, the ledger and the
    processor all say two eighty charged". Otherwise leave.
14. **15, 16 and 17 say the same list three times in about 55 seconds** (the lesson 7 review flagged the same pattern). Cut the list
    from 17_ask (see cuts). If the measured audio is over 5:30, drop 15_recap as narration and let the map pulse under the first line of
    the rule scene.
15. **16_rule, "a whole feature" is not a threshold an agent can test.** Lesson 3 used "any job with more than one part". On the page's
    full rule write "a feature with more than one part"; the card can stay. The rule also never says to wait for the person: on the page,
    "show a person, and wait for a yes".
16. **12_run, "Every step leaves a record" is spoken and nothing on screen shows a record.** That was lesson 8's central picture. Make
    each stage note the record ("charged $280", "invoice written", "receipt sent").
17. **Lesson 9 is not a video.** "Lesson nine's idea" is within the brief, but recorded lesson 8 says "That's the last lesson... See you
    in lesson nine" and lesson 1 says "And finally, agents that operate enterprise systems". The series page must explain that 9 is an
    outline and 10 is the capstone. Nothing to change in the narration.
18. **Nothing goes wrong.** Lessons 6 and 8 each have a failure the method catches (three wrong renewals inside a matching total; the
    2 a.m. retry). Here every check passes and the operator's flag is hypothetical. If 15_recap is dropped, spend 15 of the saved words
    in 13: "One night, an upgrade shows two charges. The agent flags it. A person refunds it. And the miss becomes a fourth check." That
    also restores lesson 6's "feed every miss back", which the capstone omits.
19. **18_close.** "Thanks for watching" is fine and promises nothing. "Every box on that map is still one loop: plan, build, verify"
    matches lesson 3. No change.

---

## Screen vs voice, scene by scene

Words are spoken words, tags and [pause] stripped. "Late still" problems are what the PNG shows.

| Scene | Words | On screen, never spoken in the scene | Spoken, not shown | Still: layout problems |
|---|---|---|---|---|
| 01_title | 13 | "From loop to enterprise systems • clarkhuang.github.io" (standard) | none | none |
| 02_quiz | 55 | "credit the days not used" (option B) | "an agent can build either answer in an afternoon" | none |
| 03_feature | 41 | "MID-MONTH", "MADE-UP NUMBERS" | none | Right column of the lower panel is half empty; the skeleton shows placeholders 1-5 only, though nine numbers arrive |
| 04_right | 52 | caption "Until a person decides the rule, there is no right answer to build."; "DAY 10 OF 30"; "10 DAYS USED"; "Annual plan $300" | "what's scarce?" (nothing on screen says scarce) | none |
| 05_readable | 44 | "billing/upgrade/"; spec lines 2-3 "Charge the new price minus the credit, exactly once."; label "READABLE" | "in the repository" | none |
| 06_graph | 51 | caption "An arrow only where something crosses."; "Monthly · Annual · $20 · $280" | none | All three arrows point down, including into the part that produces the quote (M10) |
| 07_parallel | 45 | caption "Plan how the work comes back together, before it splits."; "AGENT A/B/C" | "Three parts are new work" | "Add the annual plan" sits unlabelled and unlit with no reason given (M6); agent labels about 15 px |
| 08_decide | 46 | "FIRST OF THE FOUR QUESTIONS"; "WHO APPROVES WHAT · A FILE IN THE REPO"; "fees and prices:"; caption "Money moves, so a named person decides." | "who set that credit rule" | none |
| 09_checks | 52 | caption "Green only says the code did what its tests asked. These say what right is." | none | Badge 6 appears twice (top bar and under the merge box); "CHECKS, BEFORE" is about 15 px |
| 10_skill | 43 | "OR A PRICE"; caption "Seven lessons in, and nothing is built yet. The plan is." | "came back often enough" | "THE FOURTH PART" while the first box is lit (M6) |
| 11_go | 46 | "THE BUILD, AS IT RUNS"; "SHIPS" | none | "SHIPS" stub is a bare line with no arrowhead at this moment; check it in motion |
| 12_run | 75 | "credit $20 / due $280"; "$20 + $280 = $300"; "a receipt"; first stage "Quote" contradicts the trigger tag | "Every step leaves a record"; "double-click"; "dropped connection"; "our ledger against the processor's record" | Dashed slot 9 holds about a quarter of the panel empty for the longest scene (about 29 s); stage notes about 21 px; Email -> Reconcile arrow is wrong (M2) |
| 13_operate | 64 | "id: billing-ops-agent"; "THE OPERATOR" | "the least access the job needs" (caption only, late) | Operator body text about 21 px, the smallest body text in the lesson, five lines tight in the box |
| 14_constants | 61 | "KNOWS" where the voice says "understands"; "The payment processor" for "the processor" | "a person who can work that credit out by hand" (screen: "Can work it out by hand") | Constant-card heads about 14 px with wide tracking: unreadable on a phone. The densest frame; no overlap |
| 15_recap | 47 | nothing new | all nine recap phrases (pulse only) | none |
| 16_rule | 56 | "THE FULL RULE IS ON THE LESSON PAGE" (standard) | none | none; seven lines fit |
| 17_ask | 45 | none | "what right means, the graph, the contract, who decides, what runs on its own" | none |
| 18_close | 39 | none | "plan, build, verify"; "You still own the outcome" | none |

General: no overflow, overlap or clipping in any still. In 03-13 the frame is empty below y = 920 (about 15%), which is acceptable. The
disclosure line "A MADE-UP EXAMPLE, MADE-UP NUMBERS · ..." is the dimmest text on screen; raise its contrast one step. Map text at 55% dim
in 12-13 is still legible.

---

## Accuracy against lessons 1-8

| Beat | Verdict |
|---|---|
| 04 (L1) "what's scarce? Knowing it's right." | Matches lesson 1 ("Knowing that it's right. That, and context"). |
| 05 (L2) "The spec is the source. Change it, and the build follows." | Matches ("Change the brief, and the build follows"). "Markdown twin" dropped (minor 11). Staging plus a person's approval is honoured in 11. |
| 06 (L3) "its own node, with one owner"; caption "An arrow only where something crosses" | Matches rule 3. The arrows drawn do not (M10). |
| 07 (L4) contract first; brief, finish line, check; one merge point; test the whole | Matches rule 4. "Merge early" appears in 11 ("They meet early"). |
| 08 (L5) four questions; packet | "the change, the evidence, the risk, and the way back" matches rule 5. Drops "doesn't classify it" (minor 3). 11 keeps "An engineer reviews the code", matching lesson 5. |
| 09 (L6) "Write them once, run them twice" | Matches. Omits "feed every miss back" and "when a check fails, stop and tell a person" (minor 18). |
| 10 (L7) skill "written down, and tested" | Matches. "Came back often enough" is a fair stand-in for "the third time". |
| 12 (L8) trigger, records, key, reconcile | "a key that never changes" and "reconcile ... our ledger against the processor's record" match. Missing: "routine", "pipeline", "idempotency key", and lesson 8's hedge (M2, M3). |
| 13 (L9 outline) identity, least access, audit trail, people at decision points | Consistent with the outline; presented as an idea, not as recorded content. |
| 14 four constants | Wording matches lesson 1 except the on-screen "KNOWS" (minor 12). |

---

## Rule 10

- Consistent with the example: yes, lines 2-6 each map to a scene (04/09, 06/07, 08, 10, 12/13).
- Not demonstrated: "show a person" and "A blank line? Stop, and ask." (M7).
- Missing from the rule but taught in the lesson: one merge point (lesson 4) and what happens when a step fails or runs twice (lesson 8).
  Acceptable on the card; put both in the full rule on the page.
- Usable by an agent: mostly. "A whole feature" needs a threshold and "show a person" needs "and wait for a yes" (minor 15).

## Where it is weaker than lessons 5-8

- No failure and no surprise. Lesson 6 has the matching totals and lesson 8 has the 2 a.m. retry. The capstone's only tension is the quiz.
- Seven same-shaped beats in a row (M5). Lessons 5-8 vary scene length and form.
- More technical loose ends per minute than lesson 8 after its round 2 (M1-M4, M10).
- Stronger than 5-8 in one respect: the single map that fills in, dims for the run, then pulses in the recap. Keep it.

---

## Proposed cuts: 875 -> 835 spoken words (about 5:21 before pauses)

Every lesson's beat is kept. Count per scene, old -> new.

- **01_title (13 -> 13)** unchanged.
- **02_quiz (55 -> 57)** "Picture a made-up billing system. A customer pays thirty dollars a month. Ten days in, they click: switch to
  annual. Three hundred a year. What do you charge them, today? [pause] Three hundred? Two eighty? Or: nobody knows yet? [pause]
  <emphasis>Nobody knows yet.</emphasis> Nobody has written down what right means. And an agent will build either answer, without asking."
- **03_feature (41 -> 33)** Cut "It's small enough to hold in your head. And it takes every lesson in the series." Text: "So this last
  lesson builds that one feature, end to end, in our made-up subscription-billing system from lesson one. [pause] Here's the map we'll
  fill in. Each number is the lesson it comes from." Caption becomes "Each number is the lesson it comes from."
- **04_right (52 -> 56)** "What's scarce, lesson one said, is knowing it's right. So first, say what right means: every upgrade is
  charged the right amount, exactly once. [pause] The amount is a person's call, so the agent asks. The finance owner's rule: credit the
  days paid for, and not used. Twenty days, twenty dollars. So, before tax, charge two eighty."
- **05_readable (44 -> 43)** "Now make it readable. The rule goes into a spec, in the repository, with an agents file that says how to
  work there, and an index, so an agent can find it. [pause] The spec is the source. Change it, and the build follows."
- **06_graph (51 -> 51)** "Next, the graph. Four parts. Add the annual plan. Calculate the credit. Show the amount, and get a yes.
  Charge it, and switch the plan. [pause] What crosses? One new thing: the quote. Old plan, new plan, credit, amount due. Three parts
  share it, so it's its own node, with one owner."
- **07_parallel (45 -> 41)** "Then plan the integration, before anyone starts. The quote's format is the shared contract. Three parts
  are new work: three agents, each with its own brief, finish line, and check. One merge point, on staging, where the whole feature is
  tested."
- **08_decide (46 -> 44)** "Who decides? It moves money, so a person does. The repository already says who: fees and prices, the
  finance owner. The agent that writes the change doesn't classify it, or approve it. It brings the change, the evidence, the risk, and
  the way back."
- **09_checks (52 -> 47)** "Now turn right into checks an agent can run. No upgrade is charged twice. Each charge equals its quote. And
  the old monthly plan doesn't renew again. [pause] Write them once, run them twice: before it ships, on sample upgrades. And every night
  after, on the real ones."
- **10_skill (43 -> 32)** Cut "Billing period: one year. The price: a new version." Text: "One part isn't new. Adding a plan has come
  back often enough to be a skill: written down, and tested. So that part needs no new brief. An agent runs the skill."
- **11_go (46 -> 52)** "The plan is written, and a person has read it. Now, build. Four parts, at the same time. They meet early, at the
  merge point, and the whole feature runs on staging. The three checks pass, on sample upgrades. An engineer reviews the code. The
  finance owner says yes. [pause] And it ships."
- **12_run (75 -> 76)** text in M2.
- **13_operate (64 -> 58)** Cut "and it never sees a card". Text: "Lesson nine's question: who operates it? An agent works that nightly
  reconcile. It gets its own identity, not a borrowed login, and the least access the job needs: it reads the ledger, and the
  processor's report. It can't move money. Every action is logged. And when an upgrade doesn't add up, it flags it, and a person decides."
- **14_constants (61 -> 60)** last clause "someone who can work that credit out by hand"; otherwise unchanged.
- **15_recap (47 -> 43)** "So that's the series, in one feature. Say what right means. Write it down. Draw the graph. Merge in one
  place. Put a person where it matters. Check it, before and after. Reuse what recurs. Let it run. And know who's running it." (merges
  "Build in parallel, merge in one place.")
- **16_rule (56 -> 56)** unchanged.
- **17_ask (45 -> 34)** Cut the repeated list. Text: "Now, your turn. Pick one small feature in a system you work on. Before any code,
  ask your A.I. to write that plan. [pause] Then find the line it guessed, when it should have asked." Card last line: "Then find the
  line it guessed."
- **18_close (39 -> 39)** unchanged.

**Total: 835 words = 5:21 at 2.6 words/second, plus twelve pauses.** That is close to the cap once pauses are added. If the measured
audio exceeds 5:30, drop the 15_recap narration (minus 43, total 792, about 5:05) and run the map pulse under the opening sentence of
16_rule; optionally spend 15 of those words on the failure beat in minor 18 (total 807).

---

## Author's disposition (added after the revision; the review above is unchanged)

| Finding | Disposition |
|---|---|
| M1 nothing switches the plan | Fixed. Part 4 is "Charge it, and switch the plan"; the pipeline has a "Switch the plan" step with the record "now annual / monthly renewal off". Declined charges are in the page notes. |
| M2 run diagram | Fixed. "Quote" stage removed; four chained steps under "WHEN THE CUSTOMER CONFIRMS"; Reconcile stands apart under its own "EVERY NIGHT" trigger, no arrow from Email; "pipeline" and "idempotency key" are spoken and shown. "Routine" is not used. |
| M3 idempotency absolute | Fixed. "this quote's I.D." and "doesn't charge twice"; caption "Safe to run twice: same key, no second charge."; the quote now has an ID on screen. Processor support is in the page notes. |
| M4 check 2 vs tax | Fixed, then tightened in round 2: "Each quote follows the rule, and each charge equals its quote." The spec reads "Quote = new price - credit, plus tax." |
| M5 "Lesson N:" list | Fixed. Said once ("Each number is the lesson it comes from"); scene openers now follow the feature. |
| M6 three parts / fourth part | Fixed. "NOT NEW" sits under the plan part from scene 07; scene 10 opens "One part isn't new." |
| M7 rule not demonstrated | Fixed. 04 "so the agent asks"; 11 "The plan is written, and a person has read it"; 17 "the line it guessed, when it should have asked". |
| M8 made-up | Fixed. The lesson's first sentence after the title is "Picture a made-up billing system." |
| M9 length | Fixed: 852 words, 5:28 by the estimate. |
| M10 format vs value, arrows | Fixed. "One new thing: the quote"; "The quote's format is the shared contract"; Calculate's arrow points up into the quote, the other two point down. |
| Minors 1-14, 16 | Applied (quiz reworked to "It depends"; "doesn't classify it, or approve it"; card line cut; "works that nightly reconcile"; captions replaced; skill detail cut; "doesn't renew again"; "an agent"; constants cards rebuilt with readable text and the spoken wording; "all say two eighty"; list cut from the your-turn; stage notes are now records). |
| Minor 15 rule threshold | On the page: "a feature with more than one part ... show it to a person, and wait for a yes". Card unchanged. |
| Minor 17 lesson 9 | Noted in `series-update.md` and `lesson9-outline.md`. |
| Minor 18 nothing goes wrong | Applied: the two-charges beat in 13, which also restores lesson 6's "feed every miss back". |
| Minor 19 | No change needed. |

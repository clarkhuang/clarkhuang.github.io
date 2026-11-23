# Review round 1: SE201 Lesson 5, Governance: Where People Decide

Reviewer: an independent agent that did not write the script. It read the first draft (kept here as `make_se201_05_governance.round1.py`),
every preview still, lessons 1 and 4, and the series outline. Verdict: **CHANGES NEEDED**. No presenter-fact, name or statistic violations
were found. Each finding is followed by my disposition.

## MAJOR
1. **Contradicts lesson 2's rule.** "Four no's, and it ships on its checks" clashed with lesson 2's "every change through staging for a
   person to approve"; the reconciliation only arrived late and the rule card left it out. *Fixed.* Scene 04 now says "that kind of change
   can ship on its checks"; 08c says "start strict, like lesson two: a person on every change. Then release one kind at a time, as its
   checks earn trust"; the recap says "one released kind at a time"; the rule card's last line is "Ship on checks alone only what a person
   released."
2. **Low-risk examples were misclassified.** A typo in a customer email template is customer-facing and cannot be unsent; "wording, tests,
   internal tools" on checks lets an agent weaken a test; nothing covered the pipeline or the approvals file itself. *Fixed.* The free rows
   are now "Fix a typo on an internal admin screen" and "Add a missing test for renewals"; the table row is "Internal screens, docs, added
   tests"; a new row says "The checks, the pipeline, this file: always a person".
3. **The agent classified its own change.** *Fixed.* 07 now says "the pipeline enforces it, by what a change touches. The agent that wrote
   a change doesn't classify it, or approve it." The rule card's first line is now "find out who decides", not "check who decides".
4. **Separation of duties cited, then broken** (changes shipping with no approver in audited systems). *Fixed in part.* 08c adds "And where
   an audit requires a review, that review stays", and the dial card says "Required reviews stay."
5. **The decision card seemed to replace code review on a money path**, the agent authored its own evidence, and the way back ignored fees
   already charged. *Fixed.* Evidence is now "From the pipeline"; the risk is "Some customers pay more; they must be told first"; the way
   back is "Restore the flat fee; credit anyone already charged"; the closing line is "Now the finance owner decides about the fee. And an
   engineer still reviews the code that moves money."
6. **"Touches customer data" had no example and never lit.** *Fixed.* Added a sixth piece of work, "Send customer emails to a new partner",
   which stops for a data owner. The example is now six things, four stops.
7. **Refund example inconsistent with question 1.** *Fixed.* 05c adds "Under the limit, a person already decided, when they set it."
8. **On-screen text not spoken** (table rows, card fields, question examples, "Every change"). *Fixed in part.* The examples under the
   four questions were removed; 07 now reads the table's rows aloud; "Every change" became "Most changes". The decision card keeps its five
   field values: the narration names all five fields and the evidence, and the values are the worked example itself.

## MINOR
- **Hook telegraphed its answer.** *Fixed:* "Forty changes, all green. One changes what customers are charged. Who catches it?"
- **08a/08b repeated the quiz; "honest" is a verbal tic across lessons.** *Fixed:* chapter renamed "What it costs", both beats cut to one
  sentence each.
- **Recap and rule were near duplicates.** *Fixed:* recap cut to three lines and 27 words.
- **03c conflated pull-request review with a deploy approval.** *Fixed:* "a pull request a reviewer approves, before it merges."
- **08b sub-line read broken.** *Fixed:* "Fast, until money moves unapproved / Nobody decided. It just shipped."
- **"After a rehearsal on a copy" spoken but not shown.** *Fixed:* cut.
- **The billing system appears in the quiz before "made-up".** *Fixed in part:* the quiz now opens "Picture this", which marks it as a
  hypothetical; the worked example still opens "Take our made-up example".
- **Your turn: "and who?" is unanswerable without the file.** *Fixed:* the exercise now hands the AI "the four questions" and drops "who".
- **Code owners file.** The spoken mention was cut for time; see `se201-05-claims-toned-down.md`.
- **Dial stills are half empty.** *Not changed:* that is the recorded `dial` layout from 101; the cards fill in over three beats.
- **Runtime at the ceiling.** After the fixes: 700 words, an estimated 269 s.

## Layout fixes found in my own pass over the stills
- The gate's tick overlapped a long reason label ("MONEY · HARD TO UNDO"): moved to the box's lower right.
- The eras cards had a large empty middle: added a fourth row ("Who wrote it: people").
- The third dial card overlapped the first at position 0.3: moved to 0.5.

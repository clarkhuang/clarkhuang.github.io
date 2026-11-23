# Review round 1: SE201 Lesson 6, Quality, Feedback, and Observability

Reviewer: an independent agent that did not write the script. It read the first draft (kept here as `make_se201_06_quality.round1.py`),
every preview still, lessons 1 and 4, and the series outline. Verdict: **CHANGES NEEDED**. The arithmetic added up and the stills had no
overflow, overlap or clipping. Each finding is followed by my disposition.

## MAJOR
1. **04a: the screen contradicted the narration.** "The table looks fine... From here, you can't say", while the table plainly showed a 2,
   a wrong amount and a zero. *Fixed:* "Here are last night's renewals. And the build is green. But no test ever looked at this table. So
   was last night right? The green can't say."
2. **04c: the totals argument backfired.** A $30 break is a failed reconciliation, so the total would have caught it. *Fixed:* R-1045 is
   now charged $119.00, so the three errors cancel (+29, +20, -49) and both totals read $354.00. "And look at the totals: they match. Three
   wrong renewals, inside a sum that's exactly right."
3. **Check 1 was naive for billing** ("every renewal due got charged" ignores declined cards). *Fixed:* "every renewal that was due was
   attempted"; the flag is "Never attempted".
4. **06: "the record says why" was overclaimed**; nothing in the record showed the first attempt had gone through. *Fixed:* the two charge
   steps now carry different keys (key A, key B), the reconcile step reads "processor: 2 charges", and the narration says "Then reconcile,
   against the processor's own report: two charges. The first attempt had gone through."
5. **05: the S.L.O. was a 100% deadline.** *Fixed:* "say, ninety-nine point nine percent of renewals due today, attempted by six A.M.",
   shown as "for example".
6. **On-screen text not spoken.** *Fixed:* the loop caption is now the spoken line "Every miss goes back into the brief and the checks";
   the lens label is lesson 1's wording, "architecture bends around what's scarce", which is now also spoken; the your-turn card matches
   the narration word for word.
7. **The billing system appeared in the quiz before "made-up".** *Fixed:* the quiz opens "Picture a made-up billing system."

## MINOR
- **Quiz option B was a strawman.** *Fixed:* "Probably: coverage is high".
- **Nothing said why green missed it.** *Fixed:* the fix fed back now includes "a new test: the processor times out".
- **"Here's what makes that sentence powerful".** *Fixed:* "That one sentence does double duty."
- **"Request key" is nonstandard.** *Fixed:* "a retry must reuse the same key. That's an idempotency key; more in lesson eight."
- **"What the run cost" was never exemplified.** *Fixed:* cut; the record card now reads "what happened, step by step".
- **Nobody put last night right.** *Fixed:* 07a opens "First, put last night right, with a person approving, as in lesson five."
- **Order of the checks did not follow the rows.** *Fixed:* the checks now run twice / wrong amount / never attempted, the order the sweep
  meets them.
- **Rule omitted what to do on failure.** *Fixed:* the rule card adds "When a check fails, stop and tell a person."
- **"Run on the real data" should be read-only.** *Fixed* in the exercise: "three read-only checks".
- **Observability reduced to "what happened?"; the record is really a trace.** *Not changed* for time. The record is described as "a
  line" per step, which is accurate, and the lens scene names logs, metrics and traces.
- **Outro sub lacks "Next: ...".** *Not changed:* the brief fixes the close sub as "Software Engineering 201"; the bridge is spoken.
- **03a still is half empty** (second card is a ghost). *Not changed:* that is the recorded `two_kinds` layout; the card lands in 03b.
- **Runtime.** After the fixes: 690 words, an estimated 265 s.

## Layout fixes found in my own pass over the stills
- The first version of 06 used the terminal layout and left the lower half of the frame empty; rebuilt as a chain of record steps (graph
  layout) with the written record line beneath it, timed to the narration.

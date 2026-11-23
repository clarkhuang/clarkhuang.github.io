# Review round 2: SE201 Lesson 6, Quality, Feedback, and Observability

Independent harsh pass over the script as recorded (`scripts/se201-06-quality.json`, 15 scenes, 690 words, rendered video 4:09),
the stills of every scene, the speech-to-text of every clip, lessons 1, 5 and 8, and the brief's facts.
Verdict: **PASS. No major findings. Nothing changed after the render.**

## What was checked for a major problem, and the result
| Check | Result |
|---|---|
| Anything wrong | None found. Arithmetic rechecked: prices 29 + 99 + 29 + 49 + 99 + 49 = 354; charges 29 + 99 + (2 x 29) + 49 + 119 + 0 = 354. The three errors (+29, +20, -49) cancel, so "the totals match" is true. Each of the three checks fails on exactly one renewal, as shown. |
| A claim beyond the facts | None. No claim about Clark or any company. The system is called made-up aloud in 02 and 04a and on screen in 04 and 06. The S.L.O. figure is given as "say" and "for example". |
| Rule consistent with its examples | Yes. Write right as checks (04b), run before shipping and after every run (05), leave a record at every step (06), stop and tell a person (07a opens with a person putting the night right), feed every miss back (07a). |
| On-screen text against narration | No contradiction. 04a no longer says the table looks fine; it says no test looked at it. |
| Technical accuracy | A timeout followed by a retry with a new key producing a second charge, found by reconciling against the processor's report, is a real failure mode; "a retry must reuse the same key" is the correct fix and "idempotency key" the correct name. Logs, metrics and traces, and "service level objective", are used in their usual senses. |
| Consistency with lessons 1, 5 and 8 | The lens and "seeing the whole" ten years ago match lesson 1's 2016 card. "As in lesson five" matches lesson 5's refund stop. Lesson 8 does cover the idempotency key. |
| Speech-to-text | Every clip matches the script. |
| Stills | No overflow, overlap, clipping or empty frame. |

## Minor findings: NOT applied (not worth a re-record)
| Finding | Why it is minor |
|---|---|
| 04: the CHARGED column shows $29.00 for R-1043 with TIMES 2, so adding the column by eye gives $325, not the $354 total. | The column is the amount per charge and TIMES is the count; the total is amount times count. Showing $58.00 would make check 2 fail twice and break "one failed" per check. |
| 04a: an alert viewer can already spot the 2, the $119.00 and the 0 while the narration asks "was last night right?". | The narration's claim is only that the green build cannot say, which is true. Spotting it early helps the point. |
| 04: the real table would have to be built from the processor's report, since the system's own record thought R-1043 was charged once. | 06 says exactly that (reconcile against the processor's own report). Not said in 04, but not contradicted. |
| 05: a 99.9% target sits next to a check that says "every renewal due was attempted". | One is a deadline target, the other a correctness check; both are labelled. |
| 06: observability is reduced to a per-step record; a practitioner would call it a trace. | Accurate as far as it goes; 03a names logs, metrics and traces. |
| 03a: the second card is a ghost until 03b. | Recorded layout; unchanged. |
| 11: the outro card has no "Next:" line. | The brief fixes the close sub; the bridge is spoken. |
| Generator docstring said the charges add to $324 (stale since round 1). | Comment only. Corrected in `make_se201_06_quality.py`; the generated JSON is byte-identical (checksum verified), so nothing to re-narrate or re-render. |

## What changed between round 1 and round 2
Nothing in the script or on screen. Round 1 made every substantive change (see `se201-06-review-round1.md`): the errors now cancel so
the totals truly match, "attempted" replaced "charged" in check 3, the record now shows why the double charge happened, the S.L.O.
became a percentage given as an example, and the first scene of the example no longer contradicts its own table.

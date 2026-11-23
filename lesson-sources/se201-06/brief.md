# Brief: SE201 Lesson 6, Quality, Feedback, and Observability

**Audience:** public site (clarkhuang.github.io): engineers and builders who have taken Software Engineering 101 and the first five 201 lessons, or who arrive at this lesson cold.

**Owner direction (Clark):** "create 5-8 (leave 9 alone), keep making them better than previous set." Each new lesson has to beat lessons 1 to 4: a sharper hook in the first ten seconds, a concrete worked example, diagrams instead of statements, clear chapters, a short recap, a clear rule card, a "try it with your AI" exercise, and a bridge to the next lesson.

**Job of this lesson:** lesson 5 let everything outside the gates "ship on its checks", and closed by asking how good those checks really are. This lesson answers. A green build says the code did what its tests asked; it does not say last night's run was right. So: define "right" before the work starts, in the business's words, as checks an agent can run; run the same checks before a change ships and after every run on the real data; make every step leave a record that people and agents can both read; and feed every miss back into the brief and the checks. It ends with rule 6 for agents, a "your turn" exercise to run with an AI, and a bridge to lesson 7 (a job with a brief, checks and a record is ready to become a skill).

**Worked example:** "our made-up example: the subscription-billing system from lesson one", the morning after a nightly renewal run. Six invented renewals; the build is green; the real check is "every renewal charged the right amount, exactly once", split into three checks. Run on the table, they find one renewal charged twice, one charged the wrong amount and one never charged, while the totals are only $30 apart. The record for the double charge shows a timeout followed by a retry. The fix goes back into the brief ("a retry must reuse the same request key"), which also sets up lesson 8's idempotency.

**Constraints**
- About Clark: nothing beyond the public career record; this lesson adds no claim about him or any company. The billing system, every renewal, price, time and record line are invented and called made-up aloud and on screen.
- The lens (what is scarce shapes what you build) is lesson 1's teaching lens, recalled as "the lens from lesson one".
- Terms kept standard and correct: logs, metrics, traces; service level objective (S.L.O.). No statistics.
- Be honest about the limit: a check only catches what somebody thought to ask, so a person still samples real output.
- Speech tags: only [pause], <emphasis>, <slow>. No laugh or chuckle tags.
- Runtime 3.5 to 4.5 minutes at about 2.6 words a second.

**Layouts:** one new one in `se201_layouts_58a.py` (`renewals`), plus the existing `quiz`, `two_kinds`, `graph`, `rule`, `rule_card`, `statement`, `outro`.

**Deliverables:** `make_se201_06_quality.py`, `scripts/se201-06-quality.json`, preview stills in `stills-06/`, two review rounds, `se201-06-facts.md`, `se201-06-page.md`, `se201-06-claims-toned-down.md`.

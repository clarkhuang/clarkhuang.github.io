# Brief: SE201 Lesson 5, Governance: Where People Decide

**Audience:** public site (clarkhuang.github.io): engineers and builders who have taken Software Engineering 101 and the first four 201 lessons, or who arrive at this lesson cold.

**Owner direction (Clark):** "create 5-8 (leave 9 alone), keep making them better than previous set." Each new lesson has to beat lessons 1 to 4: a sharper hook in the first ten seconds, a concrete worked example, diagrams instead of statements, clear chapters, a short recap, a clear rule card, a "try it with your AI" exercise, and a bridge to the next lesson.

**Job of this lesson:** lesson 4 ended at the merge point, where "someone still has to say yes". This lesson answers who, and to what. Agents now write changes faster than anyone can read them all, so the place where a person decides has to be designed, not inherited. It gives one rule of thumb (four questions: money, customer data, hard to undo, judgment call), shows it sorting five pieces of work in the made-up billing system, shows how to make a stop quick (the agent prepares the decision), says to write "who approves what" down and have the pipeline enforce it, and is honest about the cost of too many and too few stops. It ends with rule 5 for agents, a "your turn" exercise to run with an AI, and a bridge to lesson 6 (how good are your checks?).

**Worked example:** "our made-up example: the subscription-billing system from lesson one". Five things an agent drafts: a typo fix in an email template, a missing test for renewals, a change to how a late fee is calculated, a ledger migration, and a refund over the limit. The roles (finance owner, ledger owner, support lead) are invented for the illustration.

**Constraints**
- About Clark: nothing beyond the public career record; this lesson adds no claim about him or any company. The billing system is called made-up aloud and on screen.
- The four questions, the decision request and "start strict, release by kind" are teaching ideas written by the scriptwriter. They are presented as a rule of thumb, not as Clark's long-held belief or as industry fact.
- History stays approximate and hedged: "typically" a change board thirty years ago; "more and more" code review twenty years ago; an approval step in an automated pipeline ten years ago.
- No statistics. "Forty changes" in the quiz is a hypothetical, stated as one.
- Speech tags: only [pause], <emphasis>, <slow>. No laugh or chuckle tags.
- Runtime 3.5 to 4.5 minutes at about 2.6 words a second.

**Layouts:** two new ones in `se201_layouts_58a.py` (`gates`, `decision_card`), plus the existing `quiz`, `eras`, `perm_table`, `dial`, `rule`, `rule_card`, `statement`, `outro`.

**Deliverables:** `make_se201_05_governance.py`, `scripts/se201-05-governance.json`, preview stills in `stills-05/`, two review rounds, `se201-05-facts.md`, `se201-05-page.md`, `se201-05-claims-toned-down.md`.

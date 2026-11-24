# Brief: SE201 Lesson 9, "Agents That Operate Enterprise Systems"

Slug `09-agents-that-operate-enterprise-systems` (existing URL) · spec id `se201-09-operate` · generator `make_se201_09_operate.py` ·
layouts `accessmap`, `trail`, `access_review` in `se201_layouts_09.py` · output `09-agents-that-operate-enterprise-systems/SE201_09_Agents-That-Operate-Enterprise-Systems_public.mp4`

## What the owner asked for
Finish the series. Lesson 9 was an outline, skipped when lesson 10 was recorded; build it as a full narrated lesson, at least as
good as lessons 5 to 8 and the lesson 10 capstone.

## Audience
Engineers and technical leaders who have agents building software and are about to let one run part of a live system.

## The one idea
An agent that operates a system is an actor in it, so give it what every actor in an enterprise system gets: a name of its own, a written
job, the least access that job needs, a record of everything it does, a person where the decision is a person's, and a way to stop it.
Enforce all of that in the system, not in the prompt.

## Where it sits
Lesson 8 closes on three questions: whose name does it run under, what is it allowed to touch, who can see what it did. Lesson 9 answers
them in that order, adds lesson 5's fourth (where does a person decide), and names the whole thing with lesson 10's phrase: who operates
this system? Lesson 10 (already recorded) shows the same operator, `billing-ops-agent`, in one scene; lesson 9 is the full treatment and
uses a different night (a charge missing from the ledger) so the capstone's double charge is not used up.

## Worked example
The series' made-up subscription-billing system, and the agent that works lesson 8's nightly reconcile. One made-up night: the processor's
report has 989 charges, the ledger 988. The agent reads both and finds a $30 renewal that the processor charged, where our side timed out,
the retries ran out, and nothing reached the ledger. It can't add the entry and can't refund; it opens a case for the ledger's owner with
what it found, the evidence and a proposed fix. In the morning the ledger's owner approves and the fix goes in as a new entry under the
owner's name. Every step is a line in the log, which answers the opening question: who did it?

## The near miss (made up, labelled, nothing went wrong)
At setup the agent's access was copied from a support role, so it could issue refunds and never said so. Its owner's access review asks of
every permission "needed? used?" and removes it. Why it matters: agents read text they didn't write, and text can be written to steer them.

## Shape (15 scenes, 705 spoken words, estimate 4:31 at 2.6 words a second)
Title · The question (quiz) · Four questions · Whose name? · What may it touch? (two beats) · One night (three beats, the last answering
"who can see?") · A near miss · Limits, and a stop switch · Recap · The rule · Your turn · Close, bridging to lesson 10.

## Diagrams (three new layouts, all animated)
- `accessmap`: the agent's card (identity, job, owner) on the left; one row per action; the system each would touch on the right; and one
  vertical line between them, "enforced by the system, not by the prompt". Allowed actions cross the line; denied ones stop at it. Held
  across scenes 04 to 06 and brought back for the limits in 09. In scene 04 the right side contrasts a shared login with its own identity.
- `trail`: one night. Two counts that should match, the one that differs, what the agent does and can't do, and the log filling in line by
  line (when, who, what, why, result); at the end the WHO column lights.
- `access_review`: one row per permission, two questions, one removed; then a line of text the agent didn't write, with and without the
  spare permission.

## Voice and limits
An engaging professor; plain words; no jokes. The example is called made up aloud at first use and on screen throughout. No claim about
Clark or any company, no real incidents, no product or processor names, no other people's names. Security claims are
kept to what holds in general and hedged where needed; the finer points are in the page notes. Speech tags: only [pause] and <emphasis>.
No text-to-speech was called; stills are silent previews.

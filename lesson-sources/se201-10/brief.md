# Brief: SE201 Lesson 10, "Capstone: One Feature, End to End"

Slug `10-capstone-one-feature-end-to-end` · spec id `se201-10-capstone` · generator `make_se201_10_capstone.py` ·
layout `buildmap` in `se201_layouts_10.py` · output `10-capstone-one-feature-end-to-end/SE201_10_Capstone-One-Feature-End-To-End_public.mp4`

## What the owner asked for
A tenth lesson: a capstone that builds ONE small system end to end and ties lessons 1 to 9 together, on the same made-up
subscription-billing system, at least as good as lessons 5 to 8. Not a list-y recap: show the system being built.

## The one idea
Everything in the series is one plan, written before any agent builds: what right means, where it is written down, the graph and
the shared contract, who decides, what is already a skill, what runs on its own, and under whose identity. Then the build, the
run and the operation are that plan being carried out.

## The feature, and why this one
"Switch to annual, mid-month": a customer on a $30 monthly plan clicks "switch to annual" ($300 a year) ten days into a 30-day
month. Chosen over "pause a subscription" because it exercises all ten ideas with nothing forced:

| Lesson | What the feature gives it |
|---|---|
| 1 What's scarce | The charge has no right answer until a person sets a rule ($300 or $280), so "knowing it's right" is the whole problem. |
| 2 Readable | The rule becomes a spec in the repo, with an agents file and an index. |
| 3 Graph | Four parts; one new thing crosses (the quote), three parts share it, so it is its own node with one owner. |
| 4 Parallel | The quote's format is the shared contract; three agents; one merge point on staging. |
| 5 Who decides | It moves money, so the finance owner, named in the repo, decides; the agent brings the decision, it does not approve it. |
| 6 Checks | "Charged the right amount, exactly once" becomes three checks, run before it ships and every night after. |
| 7 Skill | Adding the annual plan is exactly lesson 7's skill ("add a plan or a price"), so one part needs no new brief. |
| 8 Pipeline | An event trigger (the customer confirms), steps that each leave a record, an idempotency key (the quote's ID), and a second, nightly trigger for reconcile. |
| 9 Operator | An agent works the nightly reconcile under its own identity, read-only, logged; it flags, a person refunds. |
| Constants | Data model (the plan, the quote), money adds up (invoice = ledger = processor), the processor, someone who can do the sum by hand. |

Pausing a subscription moves no money on the day, has no arithmetic to get wrong, and gives lesson 7 nothing to reuse.

## Shape (18 scenes, 852 spoken words, estimate 5:28 at 2.6 words/second)
Question (quiz) · One small feature (the empty map) · Plan it (lessons 1 to 7, seven beats) · Build it (the plan runs) ·
Run it (lesson 8) · Operate it (lesson 9's question, and the one thing that goes wrong) · What still holds (four constants) ·
Recap (the map lights up again in order) · The rule · Your turn · Close.

## The through-line diagram
One "build map", held on screen from scene 3 to scene 15. Every element carries the number of the lesson it comes from and starts
as a dashed outline. Top: what right means (1, then 6). Middle row: the files (2), the graph with the shared node (3), agents and
the merge point (4), the person who decides (5), checks before (6), the skill (7). Lower half: what was written down for the
current step, then a log of the build as the map turns green, then production: a pipeline with two triggers (8) and the operator
(9). Last, four cards for the constants. In the recap the numbers light again in order.

## Voice and limits
Same as lessons 5 to 8: only `[pause]`, `<emphasis>`, `<slow>`; "A.I.", "I.D.", "two oh one". The example is called made up aloud
in the first sentence and again at its first use as "our made-up subscription-billing system"; every map frame is labelled "A
MADE-UP EXAMPLE, MADE-UP NUMBERS". No claims about the presenter or any company. Lesson 9 is an outline, so it is "lesson nine's
question", never something the viewer watched. The close wraps the series and promises nothing further.

# Review round 1: SE201 Lesson 1, Four Eras of Building Systems

Reviewer: an independent agent that did not write the script. It read the first draft (`tools/make_se201_01_four_eras.round1.py`,
extracted to `review-input-round1.txt`), the three recorded 201 lessons, and the facts file.
Verdict: **CHANGES NEEDED**. Below is each finding, followed by my disposition. I also checked the history myself.

## MAJOR
1. **Numbering clashes with the recorded lessons.** The reviewer saw the old JSONs, where "Build the whole system" is
   still lesson one with rule one, and its path list leaves out the eras. *Disposition: handled by deliverable 4.* The
   renumbered scripts make that lesson lesson two with rule two, and its path list now shows "Four eras" as row 1, on screen only.
2. **Too long.** The draft had 754 words, about 4:50, above the 4.5-minute ceiling. *Fixed:* now 686 words, an estimated 264 s
   (4.4 min). Cuts: a shorter quiz reveal, a shorter lens, shorter era scenes, a shorter design scene, the caveat cut to two
   sentences, a shorter path (lesson 2 walks the same path again), a shorter ask and a shorter close. The recap stays, at
   27 words, because every recorded lesson has one.

## MINOR
- **04_lens.** "One lens I find useful" still reads as Clark's own view. *Fixed:* "Here's a useful way to see why."
- **10_caveat.** "Even some of the people arguing for it" goes beyond the facts. *Fixed:* "At least one source arguing for it
  calls it a stance built on indirect evidence."
- **08_now.** "And context" is spoken but not shown on screen. *Fixed:* the Now card gets the caption "Also scarce: context. How much
  of the system an agent can see at once." The recap also says "and context".
- **05-08.** Does the eras grid build up era by era? *Confirmed in the stills:* the later cards are ghosted until their own beat.
- **05_1996.** EDI and batch processing still run today. *Fixed:* "...through E.D.I., and much of that still runs." I also changed
  "the web was brand new" to "the commercial web was brand new", because the web itself dates from about 1991.
- **07_2016.** "Each with its own team" is naive. *Fixed:* "owned by small teams". I also added "by default, for new systems",
  because enterprises were not cloud-by-default in 2016.
- **11_constants.** "A cloud" is not a dependency in 1996. *Fixed:* "a bank, a card network, a partner's system".
- **03_career.** The grid implied a chronology that the facts don't give. *Fixed:* the companies are now grouped by kind, in
  bands labelled MONEY and COMMERCE, so the order reads as a category, not a timeline.
- **02_quiz.** The hook was abstract. *Fixed:* "An agent can now write a working piece of a billing system in an afternoon."
- **15_ask.** The screen left out the "ask your AI" step, and "Still?" was cryptic. *Fixed:* the headline is now "Your turn. Your oldest
  system: when was it built? What was scarce? Then ask your AI which era it's from."
- **Rule walk-through.** The reviewer found the rule consistent with the billing example. "The layer below" is not in the rule,
  and that is acceptable: the rule covers the design note, and the layer below is a people constant. *No change.*

## Clean according to the reviewer
No company outside the public career record is named, and no anecdotes, numbers or internal details are invented. The billing picture is labelled
an illustration. The era dates check out. The tone is professorial and not salesy. Speech tags and TTS spellings are correct. Visual
variety matches the recorded lessons. The lesson leads cleanly into lesson 2.

## My own history check (against the stated anchors)
- 1996: company-owned servers, monoliths on one RDBMS, few releases a year, batch/EDI. Accurate as a simplification.
- 2006: three tiers, rented racks, AWS S3 (March 2006) and EC2 (August 2006) "had just launched", Agile (Manifesto 2001) with sprints
  of a few weeks, SOAP/XML web services. Accurate.
- 2016: Docker (2013) and Kubernetes (2014, 1.0 in 2015) mainstream, "microservices" (term popular around 2014), continuous delivery,
  "many times a day at the best teams", API-first SaaS, and distributed tracing and dashboards. Accurate.
- Now: agent-era design advice (monorepos, modular boundaries, fast tests, machine-readable rules) is framed as where thinking is
  heading, matching the facts file.

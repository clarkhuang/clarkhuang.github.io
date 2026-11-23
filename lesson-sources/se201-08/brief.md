# Brief for Software Engineering 201, Lesson 8

Series: Software Engineering 201: From Loop to Enterprise Systems. Lessons 1 to 4 are recorded. Lesson 7 turned recurring jobs into skills. Lesson 8 is "Routines, Pipelines, and Integration". Lesson 9, "Agents That Operate Enterprise Systems", stays an outline; lesson 8 bridges to it.

Write a public, generic lesson of about four minutes in the house style of lessons 1 to 4, and make it better than them: a short title card, a hook in the first ten seconds, one worked example carried through the lesson as one animated diagram, clear chapters, a short recap, rule 8 "for your agents", a "try it with your AI" exercise, and a bridge to lesson 9 ("See you in lesson nine").

Cover (from the outline page):
- Integration is the oldest problem in the series: overnight batch files and EDI, then web services, then an API for everything, now agents calling tools. All of them still run somewhere.
- Some work should start on its own: on a schedule, when something happens, or when the last step finishes. A skill plus a trigger is a routine; routines chained are a pipeline.
- Connect the steps through clear interfaces, and make every step leave a record you can check and replay.
- You depend on systems you don't control, so design every hand-off to fail safely and be retried.

Worked example: the series' made-up subscription-billing system (introduced in lesson 1, always called made up aloud and on screen; its numbers are labelled made up). The nightly billing run: find renewals due, charge, invoice, accounting export, reconcile. Show what crosses at each hand-off, the record each step leaves and how the counts add up, a charge step that fails partway and is retried safely with an idempotency key, and reconciliation that stops and tells a person. Then a partner's nightly file that can arrive late, twice or broken.

Threads to other lessons: money has to add up and you depend on things you don't control (lesson 1); a written format at every hand-off is the contract (lesson 4); stop and tell a person (lesson 5); "the right amount, exactly once" (lesson 6); skills (lesson 7); who the pipeline is and what it may touch (lesson 9).

Honesty points for experienced engineers: exactly-once is hard to guarantee between systems, so expect at least once and make twice harmless; most pipeline steps are plain code, and an agent belongs where a step needs judgment.

Visuals: favour diagrams over statements, vary the layouts, on-screen text matches the narration. New layout only in `se201_layouts_58b.py`: `pipeline` (trigger, stages, hand-offs, records, an alert, and a look inside one stage as it fails and is retried).

Constraints: first person in Clark's voice; only the public career facts; no invented anecdotes, incidents, numbers or internal details of any company; no other people's names; no family or private information; no statistics without a source; teaching ideas framed as ideas and rules of thumb; speech tags limited to `[pause]`, `<emphasis>`, `<slow>`; no laugh or chuckle tags; spelled for text-to-speech like lesson 1; 3.5 to 4.5 minutes; voice `4lbl0krw73vf`, language `en`, speed 1.05. Tone: an engaging professor, never jokey, never condescending.

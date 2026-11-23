# Brief for Software Engineering 201, Lesson 7

Series: Software Engineering 201: From Loop to Enterprise Systems. Lessons 1 to 4 are recorded. Lesson 5 is governance, lesson 6 is quality, feedback and observability. Lesson 7 is "Skills as Building Blocks". Lesson 8 follows with routines, pipelines and integration.

Write a public, generic lesson of about four minutes in the house style of lessons 1 to 4, and make it better than them: a short title card, a hook in the first ten seconds, one worked example carried through the lesson as diagrams, clear chapters, a short recap, rule 7 "for your agents", a "try it with your AI" exercise, and a bridge to lesson 8.

Cover (from the outline page):
- Turn the jobs that keep coming back into written, tested, shared skills.
- Software has had several units of reuse: shared libraries, then frameworks, then services behind an API. A skill is another one: the written way a recurring job gets done.
- What a skill contains: when to use it, the inputs, the steps, the checks, the traps, the output.
- Write it once, test it, version it; any person or agent then runs the job the same way, and it is improved in one place.

Worked example: the series' made-up subscription-billing system (introduced in lesson 1, always called made up aloud and on screen). The recurring job is adding a new plan or price. The hook shows it done three times with three results; the middle writes the skill for it section by section; the end reruns the three jobs from the skill.

Threads to other lessons: a price change is approved by a person (lesson 5); the check is "the right amount, exactly once" (lesson 6); one skill does one job, and lesson 8 chains them.

Honesty points for experienced engineers: a skill is a runbook, and what changed is the reader; a step that needs no judgment should be a script the skill calls; "the third time" is a rule of thumb, not a law.

Visuals: favour diagrams over statements, vary the layouts, on-screen text matches the narration. New layouts only in `se201_layouts_58b.py`: `drift` (one job, several runs) and `skill_card` (a skill as a page that fills in).

Constraints: first person in Clark's voice; only the public career facts; no invented anecdotes, incidents, numbers or internal details of any company; no other people's names; no family or private information; no statistics without a source; teaching ideas framed as ideas and rules of thumb; speech tags limited to `[pause]`, `<emphasis>`, `<slow>`; no laugh or chuckle tags; spelled for text-to-speech like lesson 1; 3.5 to 4.5 minutes; voice `4lbl0krw73vf`, language `en`, speed 1.05. Tone: an engaging professor, never jokey, never condescending.

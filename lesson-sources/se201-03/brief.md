# Brief for Software Engineering 201, Lesson 2

Series: Software Engineering 201: From Loop to Enterprise Systems. Lesson 1 (recorded) covered building a whole system AI-native. Lesson 2 is "Decompose the System into a Graph". Lesson 3 follows with parallel agents and integration.

Write a public, generic lesson of about four minutes in the house style of Lesson 1, and make it better than Lesson 1: a short title card, a hook in the first ten seconds, one worked example shown as a diagram, clear chapters, a short recap, rule 2 "for your agents", a reply ask, and a bridge to Lesson 3.

Cover (from the outline page and the earlier "From Loop to Graph" recording, ideas reused, wording new):
- An enterprise system is too big for one loop. Draw it as a graph.
- Split the system into parts with clear boundaries and owners, then find the real dependencies.
- "And then" is not a dependency. If nothing crosses between two parts, they don't wait for each other.
- Loop versus graph: the graph decides which loops exist and which run at the same time. It does not replace the loop; every part still gets plan, build, verify.
- The dinner graph. Serial versus side-by-side bars, as an illustration.

Worked example: this site as a graph. Four parts sharing a generator and styles; one lesson's build as a dependency chain from script to production. Only claims that are true of the repository and the pipeline, each listed in `se201-02-facts.md`.

Visuals: favor diagrams over statements, vary the layouts, on-screen text matches the narration. New layouts allowed in `se101_layouts6.py`; a graph layout with a highlighted chain and independent branches.

Constraints: first person in Clark's voice; no invented anecdotes; no company-internal systems; no other people's names; no family or private information; no statistics without a source; anything hypothetical says "picture"; speech tags limited to `[pause]`, `<emphasis>`, `<slow>`; no laugh or chuckle tags; spelled for text-to-speech like Lesson 1; 3.5 to 4.5 minutes; speed 1.05. Tone: an engaging professor, never jokey, never condescending.

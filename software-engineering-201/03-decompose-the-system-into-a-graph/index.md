# Decompose the System into a Graph

_Software Engineering 201 · Lesson 3_

HTML page: https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/index.md (plus https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se201-03-decompose-the-system-into-a-graph.mp4
- Duration: 4:06 (246.1 seconds)
- Poster: https://clarkhuang.github.io/videos/posters/se201-03-decompose-the-system-into-a-graph.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se201-03-decompose-the-system-into-a-graph.vtt
- How it was built (script source, facts, prompts): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se201-03

## Chapters

- [0:00] The question
- [0:26] What crosses?
- [0:49] Loop and graph
- [1:08] This site, as a graph
- [1:47] One lesson, as a graph
- [2:30] Why it matters
- [2:44] At enterprise scale
- [3:08] Recap
- [3:26] The rule
- [3:48] Your turn

## The lesson

An enterprise system is too big for one loop, so draw it as a graph. A numbered plan only shows the order someone wrote the steps in; the test for any two steps is what crosses between them, and “and then” is not a dependency. The worked example is this site: four parts that share one generator, and one lesson's build, a strict chain that forks after the render. The graph decides which loops exist and which can run at the same time, and every part still gets its own plan, build, and verify loop. An earlier recording of this material, made when it was lesson 1, is at https://clarkhuang.github.io/videos/se201-01-from-loop-to-graph.mp4.

## The rule

Before any job with more than one part, draw the graph. Name the parts, and give each one a boundary and an owner. Draw an arrow only where something crosses from one part to another; “and then” is not a dependency. Anything two parts share becomes its own node, with one owner. Run the parts with no arrow between them at the same time, and give every part its own plan, build, and verify loop, with its own finish line and its own check.

This rule is written so an AI agent can follow it as a standing instruction.

## Credit

Related reading: the loop-and-graph framing for agent work also appears in “Loops and Graphs” by Hanako (@hanakoxbt, August 2026).

## Transcript

Software engineering 201. Lesson three. Decompose the system into a graph.

### The question

Quick question. An agent hands you a plan. Ten steps, numbered one to ten. How many of those steps truly have to wait for the step before? All ten? About half? Or is it impossible to tell from the list? You can't tell. A numbered list records the order someone wrote things down. It doesn't say what needs what.

### What crosses?

So here's the test. Take any two steps, and ask: what crosses between them? Think about cooking dinner. The sauce waits for the chopped onions. Something crosses, so that's a real dependency. Draw the arrow. The rice and the salad? Nothing crosses. So nobody waits for the rice before starting the salad. And then, is not a dependency.

### Loop and graph

In 101, the unit was the loop. Plan, build, verify, until one piece of work is right. The graph sits one level up. It says which pieces exist, what each one needs, and which can run at the same time. And it doesn't replace the loop. Every node in the graph is still a loop of its own.

### This site, as a graph

Let's decompose a real system: the site you're on. Start with the parts. AI tips. Software engineering 101. 201. And the book. Each part has its own folder, and its own pages. A new lesson in one needs nothing from the others. So work on one never waits on another.

But they aren't floating free. All four are built by one generator, with one stylesheet. That shared piece is a node too, and every part depends on it. So the graph shows you where to be careful. Change one part, and one part moves. Change the shared node, and everything moves. Which is why a shared node needs one clear owner.

### One lesson, as a graph

Now zoom into one node: a single video lesson. Here, the arrows are real. The narration clips need the script. The render needs those clips, because the length of the audio sets the timing. Captions need the timeline the render writes out. And the page needs all of it, before a pull request to staging, where only I merge to production. Every arrow carries something.

Script, narration, render. A strict chain. More agents won't make it shorter: the longest chain sets the minimum. But after the render, it forks. Captions need only the timeline. The sound level and the poster need only the video. Nothing crosses between those two. The build script happens to run them one after the other. The graph shows that's a choice, not a requirement.

### Why it matters

Why does this matter? Waiting. Picture three parts, with nothing crossing between them. Run as a numbered list, each one waits for the last. Run as a graph, they go side by side. Same work. Far less waiting.

### At enterprise scale

Now scale that up. Picture an enterprise system. Orders, billing, shipping, support. Far too big for one loop. It's the same picture. A few real arrows: billing needs the order, shipping needs the payment. A shared node everything leans on, like customer data. And parts that never touch, where teams and agents move without waiting. Miss the shared node, and two of them collide at the end.

### Recap

So, to recap. Drawing the graph is four moves. One. Name the parts, each with a boundary and an owner. Two. For every pair, ask what crosses, and what they share. Three. Draw only those arrows. And four. Give every part its own finish line, and its own check.

### The rule

Which gives us rule three, for your agents. Before any job with more than one part, draw the graph. Name the parts. Draw an arrow only where something crosses from one part to another. Anything two parts share becomes its own node, with one owner. Parts with no arrow between them run at the same time. And every part gets its own loop: plan, build, verify.

### Your turn

Now, your turn. Take the last multi-step plan an agent gave you. At every, and then, ask what crosses. How many arrows survive?

Next time, those parts really do run at once, and we bring the work back together. See you in lesson four.

## Related lessons

- Lesson 1: [Four Eras of Building Systems](https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/index.md) (available)
- Lesson 2: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/index.md) (available)
- Lesson 4: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/04-parallel-agents-one-integration/index.md) (available)
- Lesson 5: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/index.md) (outline)
- Lesson 6: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/06-quality-feedback-and-observability/index.md) (outline)
- Lesson 7: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/07-skills-as-building-blocks/index.md) (outline)
- Lesson 8: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/index.md) (outline)
- Lesson 9: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/index.md) (outline)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

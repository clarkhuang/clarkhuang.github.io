# Decompose the System into a Graph

_Software Engineering 201 · Lesson 2_

HTML page: https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/index.md (plus https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 201](https://clarkhuang.github.io/software-engineering-201/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/AGENTS.md)

This lesson is in planning. The video is not available yet.

## The lesson

An enterprise system is too big for one loop. Draw it as a graph: split the system into parts with clear boundaries and owners, then find the real dependencies. “And then” is not a dependency; if nothing crosses between two parts, they don't need to wait for each other. The graph decides which loops exist and which can run at the same time, and every part still gets its own plan, build, and verify loop. An earlier recording of this material, made when it was lesson 1, is at https://clarkhuang.github.io/videos/se201-01-from-loop-to-graph.mp4.

## Credit

Related reading: the loop-and-graph framing for agent work also appears in “Loops and Graphs” by Hanako (@hanakoxbt, August 2026).

## Related lessons

- Lesson 1: [Build the Whole System, AI-Native](https://clarkhuang.github.io/software-engineering-201/01-build-the-whole-system-ai-native/index.md) (available)
- Lesson 3: [Parallel Agents, One Integration](https://clarkhuang.github.io/software-engineering-201/03-parallel-agents-one-integration/index.md) (outline)
- Lesson 4: [Governance: Where People Decide](https://clarkhuang.github.io/software-engineering-201/04-governance-where-people-decide/index.md) (outline)
- Lesson 5: [Quality, Feedback, and Observability](https://clarkhuang.github.io/software-engineering-201/05-quality-feedback-and-observability/index.md) (outline)
- Lesson 6: [Skills as Building Blocks](https://clarkhuang.github.io/software-engineering-201/06-skills-as-building-blocks/index.md) (outline)
- Lesson 7: [Routines, Pipelines, and Integration](https://clarkhuang.github.io/software-engineering-201/07-routines-pipelines-and-integration/index.md) (outline)
- Lesson 8: [Agents That Operate Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/08-agents-that-operate-enterprise-systems/index.md) (outline)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-201/02-decompose-the-system-into-a-graph/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-201/AGENTS.md](https://clarkhuang.github.io/software-engineering-201/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

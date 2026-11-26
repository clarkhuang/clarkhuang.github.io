# Copy this for yourself

HTML page: https://clarkhuang.github.io/copy-this/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/copy-this/index.md (plus https://clarkhuang.github.io/copy-this/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

This repository is a GitHub template. Use it to create your own OpenBook or short video learning series: enable GitHub Pages from the main branch, replace the bio, lessons and book preview, and keep the AI-friendly files (llms.txt, AGENTS.md, and the copy-paste prompt). Book text is licensed CC BY-NC-SA 4.0. Do not present Clark's stories as your own.

## How the publishing studio will work

GitHub Pages serves this site today. A Mac Studio expected in February 2027 will do the editorial and build work. Readers will still be able to watch a lesson while the Mac is offline. The ordered configuration has an M5 Ultra, a 36-core CPU, an 80-core GPU, a 32-core Neural Engine, 512 GB of unified memory and an 8 TB SSD.

Read the [SE 301 playbook](https://clarkhuang.github.io/software-engineering-301/index.md) for the hardware budgets and labs. The first model trials will pair Qwen3-Coder-Next for everyday changes with GLM-5.3-Flash for difficult plans and second reviews. Both have open weights. Quantized copies reduce the memory needed to load them. A gateway will route each job to a named model and record the exact version. We will choose the production models after measuring accepted changes, response time and memory use on this machine.

For a course correction, a worker will take an approved issue, edit the lesson source, regenerate its HTML and Markdown, run the site checks and open the staging preview. A video change also needs a render, captions, transcript and playback check. The publishing job will record the commit and verify the deployed page. Clark retains editorial control of production.

For the OpenBook, a voice interview will produce a private transcript with timestamps. A drafting job will connect each proposed passage to the interview and flag gaps for a follow-up question. Only excerpts cleared for publication will enter the public repository. The first trial will use Grok Voice from a phone, with Bland as an optional telephone interface.

## For agents

- This page: https://clarkhuang.github.io/copy-this/index.md
- This folder’s agents file: https://clarkhuang.github.io/copy-this/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

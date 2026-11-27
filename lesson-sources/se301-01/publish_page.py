#!/usr/bin/env python3
"""Write the public Lesson 1 page from the scene script and install-prompt.md.

The page has no video element. Media is not rendered until Clark approves the
script and facts.md. Running this does not call the network.

    python3 publish_page.py
"""
from __future__ import annotations

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SLUG = "01-size-the-model-run-the-first-endpoint"
PAGE = f"software-engineering-301/{SLUG}/index.html"
URL = "https://clarkhuang.github.io/software-engineering-301/" + SLUG + "/"
E = html.escape

SUMMARY = (
    "Before you download a local model, size it to the machine you have. "
    "The weight floor is the parameter count times the bits per weight, divided by eight. "
    "That number is weights only. Add the runtime, the operating system, your other programs, and a context cache. "
    "On the playbook's 48 GB laptop, the first fixture is Qwen2.5-Coder-7B-Instruct in a four-bit build. "
    "Larger names for the ordered 512 GB Studio are candidates, not measurements. "
    "Then run one local endpoint on loopback and keep the reply. A chat reply does not, by itself, prove tool calls. "
    "The page includes one copy-paste prompt for a Mac with Apple silicon and for a Windows or Linux PC. "
    "The agent stops for a named yes before an admin install, a firewall change, or a sign-in. "
    "It does not take secrets, and it does not send local files off the machine."
)
RULE = (
    "Before a model is downloaded, write three things where the agent can read them: "
    "the weight floor, the memory you can spare, and the check that says the endpoint answered. "
    "If a step needs admin rights, a firewall change, or a sign-in, stop and ask. "
    "Do not paste secrets, and do not send local files off the machine."
)
NOTES = [
    "The video is not rendered. The script and facts.md are waiting for Clark's review. Do not treat this page as a recording.",
    "The 40 GB, 160 GB, and 240 GB figures are weight floors from the playbook's formula. They are not measured file sizes.",
    "Qwen3-Coder-Next, GLM-5.3-Flash, DeepSeek-V4-Flash, and Qwen3-Coder-480B are the playbook's November candidates for the ordered Studio. Throughput, power, and usable context are not measured yet.",
    "The playbook's named machines are Apple silicon. The Windows and Linux path in the prompt applies the same weight floor, using LM Studio's headless docs or Ollama's local OpenAI-compatible API.",
    "The prompt's first request is one chat completion. The playbook's endpoint lab still asks for a stream, a cancelled request, and a structured tool call after that. A chat reply does not prove tool calls.",
    "gpt-oss-20b is a comparison only when it is already installed. The prompt does not download it.",
]


def transcript(spec, readable):
    blocks = []
    current = None
    buf = []

    def flush():
        if buf:
            blocks.append((current, " ".join(buf)))
            buf.clear()

    for scene in spec["scenes"]:
        chapter = scene.get("chapter") or ""
        if chapter != current:
            flush()
            current = chapter
        buf.append(readable(scene["text"]))
    flush()
    return blocks


def main():
    os.environ["SITE"] = ROOT
    sys.path.insert(0, os.path.join(ROOT, "sitegen"))
    sys.path.insert(0, HERE)
    import gen
    import make_vtt

    spec = json.load(open(os.path.join(HERE, "se301-01-first-endpoint.json"), encoding="utf-8"))
    prompt = open(os.path.join(HERE, "install-prompt.md"), encoding="utf-8").read().strip() + "\n"
    blocks = transcript(spec, make_vtt.readable)

    md = [
        "# Size the model, then run the first endpoint",
        "",
        "_Software Engineering 301 · Lesson 1 · draft, video not rendered_",
        "",
        f"HTML page: {URL}",
        "",
        "The HTML version of this page has a “Use this page with your AI” box at the top. "
        "Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:",
        "",
        f"> Read https://clarkhuang.github.io/llms.txt and {URL}index.md "
        f"(plus {URL}AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: "
        "list related lessons, answer my questions citing page URLs, and quiz me if I ask.",
        "",
        "- Series: [Software Engineering 301](https://clarkhuang.github.io/software-engineering-301/index.md)",
        "- Series agents file: [https://clarkhuang.github.io/software-engineering-301/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/AGENTS.md)",
        "- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)",
        f"- This folder’s agents file: [{URL}AGENTS.md]({URL}AGENTS.md)",
        "- Video: not rendered. Narration waits on approval of the script and facts file.",
        "- How it was built (script source, facts, install prompt): "
        "https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se301-01",
        "",
        "## Planned chapters",
        "",
        "These are the chapter titles in the scene script. There is no video to seek yet.",
        "",
    ]
    for title, _text in blocks:
        if title:
            md.append(f"- {title}")
    md += [
        "",
        "## The lesson",
        "",
        SUMMARY,
        "",
        "## The rule",
        "",
        RULE,
        "",
        "This rule is written so an AI agent can follow it as a standing instruction.",
        "",
        "## What this draft does not claim",
        "",
    ]
    for note in NOTES:
        md.append(f"- {note}")
    md += ["", "## On-screen summary of the install prompt", ""]
    md.append("The prompt, pasted into a computer-use or terminal agent, does five things:")
    md.append("")
    steps_scene = next(s for s in spec["scenes"] if s["visual"] == "steps")
    for step in steps_scene["data"]["steps"]:
        md.append(f"{step[0]}. **{step[1]}.** {step[2]}")
    md += [
        "",
        "It waits for a named yes before an admin install, a firewall change, or a sign-in. "
        "Silence is not a yes. It does not take secrets, and it does not send local files off the machine.",
        "",
        "## Copy-paste install prompt",
        "",
        "The same text is in `lesson-sources/se301-01/install-prompt.md`. Paste it as a whole.",
        "",
        prompt.rstrip(),
        "",
        "## Transcript",
        "",
        "This is the script, with text-to-speech spellings made readable. It has not been narrated.",
        "",
    ]
    for title, text in blocks:
        if title:
            md += [f"### {title}", ""]
        md += [text, ""]
    md += [
        "## Related",
        "",
        "- Playbook: [Software Engineering 301](https://clarkhuang.github.io/software-engineering-301/index.md)",
        "- Sizing lab on that page: [Size the model before downloading it](https://clarkhuang.github.io/software-engineering-301/index.md#1-size-the-model-before-downloading-it)",
        "- Endpoint lab: [Build the first endpoint](https://clarkhuang.github.io/software-engineering-301/index.md#2-build-the-first-endpoint)",
        "- Next lab in the playbook: [Put a router in front of the models](https://clarkhuang.github.io/software-engineering-301/index.md#3-put-a-router-in-front-of-the-models)",
        "- [Don't Paste Secrets](https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/index.md)",
        "",
        "## For agents",
        "",
        f"Read [AGENTS.md]({URL}AGENTS.md) in this folder, "
        "[https://clarkhuang.github.io/software-engineering-301/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/AGENTS.md) "
        "for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.",
        "",
    ]
    page_dir = os.path.join(ROOT, "software-engineering-301", SLUG)
    os.makedirs(page_dir, exist_ok=True)
    open(os.path.join(page_dir, "index.md"), "w", encoding="utf-8").write("\n".join(md))

    agents = f"""# AGENTS.md — Software Engineering 301, lesson 1: Size the model, then run the first endpoint

This folder is the public draft of “Size the model, then run the first endpoint” on Clark Huang’s learning site. The video is not rendered.

- HTML: {URL}
- Markdown twin (summary, rule, transcript, install prompt): {URL}index.md
- This file: {URL}AGENTS.md
- Series index: https://clarkhuang.github.io/software-engineering-301/index.md
- Series agents: https://clarkhuang.github.io/software-engineering-301/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md
- Build source, facts, and the canonical prompt file: https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se301-01

Read `index.md` in this folder for the lesson. Treat the rule below as a standing instruction. Do not invent stories, quotes, numbers, or biography about Clark Huang. Do not present the Studio model names as measured results. Cite page URLs when you answer questions.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and {URL}index.md (plus {URL}AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

## The rule

{RULE}

## Copy-paste install prompt

Paste this into a computer-use or terminal agent on the machine where the model should run. Do not weaken the stops.

{prompt}"""
    open(os.path.join(page_dir, "AGENTS.md"), "w", encoding="utf-8").write(agents)

    steps = "".join(
        f"<li><strong>{E(title)}.</strong> {E(sub)}</li>"
        for _n, title, sub in steps_scene["data"]["steps"]
    )
    chapters = "".join(f"<li>{E(title)}</li>" for title, _text in blocks if title)
    notes = "".join(f"<li>{E(note)}</li>" for note in NOTES)
    trans = []
    for title, text in blocks:
        if title:
            trans.append(f"          <h3>{E(title)}</h3>")
        trans.append(f"          <p>{E(text)}</p>")
    transcript_html = "\n".join(trans)
    prompt_html = E(prompt.rstrip())
    body = f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/software-engineering-301/">Software Engineering 301</a> / Lesson 1</p>
      <h1>Size the model, then run the first endpoint <span class="badge soon">Draft</span></h1>
      <div class="placeholder"><div><strong>Video not rendered</strong>The script and the facts file are ready for review. Narration runs after that review. This page is the lesson a reader can follow without the video.</div></div>
      <div class="grid2" style="margin-top:34px">
        <section>
          <h2 class="label">The lesson</h2>
          <p>{E(SUMMARY)}</p>
          <div class="rulecard" data-status-scope><p class="label">The rule · for your agents</p><p id="rule-se301-01">{E(RULE)}</p><p class="tools"><button type="button" class="btn ghost" data-copy="rule-se301-01" hidden>Copy rule</button><span class="status" role="status" data-status></span></p></div>
          <h2>What this draft does not claim</h2>
          <ul>{notes}</ul>
        </section>
        <aside>
          <h2 class="label">Planned chapters</h2>
          <ol class="chapters">{chapters}</ol>
          <p class="chapter-hint">No video to seek yet. The titles are the scene script's chapters.</p>
          <p><a href="/software-engineering-301/">Back to the playbook</a></p>
          <p><a href="https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se301-01">How it was built</a></p>
        </aside>
      </div>
      <h2 id="install-prompt">Copy-paste install prompt</h2>
      <p>For a computer-use agent or a terminal agent, on a Mac with Apple silicon or on a Windows or Linux PC. On screen, and here, the prompt does five things:</p>
      <ol>{steps}</ol>
      <p>It waits for a named yes before an admin install, a firewall change, or a sign-in. Silence is not a yes. It does not take secrets, and it does not send local files off the machine.</p>
      <div class="prompt-box" data-status-scope>
        <pre id="install-prompt-text" tabindex="0">{prompt_html}</pre>
        <p class="tools"><button type="button" class="btn ghost" data-copy="install-prompt-text" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p>
      </div>
      <h2>Related</h2>
      <ul>
        <li><a href="/software-engineering-301/">Software Engineering 301 playbook</a></li>
        <li><a href="/software-engineering-301/#1-size-the-model-before-downloading-it">Size the model before downloading it</a></li>
        <li><a href="/software-engineering-301/#2-build-the-first-endpoint">Build the first endpoint</a></li>
        <li><a href="/software-engineering-301/#3-put-a-router-in-front-of-the-models">Put a router in front of the models</a></li>
        <li><a href="/ai-tips/17-dont-paste-secrets/">Don't Paste Secrets</a></li>
      </ul>
      <h2>Transcript</h2>
      <p class="muted">The script, with text-to-speech spellings made readable. It has not been narrated.</p>
{transcript_html}
"""
    desc = SUMMARY[:155]
    gen.page(
        PAGE,
        "Size the model, then run the first endpoint — Software Engineering 301 — Clark Huang",
        desc,
        body,
        "software-engineering-301",
        main_class="lesson",
    )
    print("wrote", PAGE)


if __name__ == "__main__":
    main()

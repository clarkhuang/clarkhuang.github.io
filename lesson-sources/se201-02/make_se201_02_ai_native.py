#!/usr/bin/env python3
"""Generates scripts/se201-02-ai-native.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 2: Build the Whole System AI-Native.
(Renumbered from lesson 1 when "Four Eras of Building Systems" became lesson 1; only lesson numbers changed.)

Public lesson (clarkhuang.github.io). Worked example = the site itself; every claim about it is checkable in the repo
(next-revision -> /staging/, only the owner merges to main, index.md twins, AGENTS.md per folder, llms.txt,
lessons.json, read-only GitMCP endpoint, pages generated from sitegen/content.json, REBUILD.md).
No company-internal systems, no invented anecdotes, no other people's names.

Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-02-ai-native.json
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. From loop, to enterprise systems. Lesson two. [pause] Build the whole system, A.I. native.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  \u00b7  LESSON 2", "headline": "Build the whole system,\nAI-native.",
             "sub": "From loop to enterprise systems  \u2022  clarkhuang.github.io"})

sc("02_quiz", "Quick question to start. You're asking agents to build a whole app, not just one fix. What matters most? [pause] "
   "The smartest model? The longest prompt? Or a system the agents can read, check, and rebuild on their own? [pause] "
   "<emphasis>The system they can read.</emphasis> A smarter model still guesses when the project lives in someone's head. "
   "A long prompt is gone after one chat. What's written into the system is there for every run, and every agent.",
   "quiz", {"question": "Agents are building a whole app.\nWhat matters most?",
            "options": ["The smartest model", "The longest prompt", "A system they can read"],
            "answer": 2, "why": "Written into\nthe system,\nfor every run."}, "THE QUESTION")

sc("03_shift", "In one oh one, the unit of work was one loop. Plan, build, verify. One fix. One feature. [pause] "
   "In two oh one, the unit of work is the system. Many parts. Many people. Years of history. "
   "And now, agents working in it right alongside the people.",
   "loop_to_graph", {"left_tag": "101  \u00b7  THE LOOP", "left": "One piece\nof work", "left_sub": "made correct",
                     "right_tag": "201  \u00b7  THE SYSTEM", "split": "Split", "merge": "Ship", "node": "loop",
                     "caption": "Many loops, many people, one system."}, "ONE LOOP TO A SYSTEM")

sc("04_define", "So what does A.I. native actually mean? Here's the definition this series uses. "
   "A system is A.I. native when agents and people can <emphasis>both</emphasis> read it, find their way around it, contribute to it, and rebuild it. "
   "[pause] Not only the person who wrote it. Not only whoever knows the history.",
   "statement", {"headline": "AI-native: agents and people\ncan both read it, navigate it,\ncontribute to it, and rebuild it.", "size": 80},
   "WHAT AI-NATIVE MEANS")

FOUR = ["A twin agents can read: Markdown,\nan index, an AGENTS.md",
        "Specs and briefs are the source",
        "Tests and checks are the contract",
        "Staging, then a person approves\nbefore production"]
sc("05_four", "That takes four things. One. Every page people read has a twin an agent can read: plain Markdown, an index of the whole system, "
   "and an agents file that says how to work there. Two. Specs and briefs are the source. Change the brief, and the build follows. "
   "Three. Tests and checks are the contract. An agent is done when the checks pass, not when it says it's done. "
   "And four. Every change goes to staging first, and a person approves it before it reaches production.",
   "recap", {"label": "WHAT MAKES A SYSTEM AI-NATIVE", "rows": FOUR, "upto": 4, "new_from": 0}, "WHAT AI-NATIVE MEANS")

sc("06_example", "And this isn't hypothetical. The site you're on right now is built exactly this way.",
   "statement", {"headline": "The worked example:\nthis site.", "size": 112}, "A WORKED EXAMPLE")

sc("07_files", "Every page has an index dot M D twin, and every folder has an agents dot M D file. "
   "There's an L L M S dot T X T that indexes the whole site, a machine-readable lesson catalog, and a read-only connector A.I. tools can plug into. "
   "[pause] The pages are generated from one content file, and the rebuild steps are written down, so an agent can regenerate every page.",
   "folder_transform", {"label": "CLARKHUANG.GITHUB.IO  \u00b7  WHAT AN AGENT CAN READ",
                        "folder": "clarkhuang.github.io/",
                        "files": ["index.md  (every page)", "AGENTS.md  (every folder)", "llms.txt", "lessons.json",
                                  "sitegen/content.json", "REBUILD.md"],
                        "ask": "Read it, navigate it,\nrebuild it.",
                        "result": "Readable by agents and people",
                        "punch": "Plus a read-only connector AI tools can use."}, "A WORKED EXAMPLE")

sc("08_flow", "And here's the part that matters most. Agents open pull requests into a staging branch. "
   "Staging is a full preview of the site, hidden from search. [pause] And only I merge into production.",
   "rule", {"headline": "How a change ships here",
            "items": ["An agent opens a pull request", "It lands on staging, a full preview",
                      "Checks run on every deploy", "Only the owner merges to production"]}, "A WORKED EXAMPLE")

KIT = {"left_header": "ONE GREAT COOK", "left_sub": "It's all in their head", "left": ["Recipes in memory", "Only they know where things are", "Every plate waits on them"],
       "right_header": "A BIG KITCHEN", "right_sub": "It's written into the place", "right": ["Recipes on cards", "Every station labeled", "The chef checks at the pass"]}
sc("09a_cook", "Think of a kitchen with one great cook. The recipes are in their head. Only they know where everything is. And every plate waits on them.",
   "sorter", dict(KIT, animate="left"), "AT ENTERPRISE SCALE", group="kitchen")
sc("09b_kitchen", "Now picture a big restaurant kitchen. The recipes are written down. Every station is labeled. A cook on a brand new shift can work from the cards. "
   "[pause] And nothing leaves the pass until the head chef looks at it. That's what lets a kitchen grow past one great cook.",
   "sorter", dict(KIT, animate="right"), "AT ENTERPRISE SCALE", group="kitchen")

sc("10_enterprise", "Now scale that up. An enterprise system isn't one repo. It's dozens of services, data that has to stay private, "
   "and people who need to know who changed what, and why. [pause] The same four things still hold. They just matter <emphasis>more</emphasis>. "
   "Without them, every agent starts from zero, and every person becomes the bottleneck.",
   "split", {"label": "THE SAME SYSTEM, BUILT TWO WAYS",
             "left_header": "KNOWLEDGE IN PEOPLE\u2019S HEADS", "reported": "Agents guess.\nPeople become the bottleneck.", "left_tone": "dim",
             "right_header": "KNOWLEDGE IN THE SYSTEM", "actually": "Agents read and check.\nPeople decide.", "right_tone": "accent"},
   "AT ENTERPRISE SCALE")

PATH = ["Build the whole system, AI-native", "Decompose the system into a graph", "Parallel agents, one integration",
        "Governance: where people decide", "Quality, feedback, observability", "Skills as building blocks",
        "Routines, pipelines, integration", "Agents that operate\nenterprise systems", "Capstone: one feature,\nend to end"]
sc("11_path", "That's the path for this series. Today: build the whole system, A.I. native. Then, decompose it into a graph. "
   "Run agents in parallel, and bring the work back together. Put people where the decisions matter. Measure quality, and watch it run. "
   "Turn repeated work into skills. Wire it into routines and pipelines. "
   "Then, agents that operate enterprise systems, with real permissions, and a full audit trail. [pause] "
   "And last, a capstone: one feature, built end to end.",
   "recap", {"label": "SOFTWARE ENGINEERING 201  \u00b7  FROM LOOP TO ENTERPRISE SYSTEMS", "rows": ["Four eras of building systems"] + PATH, "upto": 10, "new_from": 1},
   "THE PATH")

sc("12_rule", "Which gives us rule two, for your agents. Before you build anything bigger than one fix, make it readable: a Markdown twin, an index, and an agents file. "
   "Keep the specs as the source, and the checks as the contract. And send every change through staging, for a person to approve before production.",
   "rule_card", {"kicker": "RULE 2  \u00b7  FOR YOUR AGENTS", "size": 54,
                 "lines": [{"text": "Before you build anything bigger than one fix,"},
                           {"text": "make it readable: a Markdown twin,", "tone": "accent"},
                           {"text": "an index, and an AGENTS.md.", "tone": "accent"},
                           {"text": "Specs are the source. Checks are the contract."},
                           {"text": "Every change goes through staging,", "tone": "accent"},
                           {"text": "and a person approves it before production.", "tone": "accent"}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("13_ask", "Now, your turn. Pick a system you work on. If a brand new agent showed up tomorrow, what could it read? [pause] And what would it have to guess?",
   "statement", {"headline": "Your turn. A new agent shows up\ntomorrow. What could it read?\nWhat would it have to guess?", "size": 84}, "YOUR TURN")

sc("14_close", "See you in lesson three.", "outro", {"headline": "See you in\nlesson three.", "sub": "clarkhuang.github.io \u2022 Software Engineering 201"})

spec = {"id": "se201-02-ai-native", "title": "SE201 Lesson 2: Build the whole system, AI-native",
        "output": "02-build-the-whole-system-ai-native/SE201_02_Build-The-Whole-System-AI-Native_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
words = sum(len(s["text"].replace("[pause]", "").split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))

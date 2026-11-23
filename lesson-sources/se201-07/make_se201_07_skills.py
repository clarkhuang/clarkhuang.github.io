#!/usr/bin/env python3
"""Generates scripts/se201-07-skills.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 7: Skills as Building Blocks.

Public lesson (clarkhuang.github.io). Worked example: the series' made-up subscription-billing system (introduced in
lesson 1 as "a made-up example"), and one recurring job in it, adding a plan or a price, written as a skill. It is
called made up aloud and on screen. Nothing here describes sticky.io or any real company; there are no internal
systems, numbers, incidents or anecdotes, and no other people's names. Every factual claim and its source is in
se201-07-facts.md. The teaching ideas (a skill as a unit of reuse; "the third time" as a rule of thumb; test it with a
fresh agent) are framed as ideas and rules of thumb, not as Clark's history or long-held beliefs.

Uses the drift and skill_card layouts in se201_layouts_58b.py, plus graph, quiz, statement, rule, rule_card, outro.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-07-skills.json
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. Lesson seven. [pause] Skills as building blocks.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 7", "headline": "Skills as\nbuilding blocks.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

# ---- the hook: one job, three runs, three results (a made-up example; said aloud and on screen)
STEPS = ["Step 1", "Step 2", "Step 3", "Step 4"]
OK = {"text": ""}
sc("02_hook", "Why would three capable agents do the same job three different ways? [pause] "
   "Take our made-up subscription-billing system. Now and then, someone asks for a new plan, or a new price. "
   "The first time, an agent works out the four steps, and gets it right. "
   "The second time, a different agent starts from zero, and skips the tax setup. "
   "The third time, another one edits the old price in place, and every existing subscriber is on the new price. [pause] "
   "Same job. Three results. Nobody wrote down how.",
   "drift", {"label": "A MADE-UP EXAMPLE  ·  THE JOB: ADD A PLAN, OR A NEW PRICE, TO THE BILLING SYSTEM",
             "steps": STEPS, "cell_step": 0.5,
             "runs": [{"name": "First time", "sub": "Works out the steps", "at": 0.3,
                       "cells": [OK, OK, OK, OK], "result": "Right"},
                      {"name": "Second time", "sub": "Starts from zero", "at": 0.46,
                       "cells": [OK, {"text": "Skipped the\ntax setup", "state": "skip"}, OK, OK],
                       "result": "No tax set up", "tone": "amber"},
                      {"name": "Third time", "sub": "Starts from zero", "at": 0.62,
                       "cells": [{"text": "Edited the old\nprice in place", "state": "odd"}, OK, OK, OK],
                       "result": "Every subscriber\non the new price", "tone": "amber"}],
             "caption": "Same job. Three results.\nNobody wrote down how.", "caption_at": 0.86, "caption_tone": "amber"},
   "ONE JOB, THREE RESULTS")

# ---- units of reuse: general software history, kept approximate
sc("03_reuse", "Software keeps finding new units of reuse. Libraries: shared code. Frameworks: an application's structure. "
   "Services: something running, behind an A.P.I. [pause] All three reuse software. "
   "A skill reuses something different: <emphasis>how a job gets done.</emphasis> One recurring job, written down, tested, and shared.",
   "graph", {"label": "UNITS OF REUSE  ·  ROUGHLY IN THE ORDER THEY BECAME COMMON",
             "nodes": [{"id": "lib", "text": "Libraries", "sub": "Shared code", "x": 330, "y": 500, "w": 360, "h": 150, "size": 40, "sub_size": 25, "at": 0.12},
                       {"id": "fw", "text": "Frameworks", "sub": "An app’s structure", "x": 750, "y": 500, "w": 360, "h": 150, "size": 40, "sub_size": 25, "at": 0.24},
                       {"id": "svc", "text": "Services", "sub": "Running, behind an API", "x": 1170, "y": 500, "w": 360, "h": 150, "size": 40, "sub_size": 25, "at": 0.36},
                       {"id": "skill", "text": "Skills", "sub": "How a job gets done", "x": 1590, "y": 500, "w": 360, "h": 150, "size": 40, "sub_size": 25,
                        "tone": "accent", "tag": "NOW, ALSO", "at": 0.66}],
             "edges": [["lib", "fw"], ["fw", "svc"], ["svc", "skill"]],
             "bands": [{"x": 130, "y": 370, "w": 1240, "h": 232, "label": "ALL THREE REUSE SOFTWARE", "at": 0.54}],
             "caption": "A skill reuses how a job gets done:\none recurring job, written down, tested, and shared.",
             "caption_y": 690, "caption_at": 0.74, "caption_size": 48},
   "A NEW UNIT OF REUSE")

# ---- the worked example: the made-up system's "add a plan" job as one page
COLS = [[{"head": "WHEN TO USE", "lines": ["Someone asks for a new plan, or a new price"]},
         {"head": "INPUTS", "lines": ["Name  ·  price  ·  billing period  ·  start date"]},
         {"head": "STEPS", "span": 0.5,
          "lines": ["1   Add the plan, with its price as a new version", "2   Set its tax category",
                    "3   Map it in the accounting export", "4   Open a pull request: a person approves the price"]}],
        [{"head": "CHECKS", "span": 0.5,
          "lines": ["Test renewal on staging: right amount, tax included, exactly once", "The ledger still adds up",
                    "Existing subscribers renew at their old price", "If one fails: stop, and say so"]},
         {"head": "TRAPS", "span": 0.2, "lines": ["Never edit a price in place.", "Add a new version."]}]]
def card(**kw):
    return dict({"label": "A MADE-UP EXAMPLE  ·  THE SKILL FOR ADDING A PLAN, OR A PRICE", "path": "skills/add-a-plan/SKILL.md",
                 "version": "v1", "cols": COLS, "card_h": 500}, **kw)

sc("04a_when", "Several agent tools now share a format for this: a folder, with an instruction file. "
   "It starts with when to use it: someone asks for a new plan, or a new price. That line is how an agent finds the skill. "
   "Then the inputs: name, price, billing period, start date. If one is missing, the agent asks. It doesn't guess.",
   "skill_card", card(active=["WHEN TO USE", "INPUTS"], at={"WHEN TO USE": 0.3, "INPUTS": 0.62},
                      caption="When to use it. What it needs. If an input is missing: ask, don’t guess.", caption_at=0.82),
   "ANATOMY OF A SKILL", group="card")
sc("04b_steps", "Then the steps, in order. Add the plan, with its price as a new version. Set its tax category. "
   "Map it in the accounting export. Then open a pull request, because a price is money, and a person approves it.",
   "skill_card", card(held=True, shown=["WHEN TO USE", "INPUTS"], active=["STEPS"], at={"STEPS": 0.04},
                      caption="The steps, in order. And where a person approves.", caption_at=0.1),
   "ANATOMY OF A SKILL", group="card")
sc("04c_checks", "Then the checks: how the agent knows the job worked. "
   "A test renewal on staging charges the right amount, tax included, exactly once. The ledger still adds up. "
   "And existing subscribers still renew at their old price. If one fails, the agent stops, and says so.",
   "skill_card", card(held=True, shown=["WHEN TO USE", "INPUTS", "STEPS"], active=["CHECKS"], at={"CHECKS": 0.16},
                      caption="The checks: how the agent knows the job worked.", caption_at=0.06),
   "ANATOMY OF A SKILL", group="card")
sc("04d_traps", "And the traps: what went wrong before. Never edit a price in place. Add a new version. "
   "That's the mistake from the third run, written down, so nobody repeats it.",
   "skill_card", card(held=True, shown=["WHEN TO USE", "INPUTS", "STEPS", "CHECKS"], active=["TRAPS"], at={"TRAPS": 0.06},
                      caption="The traps: what went wrong before, written down.", caption_at=0.1),
   "ANATOMY OF A SKILL", group="card")

sc("05_runbook", "If that sounds like a runbook, it is. Engineers have written those for decades. What's changed is the reader. "
   "A person reads a runbook now and then, and fills the gaps from memory. "
   "An agent reads the skill on every run, with no memory of the last. Where the page is silent, it guesses. [pause] "
   "And when a step needs no judgment, make it a script the skill calls.",
   "graph", {"label": "IT’S A RUNBOOK  ·  WHAT’S CHANGED IS THE READER",
             "bands": [{"x": 150, "y": 300, "w": 780, "h": 380, "label": "A RUNBOOK  ·  READ BY A PERSON", "at": 0.12},
                       {"x": 990, "y": 300, "w": 780, "h": 380, "label": "A SKILL  ·  READ BY AN AGENT", "tone": "accent", "at": 0.46}],
             "nodes": [{"id": "r1", "text": "Read now and then", "x": 540, "y": 430, "w": 660, "h": 96, "size": 34, "at": 0.3},
                       {"id": "r2", "text": "Gaps filled from memory", "x": 540, "y": 570, "w": 660, "h": 96, "size": 34, "at": 0.38},
                       {"id": "s1", "text": "Read on every run, no memory of the last", "x": 1380, "y": 430, "w": 660, "h": 96, "size": 30, "at": 0.5},
                       {"id": "s2", "text": "Where the page is silent, it guesses", "x": 1380, "y": 570, "w": 660, "h": 96, "size": 32, "tone": "amber", "at": 0.66},
                       {"id": "sc", "text": "A step that needs no judgment?  Make it a script the skill calls.", "x": 960, "y": 790, "w": 1620, "h": 100,
                        "size": 36, "tone": "accent", "at": 0.84}],
             "edges": []},
   "IS THIS JUST A RUNBOOK?")

sc("06_test", "So treat a skill like code. Keep it in the repository, versioned, and reviewed when it changes. [pause] "
   "And test it. Hand it to a fresh agent that has never seen the job, and let it run on staging. "
   "If it can't finish from the page alone, the skill isn't done.",
   "graph", {"label": "TEST IT WITH A FRESH AGENT",
             "nodes": [{"id": "skill", "text": "The skill", "sub": "In the repo · versioned", "x": 320, "y": 440, "w": 380, "h": 140, "size": 38, "sub_size": 24,
                        "tone": "accent", "tag": "REVIEWED WHEN IT CHANGES", "at": 0.1},
                       {"id": "agent", "text": "A fresh agent", "sub": "Never seen the job", "x": 800, "y": 440, "w": 380, "h": 140, "size": 38, "sub_size": 24, "at": 0.48},
                       {"id": "stage", "text": "Runs it\non staging", "x": 1240, "y": 440, "w": 300, "h": 140, "size": 34, "at": 0.62},
                       {"id": "ok", "text": "Finishes from\nthe page alone", "x": 1630, "y": 440, "w": 320, "h": 140, "size": 30, "tone": "accent", "at": 0.7},
                       {"id": "fix", "text": "Can’t finish from the page alone?  The skill isn’t done.", "x": 780, "y": 700, "w": 1100, "h": 100, "size": 32,
                        "tone": "amber", "at": 0.8}],
             "edges": [["skill", "agent"], ["agent", "stage"], ["stage", "ok"],
                       {"from": "stage", "to": "fix", "tone": "amber", "at": 0.82}, {"from": "fix", "to": "skill", "tone": "amber", "at": 0.9}],
             "caption": "Treat a skill like code: in the repo, versioned, reviewed.", "caption_y": 850, "caption_at": 0.2, "caption_size": 46},
   "TREAT IT LIKE CODE")

# ---- the hook's picture again, repaired; then the skill itself is fixed (v1 -> v2)
def same(name, at):
    return {"name": name, "sub": "From the skill", "at": at, "cells": [OK, OK, OK, OK], "result": "Checks pass"}
sc("07_improve", "Now run those three jobs again, from the skill. Same steps. Same checks. [pause] "
   "No guarantee: agents still vary. That's what the checks are for. "
   "And when a run goes wrong, don't just fix the run. Fix the skill. One change, in one place, and every later run gets it. "
   "That's a building block: reliable enough to build on.",
   "drift", {"label": "THE SAME THREE RUNS  ·  THIS TIME FROM THE SKILL",
             "steps": STEPS, "cell_step": 0.2,
             "header": {"text": "skills/add-a-plan  ·  v1", "text2": "skills/add-a-plan  ·  v2", "note2": "Fixed once, here",
                        "tag": "ONE SKILL,\nONE PLACE", "at": 0.03, "swap_at": 0.6, "mono": True},
             "runs": [same("First time", 0.08), same("Second time", 0.14), same("Third time", 0.2)],
             "caption": "When a run goes wrong, fix the skill, not just the run.", "caption_at": 0.5, "caption_tone": "accent"},
   "FIX IT IN ONE PLACE")

sc("08_when", "So when is a job worth a skill? The first time? The third? Or never, because agents can work it out? [pause] "
   "A good rule of thumb: <emphasis>the third time.</emphasis> Once, you're learning. Twice, you see the pattern. The third time, write it down. "
   "Sooner, if a mistake costs money.",
   "quiz", {"label": "A RULE OF THUMB", "question": "When is a job worth\nwriting as a skill?",
            "options": ["The first time it comes up", "The third time it comes back", "Never: agents can work it out"],
            "answer": 1, "why": "Once: learning.\nTwice: a pattern.\nThird: write it down.\nSooner, if a mistake\ncosts money.", "options_at": 0.08, "reveal_at": 0.42},
   "WHEN TO WRITE ONE")

sc("09_recap", "So, to recap. One recurring job, written down, with its checks and its traps. In the repo, tested by a fresh agent. "
   "And when a run goes wrong, fix the skill.",
   "rule", {"headline": "Skills as building blocks",
            "items": ["One recurring job, written down", "With its checks and its traps",
                      "In the repo, tested by a fresh agent", "When a run goes wrong, fix the skill"]}, "RECAP")

sc("10_rule", "Which gives us rule seven, for your agents. When a job comes back a third time, write it as a skill: "
   "when to use it, inputs, steps, checks, and traps. Keep it in the repo, and test it with a fresh agent. "
   "And when a run goes wrong, fix the skill, not just the run.",
   "rule_card", {"kicker": "RULE 7  ·  FOR YOUR AGENTS", "size": 56,
                 "lines": [{"text": "When a job comes back a third time,"},
                           {"text": "write it as a skill:", "tone": "accent"},
                           {"text": "when to use it, inputs, steps, checks, traps.", "tone": "accent"},
                           {"text": "Keep it in the repo. Test it with a fresh agent."},
                           {"text": "When a run goes wrong,"},
                           {"text": "fix the skill, not just the run.", "tone": "accent"}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("11_ask", "Now, your turn. Pick a job you've explained to your A.I. more than twice. Ask it to draft the skill. "
   "[pause] Then open a fresh chat, give it only that page, and see if the job gets done.",
   "statement", {"headline": "Your turn. A job you’ve explained\nto your AI more than twice:\nask it to draft the skill.\nThen give only that page\nto a fresh chat.", "size": 76},
   "YOUR TURN")

sc("12_close", "One skill does one job. But real work is a chain of jobs, and some of it should start on its own. "
   "That's next: routines, pipelines, and integration. See you in lesson eight.",
   "outro", {"headline": "See you in\nlesson eight.", "sub": "Software Engineering 201"})

spec = {"id": "se201-07-skills", "title": "SE201 Lesson 7: Skills as building blocks",
        "output": "07-skills-as-building-blocks/SE201_07_Skills-As-Building-Blocks_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
def spoken(s): return re.sub(r"<[^>]+>|\[pause\]", " ", s["text"])
words = sum(len(spoken(s).split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s")
for s in S:
    print(f"  {s['id']:<14} {s['visual']:<10} {s['chapter']:<24} {len(spoken(s).split()):>3} w")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))
# (The build-machine copy also asserts that a private company name never appears; that one line is left out of this public copy.)
assert set(re.findall(r"\[[a-z]+\]|</?[a-z]+>", " ".join(s["text"] for s in S))) <= {"[pause]", "<emphasis>", "</emphasis>", "<slow>", "</slow>"}

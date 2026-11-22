#!/usr/bin/env python3
"""Generates scripts/se201-02-decompose.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 2: Decompose the System into a Graph.

Public lesson (clarkhuang.github.io). Absorbs the earlier "From Loop to Graph" recording (loop vs graph,
"and then" is not a dependency, the dinner graph, serial vs side-by-side bars, the graph doesn't replace the loop).
Worked example = this site as a graph; every claim about it is listed, with where to check it, in se201-02-facts.md:
four sections built by one generator with one stylesheet; a lesson build where narration needs the script, the render
needs the clips (audio length sets the timing), captions need the render's timeline, sound level and poster need the
rendered video, the page needs all of it, then a pull request to staging and only the owner merges to production.
The enterprise scene is a generic picture, not any real company's system.
No company-internal systems, no invented anecdotes, no other people's names.

Uses the graph and crossing layouts in se101_layouts6.py.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-02-decompose.json
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. Lesson two. [pause] Decompose the system into a graph.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 2", "headline": "Decompose the system\ninto a graph.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Quick question. An agent hands you a plan. Ten steps, numbered one to ten. "
   "How many of those steps truly have to wait for the step before? [pause] "
   "All ten? About half? Or is it impossible to tell from the list? [pause] "
   "<emphasis>You can't tell.</emphasis> A numbered list records the order someone wrote things down. "
   "It doesn't say what needs what.",
   "quiz", {"question": "A plan with ten numbered steps.\nHow many must wait for the step before?",
            "options": ["All ten", "About half", "You can’t tell from the list"],
            "answer": 2, "why": "A list shows\nwriting order,\nnot what\nneeds what.", "options_at": 0.37, "reveal_at": 0.6},
   "THE QUESTION")

sc("03_test", "So here's the test. Take any two steps, and ask: what crosses between them? [pause] "
   "Think about cooking dinner. The sauce waits for the chopped onions. Something crosses, so that's a real dependency. Draw the arrow. [pause] "
   "The rice and the salad? Nothing crosses. So nobody waits for the rice before starting the salad. [pause] "
   "<slow>And then, is not a dependency.</slow>",
   "crossing", {"label": "THE TEST FOR ANY TWO STEPS", "question": "WHAT CROSSES?",
                "rows": [{"a": "Chop the onions", "b": "Start the sauce", "crosses": "chopped onions",
                          "verdict": "A real dependency.", "sub": "Draw the arrow.", "at": 0.2},
                         {"a": "Cook the rice", "b": "Make the salad", "crosses": "", "nothing": "nothing crosses",
                          "verdict": "No arrow.", "sub": "Nobody waits.", "at": 0.56}],
                "caption": "“And then” is not a dependency.", "caption_at": 0.86, "y0": 390, "row_h": 176}, "WHAT CROSSES?")

sc("04_loop_graph", "In one oh one, the unit was the loop. Plan, build, verify, until one piece of work is right. "
   "The graph sits one level up. It says which pieces exist, what each one needs, and which can run at the same time. [pause] "
   "And it doesn't replace the loop. Every node in the graph is <emphasis>still</emphasis> a loop of its own.",
   "loop_to_graph", {"left_tag": "101  ·  THE LOOP", "left": "One piece\nof work", "left_sub": "made correct",
                     "right_tag": "201  ·  THE GRAPH", "split": "Split", "merge": "Merge", "node": "loop",
                     "caption": "Every node is still a loop."}, "LOOP AND GRAPH")

# ---- worked example, first view: this site as parts and what they share
SEC = [("tips", "AI Tips", "ai-tips/", 400), ("se101", "Software Engineering 101", "software-engineering-101/", 528),
       ("se201", "Software Engineering 201", "software-engineering-201/", 656), ("book", "The book", "book/", 784)]
BAND = {"x": 700, "y": 290, "w": 520, "h": 580, "label": "FOUR PARTS"}
def site_nodes(held):
    return [{"id": i, "text": name, "sub": folder, "sub_mono": True, "sub_size": 20, "x": 960, "y": y, "w": 440, "h": 104,
             "size": 29, "held": held, "at": 0.2 + 0.11 * k} for k, (i, name, folder, y) in enumerate(SEC)]

sc("05a_parts", "Let's decompose a real system: the site you're on. Start with the parts. A.I. tips. Software engineering one oh one. Two oh one. And the book. "
   "Each part has its own folder, and its own pages. [pause] A new lesson in one needs nothing from the others. So work on one never waits on another.",
   "graph", {"label": "CLARKHUANG.GITHUB.IO  ·  THE PARTS", "nodes": site_nodes(False),
             "bands": [dict(BAND, at=0.08)], "edges": [],
             "caption": "No arrows\nbetween them.\nNobody waits.", "caption_x": 1300, "caption_y": 490, "caption_at": 0.72, "caption_size": 50},
   "THIS SITE, AS A GRAPH", group="site")

sc("05b_shared", "But they aren't floating free. All four are built by one generator, with one stylesheet. That shared piece is a node too, and every part depends on it. [pause] "
   "So the graph shows you where to be careful. Change one part, and one part moves. Change the shared node, and <emphasis>everything</emphasis> moves. "
   "Which is why a shared node needs one clear owner.",
   "graph", {"label": "CLARKHUANG.GITHUB.IO  ·  THE PARTS, AND WHAT THEY SHARE",
             "nodes": site_nodes(True) + [
                 {"id": "gen", "text": "One generator\nOne stylesheet", "x": 380, "y": 590, "w": 360, "h": 150, "size": 32,
                  "tone": "amber", "tag": "SHARED  ·  ONE OWNER", "at": 0.06},
                 {"id": "site", "text": "The site", "x": 1560, "y": 590, "w": 300, "h": 120, "size": 34, "tone": "hi", "at": 0.3}],
             "bands": [dict(BAND, held=True)],
             "edges": [["gen", i] for i, _, _, _ in SEC] + [[i, "site"] for i, _, _, _ in SEC],
             "caption": "Change one part: one part moves.\nChange the shared node: everything moves.",
             "caption_x": 160, "caption_y": 890, "caption_at": 0.55, "caption_size": 40},
   "THIS SITE, AS A GRAPH", group="site")

# ---- worked example, second view: one lesson as a chain with a fork
def chain(extra):
    nodes = [{"id": "script", "text": "Scene\nscript", "x": 270, "y": 520},
             {"id": "narr", "text": "Narration\nclips", "x": 560, "y": 520},
             {"id": "render", "text": "Render", "x": 850, "y": 520},
             {"id": "caps", "text": "Captions", "x": 1140, "y": 400},
             {"id": "sound", "text": "Sound level,\nposter", "x": 1140, "y": 640},
             {"id": "page", "text": "Lesson\npage", "x": 1430, "y": 520},
             {"id": "stage", "text": "Staging, then\nI merge", "x": 1720, "y": 520}]
    for n in nodes:
        n.update({"w": 224, "h": 104, "size": 27})
    edges = [{"from": "script", "to": "narr", "label": "script", "size": 18}, {"from": "narr", "to": "render", "label": "audio"},
             {"from": "render", "to": "caps", "label": "timeline", "dy": -50, "dx": -52},
             {"from": "render", "to": "sound", "label": "video", "dy": 24, "dx": -44},
             ["caps", "page"], ["sound", "page"], {"from": "page", "to": "stage", "label": "PR"}]
    return dict({"label": "ONE LESSON OF THIS SITE  ·  WHAT EACH STEP NEEDS", "nodes": nodes, "edges": edges,
                 "caption_x": 160, "caption_y": 800, "caption_size": 44}, **extra)

sc("06a_chain", "Now zoom into one node: a single video lesson. Here, the arrows are real. The narration clips need the script. "
   "The render needs those clips, because the length of the audio sets the timing. Captions need the timeline the render writes out. "
   "And the page needs all of it, before a pull request to staging, where only I merge to production. [pause] Every arrow carries something.",
   "graph", chain({"spread": 0.62, "caption": "Every arrow carries something.", "caption_at": 0.86}),
   "ONE LESSON, AS A GRAPH", group="chain")

sc("06b_fork", "Script, narration, render. A strict chain. More agents won't make it shorter: the longest chain sets the minimum. [pause] "
   "But after the render, it forks. Captions need only the timeline. The sound level and the poster need only the video. Nothing crosses between those two. "
   "The build script happens to run them one after the other. The graph shows that's a choice, not a requirement.",
   "graph", dict(chain({"static": True, "path": ["script", "narr", "render"], "path_tone": "amber", "path_at": 0.04,
                        "runner": False, "caption": "The longest chain sets the minimum.\nThe fork is where you get time back.",
                        "caption_at": 0.62}),
                 bands=[{"x": 984, "y": 300, "w": 312, "h": 432, "label": "NOTHING CROSSES", "tone": "accent", "at": 0.36, "held": False}]),
   "ONE LESSON, AS A GRAPH", group="chain")

sc("07_bars", "Why does this matter? Waiting. Picture three parts, with nothing crossing between them. "
   "Run as a numbered list, each one waits for the last. Run as a graph, they go side by side. Same work. Far less waiting.",
   "cost_bars", {"label": "TIME FROM START TO DONE  ·  AN ILLUSTRATION",
                 "bars": [{"name": "As a numbered list: each part waits for the last", "frac": 1.0, "tone": "amber", "segments": 3},
                          {"name": "As a graph: side by side", "frac": 0.34, "tone": "accent", "segments": 1}],
                 "note": "Same work. Far less waiting.",
                 "fine": "THREE EQUAL PARTS, NOTHING CROSSING BETWEEN THEM"}, "WHY IT MATTERS")

# ---- a generic picture, not any real company's system
ENT = [("orders", "Orders", 420), ("billing", "Billing", 800), ("shipping", "Shipping", 1180), ("support", "Support", 1560)]
sc("08_scale", "Now scale that up. Picture an enterprise system. Orders, billing, shipping, support. Far too big for one loop. [pause] "
   "It's the same picture. A few real arrows: billing needs the order, shipping needs the payment. A shared node everything leans on, like customer data. "
   "And parts that never touch, where teams and agents move without waiting. [pause] "
   "Miss the shared node, and two of them collide at the end.",
   "graph", {"label": "PICTURE AN ENTERPRISE SYSTEM  ·  THE SAME GRAPH, BIGGER",
             "nodes": [{"id": i, "text": name, "x": x, "y": 400, "w": 290, "h": 110, "size": 34, "at": 0.08 + 0.05 * k}
                       for k, (i, name, x) in enumerate(ENT)] +
                      [{"id": "shared", "text": "Customer data", "x": 990, "y": 660, "w": 1430, "h": 100, "size": 34,
                        "tone": "amber", "tag": "SHARED", "at": 0.56}],
             "edges": [{"from": "orders", "to": "billing", "label": "order", "tone": "accent", "at": 0.36},
                       {"from": "billing", "to": "shipping", "label": "payment", "tone": "accent", "size": 17, "at": 0.44}] +
                      [{"from": "shared", "to": i} for i, _, _ in ENT],
             "caption": "A few real arrows. A shared node. Parts that never touch.",
             "caption_x": 275, "caption_y": 800, "caption_at": 0.74, "caption_size": 44},
   "AT ENTERPRISE SCALE")

sc("09_recap", "So, to recap. Drawing the graph is four moves. One. Name the parts, each with a boundary and an owner. "
   "Two. For every pair, ask what crosses, and what they share. Three. Draw only those arrows. And four. Give every part its own finish line, and its own check.",
   "rule", {"headline": "Drawing the graph: four moves",
            "items": ["Name the parts: a boundary and an owner for each", "For every pair: what crosses? What do they share?",
                      "Draw only those arrows", "Give every part its own finish line and check"]}, "RECAP")

sc("10_rule", "Which gives us rule two, for your agents. Before any job with more than one part, draw the graph. Name the parts. "
   "Draw an arrow only where something crosses from one part to another. Anything two parts share becomes its own node, with one owner. "
   "Parts with no arrow between them run at the same time. And every part gets its own loop: plan, build, verify.",
   "rule_card", {"kicker": "RULE 2  ·  FOR YOUR AGENTS", "size": 54,
                 "lines": [{"text": "Before any job with more than one part,"},
                           {"text": "draw the graph: name the parts,", "tone": "accent"},
                           {"text": "and draw an arrow only where something crosses.", "tone": "accent"},
                           {"text": "Anything shared becomes its own node, with one owner."},
                           {"text": "No arrow? Those parts run at the same time.", "tone": "accent"},
                           {"text": "Every part gets its own loop: plan, build, verify."}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("11_ask", "Now, your turn. Take the last multi-step plan an agent gave you. At every, and then, ask what crosses. [pause] How many arrows survive?",
   "statement", {"headline": "Your turn. Your last multi-step plan.\nAt every “and then”: what crosses?\nHow many arrows survive?", "size": 82}, "YOUR TURN")

sc("12_close", "Next time, those parts really do run at once, and we bring the work back together. See you in lesson three.",
   "outro", {"headline": "See you in\nlesson three.", "sub": "Next: parallel agents, one integration"})

spec = {"id": "se201-02-decompose", "title": "SE201 Lesson 2: Decompose the system into a graph",
        "output": "02-decompose-the-system-into-a-graph/SE201_02_Decompose-The-System-Into-A-Graph_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
words = sum(len(s["text"].replace("[pause]", "").split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))

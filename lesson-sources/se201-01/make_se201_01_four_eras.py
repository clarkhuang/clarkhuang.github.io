#!/usr/bin/env python3
"""Generates scripts/se201-01-four-eras.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 1: Four Eras of Building Systems.

Public lesson (clarkhuang.github.io). Rewritten from the scriptwriter's Mac draft (make_se201_01_four_eras_mac.py).
Every factual claim, and where it comes from, is in facts.md beside this lesson's sources:
  - about Clark: only the public career record (PropertyBridge, Marqeta, sticky.io, eCIO, QRS, "now CTO of an
    e-commerce company", unnamed) and the facts file (about 30 years; one monorepo with agent instruction files).
  - industry history: general knowledge, kept approximate (Agile Manifesto 2001; first big public cloud services 2006;
    containers and microservices mainstream in the mid-2010s).
The lens ("architecture bends around whatever is scarcest"), the scarce resource per era and the four constants were
written by the scriptwriter: they are presented as a teaching lens, not as Clark's quote. The agent-era design list is
presented as where thinking is heading, not settled. The subscription-billing picture is an illustration, not
sticky.io's design. No internal systems, numbers, incidents or anecdotes; no other people's names.

Uses the eras and constants layouts in se201_layouts_eras.py.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-01-four-eras.json
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. From loop, to enterprise systems. Lesson one. [pause] Four eras of building systems.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 1", "headline": "Four eras of\nbuilding systems.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Quick question. An agent can now write a working piece of a billing system in an afternoon. "
   "So in a big system today, what's scarce? [pause] Code? Servers? Or knowing that what got built is right? [pause] "
   "<emphasis>Knowing it's right.</emphasis> Code got cheap. Checking it didn't. [pause] Thirty years ago, the answer was very different.",
   "quiz", {"question": "Agents write code fast now.\nBuilding a big system, what’s scarce?",
            "options": ["Code", "Servers", "Knowing it’s right"],
            "answer": 2, "why": "Code got\ncheap.\nChecking it\ndidn’t.", "options_at": 0.3, "reveal_at": 0.52},
   "THE QUESTION")

# ---- public career record only (company descriptions from public profiles); no order implied except "early" and "now"
CAREER = [("pb", "PropertyBridge", "Electronic rent payments", "CO-FOUNDER", 560, 470),
          ("mq", "Marqeta", "Card issuing", "CO-FOUNDER", 1080, 470),
          ("ec", "eCIO", "Investment adviser, nonprofits", "CO-FOUNDER · CTO", 1600, 470),
          ("qrs", "QRS", "Retail e-commerce, EDI", "EARLY ROLE", 560, 740),
          ("st", "sticky.io", "Subscription billing", "CTO", 1080, 740),
          ("now", "Today", "An e-commerce company", "CTO", 1600, 740)]
sc("03_career", "I've been building systems for about thirty years. Systems built around money: electronic rent payments, "
   "a card-issuing platform, an investment adviser for nonprofits. And systems that sell: retail e-commerce and E.D.I., subscription billing, and today, e-commerce again. "
   "[pause] And the way you build a big system keeps changing.",
   "graph", {"label": "ABOUT THIRTY YEARS OF BUILDING SYSTEMS",
             "bands": [{"x": 110, "y": 316, "w": 1750, "h": 230, "label": "MONEY", "at": 0.04},
                       {"x": 110, "y": 586, "w": 1750, "h": 230, "label": "COMMERCE", "at": 0.3}],
             "nodes": [{"id": i, "text": name, "sub": sub, "tag": tag, "x": x, "y": y, "w": 440, "h": 120, "size": 36,
                        "sub_size": 25, "tone": "hi" if i == "now" else None, "at": 0.06 + 0.1 * k}
                       for k, (i, name, sub, tag, x, y) in enumerate(CAREER)],
             "edges": [], "caption": "Payments, cards, billing, investing, commerce.", "caption_x": 160, "caption_y": 880,
             "caption_at": 0.74, "caption_size": 44},
   "A LENS")

sc("04_lens", "Here's a useful way to see why. <slow>Architecture bends around whatever is scarcest.</slow> "
   "Whatever is expensive, or slow, the design works around it. So for each of four eras, ask: what was scarce?",
   "statement", {"headline": "A useful lens: architecture\nbends around whatever\nis scarcest.", "size": 96}, "A LENS")

ERAS = [
 {"year": "1996", "ago": "30 YEARS AGO", "scarce": "Machines",
  "rows": [["RUNS ON", "Servers you bought\nand racked yourself"], ["SHAPE", "One big program,\none big database"],
           ["SHIPS", "A few times a year"], ["CONNECTS BY", "Overnight batch\nfiles, EDI"]]},
 {"year": "2006", "ago": "20 YEARS AGO", "scarce": "Coordination",
  "rows": [["RUNS ON", "Rented racks; the first\npublic cloud services"], ["SHAPE", "Browser, application,\ndatabase"],
           ["SHIPS", "Every few weeks"], ["CONNECTS BY", "Web services,\nXML over HTTP"]]},
 {"year": "2016", "ago": "10 YEARS AGO", "scarce": "Seeing the whole",
  "rows": [["RUNS ON", "The cloud, by default\nfor new systems"], ["SHAPE", "Many small services,\nowned by small teams"],
           ["SHIPS", "Many times a day,\nat the best teams"], ["CONNECTS BY", "An API for everything"]]},
 {"year": "Now", "ago": "AGENTS DO THE BUILDING", "scarce": "Knowing it’s right",
  "rows": [["RUNS ON", "The cloud, still"], ["SHAPE", "Clear modules an\nagent can work inside"],
           ["SHIPS", "As fast as you\ncan verify"], ["CONNECTS BY", "APIs, and agents\ncalling tools"]]},
]
def eras(n, **kw):
    return dict({"label": "FOUR ERAS OF BUILDING A SYSTEM  ·  WHAT WAS SCARCE?", "eras": ERAS, "upto": n}, **kw)

sc("05_1996", "Thirty years ago, the commercial web was brand new. You bought servers and racked them yourself, and more capacity was weeks away. "
   "So, typically, you built one big program, on one big database, and shipped a few times a year. Companies traded orders as overnight batch files, through E.D.I., and much of that still runs. "
   "[pause] What was scarce? <emphasis>The machines.</emphasis>",
   "eras", eras(1), "FOUR ERAS", group="eras")
sc("06_2006", "Twenty years ago. The web was the front door. Browser, application, database: three tiers, on rented racks. "
   "And the first big public cloud services had just launched. Agile teams shipped every few weeks. "
   "[pause] What was scarce? <emphasis>Coordination.</emphasis> Getting a growing team to change one codebase without colliding.",
   "eras", eras(2), "FOUR ERAS", group="eras")
sc("07_2016", "Ten years ago. The cloud, by default, for new systems. Many small services, in containers, owned by small teams. "
   "The best teams deployed many times a day. And parts they once built themselves became a service, behind an A.P.I. "
   "[pause] What was scarce? <emphasis>Seeing the whole.</emphasis> No one person could hold it all in their head, so we built dashboards and tracing to see it.",
   "eras", eras(3), "FOUR ERAS", group="eras")
sc("08_now", "And now. Agents can write much of the code. Building a piece is fast, and cheap. "
   "[pause] So what's scarce? <slow>Knowing that it's right.</slow> That, and context: how much of the system an agent can see, and understand, at once.",
   "eras", eras(4, caption="Also scarce: context. How much of the system an agent can see at once.", caption_at=0.72),
   "FOUR ERAS", group="eras")

# ---- an illustration of a system built today; NOT sticky.io's design (no internal details are claimed)
sc("09_design", "Now a made-up example: a subscription-billing system, built today, the kind of platform I ran as C.T.O. at sticky dot I O. "
   "Clear modules, with boundaries an agent can work inside. One repository, where it can find anything. "
   "Tests and specs it can check itself against. And decisions written down, because the agent wasn't in the meeting. "
   "[pause] My own team keeps its code that way: one repository, with instruction files for the agents.",
   "graph", {"label": "A MADE-UP EXAMPLE  ·  A SUBSCRIPTION-BILLING SYSTEM, BUILT NOW",
             "bands": [{"x": 150, "y": 300, "w": 1620, "h": 540, "label": "ONE REPOSITORY  ·  EVERYTHING FINDABLE", "tone": "accent", "at": 0.1}],
             "nodes": [{"id": "plans", "text": "Plans and\nprices", "x": 420, "y": 440, "w": 300, "h": 110, "at": 0.16},
                       {"id": "cust", "text": "Customer\naccounts", "x": 420, "y": 610, "w": 300, "h": 110, "at": 0.2},
                       {"id": "renew", "text": "Renewals", "x": 880, "y": 525, "w": 270, "h": 110, "at": 0.24},
                       {"id": "pay", "text": "Payments", "x": 1270, "y": 525, "w": 270, "h": 110, "at": 0.28},
                       {"id": "ledger", "text": "Ledger", "x": 1610, "y": 525, "w": 230, "h": 110, "tone": "amber",
                        "tag": "MUST ADD UP", "at": 0.32},
                       {"id": "tests", "text": "Tests and specs\nper module", "x": 640, "y": 760, "w": 380, "h": 96,
                        "size": 26, "tone": "accent", "at": 0.5},
                       {"id": "dec", "text": "Decisions,\nwritten down", "x": 1100, "y": 760, "w": 380, "h": 96,
                        "size": 26, "tone": "accent", "at": 0.62},
                       {"id": "agents", "text": "Instructions\nfor agents", "x": 1520, "y": 760, "w": 340, "h": 96,
                        "size": 26, "tone": "accent", "at": 0.86}],
             "edges": [{"from": "plans", "to": "renew", "label": "price", "dx": 30}, {"from": "cust", "to": "renew", "label": "who", "dx": 30, "dy": 8},
                       {"from": "renew", "to": "pay", "label": "charge"}, {"from": "pay", "to": "ledger", "label": "entry", "size": 18}],
             "caption": "Boundaries an agent can work inside. Checks it can run.", "caption_x": 160, "caption_y": 890,
             "caption_at": 0.4, "caption_size": 40},
   "BUILDING NOW")

sc("10_caveat", "I'll be straight about that list. It's where the thinking is heading, not a settled answer. The evidence for it is "
   "still thin, and indirect. Every era had a confident answer, then found its costs.",
   "statement", {"headline": "Where the thinking is heading.\nNot settled.", "size": 96}, "BUILDING NOW")

sc("11_constants", "And here's what never changed, in any era. The data model outlives the code. "
   "Money has to add up. "
   "Every system depends on things you don't control: a bank, a card network, a partner's system. "
   "And somebody has to understand the layer below.",
   "constants", {"label": "WHAT NEVER CHANGED  ·  TRUE IN ALL FOUR ERAS", "cols": ["1996", "2006", "2016", "Now"],
                 "items": [{"text": "The data model outlives the code", "sub": "Programs get rewritten. The data stays."},
                           {"text": "Money has to add up", "sub": "Every rent payment, card transaction, renewal"},
                           {"text": "You depend on what you don’t control", "sub": "A bank, a card network, a partner’s system"},
                           {"text": "Someone understands the layer below", "sub": "When it breaks, someone has to look underneath"}]},
   "WHAT NEVER CHANGES")

PATH = ["Four eras of building systems", "Build the whole system, AI-native", "Decompose the system into a graph",
        "Parallel agents, one integration", "Governance: where people decide", "Quality, feedback, observability",
        "Skills as building blocks", "Routines, pipelines, integration", "Agents that operate\nenterprise systems"]
sc("12_path", "Here's the path. Today, the four eras. Then, build a whole system A.I. native, decompose it, "
   "and run agents in parallel. Then governance, quality, skills, and pipelines. [pause] "
   "And finally, agents that operate enterprise systems.",
   "recap", {"label": "SOFTWARE ENGINEERING 201  ·  FROM LOOP TO ENTERPRISE SYSTEMS", "rows": PATH, "upto": 9, "new_from": 0},
   "THE PATH")

sc("13_recap", "So, to recap. Architecture bends around what's scarce. Today, that's knowing the work is right, and context. "
   "So design for checking. And the four constants still hold.",
   "rule", {"headline": "Four eras, one lens",
            "items": ["Architecture bends around what’s scarce", "Now: knowing it’s right, and context",
                      "So design for checking: boundaries, tests", "Four constants still hold"]}, "RECAP")

sc("14_rule", "Which gives us rule one, for your agents. Before you design a system, write down four things. Where the boundaries are. "
   "What the data model is. What you depend on, and don't control. And how you'll know it's right. "
   "Then put it in the repository, where every agent can read it.",
   "rule_card", {"kicker": "RULE 1  ·  FOR YOUR AGENTS", "size": 56,
                 "lines": [{"text": "Before you design a system, write down:"},
                           {"text": "where the boundaries are,", "tone": "accent"},
                           {"text": "what the data model is,", "tone": "accent"},
                           {"text": "what you depend on and don’t control,", "tone": "accent"},
                           {"text": "and how you’ll know it’s right.", "tone": "accent"},
                           {"text": "Put it in the repo, where every agent can read it."}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("15_ask", "Now, your turn. Pick the oldest system you still depend on. When was it built, and what was scarce back then? "
   "[pause] Then ask your A.I. which era's thinking is hiding inside it.",
   "statement", {"headline": "Your turn. Your oldest system:\nwhen was it built? What was scarce?\nAsk your AI which era’s thinking\nis hiding inside it.", "size": 74},
   "YOUR TURN")

sc("16_close", "Next: build a whole system, A.I. native, so agents and people can both read it, and rebuild it. See you in lesson two.",
   "outro", {"headline": "See you in\nlesson two.", "sub": "Software Engineering 201"})

spec = {"id": "se201-01-four-eras", "title": "SE201 Lesson 1: Four eras of building systems",
        "output": "01-four-eras-of-building-systems/SE201_01_Four-Eras-Of-Building-Systems_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
def spoken(s): return re.sub(r"<[^>]+>|\[pause\]", " ", s["text"])
words = sum(len(spoken(s).split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s")
for s in S:
    print(f"  {s['id']:<14} {s['visual']:<10} {s['chapter']:<18} {len(spoken(s).split()):>3} w")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))
# (The build-machine copy also asserts that a private company name never appears; that one line is left out of this public copy.)
assert set(re.findall(r"\[[a-z]+\]|</?[a-z]+>", " ".join(s["text"] for s in S))) <= {"[pause]", "<emphasis>", "</emphasis>", "<slow>", "</slow>"}

#!/usr/bin/env python3
"""Generates scripts/se201-06-quality.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 6: Quality, Feedback, and Observability.

Public lesson (clarkhuang.github.io). Every factual claim, and where it comes from, is in se201-06-facts.md.
  - about Clark: nothing new is claimed. The billing system is "our made-up example ... from lesson one"; every
    renewal, plan, price, total and record line on screen is invented and labelled made-up. Nothing here describes
    sticky.io or any real company.
  - the lens (ten years ago seeing the whole was scarce; now knowing it's right is) is lesson 1's teaching lens,
    recalled as "the lens from lesson one", not as fact or as Clark's quote.
  - industry terms: logs, metrics and traces as the usual observability signals; "service level objective" (S.L.O.)
    as the usual name for a written reliability target. General knowledge; no statistics.
  - "write the check once, run it twice", the three checks and the feedback loop are teaching ideas written by the
    scriptwriter. The arithmetic on screen is real: the six prices add up to $354, and so do the charges (29 + 99 + 2x29 + 49 + 119 + 0): the three errors cancel.

Uses the renewals layout in se201_layouts_58a.py, plus two_kinds and graph.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-06-quality.json
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. Lesson six. [pause] Quality, feedback, and observability.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 6", "headline": "Quality, feedback,\nand observability.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Picture a made-up billing system. Last night, it renewed its subscriptions. This morning the build is green, and every test passed. "
   "Was every customer charged the right amount, exactly once? [pause] Yes, the tests passed? Probably, coverage is high? Or: you can't tell from that? [pause] "
   "<emphasis>You can't tell from that.</emphasis> Green says the code did what its tests asked. It says nothing about what happened last night.",
   "quiz", {"question": "The build is green. Every test passed. Was every\ncustomer charged the right amount, exactly once?",
            "options": ["Yes: the tests passed", "Probably: coverage is high", "You can’t tell from that"],
            "answer": 2, "why": "Green is about\nthe code. Not\nabout last night.", "options_at": 0.5, "reveal_at": 0.7},
   "THE QUESTION")

CARDS = [{"tag": "TEN YEARS AGO", "tone": "amber", "title": "What happened?",
          "items": ["Scarce: seeing the whole", "Logs, metrics, traces"], "foot": "Observability"},
         {"tag": "NOW", "tone": "accent", "title": "Was it right?",
          "items": ["Scarce: knowing it’s right", "Define right, up front", "Watch every run", "Feed back what you learn"],
          "foot": "Quality, designed in"}]
def kinds(n): return {"label": "THE LENS FROM LESSON ONE  ·  ARCHITECTURE BENDS AROUND WHAT’S SCARCE", "cards": CARDS, "active": n}
sc("03a_then", "Back to the lens from lesson one: architecture bends around what's scarce. Ten years ago, the scarce thing was seeing the whole system. "
   "The answer was observability: logs, metrics, traces. They answer: what happened?",
   "two_kinds", kinds(1), "A LENS", group="kinds")
sc("03b_now", "Now the scarce thing is knowing it's right. That's a different question. And no dashboard can answer it, "
   "until somebody has written down what right means. [pause] So: define right, up front. Watch every run. And feed back what you learn.",
   "two_kinds", kinds(2), "A LENS", group="kinds")

# ---- the worked example: invented renewals for the made-up billing system. 29+99+29+49+99+49 = 354; 29+99+58+49+119+0 = 354: the three errors cancel.
RENEWALS = [{"id": "R-1041", "plan": "Basic", "price": "$29.00", "charged": "$29.00", "times": "1"},
            {"id": "R-1042", "plan": "Team", "price": "$99.00", "charged": "$99.00", "times": "1"},
            {"id": "R-1043", "plan": "Basic", "price": "$29.00", "charged": "$29.00", "times": "2", "flag": "Charged twice", "bad": "times"},
            {"id": "R-1044", "plan": "Pro", "price": "$49.00", "charged": "$49.00", "times": "1"},
            {"id": "R-1045", "plan": "Team", "price": "$99.00", "charged": "$119.00", "times": "1", "flag": "Wrong amount", "bad": "charged"},
            {"id": "R-1046", "plan": "Pro", "price": "$49.00", "charged": "—", "times": "0", "flag": "Never attempted", "bad": "times"}]
def renewals(phase, **kw):
    return dict({"label": "A MADE-UP EXAMPLE  ·  THE BILLING SYSTEM, THE MORNING AFTER", "phase": phase,
                 "table_tag": "LAST NIGHT’S RENEWALS", "cols": ["RENEWAL", "PLAN", "PRICE", "CHARGED", "TIMES"], "rows": RENEWALS,
                 "totals": [["DUE", "$354.00"], ["CHARGED", "$354.00"]],
                 "banner": {"title": "Build passed", "sub": "all tests green"},
                 "checks_tag": "RIGHT, WRITTEN AS CHECKS",
                 "checks": [{"text": "None was\ncharged twice", "failed": 1}, {"text": "Each charge equals\nthe plan’s price", "failed": 1},
                            {"text": "Every renewal due\nwas attempted", "failed": 1}]}, **kw)
sc("04a_green", "Take our made-up example: the subscription-billing system from lesson one. Here are last night's renewals. "
   "And the build is green. [pause] But no test ever looked at this table. So was last night right? The green can't say.",
   "renewals", renewals("green", ask="So was last\nnight right?", answer="The green\ncan’t say.", ask_at=0.7, answer_at=0.84),
   "THE REAL CHECK", group="renewals")
sc("04b_define", "So before the work starts, write down what right means, in the business's words. "
   "Every renewal charged the right amount, exactly once. Then split that into checks an agent can run. "
   "One: none was charged twice. Two: each charge equals the plan's price. Three: every renewal that was due was attempted.",
   "renewals", renewals("define", checks_at=[0.58, 0.7, 0.82],
                        caption="Right: every renewal charged the right amount, exactly once.", caption_at=0.2),
   "THE REAL CHECK", group="renewals")
sc("04c_run", "Now run them, on last night's real renewals. [pause] One was charged twice. One, the wrong amount. One was never attempted. [pause] "
   "And look at the totals: they match. Three wrong renewals, inside a sum that's exactly right. "
   "So check every renewal, not just the total.",
   "renewals", renewals("run", sweep=[0.12, 0.46], totals_note="the totals match", totals_at=0.56,
                        caption="Check every renewal, not just the total.", caption_tone="amber", caption_at=0.84),
   "THE REAL CHECK", group="renewals")

sc("05_twice", "That one sentence does double duty. You write the check once, and run it twice. "
   "Before a change ships, on sample renewals, in the pipeline. And after every nightly run, on the real ones. [pause] "
   "Add a target for time, too. A service level objective, an S.L.O.: say, ninety-nine point nine percent of renewals due today, attempted by six A.M. "
   "Now an agent can run all of it, without asking anyone what good looks like.",
   "graph", {"label": "WRITE THE CHECK ONCE  ·  RUN IT TWICE",
             "nodes": [{"id": "check", "text": "Every renewal:\nthe right amount,\nexactly once", "x": 470, "y": 500, "w": 520, "h": 230,
                        "size": 38, "tone": "accent", "tag": "THE CHECK, WRITTEN ONCE", "at": 0.04},
                       {"id": "pre", "text": "Before a change ships", "sub": "on sample renewals, in the pipeline", "x": 1330, "y": 380,
                        "w": 760, "h": 130, "size": 34, "sub_size": 25, "tag": "RUN IT", "at": 0.22},
                       {"id": "post", "text": "After every nightly run", "sub": "on the real renewals", "x": 1330, "y": 590,
                        "w": 760, "h": 130, "size": 34, "sub_size": 25, "tag": "RUN IT AGAIN", "at": 0.34},
                       {"id": "slo", "text": "99.9% of renewals due today, attempted by 6 a.m.", "sub": "a service level objective (SLO), for example",
                        "x": 1330, "y": 800, "w": 760, "h": 130, "size": 29, "sub_size": 25, "tone": "amber",
                        "tag": "AND A TARGET FOR TIME", "at": 0.56}],
             "edges": [{"from": "check", "to": "pre", "tone": "accent"}, {"from": "check", "to": "post", "tone": "accent"}],
             "caption": "An agent can run all of it,\nwithout asking what\ngood looks like.", "caption_x": 210, "caption_y": 720,
             "caption_size": 38, "caption_at": 0.84},
   "RUN IT TWICE")

# ---- the record for one renewal, as a chain of steps; times and values are invented
STEPS = [("sched", "02:00:03", "Schedule", "due $29.00", None, 0.2), ("c1", "02:00:04", "Charge, attempt 1", "key A  ·  timeout", "amber", 0.42),
         ("c2", "02:00:36", "Charge, attempt 2", "key B  ·  charged", None, 0.5), ("inv", "02:00:37", "Invoice", "sent, $29.00", None, 0.56),
         ("rec", "06:10:00", "Reconcile", "processor: 2 charges", "amber", 0.62)]
sc("06_record", "The checks say that something is wrong. The record says why. So every step of every run leaves a line, "
   "in a shape that people and agents can both read. Here's the double charge. Attempt one: a timeout. Attempt two, with a new key: charged. "
   "Then reconcile, against the processor's own report: two charges. The first attempt had gone through. [pause] Nobody has to guess.",
   "graph", {"label": "WATCH EVERY RUN  ·  EVERY STEP LEAVES A RECORD  ·  A MADE-UP EXAMPLE",
             "bands": [{"x": 130, "y": 300, "w": 1660, "h": 250, "label": "THE RECORD FOR RENEWAL R-1043, STEP BY STEP", "at": 0.12}],
             "nodes": [{"id": i, "tag": tm, "text": name, "sub": sub, "tone": tone, "x": 310 + 325 * k, "y": 450, "w": 296, "h": 120,
                        "size": 27, "sub_size": 23, "at": at} for k, (i, tm, name, sub, tone, at) in enumerate(STEPS)]
                      + [{"id": "line", "tag": "ONE LINE PER STEP  ·  PEOPLE AND AGENTS CAN BOTH READ IT", "text": "The record, as written",
                          "sub": "step=charge  renewal=R-1043  attempt=2  key=B  result=charged", "sub_mono": True, "sub_size": 30, "size": 26,
                          "x": 960, "y": 690, "w": 1660, "h": 130, "at": 0.3}],
             "edges": [["sched", "c1"], ["c1", "c2"], ["c2", "inv"], ["inv", "rec"]],
             "caption": "A timeout, then a retry with a new key. The first attempt had gone through.", "caption_tone": "amber",
             "caption_x": 130, "caption_y": 810, "caption_size": 42, "caption_at": 0.68,
             "foot": "THE CHECKS SAY SOMETHING IS WRONG  ·  THE RECORD SAYS WHY", "foot_y": 900},
   "WATCH EVERY RUN")

def loop(static, note, caption, **kw):
    return dict({"label": "FEED IT BACK  ·  EACH RUN IMPROVES THE NEXT", "static": static,
                 "nodes": [{"id": "brief", "text": "The brief\nand the checks", "x": 400, "y": 390, "w": 420, "h": 130, "size": 32, "at": 0.03},
                           {"id": "run", "text": "The run", "x": 1520, "y": 390, "w": 420, "h": 130, "size": 34, "at": 0.08},
                           {"id": "record", "text": "The record", "sub": "what happened, step by step", "x": 1520, "y": 690, "w": 420, "h": 130,
                            "size": 34, "sub_size": 23, "at": 0.13},
                           {"id": "review", "text": "The review", "sub": "what went wrong, what was fixed", "x": 400, "y": 690, "w": 420,
                            "h": 130, "size": 34, "sub_size": 23, "at": 0.18},
                           dict(note, id="note", x=960, y=890, w=1540, h=92, size=31)],
                 "edges": [["brief", "run"], ["run", "record"], ["record", "review"], ["review", "brief"]],
                 "path": ["brief", "run", "record", "review", "brief"], "path_at": 0.26, "runner_speed": 0.16,
                 "caption": caption, "caption_x": 660, "caption_y": 470, "caption_size": 40}, **kw)
sc("07a_loop", "First, put last night right, with a person approving, as in lesson five. Then close the loop. "
   "Every miss goes back into the brief, and the checks. The double charge becomes a new line in the brief: a retry must reuse the same key. "
   "That's an idempotency key; more in lesson eight. And a new test: the processor times out. [pause] "
   "So each run makes the next one better.",
   "graph", loop(False, {"text": "New in the brief: a retry reuses the same key.   New test: the processor times out.", "tone": "accent", "at": 0.42},
                 "Every miss goes back\ninto the brief\nand the checks.", caption_at=0.24),
   "FEED IT BACK", group="loop")
sc("07b_limit", "And be honest about the limit. A check only catches what somebody thought to ask. "
   "So a person still reads a sample of real invoices. And whatever they find becomes the next check.",
   "graph", loop(True, {"text": "A person still reads a sample of real invoices", "tone": "amber", "held": True},
                 "A check only catches\nwhat somebody thought\nto ask.", path_static=True, caption_tone="amber", caption_at=0.04),
   "FEED IT BACK", group="loop")

sc("08_recap", "So, to recap. Green doesn't mean right. Define right first, in the business's words. "
   "Check before you ship, and after every run. Make every step leave a record. And feed every miss back in.",
   "rule", {"headline": "Green doesn’t mean right",
            "items": ["Define right first, in the business’s words", "Check before you ship, and after every run",
                      "Every step leaves a record", "Feed every miss back in"]}, "RECAP")

sc("09_rule", "Which gives us rule six, for your agents. Before you build, write down what right means, as checks you can run, "
   "in the business's words. Run them before a change ships, and after every run. Leave a record at every step. "
   "When a check fails, stop and tell a person. And feed every miss back into the brief and the checks.",
   "rule_card", {"kicker": "RULE 6  ·  FOR YOUR AGENTS", "size": 54,
                 "lines": [{"text": "Before you build, write down what right means,"},
                           {"text": "as checks you can run, in the business’s words.", "tone": "accent"},
                           {"text": "Run them before a change ships, and after every run.", "tone": "accent"},
                           {"text": "Leave a record at every step."},
                           {"text": "When a check fails, stop and tell a person.", "tone": "accent"},
                           {"text": "Feed every miss back into the brief and the checks."}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("10_ask", "Now, your turn. Pick one job your system runs every day. Ask your A.I.: what would have to be true for last night's run to be right? "
   "Write it as three read-only checks I can run on the real data. [pause] Then run one.",
   "statement", {"headline": "Your turn. Pick one job your system\nruns every day. Ask your AI:\n“What would have to be true for last\n"
                             "night’s run to be right? Write it as three\nread-only checks on the real data.”\nThen run one.", "size": 68},
   "YOUR TURN")

sc("11_close", "Once a job has a brief, its checks, and a record of every run, it's ready to be reused. "
   "That's next: skills as building blocks. See you in lesson seven.",
   "outro", {"headline": "See you in\nlesson seven.", "sub": "Software Engineering 201"})

spec = {"id": "se201-06-quality", "title": "SE201 Lesson 6: Quality, feedback, and observability",
        "output": "06-quality-feedback-and-observability/SE201_06_Quality-Feedback-And-Observability_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
def spoken(s): return re.sub(r"<[^>]+>|\[pause\]", " ", s["text"])
words = sum(len(spoken(s).split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s")
for s in S:
    print(f"  {s['id']:<14} {s['visual']:<14} {s['chapter']:<22} {len(spoken(s).split()):>3} w")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))
# (The build-machine copy also asserts that a private company name never appears; that one line is left out of this public copy.)
assert set(re.findall(r"\[[a-z]+\]|</?[a-z]+>", " ".join(s["text"] for s in S))) <= {"[pause]", "<emphasis>", "</emphasis>", "<slow>", "</slow>"}

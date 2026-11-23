#!/usr/bin/env python3
"""Generates scripts/se201-08-pipelines.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 8: Routines, Pipelines, and Integration.

Public lesson (clarkhuang.github.io). Worked example: the series' made-up subscription-billing system (introduced in
lesson 1 as "a made-up example") and its nightly billing run: renewals due -> charge -> invoice -> accounting export ->
reconcile. It is called made up aloud and on screen, and its numbers are labelled made up. Nothing here describes
sticky.io or any real company; no internal systems, numbers, incidents or anecdotes; no other people's names.
Every factual claim and its source is in se201-08-facts.md. Industry history is the same approximate history lesson 1
used (overnight batch files and EDI, then web services, then an API for everything, now agents calling tools).

Uses the pipeline layout in se201_layouts_58b.py, plus quiz, graph, rule, rule_card, statement, outro.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-08-pipelines.json
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. Lesson eight. [pause] Routines, pipelines, and integration.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 8", "headline": "Routines, pipelines,\nand integration.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Quick question. It's two in the morning. A job charges a customer's card. The payment goes through, "
   "but the connection drops before the answer comes back. So the job tries again. [pause] What happens? "
   "Nothing? The customer is charged twice? Or the processor catches it on its own? [pause] "
   "<emphasis>Quite possibly, charged twice.</emphasis> Some processors catch a quick duplicate, but don't count on it. Design the retry to be safe. That design is this lesson.",
   "quiz", {"question": "2 a.m. A charge goes through, but the answer\nnever comes back. The job tries again.",
            "options": ["Nothing: the retry is harmless", "The customer is charged twice", "The processor catches it on its own"],
            "answer": 1, "why": "Unless the\nretry was\ndesigned\nto be safe.", "options_at": 0.5, "reveal_at": 0.74},
   "THE QUESTION")

# ---- the same approximate history as lesson 1
sc("03_oldest", "Connecting systems is the oldest problem in this series. Thirty years ago: overnight batch files, and E.D.I. "
   "Then web services. Then an A.P.I. for everything. Now, agents calling tools. [pause] "
   "And every one of those is still running somewhere, often inside the same enterprise.",
   "graph", {"label": "INTEGRATION  ·  THE OLDEST PROBLEM IN THIS SERIES",
             "nodes": [{"id": "a", "text": "Batch files, EDI", "sub": "Overnight", "tag": "30 YEARS AGO", "x": 330, "y": 440, "w": 360, "h": 140, "size": 36, "sub_size": 25, "at": 0.3},
                       {"id": "b", "text": "Web services", "sub": "XML over HTTP", "tag": "20 YEARS AGO", "x": 750, "y": 440, "w": 360, "h": 140, "size": 36, "sub_size": 25, "at": 0.46},
                       {"id": "c", "text": "An API for everything", "sub": "REST and JSON", "tag": "10 YEARS AGO", "x": 1170, "y": 440, "w": 360, "h": 140, "size": 31, "sub_size": 25, "at": 0.54},
                       {"id": "d", "text": "Agents calling tools", "sub": "On top of those APIs", "tag": "NOW", "x": 1590, "y": 440, "w": 360, "h": 140, "size": 32, "sub_size": 25, "tone": "accent", "at": 0.64},
                       {"id": "sys", "text": "One enterprise, today: often several of these at once", "x": 960, "y": 700, "w": 1620, "h": 110, "size": 38,
                        "tone": "hi", "at": 0.84}],
             "edges": [["a", "sys"], ["b", "sys"], ["c", "sys"], ["d", "sys"]],
             "caption": "Every one of them is still running somewhere.", "caption_y": 810, "caption_at": 0.76, "caption_size": 46},
   "THE OLDEST PROBLEM")

sc("04_triggers", "A skill is one job, written down and tested, that runs when someone asks. But some work should start on its own. "
   "On a schedule: every night at two. On an event: a payment fails, or a file arrives. "
   "Or when the step before it finishes. [pause] Call a skill plus a trigger a routine. And routines, chained, make a pipeline.",
   "graph", {"label": "WORK THAT STARTS ON ITS OWN  ·  THREE KINDS OF TRIGGER",
             "bands": [{"x": 1150, "y": 420, "w": 650, "h": 220, "label": "A PIPELINE  ·  ROUTINES, CHAINED", "tone": "accent", "at": 0.88}],
             "nodes": [{"id": "t1", "text": "On a schedule", "sub": "Every night at two", "x": 350, "y": 370, "w": 440, "h": 116, "size": 34, "sub_size": 24, "at": 0.3},
                       {"id": "t2", "text": "On an event", "sub": "A payment fails · a file arrives", "x": 350, "y": 540, "w": 440, "h": 116, "size": 34, "sub_size": 24, "at": 0.44},
                       {"id": "t3", "text": "When the step before finishes", "x": 350, "y": 710, "w": 440, "h": 116, "size": 28, "at": 0.6},
                       {"id": "r", "text": "A routine", "sub": "A skill + a trigger", "x": 870, "y": 540, "w": 340, "h": 150, "size": 38, "sub_size": 25,
                        "tone": "accent", "at": 0.74},
                       {"id": "p1", "text": "Routine", "x": 1270, "y": 540, "w": 170, "h": 90, "size": 26, "at": 0.88},
                       {"id": "p2", "text": "Routine", "x": 1475, "y": 540, "w": 170, "h": 90, "size": 26, "at": 0.9},
                       {"id": "p3", "text": "Routine", "x": 1680, "y": 540, "w": 170, "h": 90, "size": 26, "at": 0.92}],
             "edges": [["t1", "r"], ["t2", "r"], ["t3", "r"], ["p1", "p2"], ["p2", "p3"]],
             "caption": "A skill + a trigger: a routine.  Routines, chained: a pipeline.", "caption_y": 850, "caption_at": 0.78, "caption_size": 44},
   "WORK THAT STARTS ITSELF")

# ---- the worked example: the made-up system's nightly billing run
STAGES = [{"name": "Find renewals\ndue", "at": 0.3},
          {"name": "Charge", "tag": "CALLS THE PROCESSOR", "tone": "amber", "at": 0.42},
          {"name": "Invoice", "at": 0.56},
          {"name": "Accounting\nexport", "tag": "LEAVES OUR SYSTEM", "tone": "amber", "at": 0.66},
          {"name": "Reconcile", "at": 0.78}]
HANDOFFS = ["renewals\ndue", "charge\nresults", "invoices", "export\nfile"]
RECORDS = [["1,000 due"], ["988 charged", "12 declined"], ["988 invoices"], ["988 rows sent"], ["Ledger matches", "the processor"]]
def pipe(**kw):
    return dict({"label": "A MADE-UP EXAMPLE  ·  THE NIGHTLY BILLING RUN", "trigger": "EVERY NIGHT AT 2:00", "stages": STAGES}, **kw)

sc("05a_run", "Here's one, in our made-up subscription-billing system: the nightly billing run. On a schedule, find the renewals due. "
   "Charge each one, through the payment processor. Write the invoices. Send the export to the accounting system. "
   "And last, reconcile: does our ledger match what the processor says it charged?",
   "pipeline", pipe(caption="Five steps, chained. The first starts on a schedule.",
                    caption_size=46, caption_at=0.86, caption_y=650),
   "A WORKED EXAMPLE", group="pipe")
sc("05b_handoffs", "Between every two steps, something crosses: the renewals due, the charge results, the invoices, the export file. "
   "Give each a clear, written format. Then any step can be rebuilt, or rerun, without touching the others.",
   "pipeline", pipe(hold=True, handoffs=HANDOFFS, handoffs_at=0.14, handoffs_step=0.09, handoffs_lit=True,
                    caption="A clear, written format at every hand-off.", caption_at=0.52, caption_y=650, caption_size=46),
   "A WORKED EXAMPLE", group="pipe")
sc("05c_records", "And every step leaves a record: what came in, what went out, what failed. A thousand renewals due. "
   "Nine hundred eighty-eight charged, twelve declined. Nine hundred eighty-eight invoices, and as many rows sent. "
   "The numbers are made up, but they have to add up. When they don't, the run stops there, and you know which step to open.",
   "pipeline", pipe(hold=True, handoffs=HANDOFFS, handoffs_held=True, records=RECORDS[:4] + [[]], records_at=0.2, records_step=0.12,
                    caption="Every step leaves a record. The counts have to add up.\nWhen they don’t, the run stops there.",
                    caption_at=0.7, caption_y=800,
                    label="A MADE-UP EXAMPLE, MADE-UP NUMBERS  ·  THE NIGHTLY BILLING RUN"),
   "A WORKED EXAMPLE", group="pipe")

sc("05d_retry", "Back to two A.M. Partway through the charge step, the connection drops. One charge went out, and no answer came back. "
   "Did it go through? We don't know. [pause] So the retry has to be safe to run twice. Renewals already recorded as charged, it skips. "
   "Every other one, it sends with a key that never changes: this subscription, this billing period. "
   "If the processor has already seen that key, it returns the first result, instead of charging again. "
   "That's an idempotency key, and many payment processors support one.",
   "pipeline", pipe(hold=True, focus=1,
                    fail={"stage": 1, "title": "INSIDE THE CHARGE STEP  ·  EACH BLOCK IS ONE RENEWAL", "blocks": 10, "brk": 6,
                          "try_label": "First try", "retry_label": "Retry", "at": 0.03, "break_at": 0.1, "retry_at": 0.36, "key_at": 0.5,
                          "retry_end": 0.8, "skip_span": 0.25,
                          "note1": "Connection drops", "sub1": "One answer never came back",
                          "note2": "Each renewal charged once", "sub2": "Seen the key? Same answer back",
                          "key": "key = this subscription + this billing period", "key_note": "an idempotency key"},
                    caption="Safe to run twice: skip what’s recorded as charged; send the rest, each with its own key.",
                    caption_size=36, caption_at=0.84),
   "A WORKED EXAMPLE", group="pipe")

sc("05e_stop", "Last, reconcile compares our ledger with the processor's record. If they don't match, the pipeline doesn't guess, "
   "and doesn't fix the numbers itself. It keeps every record, and tells a person. [pause] Most of these steps are plain code. "
   "An agent earns its place where a step needs judgment, like working out why they don't match.",
   "pipeline", pipe(hold=True, focus=4, handoffs=HANDOFFS, handoffs_held=True, records=RECORDS, records_held=True, record_check=4,
                    alert={"stage": 4, "text": "Doesn’t match?\nDon’t guess. Keep every record.\nTell a person.", "at": 0.24, "w": 500, "y": 790},
                    caption="Most steps: plain code.\nAn agent: where a step needs judgment.", caption_at=0.62, caption_y=810, caption_size=40),
   "A WORKED EXAMPLE", group="pipe")

sc("06_partner", "The same thinking covers everything you don't control. Take a partner's nightly file. Check it first. "
   "Late: wait, then alert. Twice: recognize it, and skip it. Broken: set it aside, and tell a person. [pause] "
   "You can't count on anything arriving exactly once. So design for at least once, and make twice harmless.",
   "graph", {"label": "YOU DEPEND ON THINGS YOU DON’T CONTROL  ·  A PARTNER’S NIGHTLY FILE",
             "nodes": [{"id": "f", "text": "A partner’s\nnightly file", "tag": "NOT YOURS TO CONTROL", "tone": "amber", "x": 330, "y": 560, "w": 360, "h": 150, "size": 34, "at": 0.14},
                       {"id": "c", "text": "Check it first", "x": 800, "y": 560, "w": 380, "h": 150, "size": 36, "at": 0.24},
                       {"id": "o1", "text": "As expected: load it", "x": 1440, "y": 350, "w": 640, "h": 96, "size": 31, "tone": "accent", "at": 0.28},
                       {"id": "o2", "text": "Late: wait, then alert", "x": 1440, "y": 490, "w": 640, "h": 96, "size": 31, "at": 0.34},
                       {"id": "o3", "text": "Twice: recognize it, skip it", "x": 1440, "y": 630, "w": 640, "h": 96, "size": 31, "at": 0.44},
                       {"id": "o4", "text": "Broken: set it aside, tell a person", "x": 1440, "y": 770, "w": 640, "h": 96, "size": 31, "tone": "amber", "at": 0.54},
                       ],
             "edges": [["f", "c"], ["c", "o1"], ["c", "o2"], ["c", "o3"], ["c", "o4"]],
             "caption": "Design for at least once. Make twice harmless.", "caption_y": 880, "caption_at": 0.8, "caption_size": 46, "caption_tone": "accent"},
   "WHAT YOU DON’T CONTROL")

sc("07_recap", "So, to recap. Give every hand-off a clear format. Make every step leave a record that adds up. "
   "Make every step safe to run twice. And when the numbers don't match, stop, and tell a person.",
   "rule", {"headline": "Routines, pipelines, integration",
            "items": ["A clear format at every hand-off", "Every step leaves a record that adds up",
                      "Every step is safe to run twice", "Doesn’t match? Stop, and tell a person"]}, "RECAP")

sc("08_rule", "Which gives us rule eight, for your agents. Before any work runs on its own, write down four things. What starts it. "
   "What crosses at each hand-off. What record each step leaves. And what happens when a step fails, or runs twice. "
   "No answer? It isn't ready to run unattended.",
   "rule_card", {"kicker": "RULE 8  ·  FOR YOUR AGENTS", "size": 56,
                 "lines": [{"text": "Before any work runs on its own, write down:"},
                           {"text": "what starts it,", "tone": "accent"},
                           {"text": "what crosses at each hand-off,", "tone": "accent"},
                           {"text": "what record each step leaves,", "tone": "accent"},
                           {"text": "and what happens when a step fails, or runs twice.", "tone": "accent"},
                           {"text": "No answer? It isn’t ready to run unattended."}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("09_ask", "Now, your turn. Pick one job that already runs on its own: a nightly report, or a sync. Describe its steps to your A.I., and ask, for each step: "
   "what happens if it runs twice? And what record would prove it ran? [pause] The steps with no good answer are where to start.",
   "statement", {"headline": "Your turn. One job that runs on its own.\nAsk your AI, for each step:\nwhat happens if it runs twice?\nWhat record would prove it ran?", "size": 74},
   "YOUR TURN")

sc("10_close", "A pipeline that runs on its own is already operating the system. So whose name does it run under? What is it allowed to touch? "
   "And who can see what it did? [pause] That's next: agents that operate enterprise systems. See you in lesson nine.",
   "outro", {"headline": "See you in\nlesson nine.", "sub": "Software Engineering 201"})

spec = {"id": "se201-08-pipelines", "title": "SE201 Lesson 8: Routines, pipelines, and integration",
        "output": "08-routines-pipelines-and-integration/SE201_08_Routines-Pipelines-And-Integration_public.mp4",
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

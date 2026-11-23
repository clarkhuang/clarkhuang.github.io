#!/usr/bin/env python3
"""Generates scripts/se201-10-capstone.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 10 (capstone): One Feature, End to End.

Public lesson (clarkhuang.github.io). It builds ONE small feature of the series' made-up subscription-billing system
(introduced in lesson 1 as "a made-up example"): a customer switches from a monthly plan to an annual plan partway
through the month. The lesson walks that feature through lessons 1 to 9 in order on one diagram, the build map, which
is held on screen and lights up lesson by lesson: plan it (1 to 7), build it, run it (8), operate it (9), and what
still holds (the four constants of lesson 1).

The example is called made up aloud and on screen, and its numbers are made up: $30 for a 30-day month, day 10,
20 days unused = $20 credit, annual $300, so $280 before tax (quote Q-1). Nothing here describes a real company or
system; no internal systems, numbers, incidents or anecdotes; no other people's names. Lesson 9 is an
outline, not a recording, so its ideas are referred to as "lesson nine's idea". Every claim and its source is in
se201-10-facts.md.

Uses the buildmap layout in se201_layouts_10.py, plus title, quiz, rule_card, statement, outro.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-10-capstone.json
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def spoken_text(text): return re.sub(r"<[^>]+>|\[pause\]", " ", text)
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)
def fr(text, phrase, shift=0.0):
    """how far into a scene's narration a phrase starts, as a fraction of its spoken words (keeps screen and voice in step)"""
    sp = spoken_text(text)
    i = sp.index(phrase)
    return round(min(0.97, max(0.0, len(sp[:i].split()) / len(sp.split()) + shift)), 3)

TITLE = "Capstone: One Feature, End to End"
SLUG = "10-capstone-one-feature-end-to-end"

sc("01_title", "Software engineering two oh one. Lesson ten. [pause] Capstone: one feature, end to end.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 10", "headline": "Capstone: one feature,\nend to end.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Picture a made-up billing system. A customer pays thirty dollars a month. Ten days in, they click: switch to annual. "
   "Three hundred a year. What do you charge them, today? [pause] Three hundred? Two eighty? Or: it depends? [pause] "
   "<emphasis>It depends.</emphasis> On a rule nobody has written down. And an agent will build either answer, without asking.",
   "quiz", {"question": "$30 a month. Ten days in, the customer clicks\n“Switch to annual”: $300 a year. Charge today?",
            "options": ["$300: the full annual price", "$280: credit the unused days", "It depends"],
            "answer": 2, "why": "On a rule\nnobody has\nwritten down.", "options_at": 0.5, "reveal_at": 0.7},
   "THE QUESTION")

# ---------------------------------------------------------------- the build map, held from here to the recap
MAP = {"right": "Every upgrade is charged the right amount, exactly once.",
       "files": ["billing/upgrade/", " SPEC.md", " AGENTS.md", " index.md"],
       "parts": [{"name": "Add the\nannual plan"}, {"name": "Calculate\nthe credit"}, {"name": "Show it,\nget a yes"}, {"name": "Charge it,\nswitch the plan"}],
       "quote": "The quote", "quote_sub": "its own node, one owner",
       "agents": ["AGENT A", "AGENT B", "AGENT C"], "plan_note": "NOT NEW",
       "merge": ["One merge point", "On staging:", "test the whole feature"],
       "gate": "Finance\nowner", "gate_sub": "Named in the repo", "gate_yes": "Says yes",
       "checks_tag": "CHECKS, BEFORE", "skill_tag": "A SKILL", "right_checks": "AS CHECKS"}
LABEL = "A MADE-UP EXAMPLE, MADE-UP NUMBERS  ·  ONE FEATURE: SWITCH TO ANNUAL, MID-MONTH"
def bm(**kw):
    return dict({"label": LABEL, "label_held": True, "map": MAP}, **kw)

T = ("So this last lesson builds that one feature, end to end, in our made-up subscription-billing system from lesson one. [pause] "
     "Here's the map we'll fill in. Each number is the lesson it comes from.")
sc("03_feature", T, "buildmap",
   bm(label_held=False, show=[],
      lower={"kind": "panel", "at": 0.1, "cols": [
          {"head": "A MADE-UP EXAMPLE  ·  OUR SUBSCRIPTION-BILLING SYSTEM", "lines": ["One feature, end to end:", "switch to annual, mid-month"], "size": 38, "w": 1.5,
           "at": fr(T, "builds that")},
          {"head": "THE MAP WE’LL FILL IN", "lines": ["Each number is the", "lesson it comes from"], "size": 34, "at": fr(T, "Each number")}]}),
   "ONE SMALL FEATURE", group="map")

T = ("What's scarce, lesson one said, is knowing it's right. So, say what right means: "
     "every upgrade is charged the right amount, exactly once. [pause] The amount is a person's call, so the agent asks. "
     "The finance owner's rule: credit the days paid for, and not used. Twenty days, twenty dollars. So, before tax, charge two eighty.")
sc("04_right", T, "buildmap",
   bm(show=["right"], lit=["right"], ats={"right": fr(T, "say what right", -0.04)},
      lower={"kind": "days", "frame_held": True, "at": 0.02,
             "head": "A PERSON’S CALL, SO THE AGENT ASKS  ·  $30 A MONTH, DAY 10 OF 30", "days": 30, "used": 10,
             "used_label": "10 DAYS USED", "free_label": "20 DAYS PAID FOR, NOT USED  =  $20 CREDIT",
             "rule": "The finance owner’s rule: credit the days paid for, and not used.",
             "used_at": fr(T, "The amount is"), "rule_at": fr(T, "The finance owner"), "free_at": fr(T, "Twenty days"),
             "sum": [{"label": "Annual plan", "amount": "$300", "at": fr(T, "So, before tax", -0.03)},
                     {"label": "Credit, unused days", "amount": "− $20", "at": fr(T, "So, before tax")},
                     {"label": "Charge today, before tax", "amount": "$280", "at": fr(T, "two eighty", -0.03)}]},
      caption="Until a person decides the rule, there is no right answer to build.", caption_at=fr(T, "So, before tax"), caption_size=40),
   "PLAN IT", group="map")

T = ("Now make it readable. The rule goes into a spec, in the repository, with an agents file, for how to work there, "
     "and an index, so an agent can find it. [pause] The spec is the source. Change it, and the build follows.")
sc("05_readable", T, "buildmap",
   bm(show=["right", "files"], lit=["files"], ats={"files": fr(T, "The rule goes", -0.03)}, file_step=0.11,
      lower={"kind": "panel", "frame_held": True, "at": 0.03, "cols": [
          {"head": "SPEC.md  ·  THE SOURCE", "mono": True, "size": 29, "w": 2.1, "at": fr(T, "The rule goes"),
           "lines": ["Credit the days paid for and not used.", "Quote = new price - credit, plus tax.", "Charge the quote, exactly once."]},
          {"head": "AGENTS.md", "lines": ["How to", "work there"], "size": 34, "at": fr(T, "with an agents")},
          {"head": "index.md", "lines": ["So an agent", "can find it"], "size": 34, "at": fr(T, "and an index")}]},
      caption="The spec is the source. Change it, and the build follows.", caption_at=fr(T, "The spec is")),
   "PLAN IT", group="map")

T = ("Next, the graph. Four parts. Add the annual plan. Calculate the credit. Show the amount, and get a yes. "
     "Charge it, and switch the plan. [pause] What crosses? One new thing: the quote. Its I.D., old plan, new plan, credit, amount due. "
     "Three parts share it, so it's its own node, with one owner.")
sc("06_graph", T, "buildmap",
   bm(show=["right", "files", "parts", "quote"], lit=["parts", "quote"],
      ats={"parts": fr(T, "Add the annual", -0.02), "quote": fr(T, "One new thing")}, part_step=0.105,
      lower={"kind": "panel", "frame_held": True, "at": 0.03, "cols": [
          {"head": "WHAT CROSSES?  ONE NEW THING: THE QUOTE", "w": 1.9, "size": 34, "at": fr(T, "What crosses"),
           "ats": [fr(T, "Its I.D."), fr(T, "Its I.D.") + 0.1],
           "lines": ["ID  ·  Old plan  ·  New plan  ·  Credit  ·  Amount due", "~Q-1  ·  Monthly  ·  Annual  ·  $20  ·  $280"]},
          {"head": "THREE PARTS SHARE IT", "lines": ["Its own node,", "with one owner"], "size": 34, "at": fr(T, "Three parts share")}]},
      caption="An arrow only where something crosses.", caption_at=fr(T, "What crosses")),
   "PLAN IT", group="map")

T = ("Then plan the integration, before anyone starts. The quote's format is the shared contract. "
     "Three parts are new work: three agents, each with its own brief, finish line, and check. "
     "And one merge point, on staging, where the whole feature is tested.")
sc("07_parallel", T, "buildmap",
   bm(show=["right", "files", "parts", "quote", "agents", "merge"], lit=["quote", "agents", "merge"],
      quote_sub="its format: the shared contract",
      ats={"agents": fr(T, "three agents"), "merge": fr(T, "And one merge")},
      lower={"kind": "panel", "frame_held": True, "at": 0.03, "cols": [
          {"head": "FIRST: THE SHARED CONTRACT", "lines": ["The quote’s format, written", "before anyone starts"], "size": 34, "tone": "accent", "at": fr(T, "The quote's format")},
          {"head": "THREE PARTS ARE NEW WORK: THREE AGENTS", "lines": ["Each with its own brief,", "finish line, and check"], "size": 34, "at": fr(T, "three agents")},
          {"head": "ONE MERGE POINT", "lines": ["On staging: the whole", "feature, tested"], "size": 34, "at": fr(T, "And one merge")}]},
      caption="Plan how the work comes back together, before it splits.", caption_at=0.88),
   "PLAN IT", group="map")

T = ("Who decides? It moves money, so a person does. The repository already says who: fees and prices, the finance owner. "
     "The agent that writes the change doesn't classify it, or approve it. "
     "It brings the change, the evidence, the risk, and the way back.")
sc("08_decide", T, "buildmap",
   bm(show=["right", "files", "parts", "quote", "agents", "merge", "gate"], lit=["gate"],
      ats={"gate": fr(T, "the finance owner", -0.05)},
      lower={"kind": "panel", "frame_held": True, "at": 0.03, "cols": [
          {"head": "DOES IT MOVE MONEY?", "lines": ["!Yes.", "So a person decides"], "size": 34, "at": fr(T, "It moves money"),
           "ats": [fr(T, "It moves money"), fr(T, "so a person")]},
          {"head": "THE REPOSITORY ALREADY SAYS WHO", "mono": True, "lines": ["fees and prices:", "  the finance owner"], "size": 29, "at": fr(T, "The repository")},
          {"head": "THE AGENT BRINGS", "lines": ["The change, the evidence,", "the risk, the way back", "~It doesn’t classify, or approve"], "size": 34, "at": fr(T, "The agent that"), "ats": [fr(T, "It brings"), fr(T, "the risk"), fr(T, "doesn't classify")]}]},
      caption="Money moves, so a named person decides.", caption_at=0.88),
   "PLAN IT", group="map")

T = ("Now turn right into checks an agent can run. No upgrade is charged twice. Each quote follows the rule, and each charge equals its quote. "
     "And the old monthly plan doesn't renew again. [pause] Write them once, run them twice: before it ships, on sample upgrades. "
     "And every night after, on the real ones.")
sc("09_checks", T, "buildmap",
   bm(show=["right", "files", "parts", "quote", "agents", "merge", "gate", "checks"], lit=["right", "checks"],
      ats={"checks": fr(T, "turn right")},
      lower={"kind": "panel", "frame_held": True, "at": 0.03, "cols": [
          {"head": "RIGHT, AS THREE CHECKS AN AGENT CAN RUN", "w": 1.3, "size": 33, "at": fr(T, "turn right"),
           "ats": [fr(T, "No upgrade"), fr(T, "Each quote follows"), fr(T, "And the old")],
           "lines": ["1   No upgrade is charged twice", "2   Each quote = the rule; each charge = its quote", "3   The old monthly plan doesn’t renew again"]},
          {"head": "RUN THEM TWICE", "size": 33, "at": fr(T, "Write them once"), "tone": "accent",
           "ats": [fr(T, "before it ships"), fr(T, "And every night")],
           "lines": ["Before it ships: on sample upgrades", "Every night after: on the real ones"]}]},
      caption="Write them once, run them twice.", caption_at=fr(T, "Write them once")),
   "PLAN IT", group="map")

T = ("One part isn't new. Adding a plan has come back often enough to be a skill: written down, and tested. "
     "So that part needs no new brief. An agent runs the skill.")
sc("10_skill", T, "buildmap",
   bm(show=["right", "files", "parts", "quote", "agents", "merge", "gate", "checks", "skill"], lit=["skill"],
      ats={"skill": fr(T, "to be a skill")},
      lower={"kind": "panel", "frame_held": True, "at": 0.03, "cols": [
          {"head": "ONE PART ISN’T NEW: ADDING A PLAN", "w": 1.2, "size": 34, "at": 0.04, "tone": "accent",
           "ats": [fr(T, "Adding a plan"), fr(T, "written down")],
           "lines": ["It has come back often enough to be a skill:", "written down, and tested"]},
          {"head": "THAT PART", "lines": ["Needs no new brief:", "an agent runs the skill"], "size": 34, "at": fr(T, "So that part")}]},
      caption="Reuse what recurs.", caption_at=0.85),
   "PLAN IT", group="map")

T = ("The plan is written, and a person has read it. Now, build. Four parts, at the same time. They meet early, at the merge point, "
     "and the whole feature runs on staging. The three checks pass, on sample upgrades. An engineer reviews the code. "
     "The finance owner says yes. [pause] And it ships.")
sc("11_go", T, "buildmap",
   bm(show=["right", "files", "parts", "quote", "agents", "merge", "gate", "checks", "skill"], lit=[], built="go",
      go={"parts": fr(T, "Four parts"), "parts_end": fr(T, "They meet"), "merge": fr(T, "at the merge"), "checks": fr(T, "The three checks", 0.05),
          "gate": fr(T, "says yes"), "ship": fr(T, "And it ships")},
      lower={"kind": "log", "frame_held": True, "at": 0.02, "head": "THE BUILD, AS IT RUNS", "per_col": 4, "rows": [
          {"text": "The plan is written, and a person has read it", "at": fr(T, "and a person")},
          {"text": "Four parts, at the same time", "at": fr(T, "They meet", -0.03)},
          {"text": "They meet early, at the merge point", "at": fr(T, "at the merge", 0.04)},
          {"text": "The whole feature runs on staging", "at": fr(T, "runs on staging")},
          {"text": "The three checks pass, on sample upgrades", "at": fr(T, "on sample upgrades")},
          {"text": "An engineer reviews the code", "at": fr(T, "reviews the code")},
          {"text": "The finance owner says yes", "at": fr(T, "says yes"), "tone": "accent"},
          {"text": "It ships", "at": fr(T, "And it ships"), "tone": "accent"}]}),
   "BUILD IT", group="map")

STAGES = [{"name": "Charge", "tone": "amber", "notes": ["!idempotency key = quote ID", "charged $280"]},
          {"name": "Switch\nthe plan", "notes": ["now annual", "monthly renewal off"]},
          {"name": "Invoice,\nledger", "notes": ["invoice written", "$280 in the ledger"]},
          {"name": "Email", "notes": ["receipt sent"]},
          {"name": "Reconcile", "apart": True, "trigger": "EVERY NIGHT", "notes": ["ledger = processor", "+the checks"]}]
OP = {"tag": "THE OPERATOR", "id": "id: billing-ops-agent",
      "lines": ["Its own identity", "Reads: the ledger, the processor’s report",
                "!Can’t move money, or change the ledger", "Every action is logged", "+Two charges? Flags it. A person refunds it."]}
def prod(T=None, held=False, **kw):
    st = [dict(s) for s in STAGES]
    if not held:
        for s, ph in zip(st, ["Charge, switch", "switch the plan", "invoice and ledger", "email", "A second trigger"]):
            s["at"] = fr(T, ph)
        st[0]["notes_at"] = fr(T, "an idempotency key")
        st[4]["notes_at"] = fr(T, "reconcile our ledger")
    return dict({"kind": "prod", "frame_held": True, "held": held, "tag": "A PIPELINE  ·  RUNS ON ITS OWN", "trigger": "WHEN THE CUSTOMER CONFIRMS",
                 "stages": st, "op": OP}, **kw)
ALL = ["right", "files", "parts", "quote", "agents", "merge", "gate", "checks", "skill", "prod"]

T = ("Now it runs on its own: a pipeline. The trigger is an event: the customer confirms the quote. Charge, switch the plan, invoice and ledger, email. "
     "Every step leaves a record. And the charge carries an idempotency key that never changes: this quote's I.D. So a double-click, "
     "or a retry, doesn't charge twice. [pause] "
     "A second trigger, every night: reconcile our ledger against the processor's record, and run the three checks.")
sc("12_run", T, "buildmap",
   bm(show=ALL, lit=["prod"], built=True, build_dim=0.55, build_dim_from=1.0,
      lower=prod(T, at=0.02, trigger_at=fr(T, "The trigger")),
      caption="Safe to run twice: same key, no second charge.", caption_at=fr(T, "So a double-click"), caption_size=40),
   "RUN IT", group="map")

T = ("Lesson nine's question: who operates it? An agent works that nightly reconcile. It gets its own identity, "
     "and the least access the job needs: it reads the ledger, and the processor's report. It can't move money, or change the ledger. "
     "Every action is logged. [pause] One night, an upgrade shows two charges: two browser tabs, two quotes, two keys. The agent flags it. "
     "A person refunds it. And the miss becomes a fourth check: one open quote per subscription.")
sc("13_operate", T, "buildmap",
   bm(show=ALL + ["op"], lit=["op"], built=True, build_dim=0.55, ats={"op": fr(T, "An agent works")},
      lower=prod(held=True, op=dict(OP, id_at=fr(T, "its own identity"),
                                    ats=[fr(T, "its own identity"), fr(T, "it reads"), fr(T, "It can't move"), fr(T, "Every action"), fr(T, "The agent flags")])),
      caption="The miss becomes a fourth check: one open quote per subscription.", caption_at=fr(T, "And the miss"), caption_size=40),
   "OPERATE IT", group="map")

T = ("Under all of it, the four constants from lesson one. The data model outlives the code: the plan, and the quote. "
     "Money has to add up: the invoice, the ledger, and the processor all say two eighty. "
     "You depend on things you don't control: the processor. And somebody understands the layer below: "
     "someone who can work that credit out by hand.")
CONSTS = [{"head": "The data model outlives the code", "text": "The plan, and the quote", "at": fr(T, "The data model")},
          {"head": "Money has to add up", "text": "Invoice = ledger = processor: $280", "at": fr(T, "Money has")},
          {"head": "Things you don’t control", "text": "The processor", "at": fr(T, "You depend")},
          {"head": "Somebody understands the layer below", "text": "Can work that credit out by hand", "at": fr(T, "And somebody")}]
sc("14_constants", T, "buildmap",
   bm(show=ALL + ["op"], lit=[], built=True, build_dim=1.0, build_dim_from=0.55,
      lower=prod(held=True), consts={"items": CONSTS}),
   "WHAT STILL HOLDS", group="map")

T = ("So that's the series, in one feature. Say what right means. Write it down. Draw the graph. Merge in one place. "
     "Put a person where it matters. Check it. Reuse what recurs. Let it run. And know who's running it.")
sc("15_recap", T, "buildmap",
   bm(show=ALL + ["op"], lit=[], built=True,
      pulse=[[["right"], fr(T, "Say what")], [["files"], fr(T, "Write it down")], [["parts", "quote"], fr(T, "Draw the graph")],
             [["agents", "merge"], fr(T, "Merge in one")], [["gate"], fr(T, "Put a person")], [["checks"], fr(T, "Check it")],
             [["skill"], fr(T, "Reuse what")], [["prod"], fr(T, "Let it run")], [["op"], fr(T, "And know")]],
      lower=prod(held=True), consts={"items": CONSTS, "held": True}),
   "RECAP", group="map")

sc("16_rule", "Which gives us rule ten, for your agents. Before you build a whole feature, write the plan in the repo, and show a person. "
   "What right means, as checks. The graph, and the shared contract. Who decides. What's already a skill. "
   "What runs on its own, and under whose identity. A blank line? Stop, and ask.",
   "rule_card", {"kicker": "RULE 10  ·  FOR YOUR AGENTS", "size": 54,
                 "lines": [{"text": "Before you build a whole feature, write the plan"},
                           {"text": "in the repo, and show a person:"},
                           {"text": "what right means, as checks,", "tone": "accent"},
                           {"text": "the graph, and the shared contract,", "tone": "accent"},
                           {"text": "who decides, and what’s already a skill,", "tone": "accent"},
                           {"text": "what runs on its own, and under whose identity.", "tone": "accent"},
                           {"text": "A blank line? Stop, and ask."}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("17_ask", "Now, your turn. Pick one small feature in a system you work on. Before any code, ask your A.I. to write that plan. [pause] "
   "Then find the line it guessed, when it should have asked.",
   "statement", {"headline": "Your turn. One small feature\nin a system you work on.\nBefore any code, ask your AI\nto write that plan.\n"
                             "Then find the line it guessed,\nwhen it should have asked.", "size": 74},
   "YOUR TURN")

sc("18_close", "Every box on that map is still one loop: plan, build, verify. Agents do more of the building now. "
   "You still own the outcome. [pause] That's software engineering two oh one: from one loop, to enterprise systems. Thanks for watching.",
   "outro", {"headline": "From one loop\nto enterprise systems.", "sub": "Software Engineering 201"})

spec = {"id": "se201-10-capstone", "title": "SE201 Lesson 10: " + TITLE,
        "output": SLUG + "/SE201_10_Capstone-One-Feature-End-To-End_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
def spoken(s): return spoken_text(s["text"])
words = sum(len(spoken(s).split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s =", f"{words / 2.6 / 60:.2f} min")
for s in S:
    print(f"  {s['id']:<14} {s['visual']:<10} {s['chapter']:<18} {len(spoken(s).split()):>3} w")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))
# (The build-machine copy also asserts that a private company name never appears; that one line is left out of this public copy.)
assert set(re.findall(r"\[[a-z]+\]|</?[a-z]+>", " ".join(s["text"] for s in S))) <= {"[pause]", "<emphasis>", "</emphasis>", "<slow>", "</slow>"}

#!/usr/bin/env python3
"""Generates scripts/se201-05-governance.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 5: Governance: Where People Decide.

Public lesson (clarkhuang.github.io). Every factual claim, and where it comes from, is in se201-05-facts.md.
  - about Clark: nothing new is claimed. The billing system is "our made-up example ... from lesson one"; the roles
    (finance owner, ledger owner, support lead), the late fee, the refund limit and every row on screen are invented
    for the illustration and say nothing about sticky.io or any real company.
  - industry history, kept approximate and hedged ("typically", "more and more"): change boards signing off releases
    in the 1990s; peer code review spreading in the 2000s; pull requests and approval steps in automated pipelines by
    the mid-2010s. A code owners file is a real feature of the common code hosts. "Whoever prepares a payment doesn't
    approve it" is the accounting control usually called separation (segregation) of duties.
  - the four questions (money, customer data, hard to undo, judgment call), the decision request and "start strict,
    release by kind" are teaching ideas written by the scriptwriter, presented as a rule of thumb, not as Clark's quote.

Uses the gates and decision_card layouts in se201_layouts_58a.py, plus eras, perm_table and dial.
Round 1 draft kept as make_se201_05_governance.round1.py in the work folder.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-05-governance.json
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. Lesson five. [pause] Governance: where people decide.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 5", "headline": "Governance:\nwhere people decide.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Picture this. Overnight, your agents wrote forty changes to a billing system. All pass their tests. "
   "One changes what customers are charged. Who catches it? [pause] The tests? A person, reading all forty? "
   "Or a person, at a stop built for it? [pause] <emphasis>A stop built for it.</emphasis> "
   "Tests can't say whether you wanted the change. And nobody reads forty carefully.",
   "quiz", {"question": "Forty changes overnight, all green. One changes\nwhat customers are charged. Who catches it?",
            "options": ["The tests: they all passed", "A person, reading all forty", "A person, at a stop built for it"],
            "answer": 2, "why": "Tests can’t say\nwhether you\nwanted the\nchange.", "options_at": 0.42, "reveal_at": 0.66},
   "THE QUESTION")

# ---- history, approximate and hedged in the narration ("typically", "more and more")
ERAS = [
 {"year": "1996", "ago": "30 YEARS AGO", "scarce_head": "THE YES", "scarce": "A change board",
  "rows": [["WHO SAID YES", "A change board"], ["TO WHAT", "A whole release"], ["HOW OFTEN", "A few times a year"],
           ["WHO WROTE IT", "People"]]},
 {"year": "2006", "ago": "20 YEARS AGO", "scarce_head": "THE YES", "scarce": "Code review",
  "rows": [["WHO SAID YES", "A teammate"], ["TO WHAT", "The code, before\nit went in"], ["HOW OFTEN", "More and more\nchanges"],
           ["WHO WROTE IT", "People"]]},
 {"year": "2016", "ago": "10 YEARS AGO", "scarce_head": "THE YES", "scarce": "A pipeline approval",
  "rows": [["WHO SAID YES", "A reviewer"], ["TO WHAT", "A pull request,\nbefore it merges"], ["HOW OFTEN", "Most changes"],
           ["WHO WROTE IT", "People"]]},
 {"year": "Now", "ago": "AGENTS DO THE BUILDING", "scarce_head": "THE YES", "scarce": "Has to be designed",
  "rows": [["WHO WRITES IT", "Agents, more and more"], ["HOW FAST", "Faster than anyone\ncan read it all"],
           ["SO THE YES", "Can’t just be\ninherited"]]},
]
def eras(n): return {"label": "EVERY ERA HAD A PLACE WHERE A PERSON SAID YES", "eras": ERAS, "upto": n}
sc("03a_board", "Every era had a place where a person said yes. Thirty years ago, typically, a change board, signing off a whole release, a few times a year.",
   "eras", eras(1), "EVERY ERA HAD A YES", group="eras")
sc("03b_review", "Twenty years ago, more and more, a teammate, reviewing the code before it went in.",
   "eras", eras(2), "EVERY ERA HAD A YES", group="eras")
sc("03c_pipeline", "Ten years ago, an approval step in an automated pipeline: a pull request a reviewer approves, before it merges.",
   "eras", eras(3), "EVERY ERA HAD A YES", group="eras")
sc("03d_now", "Each was sized for people writing the code. [pause] Now agents write changes faster than anyone can read them all. "
   "So that place can't just be inherited. It has to be <emphasis>designed</emphasis>.",
   "eras", eras(4), "EVERY ERA HAD A YES", group="eras")

sc("04_tests", "So where does a person decide? A good rule of thumb is four questions. Does it move money? Does it touch customer data? "
   "Is it hard to undo? Is it a judgment call that no check can make? [pause] One yes, and a person decides. "
   "Four no's, and that kind of change can ship on its checks.",
   "gates", {"label": "WHERE DOES A PERSON DECIDE?  ·  A RULE OF THUMB: FOUR QUESTIONS", "intro": True,
             "tests": [{"q": "Does it\nmove money?"}, {"q": "Does it touch\ncustomer data?"},
                       {"q": "Is it hard\nto undo?"}, {"q": "Is it a\njudgment call?"}], "card_h": 300,
             "tests_at": [0.25, 0.34, 0.44, 0.53],
             "verdicts": [{"text": "One yes: a person decides.", "tone": "amber", "at": 0.74},
                          {"text": "Four no’s: that kind of change can ship on its checks.", "tone": "accent", "at": 0.86}]},
   "FOUR QUESTIONS")

# ---- the worked example: invented changes to the made-up billing system; the roles are invented too
ROWS = [{"change": "Fix a typo on an internal admin screen", "note": "four no’s"},
        {"change": "Add a missing test for renewals", "note": "four no’s"},
        {"change": "Change how a late fee is calculated", "gate": {"why": "MOVES MONEY", "who": "Finance owner"}, "hits": [0]},
        {"change": "Migrate the ledger to a new schema", "gate": {"why": "MONEY  ·  HARD TO UNDO", "who": "Ledger owner"}, "hits": [0, 2]},
        {"change": "Send customer emails to a new partner", "gate": {"why": "CUSTOMER DATA", "who": "Data owner"}, "hits": [1],
         "result": "Sent after a yes"},
        {"change": "Refund a customer, over the limit", "gate": {"why": "MONEY  ·  JUDGMENT", "who": "Support lead"}, "hits": [0, 3],
         "result": "Paid after a yes"}]
def gates(new_from, upto, ats, **kw):
    rows = [dict(r) for r in ROWS]
    for i, a in zip(range(new_from, upto), ats): rows[i]["at"] = a
    return dict({"label": "A MADE-UP EXAMPLE  ·  SIX THINGS AN AGENT DRAFTS FOR THE BILLING SYSTEM",
                 "tests": ["moves money", "touches customer data", "is hard to undo", "needs a judgment call"],
                 "rows": rows, "new_from": new_from, "upto": upto, "row_h": 90}, **kw)
sc("05a_free", "Take our made-up example: the subscription-billing system from lesson one. Overnight, an agent drafts six things. "
   "Fix a typo on an internal admin screen. Add a missing test for renewals. Four no's, both times. They ship on their checks, and nobody waits.",
   "gates", gates(0, 2, [0.42, 0.57], caption="Four no’s: nobody waits.", caption_tone="accent", caption_at=0.8),
   "A WORKED EXAMPLE", group="gates")
sc("05b_stops", "Change how a late fee is calculated. That moves money: the finance owner decides. [pause] "
   "Migrate the ledger. Money again, and hard to undo: the ledger's owner decides. [pause] "
   "Send customer emails to a new partner. Customer data: the data owner decides.",
   "gates", gates(2, 5, [0.02, 0.34, 0.66], caption="One yes: it stops for a named person.", caption_tone="amber", caption_at=0.2),
   "A WORKED EXAMPLE", group="gates")
sc("05c_refund", "And it isn't only code. A refund over the limit: the agent prepares it, a support lead approves it. "
   "Under the limit, a person already decided, when they set it. [pause] Six pieces of work. Four stops. Two never waited.",
   "gates", gates(5, 6, [0.04], caption="Six pieces of work. Four stops. Two never waited.", caption_at=0.72),
   "A WORKED EXAMPLE", group="gates")

sc("06_packet", "A stop only works if a person can clear it quickly. So the agent doesn't hand over a wall of diff and ask, okay? "
   "It prepares the decision. What changes. Why. The evidence, from the pipeline: last month's invoices, recomputed, old against new. "
   "The risk. And the way back. [pause] Now the finance owner decides about the fee. And an engineer still reviews the code that moves money.",
   "decision_card", {"label": "MAKE THE STOP QUICK  ·  THE AGENT PREPARES THE DECISION",
                     "left": {"tag": "THE WHOLE DIFF", "foot": "A wall of diff.\n“Okay?”"},
                     "card": {"tag": "DECISION REQUEST  ·  A MADE-UP EXAMPLE", "title": "Change how the late fee is calculated",
                              "fields": [["WHAT CHANGES", "A flat late fee becomes a percent of the invoice"],
                                         ["WHY", "Finance asked for it; the spec is linked"],
                                         ["THE EVIDENCE", "From the pipeline: last month’s invoices,\nrecomputed, old against new"],
                                         ["THE RISK", "Some customers pay more; they must be told first"],
                                         ["THE WAY BACK", "Restore the flat fee; credit anyone already charged"]],
                              "who": "The finance owner decides", "buttons": ["Approve", "Send back"]},
                     "card_at": 0.32, "fields_at": [0.4, 0.44, 0.48, 0.68, 0.72], "approve_at": 0.84,
                     "caption": "A person decides the fee. An engineer still reviews the code.", "caption_at": 0.86},
   "MAKE THE STOP QUICK")

sc("07_written", "Then write it down: who approves what, in a file in the repository. Fees and prices: the finance owner. "
   "The ledger: its owner. The checks, the pipeline, and this file itself: always a person. "
   "Anything the list doesn't cover: stop and ask. [pause] And the pipeline enforces it, by what a change touches. "
   "The agent that wrote a change doesn't classify it, or approve it. "
   "An old idea from accounting: whoever prepares a payment doesn't approve it.",
   "perm_table", {"label": "WHO APPROVES WHAT  ·  A FILE IN THE REPOSITORY  ·  A MADE-UP EXAMPLE",
                  "cols": ["ON ITS CHECKS", "A PERSON SAYS YES"],
                  "rows": [{"label": "Internal screens, docs, added tests", "marks": [True, False]},
                           {"label": "Fees and prices  ·  finance owner", "marks": [False, True]},
                           {"label": "The ledger, data migrations  ·  ledger owner", "marks": [False, True]},
                           {"label": "The checks, the pipeline, this file  ·  always a person", "marks": [False, True]},
                           {"label": "Anything this list doesn’t cover  ·  stop and ask", "marks": [False, True]}],
                  "punch": "Enforced by the pipeline: the author never classifies or approves."},
   "WRITE IT DOWN")

STOPS = [{"pos": 0.12, "tag": "A PERSON ON EVERYTHING", "title": "People become\nthe bottleneck",
          "sub": "And yes turns into\na rubber stamp."},
         {"pos": 0.88, "tag": "A PERSON ON NOTHING", "title": "Fast, until money\nmoves unapproved",
          "sub": "Nobody decided.\nIt just shipped."},
         {"pos": 0.5, "tone": "accent", "tag": "START STRICT, THEN RELEASE", "title": "One kind of change\nat a time",
          "sub": "As its checks earn trust.\nRequired reviews stay."}]
def dial(n): return {"label": "HOW MANY STOPS?  ·  WHAT IT COSTS", "left_end": "STOP EVERYTHING", "right_end": "STOP NOTHING",
                     "stops": STOPS, "upto": n}
sc("08a_all", "Stops cost something. A person on everything: people become the bottleneck, and yes turns into a rubber stamp.",
   "dial", dial(1), "WHAT IT COSTS", group="dial")
sc("08b_none", "A person on nothing: fast, until money moves unapproved.",
   "dial", dial(2), "WHAT IT COSTS", group="dial")
sc("08c_few", "So start strict, like lesson two: a person on every change. Then release one kind at a time, as its checks earn trust. "
   "And where an audit requires a review, that review stays.",
   "dial", dial(3), "WHAT IT COSTS", group="dial")

sc("09_recap", "So, to recap. Design where people decide. Make every stop quick to clear. And let the rest ship on its checks, one released kind at a time.",
   "rule", {"headline": "Design where people decide",
            "items": ["Money, customer data, hard to undo, judgment:\u00a0a person", "Make every stop quick to clear",
                      "The rest ships on its checks, one released kind at a time"]}, "RECAP")

sc("10_rule", "Which gives us rule five, for your agents. Before a change ships, find out who decides. "
   "Money, customer data, hard to undo, or a judgment call: stop for the person named in the repo, "
   "and bring the change, the evidence, the risk, and the way back. Not on the list: stop and ask. "
   "Ship on checks alone only what a person has released.",
   "rule_card", {"kicker": "RULE 5  ·  FOR YOUR AGENTS", "size": 54,
                 "lines": [{"text": "Before a change ships, find out who decides."},
                           {"text": "Money, customer data, hard to undo, judgment:", "tone": "accent"},
                           {"text": "stop for the person named in the repo."},
                           {"text": "Bring the change, the evidence, the risk, the way back."},
                           {"text": "Not on the list? Stop and ask.", "tone": "accent"},
                           {"text": "Ship on checks alone only what a person released.", "tone": "accent"}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("11_ask", "Now, your turn. Give your A.I. the last ten changes to a system you run, and the four questions. "
   "Ask it: which of these needed a person? Which could have shipped on checks alone? [pause] Then see where you disagree.",
   "statement", {"headline": "Your turn. Give your AI the last ten\nchanges to a system you run, and\nthe four questions. Ask it:\n"
                             "“Which needed a person? Which could\nship on checks alone?”\nThen see where you disagree.", "size": 70}, "YOUR TURN")

sc("12_close", "Ships on its checks. That phrase is carrying a lot. So how good are your checks, really? "
   "That's next: quality, feedback, and observability. See you in lesson six.",
   "outro", {"headline": "See you in\nlesson six.", "sub": "Software Engineering 201"})

spec = {"id": "se201-05-governance", "title": "SE201 Lesson 5: Governance: where people decide",
        "output": "05-governance-where-people-decide/SE201_05_Governance-Where-People-Decide_public.mp4",
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

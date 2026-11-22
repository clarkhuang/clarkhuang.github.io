#!/usr/bin/env python3
"""Generates scripts/se201-03-parallel.json
Software Engineering 201: From Loop to Enterprise Systems. Lesson 3: Parallel Agents, One Integration.

Public lesson (clarkhuang.github.io). Worked example = Software Engineering 101, lessons 3, 4 and 5, built at the
same time and brought back together through one content file, one generator, one site check and the staging pull
request. Every claim about it is listed, with where to check it, in se201-03-facts.md.
The "picture a team" scene is a generic illustration, not an account of any real team or company.
No company-internal systems, no invented anecdotes, no other people's names.

Uses the lanes layout in se101_layouts6.py.
Render with:  SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-03-parallel.json
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = []
def sc(id, text, visual, data, chapter="", group=None):
    s = {"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data}
    if group: s["group"] = group
    S.append(s)

sc("01_title", "Software engineering two oh one. Lesson three. [pause] Parallel agents, one integration.",
   "title", {"kicker": "SOFTWARE ENGINEERING 201  ·  LESSON 3", "headline": "Parallel agents,\none integration.",
             "sub": "From loop to enterprise systems  •  clarkhuang.github.io"})

sc("02_quiz", "Quick question. Three agents each build one part of a system. All three say, done. All three pass their own checks. "
   "Is the system done? [pause] Yes? Almost? Or does nobody know yet? [pause] "
   "<emphasis>Nobody knows yet.</emphasis> Each check proves one part works alone. Not one of them has seen the parts together.",
   "quiz", {"question": "Three agents. Three parts. Every part\npasses its own check. Is the system done?",
            "options": ["Yes: every check passed", "Almost: just merge it", "Nobody knows yet"],
            "answer": 2, "why": "No check has\nseen the parts\ntogether.", "options_at": 0.44, "reveal_at": 0.62},
   "THE QUESTION")

# ---- a generic picture, not any real team
sc("03_broken", "Picture a team that splits one feature across three agents. One builds the screen. One builds the service behind it. One changes the database. "
   "Each part gets finished, and each part is correct on its own. [pause] Then the parts meet. "
   "The screen asks for a field the service never sends. Two of the agents edited the same file. "
   "And nobody finds out until the very end, when it costs the most to fix.",
   "lanes", {"label": "PICTURE A TEAM  ·  ONE FEATURE, THREE AGENTS, NO PLAN FOR THE MERGE",
             "contract": {"text": "Nothing agreed\nup front", "tone": "ghost", "size": 28},
             "lanes": [{"name": "The screen", "sub": "passes its check", "frac": 0.55},
                       {"name": "The service", "sub": "passes its check", "frac": 0.8},
                       {"name": "The database", "sub": "passes its check", "frac": 1.0}],
             "merge": {"tag": "AT THE VERY END", "text": "The parts\ndon’t fit", "tone": "amber", "size": 32, "at": 0.55},
             "run": 0.34, "caption": "Every part passed. The system didn’t.", "caption_tone": "amber", "caption_at": 0.8},
   "WHAT GOES WRONG")

sc("04_first", "Parallel work is only fast if it comes back together cleanly. So plan the integration <emphasis>first</emphasis>. Before any agent starts.",
   "statement", {"headline": "Plan the integration first.\nBefore any agent starts.", "size": 100}, "PLAN THE INTEGRATION FIRST")

PLAN = {"label": "THE PLAN FOR COMING BACK TOGETHER",
        "contract": {"tag": "1  ·  CONTRACT", "text": "Interfaces\nFormats, names\nWho owns\nwhich files", "size": 28},
        "lanes": [{"name": "Agent A", "sub": "own brief · own check", "frac": 0.6},
                  {"name": "Agent B", "sub": "own brief · own check", "frac": 1.0},
                  {"name": "Agent C", "sub": "own brief · own check", "frac": 0.8}],
        "merge": {"tag": "2  ·  MERGE POINT", "text": "One place\nthe parts\nmeet", "size": 30},
        "test": {"tag": "3  ·  WHOLE SYSTEM", "text": "Test it\nrunning\nas one", "size": 30},
        "run": 0.3, "caption_now": True}
sc("05a_contract", "Three things. First, a shared contract. Write down what crosses between the parts: the interfaces, the formats, the names, and who owns which files. "
   "At enterprise scale, that's an A.P.I., or a schema. It can be one page. But it has to exist before the work starts. "
   "And when it has to change, change it in one place, where every agent sees it.",
   "lanes", dict(PLAN, idle=True, focus="contract", caption="First: write down what crosses, before the work starts."),
   "PLAN THE INTEGRATION FIRST", group="plan")
sc("05b_agents", "Then every agent gets its own brief, its own finish line, and its own check. And part of that check is: does it match the contract?",
   "lanes", dict(PLAN, hold_stages=True, focus="lanes", run=0.45, caption="Each agent: its own brief, its own finish line, its own check."),
   "PLAN THE INTEGRATION FIRST", group="plan")
sc("05c_merge","Second, one merge point. One place where the parts come together. So when something doesn't fit, there's exactly one place to look. "
   "And use it early. Join rough versions of the parts on day one. Don't let the first meeting be the last step.",
   "lanes", dict(PLAN, static=True, focus="merge", caption="Second: one place where the parts meet. Early."),
   "PLAN THE INTEGRATION FIRST", group="plan")
sc("05d_test","Third, test the whole system. Not just each part. The assembled thing, running as one. That's the check no single agent could run alone.",
   "lanes", dict(PLAN, static=True, focus="test", caption="Third: test the whole, not just each part."),
   "PLAN THE INTEGRATION FIRST", group="plan")

# ---- worked example: Software Engineering 101, lessons 3 to 5 (finish times are the files' timestamps, Nov 21, 2026)
L345 = [{"name": "Lesson 3", "sub": "done 8:46:36 pm", "frac": 0.93},
        {"name": "Lesson 4", "sub": "done 8:47:10 pm", "frac": 1.0},
        {"name": "Lesson 5", "sub": "done 8:46:32 pm", "frac": 0.9}]
sc("06_example", "Here's a real one. Lessons three, four and five of software engineering one oh one were built at the same time. "
   "Three scripts, three renders, running side by side. The three finished videos landed within forty seconds of each other.",
   "lanes", {"label": "A REAL ONE  ·  SOFTWARE ENGINEERING 101, LESSONS 3 TO 5",
             "contract": {"tag": "THE WORK", "text": "Three\nlessons", "tone": "amber", "size": 40},
             "lanes": L345, "run": 0.5,
             "caption": "Built at the\nsame time.\nDone within\n40 seconds.", "caption_x": 1200, "caption_y": 372, "caption_size": 52,
             "caption_at": 0.7}, "A WORKED EXAMPLE")

sc("07_together", "And they came back together in one place. The contract already existed: the same script format the first two lessons used, and the same page fields. "
   "One merge point: one content file, read by one generator that builds every page. And they shipped together, in one change. [pause] "
   "Today that path has two more gates. One check that walks the whole site: every link, and every file a page points to. "
   "And a pull request to staging, for me to approve. [pause] This lesson and the one before it were drafted in parallel, too.",
   "lanes", {"label": "HOW THE THREE LESSONS CAME BACK TOGETHER  \u00b7  PLUS TODAY\u2019S GATES",
             "contract": {"tag": "THE CONTRACT", "text": "Same script\nformat\n\nSame page\nfields", "size": 28, "tone": "accent", "at": 0.12},
             "lanes": [dict(l, sub="script + render") for l in L345], "hold_lanes": True,
             "merge": {"tag": "ONE MERGE POINT", "text": "One content file\nOne generator", "size": 27, "tone": "accent", "at": 0.36},
             "test": {"tag": "TODAY: WHOLE-SITE CHECK", "text": "Every link,\nevery file", "size": 28, "tone": "accent", "at": 0.6},
             "chips": ["content.json", "gen.py", "check_site.py", "pull request to staging", "I approve"],
             "chips_at": 0.64, "chip_step": 1.3},
   "A WORKED EXAMPLE")

sc("08_cost", "Parallel isn't free. You pay for it at the merge. With the integration planned first, three agents finish sooner than one working down a list. "
   "Without a plan, the time you saved comes back as rework. [pause] "
   "And if two parts keep needing each other's answers, they aren't parallel work. Go back to the graph.",
   "cost_bars", {"label": "THREE AGENTS, TWO WAYS  ·  AN ILLUSTRATION, NOT A MEASUREMENT",
                 "bars": [{"name": "No plan for the merge: build fast, then rework", "frac": 0.9, "tone": "amber", "segments": 2},
                          {"name": "Integration planned first", "frac": 0.45, "tone": "accent", "segments": 1}],
                 "note": "The time is won or lost at the merge.",
                 "fine": "IF TWO PARTS KEEP NEEDING EACH OTHER, GO BACK TO THE GRAPH"}, "THE HONEST MATH")

sc("09_recap", "So, to recap. Split only where nothing crosses. Agree the contract before anyone starts. Merge early, in one place. And test the whole, not just the parts.",
   "rule", {"headline": "Parallel agents, one integration",
            "items": ["Split only where nothing crosses", "Agree the contract before anyone starts",
                      "Merge early, in one place", "Test the whole, not just the parts"]}, "RECAP")

sc("10_rule", "Which gives us rule three, for your agents. Before you run agents in parallel, plan how the work comes back together. "
   "Write the shared contract first. Give each agent its own brief, its own finish line, and its own check. "
   "Merge early, in one place. And test the whole system, not just each part.",
   "rule_card", {"kicker": "RULE 3  ·  FOR YOUR AGENTS", "size": 56,
                 "lines": [{"text": "Before you run agents in parallel,"},
                           {"text": "plan how the work comes back together.", "tone": "accent"},
                           {"text": "Write the shared contract first.", "tone": "accent"},
                           {"text": "Each agent: its own brief, finish line, and check."},
                           {"text": "Merge early, in one place.", "tone": "accent"},
                           {"text": "Test the whole system, not just each part.", "tone": "accent"}],
                 "foot": "THE FULL RULE IS ON THE LESSON PAGE"}, "THE RULE")

sc("11_ask", "Now, your turn. Think of the last time work was split, across agents, or across people. Where did the parts first meet? [pause] And who checked the whole thing?",
   "statement", {"headline": "Your turn. The last time work was split:\nwhere did the parts first meet?\nWho checked the whole thing?", "size": 80}, "YOUR TURN")

sc("12_close", "At that merge point, someone still has to say yes. That's next. Governance: where people decide. See you in lesson four.",
   "outro", {"headline": "See you in\nlesson four.", "sub": "Next: governance, where people decide"})

spec = {"id": "se201-03-parallel", "title": "SE201 Lesson 3: Parallel agents, one integration",
        "output": "03-parallel-agents-one-integration/SE201_03_Parallel-Agents-One-Integration_public.mp4",
        "voice": "4lbl0krw73vf", "language": "en", "speed": 1.05, "scenes": S}
json.dump(spec, open(os.path.join(HERE, "scripts", spec["id"] + ".json"), "w"), indent=1, ensure_ascii=False)
words = sum(len(s["text"].replace("[pause]", "").split()) for s in S)
print(spec["id"], len(S), "scenes", words, "words, est", round(words / 2.6), "s")
assert not any(t in s["text"].lower() for s in S for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))

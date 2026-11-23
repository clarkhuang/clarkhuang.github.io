# Facts in SE201 Lesson 7, "Skills as Building Blocks", and where each comes from

Script: `pipeline/scripts/se201-07-skills.json` (generator `pipeline/make_se201_07_skills.py`). 15 scenes, 696 spoken words, 233.7 s of narration audio.

The lesson makes no claim about the narrator, about sticky.io, or about any real company, person, incident or number. It contains no statistics. The web sources below are public pages cited from the round-1 review or from general knowledge of the documentation; they were not re-fetched during round 2.

## Claims about the world

| Scene | Claim | Basis |
|---|---|---|
| 03 | Libraries, frameworks and services are units of reuse, "roughly in the order they became common" (on screen) | General software history: subroutine libraries from the 1950s on, application frameworks common from the late 1980s and 1990s, services behind an API from the 2000s on. Hedged on screen with "roughly". |
| 03 | "All three reuse software. A skill reuses something different: how a job gets done." | A framing, presented as one. Scene 05 states plainly that this is a runbook. |
| 04a | "Several agent tools now share a format for this: a folder, with an instruction file." | The Agent Skills format: a folder containing `SKILL.md`. Published as an open format in December 2025 and read by agent tools from several vendors. Sources: https://agentskills.io ; https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation |
| 04a | "It starts with when to use it... That line is how an agent finds the skill." | In that format each skill carries a short description saying what it does and when to use it; the agent sees the descriptions first and loads the full file when one applies. Same sources. |
| 04a, on screen | File name `skills/add-a-plan/SKILL.md` | `SKILL.md` is the real file name in the format. The folder name and the contents are made up and labelled so. |
| 05 | "If that sounds like a runbook, it is. Engineers have written those for decades." | Operator run books date from mainframe operations; common knowledge in operations and SRE practice. |
| 05 | "A person reads a runbook now and then, and fills the gaps from memory." | A generalisation, offered as a contrast, not a measurement. |
| 05 | "An agent reads the skill on every run, with no memory of the last. Where the page is silent, it guesses." | True of a fresh agent session, which is the case the lesson is about (the hook's "a different agent starts from zero"). Some tools add memory between sessions; the lesson does not claim otherwise for those. |
| 05 | "When a step needs no judgment, make it a script the skill calls." | Advice. The Agent Skills format allows scripts in the skill folder for this purpose (same sources). |
| 06 | Keep it in the repository, versioned, reviewed; test it with a fresh agent on staging | Advice, framed as "treat a skill like code". No factual claim. |
| 07 | "No guarantee: agents still vary. That's what the checks are for." | Language-model output is not deterministic; common knowledge. This line replaced an overclaim (see `se201-07-claims-toned-down.md`). |
| 08 | "A good rule of thumb: the third time." | The long-standing "rule of three" from refactoring practice, applied to skills. Presented aloud and on screen as a rule of thumb, with no attribution by name. |

## The worked example (made up)

| Scene | Content | Status |
|---|---|---|
| 02 | Adding a plan or price to "our made-up subscription-billing system", done three times with three results: right; tax setup skipped; old price edited in place so every existing subscriber is on the new price | Invented illustration. Said to be made up aloud at first mention; "A MADE-UP EXAMPLE" on screen. |
| 04a to 04d | The skill: when to use; inputs (name, price, billing period, start date); four steps (add the plan with its price as a new version; set its tax category; map it in the accounting export; open a pull request so a person approves the price); checks (a test renewal on staging charges the right amount, tax included, exactly once; the ledger still adds up; existing subscribers renew at their old price; if one fails, stop and say so); trap (never edit a price in place) | Invented illustration, labelled "A MADE-UP EXAMPLE" on every frame. Uses only the parts of the series' shared example: plans and prices, tax service, accounting export, ledger, renewals. |
| 07 | The same three runs from the skill; `v1` becomes `v2` | Invented illustration. |

## Threads to other lessons (checked against the brief)

| Scene | Thread |
|---|---|
| 04b | "a price is money, and a person approves it": lesson 5, governance |
| 04c | "the right amount... exactly once": lesson 6's check |
| 04c | "The ledger still adds up": lesson 1's constant, money has to add up |
| 12 | Bridge: "routines, pipelines, and integration. See you in lesson eight." |

## Production facts

| Item | Value |
|---|---|
| Voice, language, speed | `4lbl0krw73vf`, `en`, 1.05 |
| Speech tags used | `[pause]`, `<emphasis>` only |
| Spelled for speech | "two oh one", "A.P.I.", "A.I." |
| Speech-to-text check | All 15 clips match the script (`asr-check.txt`, lines for `se201-07-skills`) |
| New layouts | `drift`, `skill_card` in `pipeline/se201_layouts_58b.py` |

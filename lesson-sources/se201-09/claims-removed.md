# Claims toned down or removed: SE201 Lesson 9, Agents That Operate Enterprise Systems

Changes between the first draft (`make_se201_09_operate.round1.py`, `se201-09-operate.round1.json`) and the script as it stands. Findings are numbered as in `se201-09-review-round1.md`.

| Scene | Earlier wording | Now | Why |
|---|---|---|---|
| 02_quiz | "Nobody can tell." | "The log says: admin. Who did it?" ... "The log can't say." | Sessions, source addresses or key ids can sometimes tell. The defensible claim is about the log line on screen. (Round 1, minor 1) |
| 03_questions, 13_close | "Agents built the system. Now one runs it, every night."; "Agents can run the system." | "Who operates this system?"; "An agent can operate the system. It can't answer for it." | Lesson 8 says most steps are plain code and an agent "works" the step that needs judgment. "Runs it" claimed more. (Minor 2) |
| 04_identity | "Share a login, and the log says admin. Give it its own, and the log says who." | "Not a shared login, not a person's. So the log says who." | Shorter, and no second claim about what a shared login's log shows. |
| 05_access | "An instruction can be misread, or talked around." | "An instruction can be talked around. A permission that isn't there can't be." | Kept, with a page note: true of that permission through that identity; other routes still need the same least access. |
| 06_reach | "The card number isn't in our system: the processor holds it, and we hold a token." | "The card number: the processor holds it, and we hold a token." | Says what the made-up system does, without a claim about where card data can never appear. No claim about PCI scope was ever made. |
| 06_reach | "The processor's secret key: a tool makes the call, and the agent never sees the key." | "The processor's key: a tool fetches the report, with a read-only key the agent is never shown." | Hiding a key is not the control; its scope is. "Never sees" was absolute. (M4) |
| 06_reach | "Customer details" drawn as an allowed, green row under the head "OUT OF REACH"; caption "What an agent can't reach, it can't leak." | Row "Customer name, email: not in what it reads"; caption removed. | The screen contradicted itself, and the caption was an unspoken absolute. (M5) |
| 05_access, 09_limits | Deny row "Refund, or charge → No moving money" | "Move → Money" | A slogan sat in the column of things. (M5) |
| 07a_night | "Our side recorded a timeout, so it never reached the ledger." | "Our side timed out, the retries ran out, and it never reached the ledger." | Lesson 8 retries a timed-out charge with the same key; without "the retries ran out" the example contradicted it. (M1) |
| 07b_next | "Refund the customer?" | "Refund it, so the counts match?" | Nobody refunds a valid renewal; the tempting wrong fix is making the numbers match. (Minor 8) |
| 07c_log | "The system writes it. The agent can't edit it." | "The agent gives the why. The system writes the line, and the agent can't change it." | The agent supplies its reason and the system records it; "edit" was a weaker bar than "change". (M3, minor 5) |
| 07c_log | "the ledger's owner reads the case, and approves" | "Where does a person decide? At eight fifteen: the ledger's owner approves." | Names the fourth question where it is answered. |
| 08_nearmiss | "So for three months, it could issue refunds. It never did. Then an access review asked two questions..." | "At setup, this agent's access was copied from a support role. So it could issue refunds, and never said so. Then its owner reviewed every permission: needed? Used?" | "At setup" removes the clash with the access map; the made-up "three months" was not needed; the agent's silence is what the last clause of rule 9 answers; the owner now does something. (M3, minors 3 and 4) |
| 08_nearmiss | "Because agents read text they didn't write... And text can be written to steer an agent. With the spare permission, a refund could go out." | Kept, already hedged ("can be", "could"). "So review access on a schedule." removed for length; the practice is in the page notes. | |
| 09_limits | "Through all of it, the owner still owns the outcome." | Removed here; the close says "You still own the outcome." | Said once, where it lands. |
| 10_recap | "A person wherever money moves." | "A person decides on money, and on the ledger." | The only decision the lesson shows is a ledger change. (M2) |
| 11_rule | "If it moves money, or changes the ledger, prepare it, and hand it to the person named." | "Don't move money, or change the ledger, unless a person has released it. Otherwise: prepare it, and hand it over." | Lesson 5 lets an agent act where a person has already decided (a refund under a set limit). The first wording forbade that for every agent. (M2) |
| 11_rule | "Operate under your own identity, with only the access the job needs. Don't borrow a login, and don't work around a no. Say why, with every action." | "Use only your own identity, and only the access the job needs. Never borrow a login, or work around a no. Give your reason with every action." | An agent doesn't choose its identity or access; it can choose to use only those. (M3) |

## Kept out from the start
- Any claim about Clark or any company, and any real incident. The two stories (the 3 a.m. refund and the near miss) are hypotheticals, called made up aloud.
- Named standards, products, processors or tools in the narration. Standards appear only in the facts file as the basis for claims.
- Statistics of any kind.
- "PCI", "compliance", "zero trust", "prompt injection" as terms. The last is described in plain words ("text can be written to steer an agent") and named in the page notes.
- A claim that an audit log is tamper-proof. The narration says who writes it and that the agent can't change it.
- A claim that least access prevents misuse. It limits the damage; the lesson says "could" and "can".

Nothing about Clark or any company was claimed in any draft, so nothing of that kind was removed.

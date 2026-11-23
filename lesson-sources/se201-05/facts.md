# Facts: SE201 Lesson 5, Governance: Where People Decide

Every factual claim in the lesson (spoken or on screen), with its source. Script: `scripts/se201-05-governance.json`.
- **BRIEF** means the owner's brief for lessons 5 to 8 (`briefA.md`): the facts about Clark, the series path and the running example.
- **L1 / L2 / L4** means a recorded lesson of this series (`sitegen/content.json`, `lesson-sources/se201-0N`).
- **GH** means general industry history, with a well-known reference.
- **LENS** marks a teaching idea written by the scriptwriter. It is presented as a rule of thumb, not as fact or as Clark's quote.
- **MADE-UP** marks an invented illustration, labelled as made-up aloud and on screen.

## About Clark
No claim about Clark, his career or any company is made in this lesson. No company is named.

## History (approximate by design)
| Claim | Scene | Source |
|---|---|---|
| Thirty years ago, "typically", a change board signed off a whole release, a few times a year | 03a_board, eras card | GH: change advisory/control boards in ITIL-style change management (ITIL dates from the late 1980s); L1 (releases a few times a year in the mid-1990s). Hedged with "typically". |
| Twenty years ago, "more and more", a teammate reviewed the code before it went in | 03b_review, eras card | GH: peer code review spreading in the 2000s (pre-commit review tools such as Rietveld and Gerrit, 2008-2009; the book "Best Kept Secrets of Peer Code Review", 2006). Hedged with "more and more". |
| Ten years ago, an approval step in an automated pipeline: a pull request a reviewer approves before it merges | 03c_pipeline, eras card | GH: GitHub pull requests (2008), protected branches with required reviews (2015-2016), CI/CD pipelines mainstream by the mid-2010s. |
| On screen, 2016: "HOW OFTEN: Most changes" | 03c eras card | GH, approximate; describes teams using the pull-request flow. Listed as a minor in review round 2. |
| In each earlier era people wrote the code | 03d_now, eras cards | GH. |
| Now agents write changes "faster than anyone can read them all", "more and more" | 03d_now, 02_quiz | L1's premise (agents do much of the building; knowing it's right is the scarce thing). Stated as the situation the lesson addresses, with no number. |
| "An old idea from accounting: whoever prepares a payment doesn't approve it" | 07_written | GH: separation (segregation) of duties, a standard internal control (for example in the COSO framework). |
| "Where an audit requires a review, that review stays" | 08c_few | GH: audited environments (for example SOX or PCI DSS change control) require independent review of changes. Stated as a condition, no specific standard is named. |

## Teaching ideas (LENS)
| Claim | Scene | Source |
|---|---|---|
| Tests can't say whether you wanted the change; nobody reads forty changes carefully | 02_quiz | LENS. "Forty changes" is a hypothetical, opened with "Picture this". |
| The place where a person says yes has to be designed, not inherited | 03d_now | LENS (series outline for lesson 5). |
| Four questions: moves money, touches customer data, hard to undo, a judgment call no check can make. One yes: a person decides. Four no's: that kind of change can ship on its checks | 04_tests | LENS, called "a good rule of thumb" aloud and on screen. |
| The agent prepares the decision: what changes, why, the evidence, the risk, the way back | 06_packet | LENS. |
| Write who approves what in a file in the repository; the pipeline enforces it by what a change touches; the author neither classifies nor approves | 07_written | LENS. Files that map paths to required reviewers are a real feature of the common code hosts; the lesson does not name one. |
| A person on everything becomes a bottleneck and a rubber stamp; a person on nothing is fast until money moves unapproved | 08a_all, 08b_none | LENS. |
| Start strict, a person on every change "like lesson two", then release one kind at a time as its checks earn trust | 08c_few | LENS; L2's rule ("send every change through staging for a person to approve"). |

## The worked example (MADE-UP)
| Claim | Scene | Source |
|---|---|---|
| "Our made-up example: the subscription-billing system from lesson one" | 05a_free; on-screen labels in 05, 06, 07 | BRIEF; L1 introduced it as "a made-up example". |
| Six things an agent drafts; two ship on their checks, four stop (finance owner, ledger owner, data owner, support lead) | 05a-05c | MADE-UP. The roles, the late fee and the refund limit are invented. The count (6 = 2 + 4) is correct. |
| The decision request for the late-fee change and its five field values | 06_packet | MADE-UP, labelled "A MADE-UP EXAMPLE" on the card. |
| The "who approves what" table | 07_written | MADE-UP, labelled on screen. |

## Cross-references
| Claim | Scene | Source |
|---|---|---|
| Lesson 4 ended on "someone still has to say yes" | (context for 01-02) | L4's closing line. |
| Next: quality, feedback, and observability, lesson six | 12_close | BRIEF series path. |

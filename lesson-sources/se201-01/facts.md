# Facts: SE201 Lesson 1, Four Eras of Building Systems

Every factual claim in the lesson (spoken or on screen), with its source.
- **F#** is a line of `mirror-ref/facts-201-01.txt` (a facts file kept on the build machine, not in this repository), numbered from 1.
- **LI** means the public LinkedIn and company profiles, as summarised in F2.
- **GH** means general industry history, with a well-known reference.
- **LENS** marks a teaching framing written by the scriptwriter. It is presented as a lens and not as fact or as Clark's quote (F7).

## About Clark
| Claim | Scene | Source |
|---|---|---|
| Building systems for about thirty years | 03_career, on-screen label | F1 ("about 30 years in software... designed and in many cases architected the systems") |
| Electronic rent payments: PropertyBridge, co-founder | 03_career | F2 / LI (co-founder and VP Payment Services at PropertyBridge, an electronic rent-payment company) |
| A card-issuing platform: Marqeta, co-founder | 03_career | F2 / LI |
| An investment adviser for nonprofits: eCIO, co-founder and CTO | 03_career | F2 / LI |
| Retail e-commerce and EDI: QRS, early role | 03_career | F2 / LI |
| Subscription billing: sticky.io, CTO ("the kind of platform I ran as C.T.O. at sticky dot I O") | 03_career, 09_design | F2 / LI |
| "Today, e-commerce again": CTO of an e-commerce company, unnamed | 03_career | F2 ("now CTO of an e-commerce company") |
| "My own team keeps its code that way: one repository, with instruction files for the agents" | 09_design | F4 ("keeps its code in one monorepo with agent instruction files") |

No company outside the public career record is named. No internal architecture, numbers, incidents or anecdotes about any company appear. The billing diagram
in 09_design is called "a made-up example" aloud and on screen ("A MADE-UP EXAMPLE"). It is a generic subscription-billing picture, not sticky.io's design.

## History (approximate by design)
| Claim | Scene | Source |
|---|---|---|
| Mid-1990s: the commercial web was new; "typically" one big program on one database (client/server and mainframes also common) | 05_1996 | GH: Netscape Navigator 1994; Amazon and eBay 1995; the web itself dates from about 1991 |
| Company-owned servers you racked yourself; one big program on one relational database; releases a few times a year | 05_1996, eras card | F5; GH |
| Companies traded orders as overnight batch files through EDI, and much of that still runs | 05_1996, eras card | F5; GH: ANSI X12 / EDIFACT EDI, standard since the 1980s and still in wide retail and logistics use |
| 2006: three tiers (browser, application, database) on rented racks (hosting / colocation) | 06_2006 | GH: the classic three-tier web architecture of the 2000s |
| The first big public cloud services had just launched | 06_2006, eras card | F5 ("first major public cloud services launched in 2006"); GH: Amazon S3 (March 2006), EC2 (August 2006) |
| Agile teams shipped every few weeks | 06_2006 | F5 (Agile Manifesto, 2001); GH: Scrum sprints of 1-4 weeks |
| On screen: "Web services, XML over HTTP" | 06_2006 card | GH: SOAP/XML web services, W3C SOAP 1.2 (2003) |
| 2016: cloud by default for new systems; containers; many small services | 07_2016 | F5 ("containers and microservices became mainstream in the mid-2010s"); GH: Docker 2013, Kubernetes 2014 (1.0 in 2015), the Lewis and Fowler "Microservices" article 2014 |
| The best teams deployed many times a day | 07_2016 | F5 (continuous delivery); GH: *Continuous Delivery* (Humble & Farley, 2010); DORA / *Accelerate* research on elite performers |
| Parts teams once built became a service behind an API | 07_2016, card "An API for everything" | F5 ("API-based SaaS") |
| Dashboards and tracing to see the whole system | 07_2016 | GH: distributed tracing (Google's Dapper paper 2010, Zipkin 2012, Jaeger 2017) and the 2010s observability movement |
| Now: agents can write much of the code; context (how much an agent can see at once) is a bottleneck | 08_now, caption | F6 ("an agent's limited context is the bottleneck") |
| Agent-era design: modules with boundaries, one repository, tests and specs, decisions written down; "where the thinking is heading, not a settled answer"; "the evidence for it is still thin, and indirect" | 09_design, 10_caveat | F6 (monorepos and modular monoliths with enforced boundaries, fast tests, machine-readable rules; "at least one of those sources says this is a stance assembled from indirect evidence") |
| On screen: "APIs, and agents calling tools" | 08_now card | GH: tool-calling agents, e.g. Model Context Protocol (2024) |
| Quiz claim: an agent can write a working piece of a billing system in an afternoon; code got cheap, checking it didn't | 02_quiz | F6 (bottleneck is verification and context), as a general framing; no specific measurement is claimed |

## Teaching lens (LENS, F7: written by the scriptwriter, judged on its merits)
- "Architecture bends around whatever is scarcest" (04_lens, framed as "a useful way to see why").
- The scarce resource per era: Machines / Coordination / Seeing the whole (the draft said "Attention"; changed, see claims-removed.md) / Knowing it's right.
- The four constants: the data model outlives the code; money has to add up; you depend on what you don't control; someone understands
  the layer below (cf. Spolsky, "The Law of Leaky Abstractions", 2002). The examples are rent payment, card transaction, renewal, bank, card network, and
  partner's system. These are generic kinds from Clark's public domains, not internal facts.
- The quiz (02_quiz). It was rewritten, but it is still a framing, not a measurement.

## Series references
- The path in 12_path matches `curriculum.md` and recorded lesson 2's `11_path`.
- The bridge in 16_close ("so agents and people can both read it, and rebuild it") uses lesson 2's own definition of AI-native.

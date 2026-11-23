# Review round 2: SE201 Lesson 1, Four Eras of Building Systems

The reviewer was a fresh independent agent with no memory of round 1. It read `review-input-round2.txt`, which is the script after the round-1 revisions
(`tools/make_se201_01_four_eras.round2.py`), along with the renumbered lessons 2-4 and the facts file.
Verdict: **PASS** with no major findings. Every minor finding and what I did about it:

| Finding | Disposition |
|---|---|
| 09_design: the spoken text tied the illustration to sticky.io, and "AN ILLUSTRATION" was only on screen. "My own team works this way" could be heard as claiming the whole list. | **Fixed.** The scene now says aloud "Now a made-up example: a subscription-billing system, built today, the kind of platform I ran as C.T.O. at sticky dot I O", and the screen label is "A MADE-UP EXAMPLE · ...". The team line now reads "My own team keeps its code that way: one repository, with instruction files for the agents", which is exactly what facts F4 supports. |
| 09 vs 08: "readable end to end" contradicts "context is scarce". | **Fixed.** The line is now "One repository, where it can find anything", and the band label is "ONE REPOSITORY · EVERYTHING FINDABLE". |
| 10_caveat: an unnamed "at least one source" sounds evasive on a public video. | **Fixed.** It now says "The evidence for it is still thin, and indirect", which is supported by F6. |
| 07_2016: "rented, through an A.P.I., what they used to build" is hard to follow by ear. | **Fixed.** It now says "And parts they once built themselves became a service, behind an A.P.I." |
| 05_1996: "one big program, on one big database" ignores client/server and mainframes. | **Fixed.** It now says "So, typically, you built one big program, on one big database". |
| 15_ask: the screen said "which era it's from", but the spoken question asks which era's thinking is hiding inside the system. | **Fixed.** The screen now reads "Ask your AI which era's thinking is hiding inside it." It does not apply the rule (the reviewer's alternative), because applying the rule is lesson 2's style of ask. Here the ask stays on the lens, which is this lesson's idea. |
| TTS may say "stickyio". | **Fixed.** It is spoken as "sticky dot I O", and the screen still says sticky.io. |
| Runtime is about 4.5-4.6 minutes once pauses are counted. | **Fixed.** I cut the spoken examples in 11_constants (they stay on screen) and opened 12_path with "Here's the path." The script is now 677 words, an estimated 260 s (4.3 minutes) at 2.6 words/s, or about 4.5 minutes with pauses before the 1.05 speed-up. |
| The rule covers the data model and dependencies, but not "the layer below" or context. | **Kept.** The rule is the design note an agent writes before designing, and "the layer below" is a constant for people. The reviewer judged this acceptable. |

Confirmed clean: the hook lands at about 5 s. The lens is framed as a lens. There are no invented details, no other names, and no company outside the public career record. The dates match facts F5. The tone is steady and professorial. The TTS spellings and tags are valid. The path matches the recorded lesson titles, and the bridge uses lesson 2's definition.

After these fixes I re-rendered every still and looked at each one. There is no overflow, overlap, clipping or empty frame.

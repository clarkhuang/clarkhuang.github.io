# Interview Plan: Silicon Valley C Players and SE 201

HTML page: https://clarkhuang.github.io/interview-plan/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/interview-plan/index.md (plus https://clarkhuang.github.io/interview-plan/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

# Interview Plan: Silicon Valley C Players and SE 201

Working plan for Clark Huang's voice sessions with LegacyBot over Grok Bot voice chat. Drafted 2026-11-21; we'll iterate on it together.

Two goals: (a) real stories and positions for the public AI-native education series (AI Tips, Software Engineering 101, and next, Software Engineering 201), and (b) material for the autobiography *Silicon Valley C Players*, self-published in 2027 as an audiobook and an animated stick-figure videobook.

## 1. How the sessions work

- **Length.** 20 to 30 minutes over Grok Bot voice chat. Stop whenever you like; a 10-minute burst still counts.
- **One situation at a time.** LegacyBot asks about one moment, lets you tell it, then moves on. No multi-part questions.
- **Reflect, then ask.** After each answer LegacyBot says back what it heard in a sentence or two, so you can correct it, then asks the next question.
- **Short bursts are fine.** Short answers are welcome. If you remember something later, just add it next session or in chat.
- **Permission before publishing.** Nothing personal goes into the book, a video or the site until you say yes. Anything about other people, companies or numbers gets an extra check.
- **Your words stay your words.** Your quotes are kept verbatim. LegacyBot's own readings are labeled as suggestions until you confirm them.

### What gets recorded where (proposed)

| What | Where |
|---|---|
| Session notes: your quotes verbatim, LegacyBot's reflections, follow-ups | `Learning Videos/LegacyBot/interviews/session-NN.md` on your Mac, plus a box copy under `/workspace/legacy/interviews/` |
| Publish permission per story (yes / not yet / private) | A table at the top of each session note |
| Facts a lesson may state | The lesson's `facts-NN.txt`, as with 101 |
| Book material | A running chapter outline at `LegacyBot/book/outline.md` |
| This plan and the tracker | This page and `interview-plan.md` |

### Before and after each session

1. **Before:** LegacyBot rereads the last session's notes and picks 6 to 10 questions.
2. **During:** one situation at a time, reflect back, next question.
3. **Right after:** LegacyBot writes the session note and lists anything that needs your yes before it's used.
4. **Next time:** open with anything left hanging.

## 2. Session roadmap

Book and 201 sessions alternate so it stays fun. Every session ends with one question: "Anything you want to add from last time?"

| # | Session | Track | Length |
|---|---|---|---|
| 1 | Picking up the open threads | Book | 20 min |
| 2 | Growing up: top of the class | Book | 25 min |
| 3 | Berkeley: middle of the pack | Book | 30 min |
| 4 | Building big systems: 30, 20 and 10 years ago versus now | SE 201 | 25 min |
| 5 | First jobs and the 'C companies' | Book | 25 min |
| 6 | San Francisco after dark | Book | 25 min |
| 7 | Splitting work and running it in parallel | SE 201 | 20 min |
| 8 | Founding, co-founding and becoming CTO | Book | 30 min |
| 9 | Incidents, war stories and legacy code | SE 201 | 25 min |
| 10 | Mentors, the smarter guy in the room, failures and recoveries | Book | 30 min |
| 11 | Build versus buy, cost, and running a fleet | SE 201 | 20 min |
| 12 | Family and balance | Book | 20 min |
| 13 | The AI-native shift, investing in AI, philosophy and legacy | Book | 30 min |

## 3. Sessions

### Session 1: Picking up the open threads (Book, about 20 minutes)

**Goal.** Warm up with the three questions left hanging from the earlier interviews, so the first session feels like a continuation, not a cold start.

**Questions**

1. Last time you told me about that Math 1A midterm, Cs and Ds and no curve. What did you actually do the week after it came back?
2. Who did you talk to that week, if anyone? A roommate, your parents, nobody?
3. Did you change how you studied after that, or did you just push through?
4. You said you did C things in your career that looked like A things to everyone else. What's the first one that comes to mind?
5. What did people see from the outside, and what did you know was really going on?
6. Can you think of a moment when knowing the layer underneath solved something other people were stuck on?
7. What was the layer, and how did you know to look there?
8. Of these three stories, which one would you want to open the book with?

**Follow-up probes**

- What did that feel like in your gut at the time?
- Who else was in the room when that happened?
- If we drew this as a stick-figure scene, what's in the frame?

**Feeds.** Book: Prologue (the Math 1A opening scene), Ch. 4 (C things that looked like A things). SE 201: a story for 'the layer underneath'.

### Session 2: Growing up: top of the class (Book, about 25 minutes)

**Goal.** Collect the before picture: who Clark was when he was the top of his class in high school, so the drop to the middle at Berkeley lands.

**Questions**

1. Where did you grow up, and what did a normal day look like when you were a kid?
2. When did you first realize you were good at school, or at least that people thought you were?
3. What was it like being top of the class in high school? Was it fun, or was it pressure?
4. Tell me about school days. What's one ordinary day from back then you still remember clearly?
5. Was there a first computer, a first program, a first thing you built that made you go 'oh, this is it'?
6. Where did music come in? What did you play, and who got you started?
7. Who were the people at home or at school who shaped you most back then?
8. Was there ever a moment in high school where you weren't the smartest one in the room?
9. How did you end up choosing Berkeley?

**Follow-up probes**

- What would you tell your 16-year-old self?
- Is there a smell, a sound, or an object that brings that time back?
- What would that kid think of what you do now?

**Feeds.** Book: Ch. 1 (Top of the class). Videobook: the opening montage.

### Session 3: Berkeley: middle of the pack (Book, about 30 minutes)

**Goal.** Turn the Berkeley stories already told (Math 1A, the music and CS elective, CS61B, Algorithms) into full scenes, and fill in the music minor.

**Questions**

1. Take me to your first week at Berkeley. Where did you live, and what was the vibe?
2. When did it sink in that you'd gone from top of the class to the middle of the pack?
3. Tell me more about the music and CS class, the baroque composer you wrote. What did it actually do?
4. What did it feel like to get an A+ for something you said you barely worked on?
5. CS61B was the weeder class and you came out on top. What clicked for you there that didn't click for others?
6. And then Algorithms, where you said you barely got a B-. What was different?
7. You mentioned dreaming in green screen during CS150. What did those dreams look like, and how deep in were you when they started?
8. How did music and computer science fit together for you? Did one help the other?
9. Was there a professor, a TA, or a classmate from those years you still think about?
10. What did Berkeley teach you that you still use every week?

**Follow-up probes**

- You said 'it's all relative how smart you are.' When did you first feel that?
- What would you tell your 19-year-old self walking into Math 1A?
- If we drew the green-screen dream as a stick-figure scene, what's on the screen and what's happening around you?

**Feeds.** Book: Ch. 2 (Middle of the pack). SE 201: the 'fundamentals' thread (COOL, B-trees, a compiler). Bookend candidate: the CS150 green-screen dream.

### Session 4: Building big systems: 30, 20 and 10 years ago versus now (SE 201, about 25 minutes)

**Goal.** Get Clark's own comparison of how big software got built in each era, which also answers his earlier question to Claude and could open 201.

**Questions**

1. Pick a big system you worked on about 30 years ago. How many people, how long, and what did a normal week look like?
2. What were the tools then? How did you debug, test and ship?
3. Now jump to about 20 years ago. What had changed, and what hadn't?
4. And 10 years ago, with cloud, CI and agile everywhere. What got easier and what got harder?
5. You mentioned extreme programming and Microsoft days once. What was that about?
6. Today, with agents, what does building a big system look like for you on a normal day?
7. What's the one skill that mattered in every era?
8. What do you think people who started coding with agents will miss that you had to learn the hard way?

**Follow-up probes**

- What did you lose along the way that you wish you still had?
- Was there a moment you thought 'this changes everything' and it didn't?
- What would your 25-year-old self think of how you work now?

**Feeds.** SE 201: Lesson 1 (From loop to graph) and possibly an intro lesson on eras. Book: a bridge chapter on the industry changing around him.

### Session 5: First jobs and the 'C companies' (Book, about 25 minutes)

**Goal.** Map Clark's early career in his own words and find out what he means by 'C companies'.

**Questions**

1. What was your very first job in software, and how did you land it?
2. What did you think a career would look like back then, and how did it actually go?
3. Walk me through the companies in order, roughly. Which ones stand out?
4. When you say 'C companies', what makes a company a C company?
5. Was there a company that looked like an A company from the outside but wasn't?
6. Was there a payments company early on? (A public profile lists one; we never confirmed it.)
7. Tell me the 'PIMS After Dark' story from PropertyBridge. What was PIMS, and what happened after dark?
8. What was your longest all-night coding session, and what were you building?
9. What was a day at your favorite early job like?
10. When did you first get to lead people or own a system?

**Follow-up probes**

- What did that feel like when you walked in the first day?
- Is there anyone from back then you'd want to thank in the book?
- Is there anything here you'd want kept private?

**Feeds.** Book: Ch. 3 (C companies). Confirms or drops the unconfirmed career facts.

### Session 6: San Francisco after dark (Book, about 25 minutes)

**Goal.** Collect the wilder stories Clark flagged (Jack Dorsey's apartment, drunk nights in San Francisco, all-night coding) and decide which ones the book should leave the listener guessing about.

**Questions**

1. You mentioned being in Jack Dorsey's apartment. How did you end up there, and what was the night like?
2. Tell me about a night out in San Francisco that you still laugh about.
3. What was the city like back then for someone in tech? Where did people go?
4. What's an all-night coding session that turned into a story you still tell?
5. Who was usually with you on those nights?
6. The book will carry a playful disclaimer that some stories may have been dramatized a bit. Which of tonight's stories do you want to leave the listener guessing about?
7. Is there a story that's so unlikely it's actually true, that we should tell completely straight?
8. Where's the line: what's fun to blur, and what has to stay exactly accurate?

**Follow-up probes**

- What did that feel like at 3 AM?
- Is anyone in this story someone we should check with or leave unnamed?
- How would the videobook show it: big and cartoonish, or quiet and real?

**Feeds.** Book: an interlude chapter (San Francisco after dark) and the playful disclaimer. Videobook: the most animated scenes.

### Session 7: Splitting work and running it in parallel (SE 201, about 20 minutes)

**Goal.** Collect real stories and opinions for the 201 lessons that have none yet: finding real dependencies (Lesson 2) and choosing the right model for each job (Lesson 4). Also settle the 201 spine question.

**Questions**

1. Is 'the graph' the right spine for 201, or would you rather lean into systems topics like architecture, data modeling, legacy code and incidents?
2. Think of a project where everyone assumed step B had to wait for step A, and it didn't. What happened?
3. How do you decide how to split a big piece of work today, with people or with agents?
4. When you run several agents at once, how do you choose which model does what?
5. Have you seen a strong model wasted on a simple job, or a cheap model trusted with something it couldn't handle?
6. When one part of a parallel job fails, what do you do with the rest?
7. Where do you personally sit in that flow? What do you always want to see yourself?
8. Should 201 credit Hanako's 'Loops and Graphs' article on screen, or should we build every idea from your own examples?

**Follow-up probes**

- What would you have done differently on that project?
- What would you tell a new engineering manager about splitting work?
- Can you give me a one-line rule an agent could follow?

**Feeds.** SE 201: Lessons 2 (Find the real dependencies), 4 (The right model for each job), 5 and 8; open questions 1 and 4 in the 201 README.

### Session 8: Founding, co-founding and becoming CTO (Book, about 30 minutes)

**Goal.** Tell the founder story: co-founding eCIO, its sister company eVestech, and becoming CTO of Truly Free and Truly Free Home.

**Questions**

1. When did you first want to start something of your own?
2. Tell me the story of how eCIO started. Who was in the room, and what was the idea?
3. How do eCIO and eVestech fit together?
4. What was the first really hard week as a founder?
5. How did you end up as CTO at Truly Free, and then Truly Free Home?
6. What's different about being CTO compared with being the best engineer on the team?
7. What does 'technology strategy and operational efficiency' look like on an ordinary Tuesday?
8. You've been called a serial founder. Is that how you see yourself?

**Follow-up probes**

- What did that feel like the night before you committed?
- What would you tell your 25-year-old self about starting a company?
- Which of these stories needs a check with your co-founders before it's published?

**Feeds.** Book: Ch. 5 (Founder). Bio and About page details, once confirmed.

### Session 9: Incidents, war stories and legacy code (SE 201, about 25 minutes)

**Goal.** Gather the war stories that make systems lessons stick, plus Clark's approach to inheriting and changing old code.

**Questions**

1. What's the worst production incident you've lived through? Start wherever you like.
2. How did you find out, and what did the first hour look like?
3. You've said stop the live damage first, then find the root cause. Where did you learn that?
4. Tell me about a time you inherited code nobody understood. What did you do first?
5. You said old-school breakpoints and stepping through code gave real understanding. Is there a story behind that?
6. When do you rewrite, and when do you leave old code alone?
7. What does a good post-incident write-up look like to you?
8. How would you run that same incident today with agents helping?

**Follow-up probes**

- What did that feel like at 2 AM?
- What's the rule you wrote for yourself afterward?
- Can any names, companies or numbers stay in, or should this be told generically?

**Feeds.** SE 201: a systems track (incidents, legacy code), Lessons 7 (Gates and lanes) and 9 (The learning edge). Book: a war-story chapter.

### Session 10: Mentors, the smarter guy in the room, failures and recoveries (Book, about 30 minutes)

**Goal.** Dig into Clark's philosophy that there's always someone smarter, richer, wiser in the room, and into the setbacks he came back from.

**Questions**

1. Who's the smartest person you've ever worked with, and what made them that way?
2. Who mentored you, formally or not? What did they teach you?
3. You said there's always a smarter guy in the room. When did that sting, and when did it help?
4. Have you ever been the smartest one in the room? What did that feel like?
5. What's a failure you think about more than any success?
6. What did the recovery look like, week by week?
7. Where does 'fake it until you make it' end and 'learn deeply' begin for you?
8. Who have you mentored, and what do you hope they took from you?

**Follow-up probes**

- What would you tell your 25-year-old self after that failure?
- Is 'I just kept going' the thread through all of this, or is it something else?
- What's the stick-figure version of this lesson?

**Feeds.** Book: Ch. 6 (The smarter guy in the room) and Ch. 7 (Falling and getting up).

### Session 11: Build versus buy, cost, and running a fleet (SE 201, about 20 minutes)

**Goal.** Get real decisions and numbers-free stories behind Clark's views on ROI, total cost of ownership and spend visibility, for the 201 fleet lesson.

**Questions**

1. Tell me about a build-or-buy call you got right, and one you got wrong.
2. You said compliance is a differentiator. Where have you seen that play out?
3. How do you think about the cost of an agent run versus an engineer's day?
4. What would a good spend dashboard for engineers and agents show?
5. When have you chosen 'fix and move on' over the full process, and was it the right call?
6. If you were running dozens of agents across a company, what would you measure every week?
7. What would a 301 course cover after 201?

**Follow-up probes**

- What did the bill teach you?
- What would you tell a CFO who's nervous about AI spend?
- Is there a one-line rule here for agents?

**Feeds.** SE 201: Lesson 10 (Running a fleet); extends 101 Lesson 9 (Know what it costs).

### Session 12: Family and balance (Book, about 20 minutes)

**Goal.** Explore the personal side Clark named himself: being a father, son, brother, and how work and life fit together. Everything here is opt-in.

**Questions**

1. You listed father, son, brother, teacher in your philosophy. Which of those roles matters most to you right now?
2. What did your parents teach you about work?
3. How do you keep work from eating everything else, or do you?
4. Is there a moment when family changed a career decision?
5. What do you hope your family understands about what you've built?
6. What does a good weekend look like for you?
7. Is there anything from this part of your life you'd never put in the book?

**Follow-up probes**

- What did that feel like?
- What would you tell your younger self about balance?
- Do you want to check this with anyone in the family before it's published?

**Feeds.** Book: Ch. 8 (Father, son, brother). Private by default until Clark says otherwise.

### Session 13: The AI-native shift, investing in AI, philosophy and legacy (Book, about 30 minutes)

**Goal.** Close the arc: how Clark went AI-native, why he invests in AI through private equity and special purpose vehicles, and what he wants to leave behind.

**Questions**

1. When did you first realize AI was going to change how you work, not just what you build?
2. You've said you and a lot of people get an 'AI brain' when diving deep, dreaming about AI. What do those dreams look like for you?
3. Does dreaming about AI feel like dreaming in green screen during CS150 did? What's the same and what's different?
4. What made you change your tune on unit tests, and what else have you changed your mind about?
5. How do you pick which AI and tech deals to invest in?
6. One idea floated earlier: the C player's skills, like judgment, fundamentals and knowing when good enough is good enough, are the ones agents make most valuable. Do you buy that?
7. If the book has one sentence on the back cover, what is it?
8. Looking back across every session, which stories do you want to keep the listener guessing about, and which should be told dead straight?
9. Who is the book for?
10. Fifty years from now, what do you hope people say about your work?

**Follow-up probes**

- What would you tell your 25-year-old self about AI?
- Is 'I just kept going' the book's spine? If not, what is?
- Could the videobook open on the green-screen dream and close on the AI dream? What's the last frame?

**Feeds.** Book: Ch. 9 (The C player's advantage), the Epilogue and the possible dream bookend. AI Tips: new episodes. Back-cover copy and the disclaimer.

## 4. Tracker

| Session | Topic | Status | Feeds |
|---|---|---|---|
| 1 | Picking up the open threads | Not started | Book: Prologue (the Math 1A opening scene), Ch. 4 (C things that looked like A things). SE 201: a story for 'the layer underneath'. |
| 2 | Growing up: top of the class | Not started | Book: Ch. 1 (Top of the class). Videobook: the opening montage. |
| 3 | Berkeley: middle of the pack | Not started | Book: Ch. 2 (Middle of the pack). SE 201: the 'fundamentals' thread (COOL, B-trees, a compiler). Bookend candidate: the CS150 green-screen dream. |
| 4 | Building big systems: 30, 20 and 10 years ago versus now | Not started | SE 201: Lesson 1 (From loop to graph) and possibly an intro lesson on eras. Book: a bridge chapter on the industry changing around him. |
| 5 | First jobs and the 'C companies' | Not started | Book: Ch. 3 (C companies). Confirms or drops the unconfirmed career facts. |
| 6 | San Francisco after dark | Not started | Book: an interlude chapter (San Francisco after dark) and the playful disclaimer. Videobook: the most animated scenes. |
| 7 | Splitting work and running it in parallel | Not started | SE 201: Lessons 2 (Find the real dependencies), 4 (The right model for each job), 5 and 8; open questions 1 and 4 in the 201 README. |
| 8 | Founding, co-founding and becoming CTO | Not started | Book: Ch. 5 (Founder). Bio and About page details, once confirmed. |
| 9 | Incidents, war stories and legacy code | Not started | SE 201: a systems track (incidents, legacy code), Lessons 7 (Gates and lanes) and 9 (The learning edge). Book: a war-story chapter. |
| 10 | Mentors, the smarter guy in the room, failures and recoveries | Not started | Book: Ch. 6 (The smarter guy in the room) and Ch. 7 (Falling and getting up). |
| 11 | Build versus buy, cost, and running a fleet | Not started | SE 201: Lesson 10 (Running a fleet); extends 101 Lesson 9 (Know what it costs). |
| 12 | Family and balance | Not started | Book: Ch. 8 (Father, son, brother). Private by default until Clark says otherwise. |
| 13 | The AI-native shift, investing in AI, philosophy and legacy | Not started | Book: Ch. 9 (The C player's advantage), the Epilogue and the possible dream bookend. AI Tips: new episodes. Back-cover copy and the disclaimer. |

## 5. Story seeds from Clark

Topics you flagged to talk about. They're prompts for questions, not facts yet.

| Seed | Where it comes up |
|---|---|
| PIMS After Dark, at PropertyBridge | Session 5 (First jobs and the C companies) |
| Being in Jack Dorsey's apartment | Session 6 (San Francisco after dark) |
| Drunk nights in San Francisco | Session 6 (San Francisco after dark) |
| All-night coding sessions | Sessions 5 and 6 |
| School days | Sessions 2 and 3 |
| Dreaming in green screen during CS150 | Session 3 (Berkeley), bookend opening |
| Dreaming about AI, the 'AI brain' many people get when diving deep | Session 13 (AI-native shift), bookend closing |

### A possible bookend: from green screen to the AI brain

Open the book on dreaming in green screen during CS150, deep in the work at Berkeley. Close it on the AI dreams that you and a lot of people get when diving deep into AI. Same mind, same obsession, thirty-some years apart. This sits alongside the Math 1A midterm as a possible opening, and Sessions 3 and 13 collect the material for it. It's a proposal until you pick.

### The playful disclaimer

The book will carry a playful note that some stories may have been dramatized a bit, to keep the listener guessing what's real. A starting draft to rework in your voice: "Some of these stories may have been dramatized a little. You get to guess which." Sessions 6 and 13 ask which stories should lean into that ambiguity and which must be told straight. Anything about real, named people stays accurate or unnamed.

### Working chapter map (proposed, not confirmed)

- Prologue: a dream in green screen, or the Math 1A midterm with no curve
- Ch. 1 Top of the class
- Ch. 2 Middle of the pack
- Ch. 3 C companies
- Interlude: San Francisco after dark
- Ch. 4 C things that looked like A things
- Ch. 5 Founder
- Ch. 6 The smarter guy in the room
- Ch. 7 Falling and getting up
- Ch. 8 Father, son, brother
- Ch. 9 The C player's advantage
- Epilogue: dreaming in AI

## 6. Open threads from earlier interviews

- What did Clark do the week after the Math 1A midterm came back?
- What is a 'C thing' he did in his career that looked like an 'A thing' to everyone else?
- One moment where knowing the layer underneath solved a problem others were stuck on (open since the 101 interview).
- Is 'the graph' the right spine for 201, or should it lean toward systems (architecture, data modeling, legacy code, incidents)?
- Which 201 lessons have a real story from his work? Lessons 2, 4 and 10 have none yet.
- Should 201 credit Hanako's 'Loops and Graphs' article, or use only his own examples?
- Did he work at Microsoft? He mentioned 'extreme programming of Microsoft days' but it was never confirmed.
- A public profile lists a payments company early in his career; he hasn't confirmed it.
- Readings Claude offered that he hasn't confirmed: fake it gets you in the room, learn deeply earns the seat; the music professor as the first 'C thing that looked like an A thing'; 'I just kept going' as the book's spine; the C player's skills as the ones agents make most valuable.
- Lines added to the 101 scripts (facts-NN.txt) still need his yes or no.

## For agents

- This page: https://clarkhuang.github.io/interview-plan/index.md
- This folder’s agents file: https://clarkhuang.github.io/interview-plan/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

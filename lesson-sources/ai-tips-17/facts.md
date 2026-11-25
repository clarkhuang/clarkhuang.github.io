# Facts — AI Tips lesson 17: Don't Paste Secrets

Every claim in the lesson, spoken or on screen, and where it comes from. The deploy illustration is generic and labelled as such ("Say a deploy is failing…"). Nothing in this lesson is a story, quote, or number about Clark Huang or about a named company.

## Teaching points (from the Nov 21, 2026 public AI Tips research brief, ranked item 6)

- A chat is closer to emailing a contractor than to writing on a whiteboard in a locked room.
- Once a secret is in the thread, asking the bot to forget it does not unsay it.
- Before you paste, scan for keys, tokens, passwords, connection strings, session cookies, customer personal data, and internal URLs that aren't public, and replace them with placeholders.
- If a secret did go in, treat the paste as a leak and change that credential. Asking the chat to forget it is not a fix.
- The bot can still help from a redacted paste.

These are general public habits, not remarks about how this site stores or rotates its narration API key.

## Instances (generic descriptions of public reports cited in the research brief)

The lesson does not name the threads, give dates, or invent counts.

- Production database credentials pasted into a chatbot at work.
- An API key pasted into a chat and noticed only afterward.
- People asking whether the keys they handed over now need replacing.

Sources listed in the research brief: LayerX / The Hacker News 2026 enterprise AI usage report; public forum threads about production credentials and API keys pasted into chatbots.

## Made-up illustration

The failing-deploy paste, the `DATABASE_URL=postgres://admin:RealPassword@prod-db/app` line, and its `REDACTED` replacement are a generic teaching example. They describe no real system and no real incident.

## Not claimed

- No statistics, percentages, or named incidents.
- No biography, quotes, or stories about Clark.
- No company-internal names, bots, or systems.

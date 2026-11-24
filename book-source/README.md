# Silicon Valley C Players — a free OpenBook

*Silicon Valley C Players* is Clark Huang's autobiography: stories, lessons, and how to work with AI. It is a free **OpenBook** — a metaphor for Clark being an open book about this, and a process that works like open-source software.

This folder is the book's working source. The published preview lives at [https://clarkhuang.github.io/book/](https://clarkhuang.github.io/book/). The site and the book are one repository: [clarkhuang/clarkhuang.github.io](https://github.com/clarkhuang/clarkhuang.github.io).

The book is versioned like software. **v0** is in progress (a public teaser). **v1** is the first full draft, planned for 2027. Later editions are tagged the same way (`book-v1.1`, `book-v2.0`, …). See [VERSIONING.md](VERSIONING.md).

The editorial policy — how conflicting recollections are handled, and how claims and sources are tracked across editions — is at [https://clarkhuang.github.io/book/editorial-policy/](https://clarkhuang.github.io/book/editorial-policy/). Chapter ideas not yet in a draft are listed in [BACKLOG.md](BACKLOG.md). First-person guest stories, published under the contributor's own name, go in [guest/](guest/README.md).

## Fair warning

This is an **embellished fictional dramatization** that may or may not be based on true stories. The narrator, Charlie Hack, is a fictional character loosely inspired by the author. Every other name, character, company, school, and venue in the story chapters is fictional or used fictitiously; many characters are composites, and any resemblance is coincidental. Could that really have happened? That's the game.

The Foreword and Part Five (How to Work Now) are nonfiction: Clark's own opinions, with real, cited sources. Full text: [../DISCLAIMER.md](../DISCLAIMER.md). Naming rules: [NAMING-POLICY.md](NAMING-POLICY.md). Something affects you? [../TAKEDOWN.md](../TAKEDOWN.md).

## How a story becomes a chapter

1. Anyone can file a story, a correction, or a cleanup issue (or open a pull request). See [CONTRIBUTING.md](../CONTRIBUTING.md) and the “How to contribute” section of [AGENTS.md](https://clarkhuang.github.io/AGENTS.md).
2. Clark reviews it. The issue is labeled `needs-clark-review` until he decides.
3. If he wants it in the book, he adds the `approved` label. That label — or a `@claude` comment from Clark — is the only thing that starts an agent build.
4. An agent rewrites the affected chapter (and updates Markdown twins / `llms.txt` as needed) and opens a pull request against the `next-revision` branch. Agents never push to `main`.
5. Clark reviews the pull request and merges it into `next-revision`.
6. The published edition, and a new audiobook or videobook, are only rebuilt when Clark approves cutting that next revision. Previous editions stay up as named, tagged GitHub Releases.

## Who can contribute

Anyone can file issues and pull requests from day one. You do not have to wait for v1.

Only Clark can approve work, trigger the agents, merge pull requests, and cut a new edition.

When v1 is ready, Clark will also invite people who were around for the real-life inspiration, or related to him, to add their side of a story and any stories he may have forgotten. That outreach waits for v1 and his go-ahead. You do not need to wait for an invitation to file an issue now.

## License

Book text in this folder is [CC BY-NC-SA 4.0](LICENSE). Clark can change the license later.

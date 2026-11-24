# Contributing

This repository is both the public site ([clarkhuang.github.io](https://clarkhuang.github.io)) and the working source for Clark Huang's free OpenBook, *Silicon Valley C Players* — an **embellished fictional dramatization** that may or may not be based on true stories (see [DISCLAIMER.md](DISCLAIMER.md)).

**Anyone can take part.** You can open an issue, share a story, suggest a correction, or open a pull request from day one. You do not have to wait for v1. Most people will do it by pointing their AI agent at the site — that's welcome; you're still responsible for what your agent submits.

**Clark is the only gate.** An agent starts building only when Clark adds the `approved` label, or when he comments `@claude`. Nothing is published until he merges. Contributors cannot trigger the build agents.

Contributors and agents open PRs; only Clark merges to `main`; the site rebuilds from `main` via GitHub Pages; agent PRs target `next-revision`. Staging is the `next-revision` branch, at [https://clarkhuang.github.io/staging/](https://clarkhuang.github.io/staging/). Only Clark merges `next-revision` into `main`. The rebuild and QA flow is in [REBUILD.md](REBUILD.md).

## How to file an issue

Use one of these templates (also described in [AGENTS.md](https://clarkhuang.github.io/AGENTS.md)):

| Kind | What it is | Template |
|---|---|---|
| **Correction** | An edit to existing book text, or your side of a story already in the book | [Correction](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml) |
| **Feature / new story** | A new story, a story Clark may have forgotten, or a new chapter idea | [Share a story](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml) |
| **Refactor** | Cleanup or an improvement that does not change the facts of a story | [Refactor](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml) |
| **Site or lesson problem** | A broken link, video, caption, transcript, page, or agent surface (Markdown twin, `llms.txt`, `lessons.json`, MCP) | [Site or lesson problem](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=site-bug.yml) |
| **Chapter task** | Tracking work on a chapter (mostly for maintainers) | [Chapter task](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=chapter.yml) |
| **Takedown / privacy** | Something identifies you, or private/confidential info is here | [Takedown request](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=takedown-request.yml) — see [TAKEDOWN.md](TAKEDOWN.md) |

A good story issue is specific about *what happened* and *why it's funny or useful* — when (roughly), what you saw, which chapter if you know it. **Don't use real names of private people, companies, or venues.** Describe them by role ("my team lead," "a payments startup," "a bar in SoMa"). If you were there, say so.

## Guest stories (first-person, under your own name)

Most book contributions are fictionalized, and you are not named as a character. If you want to contribute a short first-person story published under your own name, that is a guest story.

- Put the file in [`book-source/guest/`](book-source/guest/README.md), following the format in that README.
- Open a pull request against `next-revision`.
- The file must include your own written consent to publish your name.
- Do not name other private people, and do not include confidential material.
- Clark still reviews and merges. A guest story is not published until he does.

## How a change lands

1. You file an issue (or open a pull request). It is labeled `needs-clark-review`.
2. Clark reviews it. If he wants it built, he adds the `approved` label.
3. An agent (Claude via GitHub Actions, or Grok for narration and video) fictionalizes and implements the change on a branch and opens a pull request against the `next-revision` branch — never against `main`, and never a direct push to `main`. If the work is an outside contribution that is landing on the site, that same pull request must add the credit on the [Contributors](https://clarkhuang.github.io/contributors/) page (see [Credit](#5-credit) below).
4. Clark reviews the pull request (including the pre-publication checklist) and merges it into `next-revision`. Staging at https://clarkhuang.github.io/staging/ updates automatically.
5. Only Clark merges `next-revision` into `main`. The live site then rebuilds from `main` via GitHub Pages, after the QA in [REBUILD.md](REBUILD.md). Previous editions stay available as tagged GitHub Releases. See [book-source/VERSIONING.md](book-source/VERSIONING.md).

## Pull requests

- Book, chapter, and OpenBook changes should target `next-revision`.
- Live lesson/site fixes may target `main` when they need to go out before the next book edition, but they still land only when Clark merges.
- Use the pull request checklist. Only Clark merges.
- After a merge to `next-revision` or `main`, check [REBUILD.md](REBUILD.md) and the staging URL before treating the change as done.
- **Every commit must be signed off** (see the DCO below): `git commit -s`.

## Contributor terms

By opening an issue, comment, or pull request with story or book content, or by signing off a commit, you agree to the following. If you don't agree, please don't submit.

### 1. Developer Certificate of Origin (DCO) sign-off

Every commit must include a `Signed-off-by: Your Name <you@example.com>` line (use `git commit -s`). By signing off, you certify the [Developer Certificate of Origin 1.1](https://developercertificate.org/): in short, that you wrote the contribution or otherwise have the right to submit it under this project's licenses, and that you understand the contribution and your sign-off are public and kept indefinitely. Content submitted through issue forms or comments is covered by the same certification.

### 2. Your promises (warranties)

For anything you submit, you confirm that, to the best of your knowledge:

- **It's yours to share.** You created it or have the right to submit it, and it doesn't copy anyone else's copyrighted work (no pasted articles, photos, or song lyrics you don't own).
- **It's not confidential.** It contains no trade secrets, no information covered by an NDA or employment/confidentiality agreement, no customer or user data, no security details, no deal or financial terms, and nothing from a non-public company system — including your current or former employers'.
- **It's not defamatory or invasive.** You aren't knowingly stating false facts about a real, identifiable person or company, and you aren't revealing anyone's private information (health, family, finances, sex life, addresses, contact details). No content about minors.
- **No real names of private people.** You don't name private individuals, and you describe real companies, schools, and venues generically. (Public sources in the nonfiction AI half may be named and cited.)
- **You're honest about what you saw.** Embellishment is the *author's* job at drafting time; your submission should be your genuine recollection, clearly marked if you weren't there.

### 3. Consent to fictionalization

You agree that Clark and the project's AI agents may **rename, fictionalize, combine into composites, exaggerate, shorten, rewrite, move in time or place, or not use** anything you submit, as part of an embellished fictional dramatization. You understand your story may appear as fiction and that characters may not match you or anyone else.

### 4. License to your contribution

You license your contribution under the project's licenses — book text under [CC BY-NC-SA 4.0](book-source/LICENSE), code under the repository's code license — **and** you grant Clark Huang a non-exclusive, perpetual, irrevocable, worldwide, royalty-free right to use, adapt, and publish your contribution in any edition or format of the book and its derivatives (including audiobook, videobook, print, and translations, whether free or paid). You keep your copyright.

### 5. Credit

If you'd like credit, tell us the GitHub handle to use on the [Contributors](https://clarkhuang.github.io/contributors/) page (or say you prefer not to be credited). Credit there is separate from the story: you won't be named *as a character*. The public list uses your GitHub display name when your profile has one, otherwise your handle. A name is never invented.

**Any outside contribution that lands on the site must be credited on the Contributors page in the same pull request.** Add an entry to [`sitegen/landed-contributions.json`](sitegen/landed-contributions.json) describing what landed, with links to the issue and/or pull request, and run `python3 scripts/build_credits.py`. Do not credit input that did not land. Use only the public GitHub display name and handle; do not add other personal details. Honor a “don't credit me” request.

### 6. Clark's editorial discretion

Clark decides what goes in, how it's told, and when it ships. Filing an issue or PR doesn't oblige him to use it, credit it in a particular way, or keep it. He may edit, hide, or delete issues, comments, and PRs, including to remove names or sensitive details.

### 7. Corrections and takedowns

If something here affects you, use the [Takedown request](https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=takedown-request.yml) template (label `takedown-request`) or the private route in [TAKEDOWN.md](TAKEDOWN.md). We acknowledge within 7 days and hide credible items while we review.

### 8. Code of conduct

Be kind. Punch up and inward, never down. No harassment, no doxxing, no "guess who this really is."

*These terms are a good-faith project policy and not legal advice; they may be updated, with changes noted in [CHANGELOG.md](CHANGELOG.md).*

## License

Book text in `book-source/` is offered under [CC BY-NC-SA 4.0](book-source/LICENSE), unless Clark changes that later. The CC license covers copyright only; it does not grant any rights in anyone's name, likeness, privacy, or publicity.

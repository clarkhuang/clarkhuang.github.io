# Versioning and branching

*Silicon Valley C Players* is versioned like software. Previous audiobook and videobook editions are kept as named, tagged releases. The next edition is only rewritten and released when Clark approves cutting that revision.

## Branches

| Branch | Role |
|---|---|
| `main` | The **published edition**. This is what GitHub Pages serves at [clarkhuang.github.io](https://clarkhuang.github.io). |
| `next-revision` | The **next edition in progress**. Approved corrections, new stories, and refactors accumulate here through pull requests. |

Agent pull requests target `next-revision`, never `main`. Agents never push to `main`.

Live lesson or site fixes that need to go out before the next book edition may still target `main`.

## How an edition is cut

1. Work lands on `next-revision` after Clark merges agent (or human) pull requests.
2. When Clark is ready for the next published edition, he approves cutting that revision (the manual “Cut edition” workflow, which only he can run).
3. Audiobook and videobook files are rendered for that edition only at this point — not on every merged story.
4. `next-revision` is proposed as a pull request into `main`. Clark merges it.
5. The edition is tagged, for example `book-v0.1` or `book-v1.0`, and a GitHub Release holds the audio and video assets for that tag.
6. Prior tags and releases stay up. The book page should link “Previous editions.”

Do not retag an old edition. If something in a published edition needs a fix, it goes into `next-revision` and ships in the next cut.

## Tags and releases

- Tags: `book-v0.1`, `book-v1.0`, `book-v1.1`, …
- Each GitHub Release attached to that tag keeps that edition's audiobook and videobook (and release notes)
- The site's current preview always reflects `main`

## Branch protection (later — do not enable yet)

Enabling this now would block in-flight direct pushes to `main`. When everyday site work no longer needs those pushes, require a pull request and a review on `main` with:

```bash
gh api -X PUT repos/clarkhuang/clarkhuang.github.io/branches/main/protection \
  -H "Accept: application/vnd.github+json" \
  --input - <<'EOF'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

Note: on a personal repository, requiring one approving review can prevent the author from approving their own pull request. If that gets in the way, use a ruleset that requires a pull request but sets `required_approving_review_count` to 0, or add a bypass for Clark. Requiring a pull request (no direct pushes) is the important part: nothing lands on `main` unless Clark merges it.

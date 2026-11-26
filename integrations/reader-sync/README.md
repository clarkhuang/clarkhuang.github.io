# Optional GitHub reader sync

The static site runs without accounts. A reader can opt in to sync versioned course progress using their GitHub identity. A person copying the site needs only GitHub for Pages. They provision Atlas Free and a small HTTPS service when they want account sync. Site visitors need only GitHub to use sync.

## Provision

1. Create a template copy and enable GitHub Pages with the existing Actions workflow. Confirm the static site, captions and guest bookmarks work on their own.
2. Sign up for Atlas, select Free, and create a project for the copy. Store private user state in reader_sync. Create separate staging and production databases, credentials and API origins. Grant each runtime role only the operations it needs. Restrict Atlas network access to the backend's supported egress addresses or private networking; verify the hosting plan supports that connection.
3. Serve the static site and /api under one custom origin via a reverse proxy, or use sibling hosts under a domain you control. On the default github.io address, use top-level redirects and a deliberate cross-origin session design validated on iPhone Safari. A third-party session cookie is an unreliable dependency. A portable fallback is to serve the optional signed-in reader and its API together on the backend origin while keeping anonymous Pages available.
4. Register a GitHub OAuth application with the exact callback URL for each environment. Ask for public identity only. Keep the client secret, Atlas connection URI and session secret in the backend secret store. Use the authorization-code flow with state, PKCE, exact redirect validation and a short-lived, single-use login transaction. Fetch GET /user on the server and use the returned numeric id for ownership. Discard the GitHub token after identity verification.
5. Issue an expiring, revocable opaque session via a Secure, HttpOnly cookie. Use SameSite appropriate to the chosen topology, CSRF protection and origin checks on writes. Derive the reader id from the session on every request. Accept only known preference keys, validated media IDs, media versions, bounded playback positions and bounded request sizes.
6. Add a Sign in with GitHub link and a local guest mode. On first sign-in offer to import this device's progress. Preserve the existing per-media version semantics. Use a revision check for overlapping updates from two devices; allow explicit rewind, replay and clear operations. Sign-out revokes the session and clears account-specific state from the device. Provide export and deletion.
7. Verify two independent accounts cannot read or write one another’s state, a username change preserves progress, a changed video starts fresh, and an Atlas outage leaves the course readable. Test fresh sign-in and cross-device resume on iPhone Safari. Recheck current free-tier quotas and suspension rules before deployment.

## Data ownership

Use one record per user and versioned media item, with a unique index on (githubUserId, mediaId, mediaVersion). Keep settings in a separate record per GitHub user. A progress record stores completion, position, revision and update time. Server-side access rules own the user key. Keep private reader data out of search indexes, public exports, GitHub issues and analytics.

## Current status

Design and provisioning checklist. Account sync is ready to advertise only after the live two-account and iPhone checks pass.

## Agent access

Suggested public instruction once implemented: “Read public lessons anonymously. When your reader asks you to use their saved settings or progress, start Connect an agent. Give the reader the site approval link. Continue after the site confirms the scopes they approved.”

The site issues a one-time pairing code with a short expiry. The reader opens the site in their browser, authenticates with GitHub, verifies the code and approves the named agent and requested scopes. Default to progress:read; request progress:write or settings:write when needed. Enforce each grant on the API. Rate-limit code attempts and polling. Bind redemption to the initiating client using a high-entropy device secret, consume each grant once, and support expiry and revocation. Store the reader ID and agent grant ID on writes for attribution. Give the agent a site-scoped credential and provide a Connected agents screen. The public read-only MCP remains usable anonymously.

## Learning profile

Start with the reader's chosen goal, hardware and unified memory, experience level, preferred lesson format and available study time. Make each field optional and editable. Track watched position separately from lab attempts, the learner's own confidence, and an exercise result with supporting evidence. A watched video alone cannot establish mastery. Show the evidence and reason behind each suggested next lab, let readers dismiss or correct it, and let an agent propose profile changes for approval. Keep profile:read, progress:write and profile:write independent. Carry completed prerequisites forward when a lesson is revised, while marking changed material for review. Use the smallest set of signals that improves the next learning decision.

### Run the backend

Install requirements.txt into a virtual environment. Configure READER_ENV (staging or production), READER_ORIGIN (the HTTPS origin of this service), GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, SESSION_SECRET and MONGODB_URI through the runtime's secret manager. Use independent OAuth applications, Atlas database users and signing secrets. The service derives its database name from READER_ENV. Atlas must enforce the same boundary with a role scoped to that single database. Set the redirect in GitHub to READER_ORIGIN followed by /callback. From this directory run gunicorn 'app:create_app()' behind HTTPS. Never enable access logging of callback query strings or pairing secrets. Run python -m unittest with mongomock installed for the local isolated tests.

The backend serves its own top-level profile and approval screens. Agent clients POST a name and scopes to /agent/pair, show approval_url and user_code to the reader for comparison, retain device_secret privately and POST it to /agent/redeem after approval. If the response is lost, repeat redemption with the same device secret within the original five-minute window. Use the returned bearer credential for the permitted API only. Current implementation covers profile editing, progress reads/writes with revision checks, OAuth login, agent approval and revocation. Automatic Pages player integration, account export/deletion and live verification are pending.

### Stage the reader service

Build the container from the repository root with `docker build -f integrations/reader-sync/Dockerfile -t reader-sync .`. Deploy it on an HTTPS container host with network access to Atlas. Configure the six settings listed above through the host. Use the assigned HTTPS origin in both READER_ORIGIN and the GitHub callback registration. The server listens on PORT (default 8080). Deploy this same revision of the service and Pages together when media versions change.

The pull request workflow runs isolated tests, repeats the core reader tests against a disposable MongoDB 8 service, and builds the image. Live acceptance requires signing in with two independent accounts, resuming the same lesson on another device, and verifying the staging database user cannot access the production database. Register a separate production OAuth app before enabling the live sign-in link.

For a free staging deployment on Render, create a Blueprint for this repository and select `integrations/reader-sync/render-staging.yaml` as its path once the changes reach next-revision. Customize the service name for your copy. Set READER_ORIGIN to its exact public HTTPS origin and use that origin plus /callback in the staging GitHub OAuth app. Allowlist the service region’s outbound ranges in Atlas and give its Atlas user access only to reader_staging. Enter credentials directly into the host’s secret fields. The health check verifies database reachability without exposing data. Free staging may need to wake up on the first visit.

### Agent discovery

Fetch `assets/reader-endpoints.json` from the static site and select the environment the reader is using. A null origin means account access has not been enabled there. At a configured origin, fetch `/.well-known/reader-sync.json` for pairing and API routes. GET /api/catalog lists the exact media keys and durations accepted by this deployment without exposing any reader state. Request only the scopes needed for the task. GET /api/progress requires progress:read. For a write, send PUT to that route with item, revision, position (seconds), and completed using progress:write. Start an unseen item at revision zero. A conflict returns 409; reload current progress with the reader’s permission before deciding whether to write again.

# Software Engineering 301 • Run your own AI studio

In 101 you took one change from plan to proof. In 201 you connected those changes into a system. In 301 you own the computer that runs the system. The graduation exercise is to take a real course correction from an issue to a verified page, then explain what it cost and what happens if the machine stops halfway through.

Start with a job you could use on the computer you already have. For example, a small nonprofit could try producing a captioned training clip for new volunteers. Record how long one scene takes, what it costs, and whether a volunteer can follow the instructions. Those observations give you a reason to keep the setup, change the model or try a larger machine.

This is the playbook for our February 2027 build. The hardware is ordered. Model choices are candidates. We will add measured throughput, power, usable context and accepted patches per hour after the machine arrives.

## Lesson 1

[Size the model, then run the first endpoint](https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/index.md) is the first video lesson. It covers the weight floor, the first local endpoint, and a copy-paste install prompt for a Mac with Apple silicon or a Windows or Linux PC.

## Already running local AI?

Already running models on your own hardware? Tell us what you tried, what broke, and what you would do differently. [Share your field notes](https://github.com/clarkhuang/clarkhuang.github.io/issues/148). Include your hardware, model, runtime and one reproducible result.

## Build along now on a 48 GB M4 Pro MacBook Pro

Start on the laptop with the editor, site checkout, job queue and model gateway you intend to keep using after February. Choose a small coding model so the browser, editor and tests have room to run. Qwen2.5-Coder-7B-Instruct in a four-bit build is a reasonable first fixture. If you already have gpt-oss-20b working, run it against the same tasks as a comparison.

| Stage | On the 48 GB laptop now | On the 512 GB Studio in February |
|---|---|---|
| First request | Install llmster, load one model, run a short streamed answer and a structured tool call. Record the revision and memory use. | Restore the pinned configuration and replay both requests before installing larger models. |
| Personal coding | Point OpenCode at a stable code-fast gateway alias. Work one real issue in a disposable worktree. Record time to an accepted patch. | Point the alias at Qwen3-Coder-Next. Keep using the laptop as your editing client. Compare the patch on the same base commit. |
| Site worker | Keep a single queued job. Build a staging preview, interrupt it, resume it, and verify one change. | Move the durable queue and worker to the wired Studio. Rehearse reboot recovery before enabling unattended jobs. |
| Media and interviews | Render one short scene with captions. Record one consented interview sample and check its timestamps. Keep recordings private. | Restore the approved assets, render the full lesson, and test concurrent editing while the render runs. |
| Serving capacity | Meter a local test key and reconcile a cancelled stream. Save the fixtures and a sample invoice. | Load the reviewer alongside the coder. Measure personal latency under a pilot company workload before offering a capacity commitment. |

**Laptop finish line:** one testable patch, one resumable job, one captioned scene, and a private configuration repository containing aliases, pinned versions and replay fixtures. Keep credentials in Keychain and copy private media using encrypted storage. On the Studio’s first login, restore those assets, reproduce the laptop baseline, then run Lab 10. This gives both machines a common starting point for measuring the benefit of the upgrade.

## Choose your lab

US hardware prices checked November 26, 2026. The featured price is from our order. The configured alternatives use retailer listings. Cluster totals exclude cables, switches, tax, displays and backup storage.

| Lab | Compute | Price | First assignment |
|---|---|---:|---|
| Use what you own | Existing Apple silicon Mac | $0 incremental | Run the harness and an issue replay. Try a 3B–8B four-bit model if memory permits. |
| Entry Mac mini | M6 base model | From $899 | One small coding model, one user. Use short prompts and run builds sequentially. |
| Mac mini Pro | M5 Pro base, 15-core CPU, 16-core GPU, 24 GB, 512 GB | From $1,699 | Try a 7B–14B four-bit coder. Verify a patch and record a first benchmark. |
| Single 64 GB mini | M5 Pro, 18-core CPU, 20-core GPU, 64 GB, 1 TB, 10GbE | $3,299 | Start with a 30B-class four-bit coder. Trial Qwen3-Coder-Next at short context once memory is measured. |
| Two minis | 2 × the 64 GB configuration; 128 GB aggregate | $6,598 | Keep one coder responsive while the other reviews, transcribes or builds. |
| Single 256 GB Studio | M5 Ultra, 36-core CPU, 80-core GPU, 256 GB, 2 TB | $11,299 | Trial a 320B-class four-bit reviewer alone. Measure context headroom before adding a second resident model. |
| Four minis | 4 × the 64 GB configuration; 256 GB aggregate | $13,196 | Split independent jobs across four workers. Then measure whether sharding one supported model is worthwhile. |
| **Our February build** | **M5 Ultra Studio, 36-core CPU, 80-core GPU, 32-core Neural Engine, 512 GB unified memory, 8 TB SSD, 10GbE, six Thunderbolt 5 ports** | **$25,799** | Keep an interactive coder and a reviewer resident, then add a media job and measure contention. |

For a new purchase aimed at one large model, the quoted 256 GB Studio saves $1,897 over four configured minis before networking. For a lab that grows one machine at a time, the minis let you buy the next worker when there is a queue for it. Four idle minis earn the same revenue as one idle Studio.

[Apple starting prices](https://www.apple.com/newsroom/2026/09/the-new-mac-mini-and-mac-studio-are-available-today/) · [Mac mini specifications](https://www.apple.com/mac-mini/specs/) · [Configured mini price](https://www.bhphotovideo.com/c/product/1997768-REG/apple_mm_m5p_56_mac_mini_m5_pro.html/accessories) · [Configured Studio price](https://www.bhphotovideo.com/c/product/1997827-REG/apple_ms_m5u_16_mac_studio_m5_ultra.html/overview)

## 1. Size the model before downloading it

Estimate the raw weight floor as total parameters × bits per weight ÷ 8. An 80B four-bit model starts at 40 GB. A 320B model starts at 160 GB and a 480B model at 240 GB. The active-expert count affects work per token. All resident expert weights still take memory. Add quantization metadata, runtime buffers, macOS, other processes and a context cache per active session. A 240 GB raw floor makes the 480B candidate a poor everyday choice on a 256 GB host.

On our Studio, start with Qwen3-Coder-Next MLX 4-bit for code and GLM-5.3-Flash MLX 4-bit for review. Keep DeepSeek-V4-Flash MLX 8-bit and Qwen3-Coder-480B MLX 4-bit as challengers. Record the upstream license, conversion revision, download size, loader and tool template for each. Open weights and the software license for a serving runtime are separate considerations.

**Lab:** load the small model first. Run the same prompt at 4K, 16K and 32K contexts. Record peak memory, swap growth, time to first token and output tokens per second. Stop increasing context when interactive latency misses your target.

[Qwen coding model](https://huggingface.co/Qwen/Qwen3-Coder-Next) · [GLM Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) · [DeepSeek MLX conversion](https://huggingface.co/mlx-community/DeepSeek-V4-Flash) · [480B MLX conversion](https://huggingface.co/mlx-community/Qwen3-Coder-480B-A35B-Instruct-4bit)

## 2. Build the first endpoint

On first login, record the machine inventory and free space. Set up a service account, wired networking, encrypted backups and a recovery procedure. Install a pinned llmster runtime and one supported MLX model. Bind inference to loopback. Send a completion, a streaming request, a cancelled request and a structured tool call. Save the request fixtures and outputs with the model manifest. A successful chat alone does not establish tool compatibility.

## 3. Put a router in front of the models

Connect OpenCode to LiteLLM through an OpenAI-compatible base URL. Give clients stable aliases such as code-fast and review. Map each alias to a pinned runtime and exact model. Use PostgreSQL for usage and job state. Give each app its own key. Start with one interactive slot and one background job. Run the same coding task while a batch is active. Keep the settings that meet your measured response-time target.

[Serving daemon](https://lmstudio.ai/docs/developer/core/headless) · [Gateway keys](https://docs.litellm.ai/docs/proxy/virtual_keys) · [Coding client](https://opencode.ai/docs/providers/)

## 4. Choose how the minis cooperate

For independent jobs, connect each mini to Ethernet and set up one inference endpoint per machine. Route at the request boundary. With four nodes, start with interactive coding, review, editorial work and rendering respectively. Change assignments if one queue grows. An individual model must fit on the node serving it.

For one model spread across machines, start with two minis, direct Thunderbolt 5 cabling, matching compatible macOS and runtime releases, and an EXO-supported model. Follow the runtime’s RDMA setup guide and verify peer discovery and actual transport. Each node holds a shard plus its own OS and buffers. Verify the topology supported for four nodes before buying cables. Compare one-node versus two-node latency with the same model that fits both, then try a larger supported model across the pair. Test a node disconnect and recovery. Expand to four only after the measurements justify it.

**Decision:** choose sharding to fit a specific model. Choose independent workers when the queue already contains independent jobs. Measure completed tasks per hour for both.

[EXO setup and supported transports](https://github.com/exo-explore/exo)

## 5. Give the coding worker a finish line

Clone the full site history. Reproduce a known issue in a clean worktree. A durable worker claims an approved issue, stores the base commit and attempt number, edits the canonical source, regenerates only the relevant surfaces and runs the repository checks. Save the diff and results, then open staging. After release verify the deployed URL against the intended revision. Kill the worker mid-build and restart it. Passing means one change and one issue update. Respect issues reserved for Clark’s decisions and private authorship.

## 6. Produce one lesson people can use

Start with one observable learning objective. Write a worked example and an exercise that fails in a recognizable way. Write a facts file that distinguishes sourced claims from writer-added lines. Have a second reviewer check the script before narration. Cache narration by scene so a one-line correction only requires one new clip. Reuse the repository’s lesson-sources build scripts for slides, narration, FFmpeg video, captions and transcript. Stamp changed media versions, run the site check and play the beginning, middle and end on a phone. Check that a learner can perform the exercise using the Markdown twin alone. Archive narration inputs so a retry can reuse approved audio.

## 7. Interview the author

Pick one unresolved chapter question. A mobile voice client uses a short-lived Grok Voice session; a Bland telephone entry point can call the same narrow job API. Use a standard assistant voice for live conversations. Reserve Clark’s cloned voice for approved, published narration. Ask one question at a time, checkpoint the answer, and resume after interruption. Store consent, original audio, transcript and timestamps in private storage. The writing worker produces an excerpt-to-source map and flags uncertain names or dates for the next interview. Only approved material goes into the public repository.

[xAI voice API](https://docs.x.ai/developers/model-capabilities/audio/speech-to-speech) · [Bland custom tools](https://www.bland.ai/integrations/custom-api)

## 8. Meter a company pilot

Give one app a revocable inference-only key with a budget, rate limit and allowed model list. Keep company data separate from interviews and public-site workers. Record request ID, model revision, input/output tokens, status, latency and price version. Reconcile streaming, cancellation, retries and missing usage before generating a monthly shadow invoice. Compare its price and quality to hosted inference. Require a commercial-use license review and independent company approval before billing.

For our machine, $25,799 divided by 36 months is $716.64 per month for hardware alone. Add measured electricity, storage, support and an allowance for downtime. A reserved-capacity agreement needs a defined service window and a recovery plan. Track successful work per dollar alongside tokens.

## Prove one improvement on the laptop

To test recursive self-improvement, choose one reported lab failure and save a failing example. Have a local model propose a correction, then ask an independent reviewer to run both the old and revised instructions from scratch. Record the outcome, elapsed time, model revision and token usage. Keep the example as a regression test. If the correction calls for new narration, send Clark the ticket and timestamp for validation.

Replay the same case on the 512 GB Mac Studio in February. Compare a smaller local model with a frontier-class open-weight candidate on accepted fixes per hour, memory use and cost. Use those results to decide which models can serve member applications while site maintenance is running.

## 9. Rehearse the build and test the update loop

Use the hardware you have today. Save a small replay set from Labs 1–8: a coding issue with a known acceptance test, a review with a planted error, a captioned lesson, a consented interview excerpt and a metered request with a known token count. Record the model, quantization, runtime, context, concurrency and pass criteria. Restart the worker mid-job and restore a backup. Someone else should be able to repeat the run and explain any difference.

Now change one thing. Try a second model or runtime on the same fixtures. Compare accepted work per hour, time to first token, peak memory and cost per accepted result. Record failures and sample counts. A model that improves interactive coding on the Studio may still be a poor choice for a 24 GB mini. Write a separate verdict for each affected budget tier.

**Lab result:** a replay kit, a baseline scorecard and a staging preview of one evidence-backed lesson revision. Force a failed media check and verify that the previous edition stays available.

## 10. Build the actual studio • February 2027 field report

**Status: awaiting hardware.** This final lab is reserved for the first real build on our 512 GB M5 Ultra Mac Studio. The November plan is our starting hypothesis. When the machine arrives, we will publish what we installed, what changed by February and what the machine actually delivered.

1. **Take a fresh inventory.** Record the delivered configuration, actual cost, macOS version and setup from first login. Date the report. Recheck model releases, runtime support, licensing and hardware prices against primary sources. Preserve the November figures as the historical comparison.
2. **Challenge the original picks.** Run the Lab 9 fixtures against the original candidates and the strongest February alternatives that fit. Log exact revisions, quality, cold and warm latency, throughput, memory pressure and measured power. Repeat with company traffic and a video render running. Mark any untested budget tier explicitly.
3. **Run the site for real.** Take one open issue through coding, independent review, staging and a verified release. Produce a playable lesson with captions. Turn a consented interview into a private chapter draft with timestamped evidence. Reconcile a company pilot request to its shadow invoice. Interrupt one job and demonstrate recovery without duplicate work.
4. **Reconcile all ten labs.** Publish a table with one row per decision, showing the November recommendation, February result, evidence and the resulting lesson or video revision. Include the cases where the original choice won. Link the public commit, benchmark fixtures, captioned build video and recovery record. Keep the interview and customer records private.

### How the course will stay current

After commissioning, the planned maintenance worker will watch upstream model and runtime releases, reported lesson failures, and changes to cited prices. Each signal opens a deduplicated review job for the affected lesson and hardware tier. A price correction can use a dated vendor listing. A model or architecture change must beat the incumbent on the lesson’s stated objective in repeat runs while still passing its quality, compatibility and recovery checks. Record a mixed result as a tradeoff.

When the evidence changes a recommendation, the worker will revise the canonical lesson, regenerate its HTML and Markdown, and identify every video segment that teaches the superseded approach. It will rebuild affected narration, visuals, captions and transcripts, stamp the new media version, and test playback and links in staging. Run the media-version and site checks. After Clark authorizes the public change, open a PR targeting next-revision. Clark merges to staging. Check playback, captions, mobile layout and the watched/resume behavior there. Clark authorizes and merges each production release. The worker then verifies the live revision and records the previous edition for rollback. Each changed lesson will show **last tested**, **tested on** and **what changed** so a reader can decide whether to rerun the lab.

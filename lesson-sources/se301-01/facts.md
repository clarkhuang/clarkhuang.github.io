# Facts and sources: SE 301 Lesson 1, Size the model, then run the first endpoint

Script: `se301-01-first-endpoint.json` (13 scenes, 602 spoken words). Estimate 232 seconds at 2.6 words/second, about 3:52. Recorded SE 201 lessons ran nearer 2.8 words/second, which would land closer to 3:35. Measure after narration. Nothing in this folder has been narrated.

No statement in the script is about Clark Huang's life, employers, or a measured result from the February 2027 machine. The machine is described the way the playbook describes it: ordered, not yet the source of throughput numbers.

## Verified from the SE 301 playbook

Source: https://clarkhuang.github.io/software-engineering-301/index.md (this repository, `software-engineering-301/index.md`). Prices on that page were checked November 26, 2026. This lesson does not repeat the price table.

| Claim in the lesson | Where it is said | Playbook basis |
|---|---|---|
| Weight floor = parameter count × bits per weight ÷ 8. An 80B four-bit model starts at 40 GB. 320B starts at 160 GB. 480B starts at 240 GB. | Scene 03, on-screen cards | "1. Size the model before downloading it." The playbook uses those three examples. |
| The floor is weights only. Add quantization metadata, the runtime, the operating system, other processes, and a context cache per session. | Scene 04. Speech says "metadata" for quantization metadata. | Same section. |
| A 240 GB raw floor is a poor everyday choice on a 256 GB host. | Scene 04 | "A 240 GB raw floor makes the 480B candidate a poor everyday choice on a 256 GB host." |
| On a Mac you already own, try a 3B–8B four-bit model if memory permits. | Scene 05 | "Use what you own" row. |
| First fixture on the 48 GB laptop: Qwen2.5-Coder-7B-Instruct, four-bit. | Scene 05 | "Build along now on a 48 GB M4 Pro MacBook Pro." |
| If gpt-oss-20b is already working, compare it. Do not download it in order to start. | Scene 05 | "If you already have gpt-oss-20b working, run it against the same tasks as a comparison." The "don't download it in order to start" line is the lesson's instruction for that sentence. See writer-added. |
| Studio candidates, not measurements: Qwen3-Coder-Next MLX 4-bit for code, GLM-5.3-Flash MLX 4-bit for review. Challengers: DeepSeek-V4-Flash MLX 8-bit and Qwen3-Coder-480B MLX 4-bit. | Scene 06 | "On our Studio, start with…" The page also says model choices are candidates, and measured throughput, power, usable context, and accepted patches per hour come after the machine arrives. |
| The Studio in that plan has 512 GB. The hardware is ordered. | Scene 06 | "Our February build" row and the opening status. The spoken line says "ordered" and does not quote the $25,799 price. |
| Run the same prompt at 4K, 16K, and 32K. Record peak memory, swap, time to first token, and output tokens per second. Stop when latency misses the target. | Scene 07 | Lab under section 1. |
| Record the machine and free disk. One pinned llmster runtime and one model. Bind to loopback. Send a completion, a stream, a cancel, and a structured tool call. A chat reply does not prove tools. | Scene 08 | "2. Build the first endpoint." "A successful chat alone does not establish tool compatibility." |
| Next lab is a router and stable aliases such as code-fast and review. | Scene 13 | "3. Put a router in front of the models." |

The script does not say the 48 GB machine is an M4 Pro, and it does not say the Studio chip is an M5 Ultra. Those details are on the playbook page. They are not needed for this lesson's rule. Leaving them out is not a denial of the playbook.

## Verified from public docs (install mechanics only)

Checked against the live docs while this lesson was drafted (November 27, 2026). These sources support the copy-paste prompt. The narration names the runtimes. It does not quote install commands.

| Claim the prompt relies on | Source |
|---|---|
| llmster is LM Studio's headless daemon. Mac/Linux install: `curl -fsSL https://lmstudio.ai/install.sh \| bash`. Windows: `irm https://lmstudio.ai/install.ps1 \| iex`. Then `lms daemon up`. | https://lmstudio.ai/docs/developer/core/headless |
| `lms server start` defaults to loopback. `--bind 127.0.0.1` is the localhost value. Any other bind is wider than this lesson allows. Default port used in the OpenAI-compat examples is 1234. | https://lmstudio.ai/docs/cli/serve/server-start and https://lmstudio.ai/docs/developer/openai-compat |
| `lms get` / `lms load` are the documented CLI downloads and loads. The docs' own example model is `openai/gpt-oss-20b`, which is why the playbook's comparison name is a real LM Studio id. This lesson does not tell the agent to download it. | https://lmstudio.ai/docs/app/basics/lmstudio-vs-llmster-vs-lms |
| Chat completions: `POST /v1/chat/completions`. | https://lmstudio.ai/docs/developer/openai-compat |
| `mlx-lm` installs with `pip install mlx-lm` and serves an OpenAI-style API with `mlx_lm.server`. The project's example listens on localhost port 8080. The server doc says it is not recommended for production. | https://github.com/ml-explore/mlx-lm and https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md |
| `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` is a public MLX conversion of `Qwen/Qwen2.5-Coder-7B-Instruct`. | https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit |
| Ollama's local OpenAI-compatible base is `http://localhost:11434/v1`. `ollama pull` then `POST /v1/chat/completions`. The library tag `qwen2.5-coder:7b` exists. | https://docs.ollama.com/api/openai-compatibility and https://ollama.com/library/qwen2.5-coder:7b |
| Qwen2.5-Coder-7B is listed at 7.61B parameters. Apache 2.0 applies to that size on Qwen's model table. The lesson narration does not state the license or the 7.61B count. The prompt shows the arithmetic and the URL. | https://qwenlm.github.io/blog/qwen2.5-coder-family/ |
| xAI text-to-speech: `POST https://api.x.ai/v1/tts`, voice id, language, speed. `[pause]` is a documented speech tag. The lesson's `<emphasis>` and `<slow>` tags are the tags this site's narration pipeline already allows. | https://docs.x.ai/developers/model-capabilities/audio/text-to-speech and the SE 201 `BUILD.md` files |

## Writer-added phrasing for Clark's yes/no

These lines are teaching instructions written for this lesson. They are not quotes, and they are not new measurements.

| Line | Scene or file | Why it is marked |
|---|---|---|
| Second person throughout. No "I". | All scenes | The playbook is not spoken in the second person. This avoids putting a biography in Clark's voice. |
| Quiz: product name, sticker memory, or the floor with room left. Answer: the floor. "The sticker is the whole machine." | Scene 02 | A teaching question. The sticker point restates the playbook's "add the OS and other processes." It is not a quote. |
| "Don't download it in order to start." | Scene 05 | The playbook says to compare gpt-oss-20b if you already have it. It does not forbid a download in so many words. |
| "Today, start small." | Scene 06 | The playbook says to load the small model first in the sizing lab, and to install one model on first login. "Start small" is that instruction in shorter words. |
| "Silence is not a yes." You name the action. | Scene 10 and the prompt | A safety rule for the agent. Not in the playbook. |
| The prompt's five on-screen steps. | Scene 09 | A summary of the prompt, written so it can be read on a 1920×1080 frame. |
| Windows and Linux path, Ollama, and VRAM instead of unified memory. | Prompt, scene 09 | The playbook's named machines are Apple silicon. LM Studio's headless docs cover Linux and Windows. Ollama is the PC OpenAI-compatible path, from Ollama's own docs. A PC tier is this lesson's application of the same weight floor, not a new hardware row. |
| About 4 GB for an 8B-class four-bit floor (8 × 4 ÷ 8), and about 3.8 GB for 7.61B (7.61 × 4 ÷ 8). | Prompt only. Not spoken. | Arithmetic in the playbook's formula. Not a measured download size or a runtime memory number. |
| "Say yes only to the install you understand. Keep the reply. That reply is your baseline." | Scene 12 | The exercise. The playbook's laptop finish line is larger (a patch, a job, a scene, a private config). This lesson stops at the first endpoint. |
| Rule 1 wording. | Scene 11 and the lesson page | A standing instruction written for agents. Not a quote. |

## Not claimed

- No tokens per second, watts, cold-start time, or "fits in X GB of VRAM" from a third-party table. Those numbers were in front of the writer and were left out.
- No ranking of Qwen, GLM, DeepSeek, or gpt-oss against each other.
- No statement that the Ollama tag `qwen2.5-coder:7b` is four-bit. The prompt tells the agent to record the quant the tool prints.
- No statement that a smoke-test reply proves tool calling. Scene 08 says the opposite. The prompt's first request is chat-only and says so.
- No price, no electricity cost, no "our order" dollar figure.
- The cancellation replay is a learner exercise. Record observations from the local server when you run it.

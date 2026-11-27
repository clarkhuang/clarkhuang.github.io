# Size the model, then run the first endpoint

_Software Engineering 301 · Lesson 1_

HTML page: https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/index.md (plus https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

- Series: [Software Engineering 301](https://clarkhuang.github.io/software-engineering-301/index.md)
- Series agents file: [https://clarkhuang.github.io/software-engineering-301/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/AGENTS.md)
- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)
- This folder’s agents file: [https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/AGENTS.md)
- Video (MP4): https://clarkhuang.github.io/videos/se301-01-size-the-model-run-the-first-endpoint.mp4
- Duration: 3:34 (214.7 seconds)
- Published: Nov 26, 2026
- Poster: https://clarkhuang.github.io/videos/posters/se301-01-size-the-model-run-the-first-endpoint.jpg
- Captions (WebVTT): https://clarkhuang.github.io/videos/se301-01-size-the-model-run-the-first-endpoint.vtt
- How it was built (script source, facts, install prompt): https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se301-01

## Chapters

- [0:00] The question
- [0:22] The floor
- [0:41] Headroom
- [0:56] The ladder
- [1:18] Candidates
- [1:43] Context
- [1:57] The endpoint
- [2:20] The prompt
- [2:41] The stop
- [3:02] The rule
- [3:17] Your turn
- [3:27] Next

## The lesson

Before you download a local model, size it to the machine you have. The weight floor is the parameter count times the bits per weight, divided by eight. That number is weights only. Add the runtime, the operating system, your other programs, and a context cache. On the playbook's 48 GB laptop, the first fixture is Qwen2.5-Coder-7B-Instruct in a four-bit build. Larger names for the ordered 512 GB Studio are candidates, not measurements. Then run one local endpoint on loopback and keep the reply. A chat reply does not, by itself, prove tool calls. The page includes one copy-paste prompt for a Mac with Apple silicon and for a Windows or Linux PC. The agent stops for a named yes before an admin install, a firewall change, or a sign-in. It does not take secrets, and it does not send local files off the machine.

## The rule

Before a model is downloaded, write three things where the agent can read them: the weight floor, the memory you can spare, and the check that says the endpoint answered. If a step needs admin rights, a firewall change, or a sign-in, stop and ask. Do not paste secrets, and do not send local files off the machine.

This rule is written so an AI agent can follow it as a standing instruction.

## What this lesson does not claim

- The 40 GB, 160 GB, and 240 GB figures are weight floors from the playbook's formula. They are not measured file sizes.
- Qwen3-Coder-Next, GLM-5.3-Flash, DeepSeek-V4-Flash, and Qwen3-Coder-480B are the playbook's November candidates for the ordered Studio. Throughput, power, and usable context are not measured yet.
- The playbook's named machines are Apple silicon. The Windows and Linux path in the prompt applies the same weight floor, using LM Studio's headless docs or Ollama's local OpenAI-compatible API.
- The prompt's first request is one chat completion. The playbook's endpoint lab still asks for a stream, a cancelled request, and a structured tool call after that. A chat reply does not prove tool calls.
- gpt-oss-20b is a comparison only when it is already installed. The prompt does not download it.

## On-screen summary of the install prompt

The prompt, pasted into a computer-use or terminal agent, does five things:

1. **Read the machine.** OS, CPU, GPU, memory, free disk
2. **Pick a tier.** From this ladder. Show the arithmetic.
3. **Install one runtime.** llmster, MLX on Apple silicon, or Ollama
4. **Send one request.** To the local endpoint. Read the reply.
5. **Stop for you.** Name the action. Wait for a yes.

It waits for a named yes before an admin install, a firewall change, or a sign-in. Silence is not a yes. It does not take secrets, and it does not send local files off the machine.

## Copy-paste install prompt

The same text is in `lesson-sources/se301-01/install-prompt.md`. Paste it as a whole.

# Copy-paste prompt: first local endpoint (macOS Apple silicon, Windows, Linux)

Paste this whole prompt into a computer-use agent or a terminal agent on the machine where the model should run. It is the install prompt for Software Engineering 301, Lesson 1. The playbook is https://clarkhuang.github.io/software-engineering-301/index.md. Lesson page: https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/index.md.

You are a computer-use or terminal agent setting up one local OpenAI-compatible endpoint for the person at the keyboard. Work only on this machine. Do the read-only inspection first. Then stop and wait whenever this prompt says to wait.

## Hard limits

- Do not paste secrets into the chat. That includes API keys, tokens, passwords, cookies, SSH keys, cloud credentials, and the contents of `.env` files or keychains.
- Do not send local files, repositories, prompts, or model outputs off this machine. Do not upload a folder. Do not call a hosted model API as a fallback.
- Do not bind the server to `0.0.0.0`, a LAN address, or a public address. The endpoint stays on loopback (`127.0.0.1`).
- Do not change the firewall, open a port, or disable a security prompt.
- Do not sign in, create an account, or accept a license click-through. If a download asks for a login, stop and show the person the prompt. Do not type credentials.
- Do not run `sudo`, an installer, `curl | sh`, `curl | bash`, `irm | iex`, a system package install, or anything that changes the machine, until the person has replied in this chat with an explicit yes that names the action. Silence, an earlier yes, or "go ahead" without the action name is not enough.
- If a step is ambiguous, stop and ask. Do not guess a model id, a port, or a bind address.

## 1. Read the machine, and change nothing

Inspect the operating system, CPU, GPU (if any), unified memory or VRAM, and free disk space. Use read-only commands. Print the results in the chat. Do not print environment variables.

- macOS: `sw_vers`; `sysctl -n machdep.cpu.brand_string`; `sysctl -n hw.memsize`; `sysctl -n hw.optional.arm64` (Apple silicon is `1`); `df -h /`. Memory in use: Activity Monitor is fine if you already have a GUI; otherwise say you only have total memory, not free memory.
- Linux: `uname -srm`; `lscpu` (model name); `free -h`; if `nvidia-smi` exists, `nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv`; `df -h /`.
- Windows (PowerShell): `Get-CimInstance Win32_OperatingSystem | Select Caption, Version`; `Get-CimInstance Win32_Processor | Select Name`; `Get-CimInstance Win32_ComputerSystem | Select TotalPhysicalMemory`; `Get-CimInstance Win32_VideoController | Select Name, AdapterRAM`; `Get-PSDrive -PSProvider FileSystem`.

Also note whether `lms`, `llmster`, `ollama`, or `mlx_lm.server` is already on `PATH`. Do not start them yet.

## 2. Choose a tier, then wait

Apply the playbook's weight floor before any download. Floor in bytes = parameter count × bits per weight ÷ 8. An 80B four-bit model starts at 40 GB of weights. A 320B model starts at 160 GB. A 480B model starts at 240 GB. Weights are not the whole bill. Say what you are holding back for the operating system, other programs, and one short context.

This lesson downloads one small model, or it downloads nothing.

| What you measured | Playbook tier | What you may propose |
|---|---|---|
| You cannot show room for about 4 GB of four-bit weights (an 8B-class floor: 8 × 4 ÷ 8) plus the operating system and a short context | Use what you own. Memory does not permit the fixture. | Do not download. Stop. |
| Apple silicon, and a 3B–8B four-bit model fits | Use what you own | Propose Qwen2.5-Coder-7B-Instruct in a four-bit build. If that floor does not fit, stop. Do not invent a smaller model name. |
| About 48 GB unified memory | The playbook's laptop fixture | Same 7B four-bit fixture. Leave room for the browser, editor, and tests. |
| 24 GB, 64 GB, 256 GB, or 512 GB unified memory | Later labs try larger models | Still propose only the 7B four-bit fixture today. |
| Windows or Linux with a discrete GPU | The playbook's machines are Apple silicon. Use the same floor against free VRAM. | Same 7B four-bit fixture, if free VRAM covers the floor plus a short context. |
| Windows or Linux, CPU only | Say so. It can be slow. | Same fixture only if free RAM covers the floor plus the OS and a short context. Otherwise stop. |

Name these as candidates, not as downloads, and not as measured results. The playbook has not published throughput, power, or usable context for them yet:

- 512 GB Studio plan: Qwen3-Coder-Next MLX 4-bit for code, GLM-5.3-Flash MLX 4-bit for review. Challengers: DeepSeek-V4-Flash MLX 8-bit, Qwen3-Coder-480B MLX 4-bit.
- If `gpt-oss-20b` is already installed, offer it later as a comparison on the same prompt. Do not download it in order to start.

Qwen's published card lists 7.61B parameters for Qwen2.5-Coder-7B (https://qwenlm.github.io/blog/qwen2.5-coder-family/). At four bits that floor is about 3.8 GB of weights (7.61 × 4 ÷ 8). The 4 GB figure above is the same formula rounded at 8B. Neither number includes the context cache. Show both, and say they are floors, not a measured file size.

Show the person: the inventory, the tier you chose, the model you propose, the floor arithmetic, and free disk versus the catalog size once you know it. Then stop. Wait until they reply with a yes that names the runtime (`yes, install llmster`, `yes, install mlx-lm`, or `yes, install ollama`).

## 3. Install one runtime, on loopback

Pick one path. Do not install two servers.

### Apple silicon: llmster (LM Studio headless)

Official install, from https://lmstudio.ai/docs/developer/core/headless. Run only after the named yes:

- Mac or Linux: `curl -fsSL https://lmstudio.ai/install.sh | bash`
- Windows: `irm https://lmstudio.ai/install.ps1 | iex`

Then, without sudo if it is already installed:

1. `lms daemon up`
2. `lms server start` so it binds `127.0.0.1`. The default port in the docs is `1234`. If you pass `--bind`, the only allowed value is `127.0.0.1`.
3. Confirm with `lms` or the docs that the listen address is loopback. If it is not, stop. Do not open the firewall.

Model id to propose, after a separate yes that names the download: `mlx-community/Qwen2.5-Coder-7B-Instruct-4bit` (a public MLX conversion of `Qwen/Qwen2.5-Coder-7B-Instruct`, https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit). Show the catalog's download size and the free disk first. Then `lms get` that id. Do not get any other model.

Smoke-test URL: `http://127.0.0.1:1234/v1/chat/completions` (https://lmstudio.ai/docs/developer/openai-compat). Auth is off by default. If this server already requires a token, stop. Do not read a token into the chat. Ask the person to run the curl.

### Apple silicon alternative: MLX

Use this only if the person asked for MLX, or llmster will not install. From https://github.com/ml-explore/mlx-lm : `pip install mlx-lm`. If pip wants sudo or would change the system Python, stop and ask. Do not install into a repository checkout.

Start, only after the download yes:

`mlx_lm.server --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit`

The project documents that this listens on localhost port `8080` and that it is not a production server. Confirm the listen address is `127.0.0.1` before the request. If you would have to pass a host other than `127.0.0.1`, stop.

Smoke-test URL: `http://127.0.0.1:8080/v1/chat/completions` (https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md).

### Windows or Linux: llmster, or Ollama

Prefer llmster when the person said yes to it. Same install lines and the same `lms server start` bind rules as above. Do not use an MLX model id on a machine that is not Apple silicon. Search the local LM Studio catalog for Qwen2.5-Coder-7B-Instruct in a four-bit or Q4 build. Show the exact id and size. Wait for `yes, download <exact id>`.

Ollama, only after `yes, install ollama`. Use the install method printed on https://ollama.com/download or https://docs.ollama.com/quickstart. Show the exact command before you run it. Do not point `OLLAMA_HOST` at anything but `127.0.0.1`. If `OLLAMA_HOST` is already set wider, stop and ask. Do not sign in to Ollama cloud.

After `yes, download qwen2.5-coder:7b`, run `ollama pull qwen2.5-coder:7b` (https://ollama.com/library/qwen2.5-coder:7b). Record the digest the tool prints. Do not claim a bit width the tool did not print.

Smoke-test URL: `http://127.0.0.1:11434/v1/chat/completions` with `"model": "qwen2.5-coder:7b"` (https://docs.ollama.com/api/openai-compatibility). The local server does not use a real API key. If a client library requires a key string, use the placeholder `local` and do not substitute a real key.

## 4. Live smoke test

Send one short request. No files. No tools. No streaming, for this first check.

```bash
curl -sS -m 180 -D - \
  http://127.0.0.1:PORT/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Reply with the single word: ready"}],"max_tokens":32,"temperature":0,"stream":false}'
```

Replace `PORT` and `MODEL_ID` with the values you actually started. Success is an HTTP 200 and a non-empty assistant message. Print the status line, the model id, and the reply text. Then stop.

Write down, in the chat, a baseline the person can keep: OS, CPU, GPU, total and free memory or VRAM, free disk, runtime and version, model id, listen address, and the reply. A chat reply does not prove tool calls. Say that. Do not start a second request unless the person asks.

If the request fails, print the status and the error body with any token-like string redacted. Do not switch runtimes, do not change the firewall, and do not fall back to a cloud API.

## Transcript

This is the script, with text-to-speech spellings made readable. It matches the captions.

Software engineering 301. Run your own AI studio. Lesson one. Size the model. Then run the first endpoint.

### The question

Quick question. Before you download a local model, what do you check? The product name? The memory on the sticker? Or the weight floor, with room left over? The floor, with room left over. The sticker is the whole machine.

### The floor

Start with the weight floor. Parameter count, times bits per weight, divided by eight. That is gigabytes of weights, and only weights. Eighty billion parameters, at four-bits, starts at forty gigabytes. Three hundred twenty billion starts at one hundred sixty. Four hundred eighty billion starts at two hundred forty.

### Headroom

The floor is not the whole bill. Add metadata, the runtime, the operating system, your other programs, and a context cache for each open session. A two hundred forty gigabyte floor is a poor everyday choice on a two hundred fifty six gigabyte host.

### The ladder

Load a small model first. On an Apple silicon Mac you already own, try a three to eight billion parameter model, four-bit, only if memory permits. The playbook's first fixture, on its forty eight gigabyte laptop, is Qwen2.5 Coder, 7B, Instruct, four-bit. If gpt-oss-20b is already working, compare it. Don't download it in order to start.

### Candidates

Larger names are candidates, not measurements. The November plan, for the ordered five hundred twelve gigabyte Studio, starts code on Qwen3 Coder Next and review on GLM 5.3 Flash, both MLX four-bit. The challengers are DeepSeek V4 Flash at eight-bit, and Qwen3 Coder 480B at four-bit. Measure speed and power after the machine arrives. Today, start small.

### Context

When it loads, run one prompt at 4K, at 16K, and at 32K. Write down peak memory, swap, time to first token, and output tokens per second. Stop when the wait misses your target.

### The endpoint

Then build the endpoint. Write down the machine and the free disk. Install one pinned llmster runtime, and one model that fits. Bind it to loopback. One two seven point zero point zero point one. Not the open network. Send a completion, a stream, a cancel, and a tool call. Save them with the model manifest. A chat reply does not prove the tools.

### The prompt

One prompt on this page drives a computer-use agent, or a terminal agent, on a Mac or a PC. It reads the operating system, the CPU, the GPU, the memory, and free disk. It picks a tier. It installs llmster, or MLX on Apple silicon, or Ollama on a PC. It sends one live request. Then it waits.

### The stop

It waits before any admin install, any firewall change, and any sign-in. You name the action, and you say yes. Silence is not a yes. Don't paste a key, a token, or a password. Don't send a local file off the machine. The smoke test is one short sentence, to loopback. The reply stays on your computer.

### The rule

Rule one, for your agents. Before a download, write the weight floor, the memory you can spare, and the check that says the endpoint answered. Put that note where the agent can read it. Admin rights, a firewall change, or a sign-in: stop and ask.

### Your turn

Your turn. Open the prompt. Let the agent show you the tier it chose. Say yes only to the install you understand. Keep the reply. That reply is your baseline.

### Next

Next in the playbook: a router in front of the models, with stable names like code-fast and review. See you in that lab.

## Related

- Playbook: [Software Engineering 301](https://clarkhuang.github.io/software-engineering-301/index.md)
- Sizing lab on that page: [Size the model before downloading it](https://clarkhuang.github.io/software-engineering-301/index.md#1-size-the-model-before-downloading-it)
- Endpoint lab: [Build the first endpoint](https://clarkhuang.github.io/software-engineering-301/index.md#2-build-the-first-endpoint)
- Next lab in the playbook: [Put a router in front of the models](https://clarkhuang.github.io/software-engineering-301/index.md#3-put-a-router-in-front-of-the-models)
- [Don't Paste Secrets](https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/index.md)

## For agents

Read [AGENTS.md](https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/AGENTS.md) in this folder, [https://clarkhuang.github.io/software-engineering-301/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/AGENTS.md) for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.

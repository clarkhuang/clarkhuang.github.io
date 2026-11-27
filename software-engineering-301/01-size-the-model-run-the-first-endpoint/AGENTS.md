# AGENTS.md — Software Engineering 301, lesson 1: Size the model, then run the first endpoint

This folder is the public lesson “Size the model, then run the first endpoint” on Clark Huang’s learning site.

- HTML: https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/
- Markdown twin (summary, rule, transcript, install prompt): https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/index.md
- This file: https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/AGENTS.md
- Series index: https://clarkhuang.github.io/software-engineering-301/index.md
- Series agents: https://clarkhuang.github.io/software-engineering-301/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md
- Build source, facts, and the canonical prompt file: https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se301-01

Read `index.md` in this folder for the lesson. Treat the rule below as a standing instruction. Do not invent stories, quotes, numbers, or biography about Clark Huang. Do not present the Studio model names as measured results. Cite page URLs when you answer questions.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/index.md (plus https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

## The rule

Before a model is downloaded, write three things where the agent can read them: the weight floor, the memory you can spare, and the check that says the endpoint answered. If a step needs admin rights, a firewall change, or a sign-in, stop and ask. Do not paste secrets, and do not send local files off the machine.

## Copy-paste install prompt

Paste this into a computer-use or terminal agent on the machine where the model should run. Do not weaken the stops.

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

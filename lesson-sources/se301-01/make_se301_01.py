#!/usr/bin/env python3
"""Write se301-01-first-endpoint.json for Software Engineering 301, Lesson 1.

Size the model to the machine you have, run one local endpoint, and introduce
the copy-paste install prompt. Spoken claims are checked in facts.md.
Second person. No biography. No measured speeds. Speech tags: [pause],
<emphasis>, <slow> only.

Does not call the network and does not write audio or video.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
S = []

def sc(id, text, visual, data, chapter=""):
    S.append({"id": id, "text": text, "visual": visual, "chapter": chapter, "data": data})

sc("01_title",
   "Your model fits on paper. Can your laptop still answer after you cancel its first stream? Start with a memory budget. Finish with two requests you can replay.",
   "title",
   {"kicker": "SOFTWARE ENGINEERING 301  ·  LESSON 1",
    "headline": "Size the model.\nThen run the first endpoint.",
    "sub": "Run your own AI studio  •  clarkhuang.github.io"},
   "")

sc("02_quiz",
   "Quick question. Before you download a local model, what do you check? [pause] "
   "The product name? The memory on the sticker? Or the weight floor, with room left over? [pause] "
   "<emphasis>The floor, with room left over.</emphasis> The sticker is the whole machine.",
   "quiz",
   {"question": "Before the download,\nwhat do you check?",
    "options": ["The product name", "The memory on the sticker", "The floor, with room left"],
    "answer": 2,
    "why": "The sticker is\nthe whole machine.\nThe model gets\nwhat’s left."},
   "The question")

sc("03_floor",
   "Start with the weight floor. Parameter count, times bits per weight, divided by eight. [pause] "
   "That is gigabytes of weights, and only weights. Eighty billion parameters, at four bits, starts at forty gigabytes. "
   "Three hundred twenty billion starts at one hundred sixty. Four hundred eighty billion starts at two hundred forty.",
   "floor",
   {"label": "WEIGHT FLOOR  ·  PARAMETERS × BITS ÷ 8",
    "formula": "parameters × bits ÷ 8",
    "note": "Gigabytes of weights. Only weights.",
    "cards": [["80B · 4-bit", "40 GB"], ["320B · 4-bit", "160 GB"], ["480B · 4-bit", "240 GB"]]},
   "The floor")

sc("04_headroom",
   "The floor is not the whole bill. Add metadata, the runtime, the operating system, your other programs, "
   "and a context cache for each open session. [pause] "
   "A two hundred forty gigabyte floor is a poor everyday choice on a two hundred fifty six gigabyte host.",
   "headroom",
   {"label": "HEADROOM  ·  THE FLOOR IS NOT THE BILL",
    "host": "256 GB host",
    "floor": "240 GB floor",
    "used": 240, "total": 256,
    "left": "Almost nothing left for the OS, the runtime, or a context cache.",
    "adds": ["Quantization metadata", "Runtime", "Operating system", "Other programs", "Context cache"]},
   "Headroom")

sc("05_ladder",
   "Load a small model first. On an Apple silicon Mac you already own, try a three to eight billion parameter model, four bit, "
   "only if memory permits. [pause] The playbook's first fixture, on its forty eight gigabyte laptop, is Qwen two point five Coder, "
   "seven B, Instruct, four bit. If gpt oss twenty b is already working, compare it. Don't download it in order to start.",
   "ladder",
   {"label": "THE PLAYBOOK’S LADDER  ·  SMALL MODEL FIRST",
    "rows": [
        ["Use what you own", "3B–8B four-bit, if memory permits"],
        ["48 GB laptop", "Qwen2.5-Coder-7B-Instruct, four-bit"],
        ["Already installed", "gpt-oss-20b, same tasks, not a new download"],
    ]},
   "The ladder")

sc("06_candidates",
   "These Studio candidates need testing on the actual hardware. Keep your small laptop baseline for comparison.",
   "candidates",
   {"label": "512 GB STUDIO  ·  CANDIDATES, NOT MEASUREMENTS",
    "rows": [
        ["Code", "Qwen3-Coder-Next · MLX 4-bit"],
        ["Review", "GLM-5.3-Flash · MLX 4-bit"],
        ["Challengers", "DeepSeek-V4-Flash 8-bit · Qwen3-Coder-480B 4-bit"],
    ],
    "foot": "Hardware is ordered. Throughput, power, and usable context come later."},
   "Candidates")

sc("07_context",
   "When it loads, run one prompt at four K, at sixteen K, and at thirty two K. Write down peak memory, swap, "
   "time to first token, and output tokens per second. <slow>Stop when the wait misses your target.</slow>",
   "contexts",
   {"label": "SAME PROMPT  ·  THREE CONTEXT LENGTHS",
    "cards": ["4K", "16K", "32K"],
    "record": ["Peak memory", "Swap growth", "Time to first token", "Output tokens / second"],
    "foot": "Stop when interactive latency misses your target."},
   "Context")

sc("08_endpoint",
   "Then build the endpoint. Write down the machine and the free disk. Install one pinned llmster runtime, and one model that fits. "
   "Bind it to loopback. One two seven point zero point zero point one. Not the open network. [pause] "
   "Send a completion, a stream, a cancel, and a tool call. Save them with the model manifest. "
   "<emphasis>A chat reply does not prove the tools.</emphasis>",
   "checklist",
   {"label": "THE FIRST ENDPOINT  ·  LOOPBACK ONLY",
    "items": [
        ["1", "Write down the machine and free disk"],
        ["2", "One pinned llmster, one model that fits"],
        ["3", "Bind to 127.0.0.1"],
        ["4", "Completion, stream, cancel, tool call"],
    ],
    "foot": "A chat reply does not prove the tools."},
   "The endpoint")

sc("08b_replay",
   "Try this on your own endpoint. Ask for the numbers one through twenty, one per line, with streaming turned on. "
   "Watch for the first piece before the final one. Cancel halfway. Then send a fresh request: reply with the word ready. "
   "Save what actually happened on both requests. A stopped display alone cannot tell you whether the server stopped computing. "
   "Check the runtime log before you mark that part as passed.",
   "steps",
   {"label": "REPLAY CARD  ·  TRY IT ON YOUR ENDPOINT",
    "steps": [
        ["1", "Stream", "Count from 1 to 20, one number per line."],
        ["2", "Observe", "Did output arrive before the final event?"],
        ["3", "Cancel", "Stop the client during the stream."],
        ["4", "Retry", "New request: reply with the word ready."],
        ["5", "Check", "Save the reply and the server log."],
    ]},
   "Replay a cancelled stream")

sc("09_prompt",
   "One prompt on this page drives a computer-use agent, or a terminal agent, on a Mac or a P.C. [pause] "
   "It reads the operating system, the C.P.U., the G.P.U., the memory, and free disk. It picks a tier. "
   "It installs llmster, or M.L.X. on Apple silicon, or Ollama on a P.C. It sends one live request. Then it waits.",
   "steps",
   {"label": "THE COPY-PASTE PROMPT  ·  ON-SCREEN SUMMARY",
    "steps": [
        ["1", "Read the machine", "OS, CPU, GPU, memory, free disk"],
        ["2", "Pick a tier", "From this ladder. Show the arithmetic."],
        ["3", "Install one runtime", "llmster, MLX on Apple silicon, or Ollama"],
        ["4", "Send one request", "To the local endpoint. Read the reply."],
        ["5", "Stop for you", "Name the action. Wait for a yes."],
    ]},
   "The prompt")

sc("10_stop",
   "<slow>It waits before any admin install, any firewall change, and any sign-in.</slow> "
   "You name the action, and you say yes. Silence is not a yes. [pause] "
   "Don't paste a key, a token, or a password. Don't send a local file off the machine. "
   "The smoke test is one short sentence, to loopback. The reply stays on your computer.",
   "stop",
   {"label": "THE PROMPT STOPS",
    "stops": ["Admin or sudo install", "Firewall change", "Account sign-in"],
    "nevers": ["No secrets in the chat", "No local files off the machine"],
    "foot": "Silence is not a yes. The reply stays on your computer."},
   "The stop")

sc("11_rule",
   "Rule one, for your agents. Before a download, write the weight floor, the memory you can spare, "
   "and the check that says the endpoint answered. Put that note where the agent can read it. "
   "Admin rights, a firewall change, or a sign-in: stop and ask.",
   "rule",
   {"kicker": "RULE 1  ·  FOR YOUR AGENTS",
    "lines": [
        {"text": "Before a model is downloaded, write:"},
        {"text": "the weight floor,", "tone": "accent"},
        {"text": "the memory you can spare,", "tone": "accent"},
        {"text": "and the check that says the endpoint answered.", "tone": "accent"},
        {"text": "Admin, firewall, or sign-in? Stop and ask."},
    ],
    "foot": "THE FULL RULE IS ON THE LESSON PAGE"},
   "The rule")

sc("12_turn",
   "Your turn. Open the prompt. Let the agent show you the tier it chose. [pause] "
   "Say yes only to the install you understand. Keep the reply. That reply is your baseline.",
   "statement",
   {"headline": "Your turn.\nOpen the prompt.\nSay yes only to the install\nyou understand.",
    "sub": "Keep the smoke-test reply. That reply is your baseline."},
   "Your turn")

sc("13_close",
   "Next in the playbook: a router in front of the models, with stable names like code fast and review. See you in that lab.",
   "outro",
   {"headline": "See you in\nthe next lab.",
    "sub": "A router. Stable names. code-fast and review."},
   "Next")

spec = {
    "id": "se301-01-first-endpoint",
    "title": "SE301 Lesson 1: Size the model, then run the first endpoint",
    "series": "SOFTWARE ENGINEERING 301",
    "lesson": 1,
    "output": "01-size-the-model-run-the-first-endpoint/SE301_01_Size-The-Model_public.mp4",
    "voice": "4lbl0krw73vf",
    "language": "en",
    "speed": 1.05,
    "loudness": {"integrated_lufs": -16, "true_peak_dbtp_max": -1},
    "frame": {"width": 1920, "height": 1080, "fps": 30},
    "status": "Script and facts await Clark's review. Do not narrate until he says yes. No media has been rendered.",
    "scenes": S,
}
out = os.path.join(HERE, spec["id"] + ".json")
json.dump(spec, open(out, "w"), indent=1, ensure_ascii=False)
open(out, "a").write("\n")

def spoken(s):
    return re.sub(r"<[^>]+>|\[pause\]", " ", s["text"])

words = sum(len(spoken(s).split()) for s in S)
print(spec["id"], len(S), "scenes,", words, "words, est", round(words / 2.6), "s at 2.6 w/s")
for s in S:
    print(f"  {s['id']:<16} {s['visual']:<12} {s['chapter']:<16} {len(spoken(s).split()):>3} w")
low = " ".join(s["text"].lower() for s in S)
assert not any(t in low for t in ("[laugh", "[chuckle", "laugh]", "chuckle]"))
tags = set(re.findall(r"\[[a-z-]+\]|</?[a-z]+>", " ".join(s["text"] for s in S)))
assert tags <= {"[pause]", "<emphasis>", "</emphasis>", "<slow>", "</slow>"}, tags
# 3–4 minutes at the series planning rate of 2.6 words/second, with room for 2.8.
assert 470 <= words <= 640, words
print("wrote", out)

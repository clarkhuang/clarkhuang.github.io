# Brief: SE 301 Lesson 1, "Size the model, then run the first endpoint"

Slug `01-size-the-model-run-the-first-endpoint` · spec id `se301-01-first-endpoint` ·
generator `make_se301_01.py` · renderer `render_se301_01.py` ·
prompt `install-prompt.md` · facts `facts.md`

## What this lesson is

The first video lesson for Software Engineering 301, drawn from the playbook's opening labs:
size the model before downloading it, then build the first local endpoint. The lesson also introduces
one copy-paste prompt a computer-use or terminal agent can run on a Mac with Apple silicon or on a
Windows or Linux PC.

## The one idea

The download is not the first decision. The weight floor, plus room for the machine, is. Then one
endpoint, on loopback, with a reply you keep. A chat reply is not a tool-call proof.

## Shape

13 scenes, 602 spoken words. Estimate 232 seconds (3:52) at 2.6 words/second. Recorded SE 201 lessons
ran nearer 2.8 words/second, which would land closer to 3:35. Measure after narration. Do not narrate
until Clark approves the script and `facts.md`.

Question · the floor · headroom · the ladder · candidates (labeled as candidates) · three context lengths ·
the endpoint · the prompt, with a five-line on-screen summary · the stop · the rule · your turn · the next lab.

## Voice and limits

Second person. Short sentences. Contractions. University-professor tone. No hype words. No laugh or
chuckle tags. Speech tags limited to `[pause]`, `<emphasis>`, `<slow>`. No biography, no measured
tokens per second, no third-party VRAM tables, no prices. Studio model names stay candidates.
The Windows and Linux path is in the prompt and is named in the narration. It is an application of
the playbook's weight floor, not a new hardware row.

## Status

No audio and no MP4 have been rendered. `render_se301_01.py` refuses to write a silent file when
`XAI_API_KEY` is unset.

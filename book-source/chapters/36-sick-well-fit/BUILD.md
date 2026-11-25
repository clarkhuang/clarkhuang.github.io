# How the chapter 36 video was built

The videobook for Chapter 36, Sick, Well, Fit, was made with the same pipeline as the Software Engineering lessons on this site.

1. **Text.** The chapter (chapter.md) was adapted from a reading Clark Huang wrote, made generic (no company names), and expanded with more of Greg Glassman's published writing. Every quotation comes from a public source listed at the end of the chapter. Two independent review rounds checked quotes against the sources.
2. **Script.** A scene script (69 scenes) narrates the chapter. Each gym idea is drawn next to its business match (split screen), with a workout-clock progress counter. All drawings are simple generated graphics: no photos, no real people's likenesses, no CrossFit logos. Two review rounds checked the script and stills.
3. **Voice.** Clark Huang's custom xAI voice (text-to-speech), at speed 1.05, one clip per scene. No laugh tags.
4. **Render.** 1920×1080 at 30 fps, rendered with Pillow and ffmpeg (the site's lesson renderer plus chapter-specific layouts).
5. **Finish.** Loudness normalized to about −16 LUFS integrated with a true peak under −1 dBTP; captions built from the script and the measured scene timings; poster from the first frame.

Not affiliated with or endorsed by CrossFit. CrossFit is a trademark of CrossFit, LLC. The made-up company is an illustration.

Runtime: 24:56. Transcript: [transcript.md](transcript.md).

# How the chapter 17b video was built

The videobook for Chapter 17b, Building Blocks, was made with the same pipeline as the Software Engineering lessons and Chapter 36 on this site.

1. **Text.** The chapter (chapter.md) is a nonfiction interlude in Clark Huang's own voice, rewritten start to finish around the building-block stories he dictated: the ring muscle-up and the false grip, double unders and the six-year progression to unbroken sets under fatigue, the running ladder through the Carlsbad half, the swim and bike ladders, half triathlons and a full triathlon (2.4-mile swim, 112-mile bike, 26.2-mile run, unnamed), and official marathon results already on the record. Half and full triathlons are kept unnamed and undated on purpose. Weightlifting is described only generically in the narration; no invented lifts or PRs.
2. **Script.** A scene script (31 scenes) narrates the chapter. Drawings are simple generated stick-figure graphics: ring muscle-ups (including the false grip, kip, and transition), gymnastics and bodyweight work, single and double unders, general weightlifting including the clean and jerk, swimming, biking, and running. No photos, no real people's likenesses, no race-brand marks, no CrossFit logos.
3. **Voice.** Clark Huang's custom xAI voice (text-to-speech), at speed 1.05, one clip per scene. No laugh tags.
4. **Render.** 1920×1080 at 30 fps, rendered with Pillow and ffmpeg (the site's lesson renderer plus chapter-specific layouts).
5. **Finish.** Loudness normalized to about −16 LUFS integrated with a true peak under −1 dBTP; captions built from the script and the measured scene timings; poster from an early frame.

Not affiliated with or endorsed by CrossFit. CrossFit is a trademark of CrossFit, LLC.

Runtime: 8:12. Transcript: [transcript.md](transcript.md).

# How the chapter 17b video was built

The videobook for Chapter 17b, Building Blocks, was made with the same pipeline as the Software Engineering lessons and Chapter 36 on this site.

1. **Text.** The chapter (chapter.md) is a nonfiction interlude in Clark Huang's own voice, rewritten start to finish around the building-block stories he dictated: the hollow hold as the gymnastics foundation, the ring muscle-up and a false grip on the bottom of the rings, double unders (single unders, then penguin jumps, then doubles, then a few triple unders after 100 unbroken doubles), the running ladder through the Carlsbad half, the swim and bike ladders, and a triathlon distance ladder — sprint (Challenge Miami), Olympic (St. Anthony's), half (Challenge Daytona), with a full Ironman only as something ahead. Distances are given; triathlon dates and finish times are not. The Dunedin 5K is left out. Progressive overload is told through the legend of Milo of Croton (Greek, sixth century B.C., cited to Encyclopaedia Britannica as legend), then bodyweight work, added load, and a clean and jerk. Official marathon results already on the record stay named and dated.
2. **Script.** A scene script (37 scenes) narrates the chapter. Drawings are simple generated stick-figure graphics: a hollow hold on the floor, ring muscle-ups (false grip at the bottom of the ring, kip, and transition), penguin jumps and a real jump rope (handles and a flexible arc, not a hoop), the Milo calf-to-bull legend, bodyweight work then plates then a clean and jerk, a triathlon distance ladder, swimming, biking, and running. No photos, no real people's likenesses, no race-brand marks, no CrossFit logos.
3. **Voice.** Clark Huang's custom xAI voice (text-to-speech), at speed 1.05, one clip per scene. No laugh tags.
4. **Render.** 1920×1080 at 30 fps, rendered with Pillow and ffmpeg (the site's lesson renderer plus chapter-specific layouts).
5. **Finish.** Loudness normalized to about −16 LUFS integrated with a true peak under −1 dBTP; captions built from the script and the measured scene timings; poster from an early frame.

Not affiliated with or endorsed by CrossFit. CrossFit is a trademark of CrossFit, LLC.

Runtime: 9:27 (567.83 seconds). Transcript: [transcript.md](transcript.md).

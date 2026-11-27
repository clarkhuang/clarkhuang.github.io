# AI Tip 18 — Save the Case That Failed

[Watch the captioned lesson](https://clarkhuang.github.io/ai-tips/18-save-the-case-that-failed/)

## The rule

Save the exact input and expected outcome. Replay the case after the fix and follow the result to its destination.

## Transcript

These words are a heading in Software Engineering four oh one. Yet a reader who searched for that heading could miss the course entirely.

Here is the old search, replayed from the published revision. It returns results. Look for the course itself. It's missing. A test that only counts results would pass.

Save two things. The exact words the reader typed, and where the reader needed to land. Search is broken is hard to replay. This little card tells another person exactly what to try.

Now use those same words on the corrected site. There's the course. Open it. We still have one more thing to check.

There is the heading we started with. Tomorrow the result might move down a place and still be perfectly useful. Test the outcome the reader cares about.

After the next search rebuild, run that same case again. Think of the last thing you had to correct twice. What example could you save today to catch it next time?

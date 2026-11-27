# AI Tip 19 — One Batch First

[Watch the captioned lesson](https://clarkhuang.github.io/ai-tips/19-one-batch-first/)

## The rule

Run a small sample. Show the evidence for each decision. Wait for my reply before expanding the job, including work handed to another agent.

## Transcript

You ask the bot to flag gaps in a volunteer roster. Eighty shifts later, you discover it counted every blank cell as a missing volunteer.

Look at these two rows. Check-in needs a person. Standby is deliberately empty. The bot can repeat a reasonable guess eighty times before you see it once.

Try a smaller instruction. Check the first three shifts only. For each gap, show the row and your reason. Then wait for my reply before scanning the rest.

Now the mistake costs one correction. The bot flagged both blanks. You can see exactly which rule it inferred.

Reply in the thread. Standby may be empty. Run those same three again and keep the rest on hold. One flag should survive: the empty check-in shift.

Once the sample matches your judgment, give it the next batch. If it calls another agent, carry the same limit into that handoff. A small Slack request can start a much larger job.

Before your next bulk request, finish this sentence: do the first how many, show me what, and stop where? Give the bot a checkpoint you can actually review.

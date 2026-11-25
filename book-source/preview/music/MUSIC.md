# Preview music bed

An original instrumental bed was composed for this start-to-finish preview on 25 November 2026. It is a dark, slow electronic pad in E minor, with a quiet pulse and a late rise under “More chapters are coming” and “Coming in 2027.”

- **Source:** Original composition. No third-party samples, loops, or licensed libraries.
- **How it was made:** `book-source/preview/music/make_bed.py` synthesizes the bed with sine pads, a low pulse, and sparse plucks (Python, NumPy, standard library only).
- **License:** Original work for *Silicon Valley C Players*, published with the preview under the same site terms as the videobook (the book's pages use [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) for the written work). The instrumental itself may be reused with the preview; it is not sold separately.
- **Mix:** The bed is ducked under the voice with a sidechain compressor and swells from about 2:30 to the close. The final mix targets about −16 LUFS, true peak at or below −1 dBTP.

Rebuild: run `python3 book-source/preview/music/make_bed.py`, then mix it under the narrated voice as described in `REBUILD.md`.

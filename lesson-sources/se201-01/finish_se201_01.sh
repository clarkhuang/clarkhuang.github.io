#!/usr/bin/env bash
# Finish SE201 lesson 1 after narrate.py + render_se101.py: loudness to about -16 LUFS, faststart MP4, poster, captions.
# Usage (from pipeline/): ./finish_se201_01.sh /path/to/site-checkout
set -euo pipefail
SITE="${1:?site checkout}"
D=../01-build-the-whole-system-ai-native
V=$D/SE201_01_Build-The-Whole-System-AI-Native_public.mp4
NAME=se201-01-build-the-whole-system-ai-native
LOG=../../logs/s201_01_ainative.log
# 1) loudnorm (speech with pauses lands near -18 LUFS in one pass), then a small gain + limiter to reach about -16 LUFS
ffmpeg -v error -y -i "$V" -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:v copy -c:a aac -b:a 160k -ar 44100 -movflags +faststart "$V.n.mp4"
# two short gain + limiter passes (the limiter eats some of the gain), stopping at -16 +/- 0.2 LUFS
for pass in 1 2 3; do
  GAIN=$(ffmpeg -hide_banner -i "$V.n.mp4" -af loudnorm=I=-16:print_format=summary -f null - 2>&1 | awk '/Input Integrated/{printf "%.2f", -16-$3}')
  awk -v g="$GAIN" 'BEGIN{exit !(g<0.2 && g>-0.2)}' && break
  ffmpeg -v error -y -i "$V.n.mp4" -af "volume=${GAIN}dB,alimiter=limit=0.82:attack=2:release=40:level=false" -c:v copy -c:a aac -b:a 160k -ar 44100 -movflags +faststart "$V.g.mp4"
  mv "$V.g.mp4" "$V.n.mp4"
done
mv "$V.n.mp4" "$V"
ffmpeg -hide_banner -i "$V" -af loudnorm=I=-16:print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True"
# 2) poster = the title card (frame 0)
ffmpeg -v error -y -ss 0 -i "$V" -frames:v 1 -q:v 3 "$D/poster.jpg"
# 3) captions from the scene script + render timeline
python3 make_vtt.py scripts/se201-01-ai-native.json "$LOG" "$D/$NAME.vtt"
# 4) copy into the site
cp "$V" "$SITE/videos/$NAME.mp4"; cp "$D/$NAME.vtt" "$SITE/videos/$NAME.vtt"; cp "$D/poster.jpg" "$SITE/videos/posters/$NAME.jpg"

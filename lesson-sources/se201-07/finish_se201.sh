#!/usr/bin/env bash
# Finish an SE201 lesson after narrate.py + render_se101.py: loudness to about -16 LUFS, faststart MP4, poster, captions.
# Usage (from pipeline/): ./finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
set -euo pipefail
D=../$1; V=$D/$2; NAME=$3; LOG=$4; SCRIPT=$5; SITE=$6
ffmpeg -v error -y -i "$V" -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:v copy -c:a aac -b:a 160k -ar 44100 -movflags +faststart "$V.n.mp4"
for pass in 1 2 3; do
  GAIN=$(ffmpeg -hide_banner -i "$V.n.mp4" -af loudnorm=I=-16:print_format=summary -f null - 2>&1 | awk '/Input Integrated/{printf "%.2f", -16-$3}')
  awk -v g="$GAIN" 'BEGIN{exit !(g<0.2 && g>-0.2)}' && break
  ffmpeg -v error -y -i "$V.n.mp4" -af "volume=${GAIN}dB,alimiter=limit=0.82:attack=2:release=40:level=false" -c:v copy -c:a aac -b:a 160k -ar 44100 -movflags +faststart "$V.g.mp4"
  mv "$V.g.mp4" "$V.n.mp4"
done
mv "$V.n.mp4" "$V"
ffmpeg -hide_banner -i "$V" -af loudnorm=I=-16:print_format=summary -f null - 2>&1 | grep -E "Input Integrated|Input True"
ffmpeg -v error -y -ss 0 -i "$V" -frames:v 1 -q:v 3 "$D/poster.jpg"
python3 make_vtt.py "$SCRIPT" "$LOG" "$D/$NAME.vtt"
cp "$V" "$SITE/videos/$NAME.mp4"; cp "$D/$NAME.vtt" "$SITE/videos/$NAME.vtt"; cp "$D/poster.jpg" "$SITE/videos/posters/$NAME.jpg"

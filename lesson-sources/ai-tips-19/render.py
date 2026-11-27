"""Build the fictional roster exercise with Clark narration, timed captions and review frames."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.request

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STEM = "ai-tips-19-one-batch-first"
FONT = Path(os.environ.get("VIDEO_FONT_DIR", "/System/Library/Fonts/Supplemental"))
SCENES = json.loads((HERE / "scenes.json").read_text())


def draw(scene, index, reveal, path, series="AI TIPS   /   19", screenshot=None):
    title, label, *items, narration = scene
    canvas = Image.new("RGB", (1280, 720), "#112723")
    d = ImageDraw.Draw(canvas)
    def line(x, y, text, size, color, family="Arial"):
        font = ImageFont.truetype(str(FONT / (family + ".ttf")), size)
        assert x + d.textlength(text, font=font) < 1260, text
        d.text((x, y), text, font=font, fill=color)
    line(65, 37, series, 27, "#B0E7B8", "Arial Bold")
    line(65, 99, title, 65, "#FAF4E5", "Georgia")
    d.rounded_rectangle((65,220,1215,584),24,fill="#F6F0DD")
    line(104,246,label,23,"#336052","Arial Bold")
    for row,item in enumerate(items[:reveal]):
        y=313+78*row
        d.line((104,y-9,1172,y-9),fill="#CECDBC",width=2)
        line(104,y,item,39 if index in (1,3,5) else 42,"#173A31","Courier New Bold" if index in (1,3,5) else "Arial")
    if screenshot:
        shot = Image.open(screenshot).convert("RGB")
        shot.thumbnail((1128, 352))
        canvas.paste(shot, ((1280-shot.width)//2, 224))
    for i in range(len(SCENES)):
        step=1150/len(SCENES)
        x=65+i*step
        d.rounded_rectangle((x,654,x+step-12,661),3,fill="#A0DFAC" if i<=index else "#3C5850")
    canvas.save(path)


def run(*args):
    subprocess.run(args,check=True)


def stamp(seconds):
    msec=round(seconds*1000)
    return f"{msec//3600000:02}:{msec//60000%60:02}:{msec//1000%60:02}.{msec%1000:03}"


def render(tmp, series="AI TIPS   /   19", frames=None):
    key=os.environ["XAI_API_KEY"]
    clips=[]
    cues=["WEBVTT",""]
    elapsed=0
    for n,scene in enumerate(SCENES):
        audio=tmp/f"{n}.mp3"
        payload={"text":scene[-1],"voice_id":"4lbl0krw73vf","speed":0.95,"language":"en"}
        req=urllib.request.Request("https://api.x.ai/v1/tts",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json","Authorization":"Bearer "+key})
        with urllib.request.urlopen(req,timeout=60) as response:
            audio.write_bytes(response.read())
        duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",audio]))
        hold = 2.4 if n == len(SCENES)-1 else 0.55
        listing=tmp/f"{n}.txt"
        lines=[]
        for i,portion in enumerate([0.20,0.25,0.55],1):
            frame=tmp/f"{n}-{i}.png"
            draw(scene,n,i,frame,series,(frames or {}).get(n))
            lines.extend([f"file '{frame}'",f"duration {duration*portion + (hold if i==3 else 0)}"])
        lines.append(f"file '{frame}'")
        listing.write_text("\n".join(lines))
        part=tmp/f"{n}.mp4"
        run("ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",listing,"-i",audio,"-vf","fps=25,format=yuv420p","-af","loudnorm=I=-16:TP=-1.5:LRA=11,apad","-ar","48000","-c:a","aac","-b:a","160k","-c:v","libx264","-preset","veryfast","-t",str(duration+hold),part)
        measured=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",part]))
        words=scene[-1].split(); start=elapsed
        for i in range(0,len(words),8):
            end=elapsed+duration*min(i+8,len(words))/len(words)
            cues.extend([f"{stamp(start)} --> {stamp(end)}"," ".join(words[i:i+8]),""]); start=end
        elapsed+=measured;clips.append(f"file '{part}'")
    listing=tmp/"clips.txt";listing.write_text("\n".join(clips))
    run("ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",listing,"-c","copy","-movflags","+faststart",ROOT/"videos"/(STEM+".mp4"))
    (ROOT/"videos"/(STEM+".vtt")).write_text("\n".join(cues))
    draw(SCENES[0],0,3,ROOT/"videos/posters"/(STEM+".jpg"),series)


if __name__=="__main__":
    with tempfile.TemporaryDirectory() as directory:
        render(Path(directory))

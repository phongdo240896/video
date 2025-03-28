from fastapi import FastAPI, Request
from moviepy.editor import VideoFileClip, AudioFileClip
import requests
import shutil
import os

app = FastAPI()

@app.post("/merge")
async def merge_video_audio(data: dict):
    video_url = data["video_url"]
    audio_url = data["audio_url"]
    output_name = data["output_name"]

    video_path = "video.mp4"
    audio_path = "audio.mp3"
    output_folder = "static"
    os.makedirs(output_folder, exist_ok=True)
    output_path = f"{output_folder}/{output_name}"

    # Tải video
    with requests.get(video_url, stream=True) as r:
        with open(video_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    # Tải audio
    with requests.get(audio_url, stream=True) as r:
        with open(audio_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    # Ghép
    videoclip = VideoFileClip(video_path)
    audioclip = AudioFileClip(audio_path)
    videoclip = videoclip.set_audio(audioclip)
    videoclip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return {"status": "done", "output_url": f"/{output_path}"}

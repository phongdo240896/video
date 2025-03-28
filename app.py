from flask import Flask, request, jsonify
import requests
import os
import subprocess

app = Flask(__name__)

@app.route("/merge", methods=["POST"])
def merge():
    data = request.get_json()
    video_url = data.get("video_url")
    audio_url = data.get("audio_url")
    output_name = data.get("output_name", "output_merged.mp4")

    video_path = "video.mp4"
    audio_path = "audio.mp3"
    output_path = output_name

    try:
        # Tải video
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(video_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Tải audio
        with requests.get(audio_url, stream=True) as r:
            r.raise_for_status()
            with open(audio_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Sử dụng FFmpeg để ghép video và audio
        command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac {output_path}"
        subprocess.run(command, shell=True, check=True)

        return jsonify({"status": "success", "output": output_name})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_video_audio():
    data = request.get_json()
    video_url = data.get('video_url')
    audio_url = data.get('audio_url')
    output_name = data.get('output_name', 'output_merged.mp4')

    # Tải video và audio
    subprocess.call(['wget', '-O', 'video.mp4', video_url])
    subprocess.call(['wget', '-O', 'audio.mp3', audio_url])

    # Ghép video và audio bằng ffmpeg
    command = [
        'ffmpeg', '-i', 'video.mp4', '-i', 'audio.mp3',
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
        output_name
    ]
    subprocess.call(command)

    return jsonify({
        'message': 'Video merged successfully',
        'file': output_name
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

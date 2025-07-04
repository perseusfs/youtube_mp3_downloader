from flask import Flask, request, send_file
import yt_dlp
import os
import re

app = Flask(__name__)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
DOWNLOAD_FOLDER = os.path.join(desktop_path, "YoutubeMP3 Downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'ffmpeg_location': 'C:/ffmpeg/bin',
        'restrictfilenames': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    filepath = None
    if 'requested_downloads' in info:
        for item in info['requested_downloads']:
            if item.get('filepath') and item['filepath'].endswith('.mp3'):
                filepath = item['filepath']
                break

    if not filepath:
        filename = sanitize_filename(f"{info['title']}.mp3")
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    filepath = os.path.normpath(filepath)
    filename = os.path.basename(filepath)

    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    app.run(port=5000)

from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(yt_url, download=True)
        filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        yt_url = request.form['youtube_url']
        file_path = download_audio(yt_url)
        return send_file(file_path, as_attachment=True)
    return render_template('index.html')


app.run(debug=True)

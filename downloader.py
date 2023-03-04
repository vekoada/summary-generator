import yt_dlp
import io
from video import generate_captions
import requests

def dl(url):
    ydl_opts = {'format': 'worstaudio[ext=m4a]', 'outtmpl': './thing.m4a'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict)
        return audio_file
    


def alt(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'extractaudio': True,
        'audioformat': 'm4a',
        'audioquality': 0,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        file_url = info_dict.get("url", None)
        if file_url is None:
            raise Exception("Could not extract video URL")
            
    response = requests.get(file_url)
    return io.BytesIO(response.content)

print(generate_captions(alt('https://www.youtube.com/watch?v=voa0btsVSfk')))
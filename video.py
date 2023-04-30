from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled
import openai
import configure
#import downloader

openai.api_key = configure.get_credentials('c:/Users/Adam/repos/summary-generator/.secret/keys.json')['openai']


def extract_id(url):
    
    error = "The url provided is not a video, or is not from the YouTube.com domain"
    # Check if the URL is from the YouTube.com domain
    if "youtube.com" not in url:
        return error

    # Extract the video ID
    params = parse_qs(urlparse(url).query)

    # Check if URL is a vid
    if 'v' not in params:
        return error

    else:
        video_id = params['v'][0]
        return video_id
        
    
def get_text(url):
    video_id = extract_id(url)
    #Grab list of dictionaries 'subs'
    subs = yt.get_transcript(video_id=video_id,languages=['en'])

    #Build text string
    text = ''
    for i in subs:
        text+= '{} '.format(i['text'])
        
    return text
    
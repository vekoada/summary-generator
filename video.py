from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled
import openai
import configure
#import downloader

openai.api_key = configure.get_credentials('c:/Users/Adam/repos/summary-generator/.secret/keys.json')['openai']

def extract_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube video URL.

    This function takes a YouTube video URL as input and extracts the unique video ID from it. The URL must be from
    the YouTube.com domain for the function to work properly. If the URL is invalid or not from YouTube.com, an error
    message is returned.

    Args:
        url (str): A string containing the YouTube video URL.

    Returns:
        str: The extracted video ID if the URL is valid and contains a video ID.
        str: An error message if the URL is not a video or not from the YouTube.com domain.

    Example:
        >>> url = "https://www.youtube.com/watch?v=abcdef12345"
        >>> extract_id(url)
        'abcdef12345'

    Note:
        This function assumes that the provided URL is a valid YouTube video URL and follows the standard format
        with the 'v' parameter containing the video ID.

    """
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
        
    
def get_text(url: str) -> str:
    """
    Retrieves the transcribed text from a YouTube video.

    This function takes a YouTube video URL as input, extracts the video ID, and fetches the transcribed text of the video
    in English (assuming English is one of the available languages). The transcribed text is returned as a single string.

    Args:
        url (str): A string containing the YouTube video URL.

    Returns:
        str: The transcribed text of the video as a single string.

    Example:
        >>> url = "https://www.youtube.com/watch?v=abcdef12345"
        >>> get_text(url)
        'This is the transcribed text of the video.'

    Note:
        This function relies on the 'extract_id' function to extract the video ID from the URL. It also assumes that the
        YouTube video has English subtitles available.

    """
    # Extract the video ID from the URL
    video_id = extract_id(url)

    # Fetch the subtitles for the video in English
    subs = yt.get_transcript(video_id=video_id, languages=['en'])

    # Build a single text string from the list of subtitle dictionaries
    text = ''
    for subtitle in subs:
        text += '{} '.format(subtitle['text'])

    return text

    
#print(get_text("https://www.youtube.com/watch?v=imAYfKW1WG8"))
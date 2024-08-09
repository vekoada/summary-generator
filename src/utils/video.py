# Python imports
import re
import os
from urllib.parse import urlparse, parse_qs

# Third-party imports
import openai
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled

# Local imports
import configure

path = os.path.dirname(os.path.abspath(__file__))
openai.api_key = configure.get_credentials(path + '/.secret/keys.json')['OpenAI']

def extract_youtube_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube video URL.

    This function takes a YouTube video URL as input and extracts the unique video ID from it. The URL must be from
    the YouTube.com domain for the function to work properly. If the URL is invalid or not from YouTube.com, a ValueError
    is raised.

    Args:
        url (str): A string containing the YouTube video URL.

    Returns:
        str: The extracted video ID if the URL is valid and contains a video ID.

    Raises:
        ValueError: If the URL is not a video or not from the YouTube.com domain.

    Example:
        >>> url = "https://www.youtube.com/watch?v=abcdef12345"
        >>> extract_youtube_video_id(url)
        'abcdef12345'

    Note:
        This function assumes that the provided URL is a valid YouTube video URL and follows the standard format
        with the 'v' parameter containing the video ID.
    """
    if not isinstance(url, str):
        raise ValueError("The URL must be a string")

    parsed_url = urlparse(url) # extracts components from URL string
    if parsed_url.netloc not in ["www.youtube.com", "youtube.com"]: # `.netloc`: URL network location containing domain name
        raise ValueError("The URL provided is not from the YouTube.com domain")

    params = parse_qs(parsed_url.query) # `.query`: URL query string
    if 'v' not in params:
        raise ValueError("The URL provided does not contain a video ID")

    video_id = params['v'][0]
    if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id): # `^[a-zA-Z0-9_-]{11}$`: regex pattern for 11 alphanumeric characters, hyphens, or underscores
        raise ValueError("The extracted video ID is not valid")

    return video_id

def get_transcript(url: str) -> str:
    """
    Retrieves the transcribed text from a YouTube video.

    This function takes a YouTube video URL as input, extracts the video ID, and fetches the transcribed text of the video
    in English (assuming English is one of the available languages). The transcribed text is returned as a single string.

    Args:
        url (str): A string containing the YouTube video URL.

    Returns:
        str: The transcribed text of the video as a single string.

    Raises:
        TranscriptsDisabled: If the video has no available transcript.

    Example:
        >>> url = "https://www.youtube.com/watch?v=abcdef12345"
        >>> get_transcript(url)
        'This is the transcribed text of the video.'

    Note:
        This function relies on the 'extract_youtube_video_id' function to extract the video ID from the URL.
        It attempts to fetch English subtitles, but will use any available language if English is not available.
    """
    # Extract the video ID from the URL
    video_id = extract_youtube_video_id(url)

    try:
        # Fetch the subtitles for the video in English
        subs = yt.get_transcript(video_id, languages=['en'])
    except yt.TranscriptsDisabled:
        raise yt.TranscriptsDisabled("No transcript available for this video.") # call imported transcript error

    return ' '.join(f"[{subtitle['start']}] {subtitle['text']}" for subtitle in subs) # generator expression https://python-reference.readthedocs.io/en/latest/docs/comprehensions/gen_expression.html

    
print(get_transcript("https://www.youtube.com/watch?v=imAYfKW1WG8"))
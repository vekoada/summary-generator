import re
from urllib.parse import urlparse, parse_qs

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
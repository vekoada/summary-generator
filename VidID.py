import re
import urllib.parse

def extract(url):
    # Check if the URL is from the YouTube.com domain
    if "youtube.com" not in url:
        return "The URL you entered is not from the YouTube.com domain."


    # Extract the video ID
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)

    # Check if URL is a vid
    if 'v' not in params:
        return "The url provided is not a video."

    else:
        video_id = params['v'][0]
        return video_id
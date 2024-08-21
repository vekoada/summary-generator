# IGNORE THIS FILE. Currently not functional. 
# Ultimate goal is to be able to transcribe YouTube videos.
# However, YouTube has explicit protections from this. A workaround would be to download MP3 and then transcribe. Will figure out later.

# Standard library imports
import os

# Third party imports
from deepgram import DeepgramClient, PrerecordedOptions
import asyncio

# Local imports
from configure import get_credentials

path = os.path.dirname(os.path.abspath(__file__))

key = get_credentials(path + '/.secret/keys.json')['Deepgram']

async def transcribe(url: str) -> str:
    AUDIO_URL = {
        "url": url
    }

    try:
        client = DeepgramClient(key)

        options = PrerecordedOptions(
            smart_format=True,
            summarize="v2",
        )
        url_response = await client.listen.asyncrest.v("1").transcribe_url(
            AUDIO_URL, options
        )

        load = await url_response.to_json

        return load
    
    except Exception as e:
        print(f"Exception: {e}")

#response = asyncio.run(transcribe(url='https://youtu.be/9en2brDsbH4')) 
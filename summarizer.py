import openai
import json
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled
from VidID import extract

def get_keys(path):
    with open(path) as f:
        return json.load(f)

#Grab API key from secret dict
openai.api_key = get_keys('c:/Users/Adam/repos/summary-generator/.secret/keys.json')['openai']

#Grab video id from url
vid = extract('https://www.youtube.com/watch?v=4x7MkLDGnu8')

try:
    #Grab list of dictionaries 'subs'
    subs = yt.get_transcript(video_id=vid,languages=['en'])

    #Build text string
    text = ''
    for i in subs:
        text+= '{} '.format(i['text'])

    #Initialize prompt with instructions and video text
    prompt = (f"Please summarize this text: {text}")

    response = openai.Completion.create(
        engine="text-curie-001",
        prompt=prompt,
        max_tokens=200,
        temperature=0.5,
        n=1)

    summary = response.choices[0].text

    #Write summary to file
    with open('c:/Users/Adam/repos/summary-generator/summary.txt', 'w') as f:
        f.write(summary)

except TranscriptsDisabled as e:
    print("Could not retrieve a transcript for the video!")



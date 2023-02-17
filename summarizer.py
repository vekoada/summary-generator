import openai
import json
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled

def get_keys(path):
    with open(path) as f:
        return json.load(f)

#Grab API key from secret dict
openai.api_key = get_keys('c:/Users/Adam/repos/summary-generator/.secret/keys.json')['openai']

#Grab list of dictionaries 'subs'
vid = 'jPQ87J_5qyw' #4x7MkLDGnu8

try:
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



import openai
import json
#from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled
from video_id_extract import extract_id
from chunker import create_chunks

def get_keys(path):
    with open(path) as f:
        return json.load(f)

#Grab API key from secret dict
openai.api_key = get_keys('c:/Users/Adam/repos/summary-generator/.secret/keys.json')['openai']

#Grab video id from url
url = 'https://www.youtube.com/watch?v=4x7MkLDGnu8'
video_id = extract_id(url)

#video = YouTube(url=url)
#video_title = video.title

try:
    #Grab list of dictionaries 'subs'
    subs = yt.get_transcript(video_id=video_id,languages=['en'])
   
    #Build text string
    text = ''
    for i in subs:
        text+= '{} '.format(i['text'])

    chunk_list = create_chunks(text, 800)
    summary_list = []

    for chunk in chunk_list:

        #Initialize prompt with instructions and video text
        prompt = (f"Please summarize this section of video captions, keeping an eye out for the main points: {chunk}")

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            n=1)

        chunk_summary = response.choices[0].text
        summary_list.append(chunk_summary)

    summary_concatenated = ""
    for chunk_summary in summary_list:
        summary_concatenated+= chunk_summary

    prompt = (f"Please summarize this video, based on the following description. Pay attention to the main points, and strive for accuracy: {summary_concatenated}")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=750,
        temperature=0.5,
        n=1)

    summary = response.choices[0].text

    #Write summary to file
    with open('c:/Users/Adam/repos/summary-generator/summary.txt', 'w') as f:
        f.write(summary)

except TranscriptsDisabled as e:
    print("Could not retrieve a transcript for the video!")



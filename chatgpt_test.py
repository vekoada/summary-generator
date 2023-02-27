from revChatGPT.V1 import Chatbot as gpt
import json
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled
from video_id_extract import extract_id
from chunker import create_chunks
import time

def get_credentials(path):
    with open(path) as f:
        return json.load(f)

start_time = time.time()

path ="c:/Users/Adam/.config/revChatGPT/config.json"
model = gpt(get_credentials(path))

#Grab video id from url
url = 'https://www.youtube.com/watch?v=5MuIMqhT8DM&ab_channel=TED' #Sleep TED Talk ~20min
video_id = extract_id(url)

try:
    #Grab list of dictionaries 'subs'
    subs = yt.get_transcript(video_id=video_id,languages=['en'])
   
    #Build text string
    text = ''
    for i in subs:
        text+= '{} '.format(i['text'])

    chunk_list = create_chunks(text, 3500) #Max chunk size (char limit)
    summary_list = []

    for chunk in chunk_list:
        #Initialize prompt with instructions and video text
        prompt = f"Please summarize this video, based on the following subtitles: {chunk}"
        chunk_summary = ""
        for data in model.ask(prompt):
            chunk_summary = data["message"]

        summary_list.append(chunk_summary)

    summary_concatenated = ""
    for chunk_summary in summary_list:
        summary_concatenated+= chunk_summary

    final_prompt = f"Please summarize this video, based on the following description. Pay attention to the main points, and strive for accuracy: {summary_concatenated}"
    final_summary = ""
    for data in model.ask(final_prompt):
        final_summary = data["message"]

    print(summary_concatenated)
    print(" ")
    print(final_summary)

    print("--- %s seconds ---" % (time.time() - start_time))

    # #Write summary to file
    # with open('c:/Users/Adam/repos/summary-generator/chatgpt_summary.txt', 'w') as f:
    #     f.write(summary)

except TranscriptsDisabled as e:
    print("Could not retrieve a transcript for the video!")
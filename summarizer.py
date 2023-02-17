import openai
import json
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import TranscriptsDisabled

def get_keys(path):
    with open(path) as f:
        return json.load(f)

#Grab API key from secret dict
openai.api_key = get_keys('c:/Users/Adam/Documents/CS 195 Project/.secret/keys.json')['openai']

#Grab list of dictionaries 'subs'
vid = 'a9TP-XlyX9s' #4x7MkLDGnu8
try:
    subs = yt.get_transcript(video_id=vid,languages=['en'])

    print(subs)

# #Write the 'text'of each dictionary to file
# with open("c:/Users/Adam/Documents/CS 195 Project/subtitles.txt", "w") as f:
#   for i in subs:
#         f.write("{}\n".format(i['text']))

# #Read subtitle file
# with open('c:/Users/Adam/Documents/CS 195 Project/subtitles.txt') as f:
#     contents = f.read()

# #Initialize text string and build from file contents
# text = ""
# for i in contents:
#     text += i

# #Initialize prompt with instructions and video text
# prompt = (f"Please summarize this text: " + text)

# response = openai.Completion.create(
#     engine="text-curie-001",
#     prompt=prompt,
#     max_tokens=200,
#     temperature=0.5,
#     n=1)

# summary = response.choices[0].text

# #Write summary to file
# with open('c:/Users/Adam/Documents/CS 195 Project/summary.txt', 'w') as f:
#     f.write(summary)

except TranscriptsDisabled as e:
    print("Could not retrieve a transcript for the video!")



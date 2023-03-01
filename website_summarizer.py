from revChatGPT.V1 import Chatbot as gpt
from configure import get_credentials
from website_parser import get_text
from chunker import create_chunks
import time

start_time = time.time()

path ="c:/Users/Adam/.config/revChatGPT/config.json"
model = gpt(get_credentials(path))

#Initialize url
url = 'https://support.doorloop.com/en/articles/6222125-the-epay-funding-cycle'

#Get text from website
text = get_text(url=url)

chunk_list = create_chunks(text, 800)
summary_list = []

for chunk in chunk_list:
    #Initialize prompt with instructions and video text
    prompt = f"Please summarize the content of this website or article, based on the following paragraph text: {chunk}"
    chunk_summary = ""
    for data in model.ask(prompt):
        chunk_summary = data["message"]

    summary_list.append(chunk_summary)

summary_concatenated = ""
for chunk_summary in summary_list:
    summary_concatenated+= chunk_summary

final_prompt = f"Please summarize this website or article, based on the following description. Strive for accuracy: {summary_concatenated}"
final_summary = ""
for data in model.ask(final_prompt):
    final_summary = data["message"]

print(summary_concatenated)
print(" ")
print(final_summary)

print("--- %s seconds ---" % (time.time() - start_time))




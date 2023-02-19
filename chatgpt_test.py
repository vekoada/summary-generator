from revChatGPT.V1 import Chatbot
import json

def get_credentials(path):
    with open(path) as f:
        return json.load(f)

chatbot = Chatbot(
  config=get_credentials("c:/Users/Adam/.config/revChatGPT/config.json")
  )

print("Chatbot: ")
prev_text = ""
for data in chatbot.ask(
    "Can you explain to me what the revChatGPT.V1 API does?",
):
    message = data["message"][len(prev_text) :]
    print(message, end="", flush=True)
    prev_text = data["message"]
print()
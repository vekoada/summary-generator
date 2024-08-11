import openai
from configure import get_credentials

def translate(target, text, path_to_credentials='c:/Users/Adam/repos/summary-generator/.secret/keys.json'):
    openai.api_key = get_credentials(path_to_credentials)['openai']

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "user", "content" : f"Translate the following text into {target}. Write like a native speaker would, retaining meaning and fluidity: {text}" }])

    result = response['choices'][0]['message']['content']

    return result
import openai
from chunker import create_chunks
from configure import get_credentials

def run(text, chunk_size=800, path_to_credentials='c:/Users/Adam/repos/summary-generator/.secret/keys.json'):
    chunk_list = create_chunks(text, chunk_size)
    summary_list = []

    openai.api_key = get_credentials(path_to_credentials)['openai']

    for chunk in chunk_list:

        #Initialize prompt with instructions and video text
        prompt = (f"Please summarize this video, article, or pdf, based on the following text: {chunk}")

        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=300,
            temperature=0.5,
            n=1)

        chunk_summary = response.choices[0].text
        summary_list.append(chunk_summary)

    summary_concatenated = ""
    for chunk_summary in summary_list:
        summary_concatenated+= ' ' + chunk_summary

    prompt = (f"Please summarize this video, based on the following description. Strive for accuracy and limit yourself to 450 words: {summary_concatenated}")
    response = openai.Completion.create(
    engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.5,
        n=1)

    summary = response.choices[0].text

    return summary
import openai
from chunker import create_chunks, random_chunks
from configure import get_credentials


def run(text, medium, overlap, mode, path_to_credentials='c:/Users/Adam/repos/summary-generator/.secret/keys.json'):
    if mode != 'random':
        chunk_list = create_chunks(text, overlap)
    else:
        chunk_list = random_chunks(text)
    
    summary_list = []

    openai.api_key = get_credentials(path_to_credentials)['openai']

    for chunk in chunk_list:

        #Initialize prompt with instructions and text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{"role": "user", "content" : f"Please summarize this section of a {medium}, based on the following text in 3 sentences or less: {chunk}" }])

        chunk_summary = response['choices'][0]['message']['content']
        summary_list.append(chunk_summary)

    summary_concatenated = ""
    for chunk_summary in summary_list:
        summary_concatenated+= ' ' + chunk_summary

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
         messages=[{"role": "user", "content": f"Please give a thorough and detailed synopsis of this {medium}, based on the following description. Fix all grammar and spelling errors. Write fluently and make it cohesive. Provide a few bullet points at the end with key points/moments. Don't overuse the word {medium}. Add process bullet points if it appears to be a tutorial. Highlight and give specific details around a key moment: {summary_concatenated}"}])

    summary = response['choices'][0]['message']['content']

    return summary

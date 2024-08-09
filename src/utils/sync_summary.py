# Standard imports
import os

# Third party imports
from openai import OpenAI
from groq import AsyncGroq
import requests

# Local imports
from chunker import create_chunks, random_chunks
from configure import get_credentials
from translate import translate

path = os.path.dirname(os.path.abspath(__file__))
groq = AsyncGroq(api_key=get_credentials(path + '/.secret/keys.json')['Groq'])
openai = OpenAI(api_key=get_credentials(path + '/.secret/keys.json')['OpenAI'])

model_config = {
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-3.5-turbo",
        "key": openai.api_key
    },
    "groq": {
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama3-70b-8192",
        "key": groq.api_key
    }
}
def summarize(text: str, medium: str, overlap: int = 50, mode: str = "standard", language: str = 'English') -> str:
    """
    Summarize text and optionally translate the summary.

    Args:
        text (str): Input text to summarize.
        medium (str): Type of media (e.g., 'video', 'article').
        overlap (int): Overlap for chunk creation. Defaults to 50.
        mode (str): Chunking mode ('random' or other). Defaults to 'standard'.
        language (str): Target language for translation. Defaults to 'English'.

    Returns:
        str: Summarized and optionally translated text.
    """
    chunk_list = random_chunks(text) if mode == 'random' else create_chunks(text, overlap)
    concatenated_summaries = concatenate_summaries(chunk_list)
    complete_summary = final_summary(concatenated_summaries, medium)
    return translate(target=language, text=complete_summary) if language.lower() != 'english' else complete_summary

def chunk_summary(chunk: str) -> str:
    """
    Generate a concise summary of a given text chunk using OpenAI's GPT-3.5-turbo model.

    Args:
        chunk (str): A segment of text to be summarized.

    Returns:
        str: A concise summary of the input text chunk.

    This function sends a request to OpenAI's API to generate a summary
    of the provided text chunk using the GPT-3.5-turbo model.
    """
    messages = [{"role": "user", "content": f"Write a concise but descriptive summary of this segment based on the following text: {chunk}"}]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def concatenate_summaries(chunk_list: list[str]) -> str:
    """
    Concatenate summaries of text chunks into a single string.

    Args:
        chunk_list (list[str]): List of text chunks to summarize.

    Returns:
        str: Concatenated summaries of all chunks.
    """
    return " ".join([chunk_summary(chunk) for chunk in chunk_list])

def final_summary(concatenated_summaries: str, medium: str, api: str = 'groq') -> str: # async_summary.py relies on this function
    """
    Generate a final, detailed summary of the content based on concatenated summaries.

    Args:
        concatenated_summaries (str): Combined summaries of content chunks.
        medium (str): Type of media (e.g., 'video', 'article').
        api (str): API to use for summarization. Options are "groq" and "openai".

    Returns:
        str: Comprehensive summary with key points and details.

    Raises:
        ValueError: If invalid API specified or API communication error occurs.
    """
    if api not in model_config:
        raise ValueError(f"Invalid API specified. Possible values are: {', '.join(model_config.keys())}")

    messages = [{"role": "user", "content": f"Provide a detailed synopsis of this {medium}: {concatenated_summaries}"}]

    config = model_config[api]
    endpoint = config["endpoint"]
    model = config["model"]
    key = config["key"]
    
    try:
        response = requests.post(
            url=endpoint,
            json={"model": model, "messages": messages},
            headers={"Authorization": f"Bearer {key}"}
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.RequestException as e:
        raise ValueError(f"Error communicating with the API: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected response format from the API: {str(e)}")
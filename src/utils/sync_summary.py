# Standard imports
import os

# Third party imports
from openai import OpenAI

# Local imports
from chunker import create_chunks, random_chunks
from configure import get_credentials
from translate import translate

path = os.path.dirname(os.path.abspath(__file__))
openai = OpenAI(api_key=get_credentials(path + '/.secret/keys.json')['OpenAI'])

def summarize(text: str, medium: str, overlap: int, mode: str, language: str = 'English') -> str:
    """
    Summarize text and optionally translate the summary.

    Args:
        text (str): Input text to summarize.
        medium (str): Type of media (e.g., 'video', 'article').
        overlap (int): Overlap for chunk creation.
        mode (str): Chunking mode ('random' or other).
        language (str): Target language for translation.

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

def final_summary(concatenated_summaries: str, medium: str) -> str: # async_summary.py relies on this function
    """
    Generate a final, detailed summary of the content based on concatenated summaries.

    Args:
        concatenated_summaries (str): Combined summaries of content chunks.
        medium (str): Type of media (e.g., 'video', 'article').

    Returns:
        str: Comprehensive summary with key points and details.
    """
    messages = [{"role": "user", "content": f"Provide a detailed synopsis of this {medium}: {concatenated_summaries}"}]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content
# Standard imports
import os

# Third party imports
from openai import OpenAI

# Local imports
from chunker import create_chunks, random_chunks
from configure import get_credentials
from translate import translate
import video

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

def final_summary(concatenated_summaries: str, medium: str) -> str:
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
    return 1 #response.choices[0].message.content

########################################################
# Asynchronous summary
########################################################
import aiohttp
import asyncio  

async def async_chunk_summary(session: aiohttp.ClientSession, chunk: str) -> str:
    messages = [{"role": "user", "content": f"Write a concise but descriptive summary of this segment based on the following text: {chunk}"}]
    
    async with session.post(
        'https://api.openai.com/v1/chat/completions',
        json={"model": "gpt-3.5-turbo", "messages": messages},
        headers={"Authorization": f"Bearer {openai.api_key}"}
    ) as response:
        response = await response.json()
        return response['choices'][0]['message']['content'] # An issue I ran into was that the coroutine was never awaited when using `return await response.json()...`. Had await reponse in a variable to fix.

    
    
async def async_concatenate_summaries(chunk_list: list[str]) -> str:
    async with aiohttp.ClientSession() as session:
        tasks = [async_chunk_summary(session, chunk) for chunk in chunk_list]
        summaries = await asyncio.gather(*tasks)
    return " ".join(summaries)

def async_summarize(text: str, medium: str, overlap: int, mode: str, language: str = "English") -> str:
    chunk_list = random_chunks(text) if mode == "random" else create_chunks(text, overlap)
    concatenated_summaries = asyncio.run(async_concatenate_summaries(chunk_list))
    complete_summary = final_summary(concatenated_summaries, medium)
    return translate(target=language, text=complete_summary) if language.lower() != "english" else complete_summary

########################################################
# Performance profiling - https://realpython.com/python-profiling/
########################################################
from cProfile import Profile
from pstats import SortKey, Stats

def log_profile(mode: str): 
    with Profile() as profile:

        # Open log file in write mode
        with open(f"src/utils/logs/{mode}_summary_profiling.log", 'w') as log_file:

            import sys
            original_stdout = sys.stdout
            sys.stdout = log_file # redirect stdout to log file

            text = video.get_transcript('https://www.youtube.com/watch?v=imAYfKW1WG8')
            args = [text, 'video', 40, '', 'english'] # 40 is the overlap. args to unpack for summarize()

            if mode != "async":
                summarize(*args) # unpack args
            else:
                async_summarize(*args) 
                
            stats = Stats(profile)  # profile stats
            stats.strip_dirs()  # strip directories
            stats.sort_stats(SortKey.TIME)  # sort by time

            print(f"Profile: {profile}")
            stats.print_stats()  # print stats
            
            # restore stdout
            sys.stdout = original_stdout

# Run profiling
log_profile("async") 
log_profile("regular")
    
########################################################
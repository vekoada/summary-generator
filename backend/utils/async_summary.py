# Standard imports
import os

# Third party imports
from openai import OpenAI
from groq import AsyncGroq
import aiohttp
import asyncio  

# Local imports
from chunker import create_chunks, random_chunks
from configure import get_credentials
from sync_summary import final_summary
from translate import translate

path = os.path.dirname(os.path.abspath(__file__))
groq = AsyncGroq(api_key=get_credentials(path + '/.secret/keys.json')['Groq'])
openai = OpenAI(api_key=get_credentials(path + '/.secret/keys.json')['OpenAI'])

model_config = {
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o-mini",
        "key": openai.api_key
    },
    "groq": {
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama3-70b-8192",
        "key": groq.api_key
    }
}


def async_summarize(text: str, medium: str, api: str = "groq", chunk_size: int = 1800, overlap: int = 50, mode: str = "standard", language: str = "English") -> str:
    """
    Asynchronously summarize text and optionally translate.

    Args:
        text (str): Input text to summarize.
        medium (str): Type of media (e.g., 'video', 'article').
        api (str, optional): API to use ('groq' or 'openai'). Defaults to 'groq'.
        chunk_size (int, optional): Size of chunk. Defaults to 1800 characters.
        overlap (int, optional): Overlap for chunk creation. Defaults to 50 characters.
        mode (str, optional): Chunking mode ('random' or 'standard'). Defaults to "standard".
        language (str, optional): Target language for translation. Defaults to "English".

    Returns:
        str: Summarized and optionally translated text.
    """
    print("Text received. Creating chunks...\n")
    chunk_list = random_chunks(text) if mode == "random" else create_chunks(text, chunk_size, overlap)
    print("Chunks created. Summarizing chunks...\n")
    concatenated_summaries = asyncio.run(async_concatenate_summaries(chunk_list, api)) # All async functions are awaited here
    print("Summaries received. Creating final summary...\n")
    complete_summary = final_summary(concatenated_summaries, medium)
    print("Final summary created.")
    return translate(target=language, text=complete_summary) if language.lower() != "english" else complete_summary

async def async_chunk_summary(session: aiohttp.ClientSession, chunk: str, api: str = "groq") -> str:
    """
    Asynchronously generate a summary for a single text chunk using either Groq or OpenAI.

    Args:
        session (aiohttp.ClientSession): Async HTTP session.
        chunk (str): Text chunk to summarize.
        api (str, optional): API to use ('groq' or 'openai'). Defaults to 'groq'.

    Returns:
        str: Concise summary of the input chunk.

    Raises:
        ValueError: If invalid API specified or API communication error occurs.
    """
    if api not in model_config:
        raise ValueError(f"Invalid API specified. Possible values are: {', '.join(model_config.keys())}") #show user possible APIs

    messages = [{"role": "user", "content": f"Write a concise but descriptive summary of this segment based on the following text: {chunk}"}]

    config = model_config[api]
    endpoint = config["endpoint"]
    model = config["model"]
    key = config["key"]

    print("Model initialized. Establishing connection...\n")
    
    try:
        async with session.post(
            url=endpoint,
            json={"model": model, "messages": messages},
            headers={"Authorization": f"Bearer {key}"}
        ) as response:
            print("Verifying connection...\n")
            response.raise_for_status() # raise an error if the response is not successful
            print("Connection successful. Waiting for response...\n")
            response_data = await response.json()
            print("Response received. Returning response...\n")
            return response_data['choices'][0]['message']['content'] # An issue I ran into was that the coroutine was never awaited when using `return await response.json()...`. Had await reponse in a variable to fix.
    except aiohttp.ClientError as e:
        raise ValueError(f"Error communicating with the API: {str(e)}")
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected response format from the API: {str(e)}") # expected format: {"choices": [{"message": {"content": "summary"}}]}

async def async_concatenate_summaries(chunk_list: list[str], api: str = "groq") -> str:
    """
    Asynchronously summarize and concatenate text chunks.

    Args:
        chunk_list (list[str]): List of text chunks to summarize.
        api (str, optional): API to use ('groq' or 'openai'). Defaults to 'groq'.

    Returns:
        str: Concatenated summaries of all chunks.
    """
    print("Initializing client session...\n")
    async with aiohttp.ClientSession() as session:
        print("Client session initialized. Creating tasks...\n")
        tasks = [async_chunk_summary(session, chunk, api) for chunk in chunk_list]
        print("Tasks created. Awaiting summaries...\n")
        summaries = await asyncio.gather(*tasks)
        print("Summaries received. Returning summaries...\n")
    return " ".join(summaries)
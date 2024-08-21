from random import randint
from math import log

def create_chunks(text: str, chunk_size: int = 1800, overlap: int = 100) -> list:
    """
    Create text chunks from a given input text with a specified overlap.

    This function takes a text input and divides it into chunks of approximately 1800 characters each, with a specified
    overlap between chunks. The chunks are created in a way that they don't split words in the middle. The chunks are
    returned as a list of strings.

    Args:
        text (str): The input text to be divided into chunks.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of characters to overlap between adjacent chunks.

    Returns:
        list of str: A list containing text chunks as strings.
    """
    chunk_size -= overlap

    # Calculate the number of chunks needed
    num_chunks = (len(text) + chunk_size) // chunk_size
    chunk_list = []

    # Loop over chunks
    start = 0
    for i in range(num_chunks):
        end = min(start + chunk_size, len(text))

        # Ensure we don't split words in the middle
        if end < len(text) and not text[end].isspace():
            end = text.rfind(' ', start, end)
            if end == -1:
                end = start + chunk_size

        # Include overlap if not the first chunk
        if i > 0:
            overlap_start = start - overlap
            if not text[overlap_start].isspace(): # if the overlap doesn't start at a space, find the first occurrence of a space within the overlap range
                overlap_start = text.find(' ', start - overlap, start)
            chunk_list.append(text[overlap_start:end])
        else:
            chunk_list.append(text[start:end])

        start = end + 1

    return chunk_list


def random_chunks(text: str) -> list:
    """
    Divide text into random-sized chunks.

    This function takes an input text and divides it into a random number of chunks, each containing approximately 900
    characters. Chunks are created in a way that avoids splitting words in the middle. The number of chunks is determined
    using a logarithmic formula based on the text length.

    Args:
        text (str): The input text to be divided into chunks.

    Returns:
        list of str: A list containing text chunks as strings.

    Example:
        >>> text = "This is a sample text that will be divided into random-sized chunks."
        >>> chunks = random_chunks(text)
        >>> for chunk in chunks:
        >>>     print(chunk)
        'This is a sample text that will be divided into'
        'random-sized chunks.'
    """
    chunk_size = 900
    chunk_list = []
    
    # Calculate the number of chunks using a logarithmic formula
    num_chunks = int(round((log((((len(text) + chunk_size) / 1000.0) ** 3) + 1)), 0)) 
    
    for i in range(num_chunks):
        start = randint(0, (len(text) - 1 - 900))
        end = min(start + chunk_size, len(text))
        
        # Ensure we don't split words in the middle
        if end < len(text) and not text[end].isspace():
            end = text.rfind(' ', start, end)
            if end == -1:
                end = start + chunk_size
        
        chunk_list.append(text[start:end])

    return chunk_list

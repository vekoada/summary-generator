from random import randint
from math import log

def create_chunks(text, overlap):
    chunk_size = 900 - overlap
    #Set number of chunks
    num_chunks = (len(text) + chunk_size) // chunk_size
    chunk_list = []

    #Loop over chunks
    start = 0
    for i in range(num_chunks):
        end = min(start + chunk_size, len(text))
        if end < len(text) and not text[end].isspace():
            #Adjust end index to stop on whitespace
            end = text.rfind(' ', start, end)
            if end == -1:
                #No whitespace; use original end index
                end = start + chunk_size
        #Include overlap if not first chunk
        if i > 0:
            overlap_start = start - overlap
            chunk_list.append(text[overlap_start:end])
            print(text[overlap_start:end])
            print("-------------------")
        else:
            chunk_list.append(text[start:end])
            print(text[start:end])
            print("-------------------")
        start = end + 1

    return chunk_list

def random_chunks(text):
    chunk_size = 900
    chunk_list = []
    
    num_chunks = int(round((log((((len(text) + chunk_size)/1000.0)**3) + 1)), 0)) 
    
    for i in range(num_chunks):
        start = randint(0, (len(text) - 1 - 900))
        end = min(start + chunk_size, len(text))
        if end < len(text) and not text[end].isspace():
            #Adjust end index to stop on whitespace
            end = text.rfind(' ', start, end)
            if end == -1:
                #No whitespace; use original end index
                end = start + chunk_size
        chunk_list.append(text[start:end])
        print(text[start:end])
        print("-------------------")

    return chunk_list
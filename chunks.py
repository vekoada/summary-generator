
def chunker(text):
    #Set default text chunk size and number of chunks
    chunk_size = 500
    num_chunks = (len(text) + chunk_size - 1) // chunk_size

    x = [] #list of chunks

    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = text[start:end]
        x.append(chunk)

    return x
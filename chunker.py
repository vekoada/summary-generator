def create_chunks(text, chunk_size):
    #Set number of chunks
    num_chunks = (len(text) + chunk_size) // chunk_size
    x = [] #List of chunks

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
        x.append(text[start:end])
        start = end + 1

    return x
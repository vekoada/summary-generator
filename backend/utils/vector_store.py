# Standard imports
import os

# Third party imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Local imports
from configure import get_credentials
from video import get_transcript
from chunker import create_chunks # Need to test performance versus RecursiveCharacterTextSplitter for more segmented text

path = os.path.dirname(os.path.abspath(__file__))
uri = get_credentials(path + '/.secret/keys.json')['MongoDB'] # need to update secret with pw
client = MongoClient(uri)
collection = client["rag_db"]["test"] # rename this

test_transcript = get_transcript('https://www.youtube.com/watch?v=imAYfKW1WG8')

docs = create_chunks(test_transcript, chunk_size=1024, overlap=64)

# Duplicate but with Langchain's RCTS
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
docs_2 = text_splitter.split_text(test_transcript)

model = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1", model_kwargs={ "trust_remote_code": True })

# Store the data as vector embeddings in Atlas
vector_store = MongoDBAtlasVectorSearch.from_documents(
    documents = docs,
    embedding = model,
    collection = collection,
    index_name = "vector_index"
)

# PRINTING CHUNKING OUTPUTS
#for i in range(0, len(docs)):
#    print(len(docs[i]), " | ", len(docs_2[i]), " :\n")
#    print("\t\t", docs[i], "\n\t\t", docs_2[i])
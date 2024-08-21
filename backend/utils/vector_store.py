# Third party imports
#from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_mongodb import MongoDBAtlasVectorSearch
#from pymongo import MongoClient
#from pymongo.server_api import ServerApi
#import warnings

# Local imports
#from video import get_transcript
from chunker import create_chunks

#warnings.filterwarnings('ignore')

test_transcript = "MacOS users can install Python using either the official installer or Homebrew, a versatile package manager. Homebrew is recommended for its simplicity and effectiveness in managing multiple software installations. Using Homebrew: Install Homebrew by running: /bin/bash -c $(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh). Once Homebrew is installed, you can install Python with: brew install python. Homebrew will automatically set up the PATH for you. Verify the installation by opening Terminal and typing: python3 --version. If you prefer the official installer, download it from the Python website, run it, and follow the prompts. Python Setup for Linux Systems Installing Python on Linux can vary slightly by distribution. Here, we’ll focus on Ubuntu but the process is similar for other distros. It’s vital to use the package manager to avoid conflicts. For Ubuntu: Open Terminal. Update the package list with: sudo apt-get update. Install Python: sudo apt-get install python3.8. Or, for a different version: sudo apt-get install python3.10. Verify the installation by typing: python3 --version. You can also install pip to manage packages: sudo apt-get install python3-pip. Using the Terminal for installations ensures everything is properly set up and ready to use. Managing Python Environments and Packages Effective management of Python environments and packages ensures smooth project operations and reduces dependency conflicts. Properly handling dependencies with tools like pip and utilizing virtual environments can make a world of difference. Handling Dependencies and Packages with Pip Pip is our go-to tool for managing Python packages. We can install, update, and remove packages with simple commands. For instance, to install a package, we use: pip install package\_name. To check outdated packages: pip list -o. This helps us keep our environments up to date. Removing a package is equally straightforward: pip uninstall package\_name. We should regularly review our installed packages to avoid bloat and potential conflicts. Keeping a list of currently installed packages can be useful for backup and documentation purposes: pip freeze > requirements.txt. This file can then be used to recreate the environment: pip install -r requirements.txt. Working with Virtual Environments Virtual environments allow us to create isolated Python environments for different projects. This prevents conflicts between project dependencies. To create a virtual environment, use: python -m venv env\_name. Activating the environment is as simple as: source env\_name/bin/activate. For Windows: env\_nameactivate. Within the virtual environment, our project dependencies remain separate from the global installation, ensuring consistent behavior. Deactivating involves: deactivate. Using virtual environments helps us manage libraries more effectively, preventing version clashes and enhancing project reliability. Uninstalling Python and Cleaning Up Whether you’re on Windows, MacOS, or Linux, removing Python involves a combination of steps to ensure no residual files remain. This guide walks through the specific commands and procedures needed for each operating system."

#text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
#docs = text_splitter.split_documents(test_transcript)
# Load the embedding model (https://huggingface.co/nomic-ai/nomic-embed-text-v1")
#model = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1", model_kwargs={ "trust_remote_code": True })
# Connect to your Atlas cluster
#client = MongoClient("<connection-string>")
#collection = client["rag_db"]["test"]
# Store the data as vector embeddings in Atlas
#vector_store = MongoDBAtlasVectorSearch.from_documents(
#    documents = docs,
#    embedding = model,
#    collection = collection,
#    index_name = "vector_index"
#)


docs = create_chunks(test_transcript, chunk_size=512, overlap=64)

print(docs[0], "\n\n")
print(docs[1], "\n\n")
print(docs[2], "\n\n")





#uri = "mongodb+srv://adam:<db_password>@og.u3awi.mongodb.net/?retryWrites=true&w=majority&appName=og"

# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)
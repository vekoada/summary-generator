import requests
from bs4 import BeautifulSoup

def get_text(url):  
    # Send a request to the website and get the response
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        
        # Extract the text content of the website
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')

        text = ''
        for data in soup.find_all("p"): 
            text+= ' ' + data.get_text()
        return text

    else:
        return "Error: Could not retrieve website content"

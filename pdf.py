from pypdf import PdfReader
from urllib import request
from io import BytesIO

def get_text(url):
    #Set custom user agent (to avoid HTTP Error 403) & create request
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = request.Request(url, headers=headers)
    #Open and read
    f = request.urlopen(req).read()

    #Create a file-like object (to avoid downloading)
    pdf_file = BytesIO(f)
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(0, number_of_pages):
        text += reader.pages[i].extract_text()

    return text
from pypdf import PdfReader
from urllib import request
from io import BytesIO

#Set custom user agent (to avoid HTTP Error 403) & create request
headers = {'User-Agent': 'Mozilla/5.0'}
req = request.Request("https://constitutioncenter.org/media/files/constitution.pdf", headers=headers)
#Open and read
f = request.urlopen(req).read()

#Create a file-like object (to avoid downloading)
pdf_file = BytesIO(f)
reader = PdfReader(pdf_file)
number_of_pages = len(reader.pages)
text = ''
for i in range(0, 10):
    text += reader.pages[i].extract_text()

print(text)

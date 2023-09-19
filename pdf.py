from pypdf import PdfReader
from urllib import request
from io import BytesIO

def get_text(url: str) -> str:
    """
    Extracts text from a PDF document accessible via a URL.

    This function takes a URL pointing to a PDF document, retrieves the PDF content, and extracts text from each page
    of the PDF. The extracted text from all pages is concatenated and returned as a single string.

    Args:
        url (str): A string containing the URL of the PDF document.

    Returns:
        str: The extracted text from the PDF document as a single string.

    Example:
        >>> pdf_url = "https://example.com/sample.pdf"
        >>> get_text(pdf_url)
        'This is the extracted text from the PDF document.'

    Note:
        This function relies on the PyPDF2 library to parse and extract text from the PDF document. Ensure that the
        provided URL points to a valid PDF document.

    """
    # Set a custom user agent to avoid HTTP Error 403
    headers = {"User-Agent": "Mozilla/5.0"}
    req = request.Request(url, headers=headers)

    # Open and read the PDF content
    pdf_content = request.urlopen(req).read()

    # Create a file-like object from the PDF content
    pdf_file = BytesIO(pdf_content)

    # Initialize a PDF reader
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)

    # Extract text from each page and concatenate it
    text = ""
    for i in range(number_of_pages):
        text += reader.pages[i].extract_text()

    return text


#print(
#    get_text(
#        "https://gateway.ipfs.io/ipfs/bafykbzacebmbo56npa3qqjw4ygr3m47ejl43obeyxn6ptsiuahshvrmp6ioos?filename=%28New%20Studies%20in%20Archaeology%29%20Joseph%20Tainter%20-%20The%20Collapse%20of%20Complex%20Societies%20%28New%20Studies%20in%20Archaeology%29-Cambridge%20University%20Press%20%281988%29.pdf"
#    )
#)

# Summary Generator

This is a Python program for generating summaries of various types of content, including videos, articles, and PDF documents. It leverages the power of OpenAI's GPT-3 model to create concise and coherent summaries.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Program Structure](#program-structure)
- [License](#license)

## Installation

Before using the summary generator, make sure you have the required Python libraries installed. You can install them using pip:

```bash
pip install youtube-transcript-api
pip install openai
pip install beautifulsoup4
pip install PyPDF2
```
## Usage
To use the summary generator, you can call the main function from `program.py`. It accepts a URL, a mode, and an optional language parameter for translation. Here's an example of how to use it:

```python
if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=2ueCyvI4DEo&ab_channel=BestEverFoodReviewShow'
    mode = 'regular'  # or 'random' for random-sized chunks
    translate_to = 'spanish'  # Optional, specify the target language for translation
    result = main(url=url, mode=mode, translate_to=translate_to)
    print(result)
```

## Structure
The summary generator is organized into several modules:

- `program.py`: The main program that orchestrates the summary generation process. It determines the medium (video, article, or PDF) and then generates the summary.
- `video.py`: Contains functions for extracting video IDs from YouTube URLs and fetching transcribed text from YouTube videos.
- `summary.py`: Generates summaries of content by breaking it into chunks, summarizing each chunk, and then combining the results into a coherent summary.
- `site_parser.py`: Retrieves the text content of an article by making an HTTP request to a website and parsing the HTML using BeautifulSoup.
- `pdf.py`: Extracts text from a PDF document accessible via a URL using the PyPDF2 library.
- `chunker.py`: Provides functions for dividing text into chunks of specified or random sizes.
- `configure.py`: Loads API credentials from a JSON file for authentication.

## Project Background
This summary generator started out as a class project born out of my curiosity for natural language processing and summarization techniques. My aim was simple: to build a tool that could benefit both my friends and me, while also allowing me to experiment with different summarization strategies.

As the project took shape, it quickly became clear that summarization had its fair share of challenges, especially when it came to context windows—the amount of text a summarization model could handle at once. While the tool did provide valuable summaries for various types of content, it soon became apparent that as context windows expanded, summarization complexity soared.

I introduced the random_chunks as a way to summarize texts with logarithmic complexity and initial results showed that summaries weren't much worse than the other method.

I temporarily stopped developing the project since the class ended and ever-expanding context windows in cutting-edge language models seemed to solve the problem. Nevertheless, this project remains a testament to the potential of summarization techniques. I may pick it up again.

### Note
This is not functional in its current state. The user must create an untracked json file with their API keys to use. 

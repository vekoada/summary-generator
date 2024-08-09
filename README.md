# YouTube Video, Article, and PDF Summarizer

## Project Overview

This project is a web app that summarizes YouTube videos, articles, and PDFs based on a user-provided URL. It's currently in the early stages of development.

## Background

I first started building this in January 2023 for a class project, about 2 months after ChatGPT's release. The goal was to create a tool for extracting information from videos to identify valuable information sources.

### Initial Challenges

- Limited context windows (ChatGPT had 4k tokens)
- Inability to summarize longer texts
- Lack of web development experience

### Initial Approach

- Developed a simple chunking algorithm
- Planned for webapp or Chrome extension implementation
- Used synchronous calls (inefficient)

## Project Revival

Despite similar tools now existing, I'm revisiting the project to improve it and learn new skills:

- Asynchronous operations
- Performance profiling
- Fullstack development
- Proper project structure
- Documentation
- Production-level coding practices

## Performance Improvements

### Base Functionality (Synchronous with GPT-3.5-turbo)

- Runtime: 25+ seconds
- 242k+ function calls
- 95% of runtime in `SSLSocket.read()`

### Asynchronous Version

- Runtime: < 9.2 seconds
- 74k function calls
- 2.74x speedup (63.55% reduction)

### Llama 70B via Groq (Asynchronous)

- Runtime: 4.84 seconds
- 53.7k function calls
- 5.63x total speedup (82.23% reduction from base)

## Recent Updates

### August 9 Update

- Improved error handling and imports in `video.py` and summary files
- Optimized code: better docstrings, naming, and separation of concerns
- Created `sync_summary.py` and `async_summary.py`
- Integrated Llama-70B-8192 via Groq API
- Switched from GPT-3.5-turbo to GPT-4-mini
- Implemented profiler for benchmarking

### August 8 Update

- Restructured directory
- Created basic HTML and CSS for future use

## Future Improvements

- Increase chunk size for larger context windows
- Implement adaptive chunking based on model context size
- Evaluate output quality of different models

## Project Status

The project is functional but still has significant room for improvement and expansion.

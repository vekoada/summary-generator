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
- Retrieval-Augmented Generation
- Vector Search
- MongoDB
- Fullstack development
- Proper project structure
- Documentation
- Production-level coding practices

### Roadmap
1. **User provides YouTube URL** (done)
2. **Extract video ID** (done)
3. **Pull transcript if available** (done)
   - If not available, transcribe with Whisper using Groq (TODO)
4. **Make call to Groq LLaMA3 to provide video summary** (done)
5. **Chunk transcript** (done)
6. **Embed transcript chunks** (TODO)
7. **Store embedded transcript chunks in MongoDB vectorstore (pymongo)** (TODO)
8. **Provide user input option on screen** (TODO)
   - Accept user query (TODO)
   - Embed user query (TODO)
   - Compute cosine similarity with embeddings (TODO)
   - Supply relevant embedded chunks as context to Groq LLaMA3 model (TODO)
   - Feed query to model (TODO)
9. **Return model response** (TODO)

### Resources for Future Use
 - Presidental Speeches RAG w/ Groq: https://shorturl.at/T9NkJ
 - RAG w/ MongoDB Atlas: https://shorturl.at/DhY2M

## Performance Improvements

### Performance Optimization
All speedups as measured from base.

| Version | Runtime (s) | Function Calls | Speedup |
|---------|-------------|----------------|---------|
| Base (Sync GPT-3.5) | 25.235 | 242367 | - |
| Async GPT-3.5 | 9.198 | 73185 | 2.74x |
| Async GPT-4o Mini | 8.999 | 54709 | 2.8x
| Async Llama-70B (Groq) | 4.844 | 53760 | 5.63x |

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

### August 10
- Restructured directories to add `frontend`, `backend`, and testing dirs
- Added testing for `video.py`
- Caught a bug in `video.get_transcript()` - default language was `'en'` and so no transcript was getting pulled. Rewrote so tries specificed language, then tries English, and then falls back on first available transcript

### August 9

- Improved error handling and imports in `video.py` and summary files
- Optimized code: better docstrings, naming, and separation of concerns
- Created `sync_summary.py` and `async_summary.py`
- Integrated Llama-70B-8192 via Groq API
- Switched from GPT-3.5-turbo to GPT-4-mini
- Implemented profiler for benchmarking

### August 8

- Restructured directory
- Created basic HTML and CSS for future use

## Future Improvements

- Increase chunk size for larger context windows
- Implement adaptive chunking based on model context size
- Profile smaller Groq model & test quality
- Evaluate output quality of different models

## Project Status

The project is functional but still has significant room for improvement and expansion.

import pytest
from backend.utils.video import get_transcript, extract_youtube_video_id, TranscriptsDisabled, NoTranscriptFound

def test_successful_transcript_retrieval():
    # Test when a valid URL is provided and transcript is available
    url = 'https://www.youtube.com/watch?v=imAYfKW1WG8'
    transcript = get_transcript(url)
    assert isinstance(transcript, str)
    assert len(transcript) > 0

def test_invalid_url():
    # Test when an invalid URL is provided
    url = 'invalid_url'
    with pytest.raises(ValueError):
        get_transcript(url)

def test_no_transcript_available():
    # Test when no transcript is available for the video
    url = 'https://www.youtube.com/watch?v=agBuBFbGZAQ'
    with pytest.raises(TranscriptsDisabled):
        get_transcript(url)

def test_non_english_transcript():
    # Test when only non-English transcripts are available
    url = 'https://www.youtube.com/watch?v=xXBWx7DH0_g'
    transcript = get_transcript(url, 'fr')
    assert isinstance(transcript, str)
    assert len(transcript) > 0

def test_extract_youtube_video_id_called():
    # Test if extract_youtube_video_id is called with the correct URL
    url = 'https://www.youtube.com/watch?v=imAYfKW1WG8'
    video_id = extract_youtube_video_id(url)
    assert video_id == 'imAYfKW1WG8'
    
    # Test if get_transcript calls extract_youtube_video_id
    transcript = get_transcript(url)
    assert isinstance(transcript, str)
    assert len(transcript) > 0

def test_return_type():
    # Test if the function returns a string
    url = 'https://www.youtube.com/watch?v=imAYfKW1WG8'
    transcript = get_transcript(url)
    assert isinstance(transcript, str)
    assert len(transcript) > 0
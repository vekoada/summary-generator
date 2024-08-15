########################################################
# Performance profiling - https://realpython.com/python-profiling/
########################################################

from cProfile import Profile
from pstats import SortKey, Stats

# Local imports
from sync_summary import summarize
from async_summary import async_summarize
from video import get_transcript

def log_profile(mode: str, api: str):
    with Profile() as profile:

        # Open log file in write mode
        with open(f"src/utils/logs/{api}_{mode}_1800_summary_profiling.log", 'w') as log_file:

            import sys
            original_stdout = sys.stdout
            sys.stdout = log_file # redirect stdout to log file

            text = get_transcript('https://www.youtube.com/watch?v=imAYfKW1WG8')
            args = [text, 'video', api] # args to unpack for summarize()

            if mode != "async":
                summarize(*args) # unpack args
            else:
                async_summarize(*args) 
                
            stats = Stats(profile)  # profile stats
            stats.strip_dirs()  # strip directories
            stats.sort_stats(SortKey.TIME)  # sort by time

            print(f"Profile: {profile}")
            stats.print_stats()  # print stats
            
            # restore stdout
            sys.stdout = original_stdout

# Run profiling
log_profile("async", "groq") 
log_profile("regular", "groq")
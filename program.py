import video as v
import site_parser as site
import summary

def main(url):
    if 'youtube.com' in url:
        video_id = v.extract_id(url)
        text = v.get_text(video_id)
    #elif '.pdf' in url:

    else:
        text = site.get_text(url)

    result = summary.run(text=text)

    return result

if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=4x7MkLDGnu8'
    main(url=url)
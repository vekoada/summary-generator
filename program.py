import video as v
import site_parser as site
import method_1
import pdf

def main(url):
    if 'youtube.com' in url:
        text = v.get_text(url=url)
        medium = 'video'
    elif '.pdf' in url:
        text = pdf.get_text(url=url)
        medium = 'PDF'

    else:
        text = site.get_text(url)
        medium = 'article'

    result = method_1.run(text=text, medium=medium)

    return result

if __name__ == "__main__":
    url = 'https://www.babbel.com/learn-spanish'
    print(main(url=url))
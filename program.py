import video as v
import site_parser as site
import summary
import pdf
import time

def main(url, mode):
    if 'youtube.com' in url:
        text = v.get_text(url=url)
        medium = 'video'
    elif '.pdf' in url:
        text = pdf.get_text(url=url)
        medium = 'PDF'

    else:
        text = site.get_text(url)
        medium = 'article'

    result = summary.run(text=text, medium=medium, mode=mode, overlap=300)

    print(len(text))
    return result

if __name__ == "__main__":
    start_time = time.time()
    url = 'https://www.icandrive.com/wp-content/uploads/2019/01/How-to-Change-a-Flat-Tire-Student-Handout.pdf'
    print(main(url=url, mode='random'))
    print("--- %s seconds ---" % (time.time() - start_time))

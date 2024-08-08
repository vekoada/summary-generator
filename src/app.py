import video as v
import site_parser as site
import summary
import pdf
import time

def main(url, mode, translate_to='english'):
    if 'youtube.com' in url:
        text = v.get_text(url=url)
        medium = 'video'
    elif '.pdf' in url:
        text = pdf.get_text(url=url)
        medium = 'PDF'
    else:
        text = site.get_text(url)
        medium = 'article'

    result = summary.run(text=text, medium=medium, mode=mode, lang=translate_to, overlap=0)

    print(len(text))
    return result

if __name__ == "__main__":
    start_time = time.time()
    url = 'https://www.youtube.com/watch?v=2ueCyvI4DEo&ab_channel=BestEverFoodReviewShow'
    print(main(url=url, mode='regular', translate_to='spanish'))
    print("--- %s seconds ---" % (time.time() - start_time))

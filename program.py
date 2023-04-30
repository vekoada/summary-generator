import video as v
import site_parser as site
import summary
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

    result = summary.run(text=text, medium=medium)

    return result

if __name__ == "__main__":
    url = 'https://www.youtube.com/watch?v=2ueCyvI4DEo&ab_channel=BestEverFoodReviewShow'
    print(main(url=url))
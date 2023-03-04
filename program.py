import video as v
import site_parser as site
import summary
import pdf

def main(url):
    if 'youtube.com' in url:
        text = v.get_text(url=url)
    elif '.pdf' in url:
        text = pdf.get_text(url=url)

    else:
        text = site.get_text(url)

    result = summary.run(text=text)

    return result

if __name__ == "__main__":
    url = 'https://arxiv.org/pdf/2004.10178.pdf'
    print(main(url=url)[0])
    print("................................")
    print(main(url=url)[1])
from bs4 import BeautifulSoup
import urllib.request

base_url = "http://www.umdmusic.com/default.asp?Lang=English&Chart=D"
user_agent = "WebDev UW Scraper (webdev@rso.wisc.edu)"


def get_page(url, dont_decode=False):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", user_agent)
    page = urllib.request.urlopen(req)
    
    if dont_decode:
        html = page.read()
    else:
        html = page.read().decode("utf-8")

    return html


if __name__ == "__main__":
    html = get_page(base_url, dont_decode=True)
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    print("")
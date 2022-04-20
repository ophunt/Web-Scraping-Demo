from bs4 import BeautifulSoup
import urllib.request

url = "https://webdevuw.org/"
page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())
print("")
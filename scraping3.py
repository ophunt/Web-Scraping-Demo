from bs4 import BeautifulSoup
import urllib.request

url = "https://webdevuw.org/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
req = urllib.request.Request(url)
req.add_header("User-Agent", user_agent)
page = urllib.request.urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())
print("")
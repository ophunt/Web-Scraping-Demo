import urllib.request

url = "https://webdevuw.org/"
page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
print(html)
print("")
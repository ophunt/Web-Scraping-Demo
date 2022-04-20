from bs4 import BeautifulSoup, Comment
import re
import urllib.request

base_url = "http://www.umdmusic.com/default.asp?Lang=English&Chart=D"
user_agent = "WebDev UW Scraper (webdev@rso.wisc.edu)"


# Class to store songs
class Song:
    def __init__(self, name, date, artists):
        self.name = name
        self.date = date
        self.artists = artists

    def __eq__(self, other):
        return self.name == other.name \
           and self.date == other.date \
           and self.artists == other.artists

    def __hash__(self):
        return hash((self.name, self.date, *self.artists))

    def __str__(self):
        return self.name + " (" + self.date + ")" + " by " + ", ".join(self.artists)

    def __repr__(self):
        return self.name + " (" + self.date + ")" + " by " + ", ".join(self.artists)


def get_page(url, dont_decode=False):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", user_agent)
    page = urllib.request.urlopen(req)
    
    if dont_decode:
        html = page.read()
    else:
        html = page.read().decode("utf-8")

    return html


# Takes a soup of a page and returns the table of hits
def get_table(soup):
    # Get a list of all the comments
    comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    # Find the comment that immediately precedes the table of songs
    for c in comments:
        if c == " Display Chart Table ":
            return c.findNext("table")


# Takes the table and returns the important rows of it
def parse_table(table):
    table_rows = table.findChildren("tr", recusive=False)
    return table_rows[2:]


# Go through each row and put songs in the table
def parse_rows(table_rows, songs, art_re):
    for row in table_rows:
        # Get the song info out of the row
        song_num, song_name, song_date, song_artists = parse_table_row(row, art_re)
        # Only parse the top 40
        if song_num > 40:
            break
        # Create a Song from the row
        song = Song(song_name, song_date, song_artists)
        # Add the song to the set of songs
        songs.add(song)


# Takes the row in a table and get all the song info we need from it
def parse_table_row(row, art_re):
    cells = row.findChildren("td", recusive=False)
    song_name = cells[4].findChildren("b")[0].text
    song_num = int(cells[0].text.strip())
    song_date = cells[5].text.strip()
    song_artists_str = cells[4].text.replace(song_name, "").strip()
    song_artists = parse_artists(song_artists_str, art_re)
    return song_num, song_name, song_date, song_artists


# Take the string of all artists and split it up into the actual individual artists
def parse_artists(str, art_re):
    raw_artists = re.split(art_re, str)
    artists = [s.strip() for s in raw_artists]
    return artists


if __name__ == "__main__":
    songs = set()

    art_delimiters = [",", "/", "&", "x", "featuring", "feat", "with"]
    delim_pattern = "|".join(map(re.escape, art_delimiters))
    art_regex = re.compile(delim_pattern)

    html = get_page(base_url, dont_decode=True)
    soup = BeautifulSoup(html, 'html.parser')
    table = get_table(soup)
    rows = parse_table(table)
    parse_rows(rows, songs, art_regex)

    for s in songs:
        print(s)

    print("")
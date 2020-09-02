from bs4 import BeautifulSoup
# Opted to use BeautifulSoup as it's fairly standard and it makes scraping a lot easier
from urllib.request import urlopen, urlretrieve
from datetime import datetime
import os


class ComicStrip:
    id = ""  # comic name
    path = ""  # path to local file
    last_scraped = ""  # time


# Use the XKCD automatic random comic generator
XKCD_RANDOM_LINK = "https://c.xkcd.com/random/comic/"
# We assume the execute directory of the service will store the images
STORAGE_PATH = os.getcwd()

# Only saving two comic strips at a time
# Set up the storage paths here since we a) are only allowed two and b) they won't be changing
comic_strip_a = ComicStrip()
comic_strip_a.path = STORAGE_PATH + "/a.png"
comic_strip_b = ComicStrip()
comic_strip_b.path = STORAGE_PATH + "/b.png"

# Open up the page and create BeautifulSoup Object
page = urlopen(XKCD_RANDOM_LINK)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')

# Find the comic ID using the title of the comic's page
comic_id = soup.title.string
# Find the url of the comid
comic_div = soup.find(id="comic")
raw_link = comic_div.img['src']
# Make the comic url gettable
get_link = raw_link.replace("//", "https://")  # Why replace when you can just prepend?
print(get_link)

# Create the timestamp of when we acquired the comic
now = datetime.now()
time_stamp = now.strftime("%d/%m/%Y %H:%M:%S")
print(time_stamp)

# Replace the oldest ComicStrip and download and store the comic
if comic_strip_a.last_scraped <= comic_strip_b.last_scraped:
    comic_strip_a.last_scraped = now
    comic_strip_a.id = comic_id
    # download and save to a's path
    urlretrieve(get_link, comic_strip_a.path)
else:
    comic_strip_b.last_scraped = now
    comic_strip_b.id = comic_id
    # download and save to b's path
    urlretrieve(get_link, comic_strip_b.path)

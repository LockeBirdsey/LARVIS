from bs4 import BeautifulSoup
# Opted to use BeautifulSoup as it's fairly standard and it makes scraping a lot easier
from urllib.request import urlopen, urlretrieve
from datetime import datetime, timedelta
from threading import Timer
import os


class ComicStrip:
    def __init__(self, path, last_scraped):
        self.path = path
        self.last_scraped = last_scraped

    def new_comic(self, comic_id, time):
        self.comic_id = comic_id
        self.last_scraped = time

    comic_id = ""  # comic name
    path = ""  # path to local file
    last_scraped = ""  # time


class XKCDScraper:
    # Use the XKCD automatic random comic generator
    XKCD_RANDOM_LINK = "https://c.xkcd.com/random/comic/"
    # We assume the execute directory of the service will store the images
    STORAGE_PATH = os.getcwd()

    # Initialisation of the ComicStrip objects
    # Only saving two comic strips at a time
    # Set up the storage paths here since we a) are only allowed two and b) they won't be changing
    start_time = datetime.now()
    comic_strip_a = ComicStrip(os.path.join(STORAGE_PATH, "a.png"), start_time)
    comic_strip_b = ComicStrip(os.path.join(STORAGE_PATH, "b.png"), start_time)

    # Get the link and other information to the comic
    def get_comic(self):
        # Open up the page and create BeautifulSoup Object
        page = urlopen(self.XKCD_RANDOM_LINK)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')

        # Find the comic ID using the title of the comic's page
        comic_id = soup.title.string
        # Find the url of the comic
        comic_div = soup.find(id="comic")
        raw_link = comic_div.img['src']
        # Make the comic url gettable
        comic_link = raw_link.replace("//", "https://")
        # Create the timestamp of when we acquired the comic
        time_stamp = datetime.now()
        return comic_id, comic_link, time_stamp

    # Check ID against existing downloads
    def check_duplicate(self, comic_id):
        return self.comic_strip_a.comic_id == comic_id or self.comic_strip_b.comic_id == comic_id

    # Return the oldest updated comic strip
    def get_oldest_comic_strip(self, comic_a, comic_b):
        if comic_a.last_scraped <= comic_b.last_scraped:
            return comic_a
        else:
            return comic_b

    # Replace the oldest ComicStrip and download and store the comic
    def store_comic(self, comic_id, link, time_stamp):
        comic = self.get_oldest_comic_strip(self.comic_strip_a, self.comic_strip_b)
        comic.new_comic(comic_id, time_stamp)
        urlretrieve(link, comic.path)
        print("Saving comic to " + comic.path)


class XKCDService:
    # Run hourly +/- 1.5 seconds
    # Not suitable if this service is time critical
    def main(self):
        scraper = XKCDScraper()
        comic_details = scraper.get_comic()
        while scraper.check_duplicate(comic_details[0]) is True:
            comic_details = scraper.get_comic()
        scraper.store_comic(comic_details[0], comic_details[1], comic_details[2])
        self.schedule_next()

    def schedule_next(self):
        # start the timer for the next Execution of the service
        now = datetime.now()
        next_exec = now.replace(day=now.day, hour=now.hour, minute=now.minute, second=now.second,
                                microsecond=now.microsecond) + timedelta(minutes=1)
        time_delta = next_exec - now
        seconds = time_delta.total_seconds()
        timer = Timer(seconds, self.main)
        timer.start()


if __name__ == '__main__':
    comic_service = XKCDService()
    comic_service.main()

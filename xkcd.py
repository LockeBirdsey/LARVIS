from bs4 import BeautifulSoup
# Opted to use BeautifulSoup as it's fairly standard and it makes scraping a lot easier
from urllib.request import urlopen, urlretrieve
from datetime import datetime, timedelta
from threading import Timer
import os


class ComicStrip:
    id = ""  # comic name
    path = ""  # path to local file
    last_scraped = ""  # time


class XKCDScraper:
    # Use the XKCD automatic random comic generator
    XKCD_RANDOM_LINK = "https://c.xkcd.com/random/comic/"
    # We assume the execute directory of the service will store the images
    STORAGE_PATH = os.getcwd()

    # Only saving two comic strips at a time
    # Set up the storage paths here since we a) are only allowed two and b) they won't be changing
    start_time = datetime.now()
    comic_strip_a = ComicStrip()
    comic_strip_a.path = STORAGE_PATH + "/a.png"
    comic_strip_a.last_scraped = start_time
    comic_strip_b = ComicStrip()
    comic_strip_b.path = STORAGE_PATH + "/b.png"
    comic_strip_b.last_scraped = start_time

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
        get_link = raw_link.replace("//", "https://")  # Why replace when you can just prepend?
        print(get_link)
        # Create the timestamp of when we acquired the comic
        time_stamp = datetime.now()
        # time_stamp = now.strftime("%d/%m/%Y %H:%M:%S")
        print(time_stamp)
        return (comic_id, get_link, time_stamp)

    def check_duplicate(self, comic_id):
        # Check ID against existing downloads
        return self.comic_strip_a.id == comic_id or self.comic_strip_b.id == comic_id

    def store_comic(self, comic_id, link, time_stamp):
        # Replace the oldest ComicStrip and download and store the comic
        if self.comic_strip_a.last_scraped <= self.comic_strip_b.last_scraped:
            self.comic_strip_a.last_scraped = time_stamp
            self.comic_strip_a.id = comic_id
            # download and save to a's path
            urlretrieve(link, self.comic_strip_a.path)
        else:
            self.comic_strip_b.last_scraped = time_stamp
            self.comic_strip_b.id = comic_id
            # download and save to b's path
            urlretrieve(link, self.comic_strip_b.path)


class XKCDService:
    # run hourly
    # on the hour
    def main(self):
        scraper = XKCDScraper()
        comic_details = scraper.get_comic()
        while scraper.check_duplicate(comic_details) is True:
            comic_details = scraper.get_comic()
        scraper.store_comic(comic_details[0], comic_details[1], comic_details[2])
        self.schedule_next()

    def schedule_next(self):
        # start the timer for the next Execution
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

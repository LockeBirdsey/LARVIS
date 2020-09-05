from bs4 import BeautifulSoup
# Opted to use BeautifulSoup as it's fairly standard and it makes scraping a lot easier
from urllib.request import urlopen, urlretrieve
from datetime import datetime, timedelta
from threading import Timer
from pathlib import Path


class ComicStrip:
    def __init__(self, path, last_scraped, comic_name):
        self.root_path = path
        self.last_scraped = last_scraped
        self.comic_name = comic_name

    def new_comic(self, comic_id, time, save_path):
        self.comic_id = comic_id
        self.last_scraped = time
        self.most_recent_save = save_path

    comic_id = ""  # comic name
    comic_name = ""  # local name for comic
    root_path = ""  # path to local file
    last_scraped = ""  # time
    most_recent_save = ""  # the most recent save location on disk


class XKCDScraper:
    # Use the XKCD automatic random comic generator
    XKCD_RANDOM_LINK = "https://c.xkcd.com/random/comic/"
    # We assume the execute directory of the service will store the images
    STORAGE_PATH = Path.cwd()

    # Initialisation of the ComicStrip objects
    # Only saving two comic strips at a time
    # Set up the storage paths here since we a) are only allowed two and b) they won't be changing
    start_time = datetime.now()
    comic_strip_a = ComicStrip(STORAGE_PATH, start_time, "xkcd_comic_a")
    comic_strip_b = ComicStrip(STORAGE_PATH, start_time, "xkcd_comic_b")

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

    def delete_previous_comic_instance(self, comic):
        if len(str(comic.most_recent_save)) > 0:
            Path(comic.most_recent_save).unlink(missing_ok=False)

    # Replace the oldest ComicStrip and download and store the comic
    def store_comic(self, comic_id, link, time_stamp):
        comic = self.get_oldest_comic_strip(self.comic_strip_a, self.comic_strip_b)
        self.delete_previous_comic_instance(comic)
        comic_path = comic.root_path.joinpath(comic.comic_name + Path(link).suffix)
        comic.new_comic(comic_id, time_stamp, comic_path)
        print("Saving comic to " + str(comic_path))
        urlretrieve(link, comic_path)


class XKCDService:
    # Run hourly +/- 1.5 seconds (comic scraping is not constant in time)
    # Not suitable if this service is time critical
    def main(self):
        scraper = XKCDScraper()
        new_exec_time = datetime.now()
        comic_details = scraper.get_comic()
        while scraper.check_duplicate(comic_details[0]) is True:
            comic_details = scraper.get_comic()
        scraper.store_comic(comic_details[0], comic_details[1], comic_details[2])
        self.schedule_next(new_exec_time)

    def schedule_next(self, last_exec):
        # start the timer for the next Execution of the service
        next_exec = last_exec + timedelta(hours=1)
        time_delta = next_exec - last_exec
        seconds = time_delta.total_seconds()
        timer = Timer(seconds, self.main)
        timer.start()


if __name__ == '__main__':
    comic_service = XKCDService()
    comic_service.main()

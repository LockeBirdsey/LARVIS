import unittest
from datetime import datetime, timedelta
from time import sleep
from xkcd import XKCDScraper, XKCDService, ComicStrip


class TestXKCDScraper(unittest.TestCase):
    def test_for_duplicates(self):
        scraper = XKCDScraper()
        start_time = datetime.now()
        comic_a = ComicStrip("", start_time, "comic_a")
        comic_b = ComicStrip("", start_time, "comic_b")
        scraper.comic_strip_a = comic_a
        scraper.comic_strip_b = comic_b
        # update both comics manually

        # Make request
        scraped_id = "SomeComic1"
        # No duplicates can exist at this stage
        self.assertFalse(scraper.check_duplicate(comic_id=scraped_id))
        sleep(1)  # simulate downloading the comic
        comic_a.new_comic(scraped_id, datetime.now(), scraped_id + ".png")

        # Make new request
        scraped_id = "SomeComic2"
        self.assertFalse(scraper.check_duplicate(comic_id=scraped_id))
        sleep(1)  # simulate downloading the comic
        comic_b.new_comic(scraped_id, datetime.now(), scraped_id + ".png")

        # Make new request
        scraped_id = "SomeComic2"
        self.assertTrue(scraper.check_duplicate(comic_id=scraped_id))
        sleep(1)  # simulate downloading the comic
        comic_a.new_comic(scraped_id, datetime.now(), scraped_id + ".png")

    def test_get_newest_comic(self):
        scraper = XKCDScraper()
        start_time = datetime.now()
        comic_a = ComicStrip("", start_time, "comic_a")
        comic_b = ComicStrip("", start_time, "comic_b")
        # Will return the first comic if both are equal
        self.assertEqual(scraper.get_newest_comic_strip(comic_a, comic_b), comic_a)
        sleep(1)  # simulate downloading the comic
        comic_a.new_comic("SomeComic1", datetime.now(), "aPath.png")
        self.assertEqual(scraper.get_newest_comic_strip(comic_a, comic_b), comic_a)
        sleep(1)  # simulate downloading the comic
        comic_b.new_comic("SomeComic2", datetime.now() + timedelta(hours=1), "bPath.png")
        self.assertEqual(scraper.get_newest_comic_strip(comic_a, comic_b), comic_b)

    def test_get_oldest_comic(self):
        scraper = XKCDScraper()
        start_time = datetime.now()
        comic_a = ComicStrip("", start_time, "comic_a")
        comic_b = ComicStrip("", start_time, "comic_b")
        # Will return the first comic if both are equal
        self.assertEqual(scraper.get_oldest_comic_strip(comic_a, comic_b), comic_a)
        sleep(1)  # simulate downloading the comic
        comic_a.new_comic("SomeComic1", datetime.now(), "aPath.png")
        self.assertEqual(scraper.get_oldest_comic_strip(comic_a, comic_b), comic_b)
        sleep(1)  # simulate downloading the comic
        comic_b.new_comic("SomeComic2", datetime.now() + timedelta(hours=1), "bPath.png")
        self.assertEqual(scraper.get_oldest_comic_strip(comic_a, comic_b), comic_a)

from scraper.base_scraper import Scraper


class TestScraper:

    def test_split_url(self):
        url = "https://www.example.com/about"
        assert Scraper().split_url(url) == ["www.example.com", "about"]


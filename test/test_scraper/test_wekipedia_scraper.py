import pytest
from bs4 import BeautifulSoup

from scraper.wikipedia_scraper import CityTemperatureCrawler
from test.fixtures import table_html


class TestCityTemperatureCrawler:

    @classmethod
    def setup_class(cls):

        cls.table_html = table_html
        cls.table_soup = BeautifulSoup(table_html, features="lxml")

    def test_scrape_table(self):
        
        expected_table_response = [
            {
                "Firstname": "Jill",
                "Lastname": "Smith",
                "Age": '50'
            },
            {
                "Firstname": "Eve",
                "Lastname": "Jackson",
                "Age": '94'
            }
        ]

        actual_result = CityTemperatureCrawler().scrape_table(self.table_soup)
        print(actual_result)
        assert expected_table_response == actual_result

import random
import re
import sys
from bs4 import BeautifulSoup
from utils.requester import Requester
# url = "https://www1.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm"
# url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"


class Scraper:

    def __init__(self, urls=None, timeout=15, list_of_regex=None, tags=None):

        self.urls = urls or []
        self.failed = []
        self.timeout = timeout
        self.links = []
        self.list_of_regex = []
        self.tags = []
        self.soup = None
        self.pages = set()

    def scrape(self, url):
        failed = []
        response = Requester(url, timeout=self.timeout).make_request(self.failed)
        self.add_soup(response)
        return self.soup

    def add_soup(self, response):
        self.soup = BeautifulSoup(response, features="lxml")

    def generate_links(self, url, tag=None, attribs=None, regex=None):
        soup = self.scrape(url)
        if attribs:
            soup = soup.find(tag, attribs)
        else:
            soup = soup.find(tag)
        if regex:
            soup = soup.findAll(href=re.compile(regex))
        else:
            soup = soup.findAll("a")
        links = []
        for s in soup:
            if "href" in s.attrs:
                if s.attrs["href"] not in self.pages:
                    link = s.attrs["href"]
                    links.append(link)
        return links

    def get_internal_links(self, soup, host, include_url=None):
        internal_links = set()
        regex = "^(\/|.*" + include_url +")"
        try:
            link_result_set = soup.findAll("a", href=re.compile(regex))
        except Exception as e:
            link_result_set = []
            print(soup)
            print(regex)
            print(f"failed   external link. {e}" )
        for link in link_result_set:
            if "href" in link.attrs:
                if link.attrs["href"] not in internal_links:
                    if link.attrs["href"].startswith("/"):
                        internal_links.add(f"{host}/{link.attrs['href']}")
                    else:
                        internal_links.add(link.attrs["href"])
        return internal_links


    def get_external_links(self, soup, exclude_url):
        external_links = set()
        if not exclude_url:
            regex = "^(https?|www).*"
        else:
            regex = f"^(https?|www).*(?!{exclude_url}).*"
        try:
            link_result_set = soup.findAll("a", href=re.compile(regex))
        except Exception as e:
            link_result_set = []
            print(soup)
            print(regex)
            print(f"failed   external link. {e}" )
        for link in link_result_set:
            if "href" in link.attrs:
                if link.attrs["href"] not in external_links:
                    external_links.add(link.attrs["href"])

        return external_links

    def split_url(self, url):

        regex = r"https?:\/\/"
        return re.sub(regex, "", url).split("/")

    def get_random_external_link(self, start_url):

        soup = self.scrape(start_url)
        external_links = self.get_external_links(soup, self.split_url(start_url))
        while len(external_links) == 0:
            internal_links = self.get_internal_links(soup, self.split_url(start_url)[0], self.split_url(start_url)[0])
            start_url = random.sample(internal_links, 1)[0] if internal_links else None
            external_links = self.get_external_links(soup, self.split_url(start_url))
        return random.sample(external_links, 1)[0] if external_links else None

    def get_external_link_only(self, start_url, count=1000):

        link = start_url
        while count > 0:
            link = self.get_random_external_link(link)
            print(f"random external link is {link}")
            count -= 1

    def get_table(self):
        pass

    def crawl_link(self, tag=None, reqex=None, ):

        pass



from scraper.base_scraper import Scraper
import pandas as pd

class WikipediaCrawler(Scraper):

    def __init__(self):
        super().__init__()

    def crawl(self, url):

        links = self.generate_links(url=url,tag="div", attribs={"id":"bodyContent"}, regex="^(/wiki/)((?!:).)*$")
        for link in links:
            print(link)



class CityTemperatureCrawler(WikipediaCrawler):

    """
        <body class="mediawiki">
            <div id="content"></div>
                <div id="firstHeading">page heading here</div>
                <div id="bodyContent">
                    <div id="mw-content-text">
                        <div class="mw-parser-output">
                            <div class ="hatnote"></div>
                            <p>pragraph text here</p>
                            <h2>Table heading</h2>
                            <table class="wikitable">
                                <caption>table caption here</caption>
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th></th>
                                        .....
                                        .....
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td></td>
                                        <td></td>
                                        .....
                                        .....
                                    </tr>
                                </tbody>
                                <tfoot></tfoot>
                            </table>
                            <h2></h2>
                            <table></table>
                            ....
                            ....
                            <h2>see also</h2>
                            <ul></ul>
                            <h2>Reference</h2>
                            <div class="reflist">list of refrences</div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    """

    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature"
        super().__init__()

    def crawl(self, url):
        pass

    def scrape_tables(self):
        soup = self.scrape(self.url)
        body_soup = soup.find('div', id="bodyContent")
        tables = body_soup.findAll("table")
        for table in tables:
            if table.name == "table":
                prev_sibling_tag = table.previous_sibling
                while True:
                    if prev_sibling_tag.name == "h2":    # heading is of bs4.element.Tag type
                        heading_tag = prev_sibling_tag
                        break
                    prev_sibling_tag = prev_sibling_tag.previous_sibling
                region = heading_tag.find("span").text
                print(region)
        return None

    def scrape_table(self, table_soup):

        headers = table_soup.findAll("th")
        cols = []
        for header in headers:
            cols.append(header.text)

        rows = table_soup.findAll("tr")
        data = []
        for row in rows:
            tds = row.findAll("td")
            values = []
            print(tds)
            for td in tds:
                val = td.text
                values.append(val)
            if values:
                data.append(values)
        print(data)
        df = pd.DataFrame(data, columns=cols)
        print(df.head())
        return df.to_dict(orient="records")



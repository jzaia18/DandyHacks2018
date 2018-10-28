"""
Spider made using scrapy

Author: Justin Yau
"""

import scrapy
import argparse
import sys
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from typing import List


items = []


class RetrievedItem(Item):
    title = Field()
    body = Field()


class Crawly(CrawlSpider):
    name = 'usatoday.com'
    allowed_domains = ['usatoday.com']
    start_urls = ['https://www.usatoday.com/', 'https://www.usatoday.com/sports/', 'https://www.usatoday.com/news/',
                  'https://www.usatoday.com/money/', 'https://www.usatoday.com/tech/', 'https://www.usatoday.com/travel/'
                  'https://www.usatoday.com/opinion/', 'https://www.usatoday.com/news/investigations/']

    rules = (
        Rule(LinkExtractor(allow=('story/',)), callback='parse_item'),
    )

    def parse_item(self, response):
        item = RetrievedItem()
        item["title"] = [''.join(response.xpath(".//head/title/text()").extract()).replace("\xa0", "")]
        item["body"] = [''.join(response.xpath(".//p/text()").extract()[10:]).replace("\xa0", "")]
        return item


class ItemCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        items.append(item)


def setup_arguments(args) -> argparse.ArgumentParser:
    """
    Setups the arguments of this specific program that will return a list containing desired data from a inputted
    HTML website
    :return: An argument parser with all the arguments set up
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", help="Whether you would like to retrieve title information from the "
                                              "specified site", action="store_true")
    parser.add_argument("-b", "--body", help="Whether you would like to retrieve body information from the "
                                             "specified site", action="store_true")
    return parser.parse_args(args)


def process_item(item: scrapy.item, args: argparse.ArgumentParser) -> str:
    if args.title:
        return item["TITLE"]
    if args.body:
        return item["BODY"]
    return ""


def main(args) -> List[str]:
    args = setup_arguments(args)

    process = CrawlerProcess({
    'USER_AGENT': 'scrapy',
    'LOG_LEVEL': 'INFO',
    'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100}
    })
    process.crawl(Crawly)
    process.start()  # the script will block here until all crawling jobs are finished

    result = []
    if args.title:
        for item in items:
            result += item["title"]
    else:
        for item in items:
            result += item["body"]
    # open("usaTODAY(BODY).txt", "w", encoding="UTF-8") as f:
    #    f.write('["' + '", "'.join(result) + '"]')
    return result


if __name__ == "__main__":
    main(sys.argv[1:])

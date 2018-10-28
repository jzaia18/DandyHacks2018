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
    name = 'huffingtonpost.com'
    allowed_domains = ['huffingtonpost.com']
    start_urls = ['https://www.huffingtonpost.com', 'https://www.huffingtonpost.com/section/us-news',
                  'https://www.huffingtonpost.com/section/world-news', 'https://www.huffingtonpost.com/section/business',
                  'https://www.huffingtonpost.com/section/green', 'https://www.huffingtonpost.com/section/health',
                  'https://www.huffingtonpost.com/topic/social-justice', 'https://www.huffingtonpost.com/section/arts',
                  'https://www.huffingtonpost.com/section/media', 'https://www.huffingtonpost.com/section/celebrity',
                  'https://www.huffingtonpost.com/section/tv', 'https://www.huffingtonpost.com/topic/us-congress',
                  'https://www.huffingtonpost.com/topic/2018-elections',
                  'https://www.huffingtonpost.com/topic/extremism', 'https://www.huffingtonpost.com/section/queer-voices'
                  , 'https://www.huffingtonpost.com/section/women', 'https://www.huffingtonpost.com/section/black-voices',
                  'https://www.huffingtonpost.com/section/latino-voices', 'https://www.huffingtonpost.com/section/asian-voices',
                  'https://www.huffpost.com/life/style', 'https://www.huffpost.com/life/taste', 'https://www.huffpost.com/life/huffpost-home',
                  'https://www.huffpost.com/life/money', 'https://www.huffpost.com/life/parents', 'https://www.huffpost.com/life/relationships',
                  'https://www.huffpost.com/life/style', 'https://www.huffpost.com/life/travel', 'https://www.huffpost.com/life/healthy-living',
                  'https://www.huffpost.com/life/worklife', 'https://www.huffpost.com/life/topic/finds']

    rules = (
        Rule(LinkExtractor(allow=('entry/',)), callback='parse_item'),
    )

    def parse_item(self, response):
        item = RetrievedItem()
        item["title"] = [''.join(response.xpath(".//head/title/text()").extract()).replace(" | HuffPost", "").
                         replace("\xa0", "")]
        item["body"] = response.xpath(".//p/text()").extract()[10:]
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
    #with open("huffPost(TITLE).txt", "w", encoding="UTF-8") as f:
    #    f.write('["' + '", "'.join(result) + '"]')
    return result


if __name__ == "__main__":
    main(sys.argv[1:])

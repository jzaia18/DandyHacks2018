"""
Spider

Retrieves all article urls from a given page on an Obama site and passes it to a scrapers for processing

Author: Justin Yau
"""

import argparse                       # ArgumentParser
import requests                       # get
import sys                            # argv
from bs4 import BeautifulSoup         # findAll
from scrapers import obamaScrapper    # main
from typing import List


def setup_arguments(args) -> argparse.ArgumentParser:
    """
    Setups the arguments of this specific program
    :return: An argument parser with all the arguments set up
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("html_link", help="The html link to scrap specific information from")
    return parser.parse_args(args)


def crawl(links) -> List[str]:
    """
    Constructs the appropriate href and passes it to the scrapers for information
    :param links: The list of 'links' that are essentially elements with attributes according to the website
    :param pass_args: List of arguments based on the input
    :return: - Information collected by the scrapers concatenated together
    """
    used_href = {}
    headers = []
    for link in links:
        href = link.get("href")
        if not (href in used_href) and "htm" in href:
            used_href[href] = True
            if href[0] != "/":
                href = "/" + href
            href = "http://obamaspeeches.com" + href
            # print(href)
            headers.append(obamaScrapper.main([href]).replace("\xa0", "").strip() + " ")
    return headers


def main(args) -> str:
    args = setup_arguments(args)
    html_code = requests.get(args.html_link)
    plain_text = html_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    headers = []
    headers += crawl(soup.findAll("a"))
    # print(headers)
    return headers


if __name__ == "__main__":
    main(sys.argv[1:])

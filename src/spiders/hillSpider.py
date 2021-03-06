"""
Spider

Retrieves all article urls from a given page on the Hill and passes it to a scrapers for processing

Author: Justin Yau
"""

import argparse                 # ArgumentParser
import requests                 # get
import sys                      # argv
from bs4 import BeautifulSoup   # findAll
from scrapers import scraper    # main
from typing import List


def setup_arguments(args) -> argparse.ArgumentParser:
    """
    Setups the arguments of this specific program
    :return: An argument parser with all the arguments set up
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("html_link", help="The html link to scrap specific information from")
    parser.add_argument("-t", "--title", help="Whether you would like to retrieve title information from the "
                                              "specified site", action="store_true")
    parser.add_argument("-b", "--body", help="Whether you would like to retrieve body information from the "
                                             "specified site", action="store_true")
    return parser.parse_args(args)


def main(args) -> List[str]:
    args = setup_arguments(args)
    html_code = requests.get(args.html_link)
    plain_text = html_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    used_href = {}
    headers = []
    pass_args = []
    if args.title:
        pass_args.append("-t")
    if args.body:
        pass_args.append("-b")
    for link in soup.findAll("h4"):
        href = link.find("a").get("href")
        if not (href in used_href):
            used_href[href] = True
            href1 = "https://thehill.com" + href
            headers.append(scraper.main([href1] + pass_args).replace("\n", "").replace("| TheHill", "").replace("\xa0",
                                                                                                                ""))
    # print(headers)
    return headers


if __name__ == "__main__":
    main(sys.argv[1:])

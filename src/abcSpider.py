"""
Spider

Retrieves all article urls from a given page on the ABC and passes it to a scraper for processing

Author: Justin Yau
"""

import argparse                 # ArgumentParser
import requests                 # get
import scraper                  # main
import sys                      # argv
from bs4 import BeautifulSoup   # findAll


def setup_arguments(args) -> argparse.ArgumentParser:
    """
    Setups the arguments of this specific program that will return a list containing desired data from a inputted
    HTML website
    :return: An argument parser with all the arguments set up
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("html_link", help="The html link to scrap specific information from")
    parser.add_argument("-t", "--title", help="Whether you would like to retrieve title information from the "
                                              "specified site", action="store_true")
    parser.add_argument("-b", "--body", help="Whether you would like to retrieve body information from the "
                                             "specified site", action="store_true")
    return parser.parse_args(args)


def main(args) -> str:
    args = setup_arguments(args)
    html_code = requests.get(args.html_link)
    plain_text = html_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    used_href = {}
    headers = ""
    pass_args = []
    if args.title:
        pass_args.append("-t")
    if args.body:
        pass_args.append("-b")
    for link in soup.findAll("a", {"class": "white-ln"}):
        href = link.get("href")
        if not (href in used_href) and "https://abcnews.go.com/US" in href:
            used_href[href] = True
            headers += scraper.main([href] + pass_args).replace("\n", "").replace("- ABC News", "")
    # print(''.join(headers))
    return ''.join(headers)


if __name__ == "__main__":
    main(sys.argv[1:])

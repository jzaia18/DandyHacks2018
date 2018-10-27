"""
HTML Scrapper

Scrapes information from websites using lxml and requests
Passes a general xpath query to retrieve specified information regarding an news article
This is to be used in co-junction with a markov chain to generate a new article

Author: Justin Yau
"""

from lxml import html       # fromstring
from typing import List
import requests             # get
import argparse             # ArgumentParser


"""
Notes:

Onion Header:
//title/text()

Onion Body: 
//p/text()

Wired Header:
//title/text()

Wired Body:
//p/text()

"""


def initialize_dictionary() -> dict:
    """
    Initializes a basic dictionary containing generalized xpath queries for news articles made by WIRED and the ONION
    :return: A dictionary filled with xpath queries
    """
    xpath_queries = {"TITLE": "//title/text()",
                     "BODY": "//p/text()"}
    return xpath_queries


def setup_arguments() -> argparse.ArgumentParser:
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
    return parser.parse_args()


def main() -> List[str]:
    queries = initialize_dictionary()
    args = setup_arguments()
    page = requests.get(args.html_link)
    if page.status_code == requests.codes.ok:
        content = html.fromstring(page.content)
        target = []
        if args.title:
            target += content.xpath(queries["TITLE"])
        if args.body:
            target += content.xpath(queries["BODY"])
        print(target)
        return target
    else:
        raise Exception("HTML link is either down or invalid! Please input another link...")


if __name__ == "__main__":
    main()

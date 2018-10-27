"""
HTML Scrapper

Scrapes information from websites using lxml and requests
Passes a general xpath query to retrieve specified information regarding an news article
This is to be used in co-junction with a markov chain to generate a new article

Author: Justin Yau
"""

import requests             # get
import sys                  # argv
import argparse             # ArgumentParser
from lxml import html       # fromstring


def setup_arguments(args) -> argparse.ArgumentParser:
    """
    Setups the arguments of this specific program that will return a list containing desired data from a inputted
    HTML website
    :return: An argument parser with all the arguments set up
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("html_link", help="The html link to scrap specific information from")
    return parser.parse_args(args)


def main(args) -> str:
    args = setup_arguments(args)
    page = requests.get(args.html_link)
    if page.status_code == requests.codes.ok:
        content = html.fromstring(page.content)
        target = []
        target += content.xpath("//font[@size='3'][@face='Verdana, Arial, Helvetica, sans-serif']/text()")
        # print(' '.join(target).replace('\n', '').replace('              ', ''))
        return (' '.join(target)).replace('\n', '').replace('              ', '')
    else:
        raise Exception("HTML link is either down or invalid! Please input another link...")


if __name__ == "__main__":
    main(sys.argv[1:])

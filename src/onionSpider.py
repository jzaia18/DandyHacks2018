"""
Spider

Retrieves all article urls from a given page on the Onion and passes it to a scraper for processing

Author: Justin Yau
"""

import argparse                 # ArgumentParser
import requests                 # get
import scraper                  # main
from bs4 import BeautifulSoup   # findAll


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


def crawl(links, pass_args) -> str:
    """
    Constructs the appropriate href and passes it to the scraper for information
    :param links: The list of 'links' that are essentially elements with attributes according to the website
    :param pass_args: List of arguments based on the input
    :return: - Information collected by the scraper concatenated together
    """
    used_href = {}
    headers = ""
    for link in links:
        href = link.get("href")
        if not (href in used_href):
            used_href[href] = True
            headers += scraper.main([href] + pass_args) + " "
    return headers


def main() -> str:
    args = setup_arguments()
    html_code = requests.get(args.html_link)
    plain_text = html_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    headers = ""
    pass_args = []
    if args.title:
        pass_args.append("-t")
    if args.body:
        pass_args.append("-b")
    headers += crawl(soup.findAll("a", {"data-contenttype": "Headline"}), pass_args)    # Headline articles
    headers += crawl(soup.findAll("a", {"class": "js_entry-link"}), pass_args)          # Lower priority articles
    #print(''.join(headers))
    return ''.join(headers)


if __name__ == "__main__":
    main()

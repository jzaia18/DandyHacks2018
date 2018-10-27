"""
Google Image Scraper

Queries specified words into google and retrieves a specified number of images

Author: Justin Yau
"""


import argparse             # ArgumentParser
import urllib.request       # urlopen
import json                 # loads
from bs4 import BeautifulSoup
from typing import List


def setup_arguments() -> argparse.ArgumentParser:
    """
    Setups the arguments of this specific program
    :return: An argument parser with all the arguments set up
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="The google image query to make", type=str)
    parser.add_argument("number", help="How many image urls to return from the specified search query", type=int)
    return parser.parse_args()


def construct_google_url(search_query: str) -> str:
    """
    Constructs the google search url based on the query
    :param search_query: - The query to make the image search for
    :return: - A google search url
    """
    search_query1 = search_query.split()
    search_query1 = '+'.join(search_query1)
    return "https://www.google.co.in/search?q="+search_query1+"&source=lnms&tbm=isch"


def main() -> List[str]:
    args = setup_arguments()
    query_url = construct_google_url(args.query)
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(query_url, headers=header)), 'html.parser')
    image_url = []
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link = json.loads(a.text)["ou"]
        image_url.append(link)
        if len(image_url) == args.number:
            return image_url
    return image_url


if __name__ == "__main__":
    main()

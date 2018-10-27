"""
Spider releaser

Author: Justin Yau
"""

from spiders import abcSpider, onionSpider, wiredSpider
from typing import List

url_to_visit = {"ONION": ["https://www.theonion.com/",
                          "https://www.theonion.com/tag/election-2018",
                          "https://politics.theonion.com/",
                          "https://sports.theonion.com/",
                          "https://local.theonion.com/",
                          "https://entertainment.theonion.com/",
                          "https://www.theonion.com/tag/opinion"],
                "WIRED": ["https://www.wired.com/",
                          "https://www.wired.com/category/business/",
                          "https://www.wired.com/category/culture/",
                          "https://www.wired.com/category/gear/",
                          "https://www.wired.com/category/ideas/",
                          "https://www.wired.com/category/science/",
                          "https://www.wired.com/category/security/",
                          "https://www.wired.com/category/transportation/"],
                "ABC": ["https://abcnews.go.com/",
                        "https://abcnews.go.com/US",
                        "https://abcnews.go.com/Politics",
                        "https://abcnews.go.com/International",
                        "https://abcnews.go.com/Entertainment",
                        "https://abcnews.go.com/Lifestyle",
                        "https://abcnews.go.com/Health",
                        "https://abcnews.go.com/VR",
                        "https://abcnews.go.com/Technology",
                        "https://abcnews.go.com/Sports",
                        "https://abcnews.go.com/alerts/weather"]}


def main() -> List[str]:
    training_set = []
    pass_arg = ["-b"]
    for link in url_to_visit["ONION"]:
        training_set += onionSpider.main([link] + pass_arg)     # + "\n"
    for link in url_to_visit["WIRED"]:
        training_set += wiredSpider.main([link] + pass_arg)     # + "\n"
    for link in url_to_visit["ABC"]:
        training_set += abcSpider.main([link] + pass_arg)       # + "\n"
    return training_set


if __name__ == "__main__":
    main()

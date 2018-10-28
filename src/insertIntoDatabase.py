from pymongo import MongoClient
import codecs
import datetime
from scrapers import googleScraper

client = MongoClient()
db = client.articles
articles = db.articles


def add_new_story(title, content, category = "General News"):
    date = str(datetime.datetime.today())
    date = date[0:date.find(' ')]
    img_url = googleScraper.main([title, "1"])[0]
    articles.insert_one({
        "title": title,
        "content": content,
        "img_url": img_url,
        "date": date,
        "category": category,
        "votes": 0
    })

if __name__ == "__main__":
    print("Input the name of the file that holds the titles")
    titles = input()
    titles = eval(codecs.open(titles, 'r', 'utf-8').read())
    print("Input the content")
    content = input()
    content = eval(codecs.open(content, 'r', 'utf-8').read())
    for i in range(len(titles)):
        #print(titles[i], content[i])
        add_new_story(titles[i], content[i])

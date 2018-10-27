from pymongo import MongoClient
from bson.objectid import ObjectId
import time

client = MongoClient()
db = client.articles
articles = db.articles
comments = db.comments


#For testing
def get_n_stories(n):
    return articles.find()[0:n]

def get_by_id(article_id):
    return articles.find_one({"_id": ObjectId(article_id)})

def update_votes(article_id, direction):
    i = 0
    if direction == "right":
        i = -1
    elif direction == "left":
        i = 1

    print(i)

    existing = articles.find_one({"_id": ObjectId(article_id)})['votes']

    articles.update_one(
        {"_id": ObjectId(article_id)},
        {"$set": {
            "votes": existing + i
        }}, upsert=False)

def add_comment(article_id, name, comment):
    result = comments.find_one({"article_id": ObjectId(article_id)})
    if (result == None):
        comments.insert({
            "article_id": ObjectId(article_id),
            "comments": []
        })
        comments.update_one(
            {"article_id": ObjectId(article_id)},
            {"$set": {
            "comments": [{
                "name": name,
                "date": int(round(time.time()* 1000)),
                "comment": comment
            }]
        }}, upsert=False)
    else:
        result['comments'] += [{
            "name": name,
            "date": int(round(time.time()* 1000)),
            "comment": comment
        }]
        print(result['comments'])
        comments.update_one(
            {"article_id": ObjectId(article_id)},
            {"$set": {
            "comments": result['comments']
        }}, upsert=False)

def get_comments(article_id):
    return comments.find_one({"article_id": ObjectId(article_id)})

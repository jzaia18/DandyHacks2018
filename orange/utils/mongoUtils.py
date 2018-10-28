from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient()
db = client.articles
articles = db.articles
comments = db.comments


def get_n_stories(n):
    return articles.find()[0:n]

def get_by_id(article_id):
    return articles.find_one({"_id": ObjectId(article_id)})

def update_votes(article_id, direction):
    direction = int(direction)
    if abs(direction) > 2: #dont accept clearly fake responses
        return

    existing = articles.find_one({"_id": ObjectId(article_id)})['votes']

    articles.update_one(
        {"_id": ObjectId(article_id)},
        {"$set": {
            "votes": existing + direction
        }}, upsert=False)

def add_comment(article_id, name, comment):
    result = comments.find_one({"article_id": ObjectId(article_id)})
    date = str(datetime.datetime.today())
    date = date[0:date.find('.')]
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
                "date": date,
                "comment": comment
            }]
        }}, upsert=False)
    else:
        result['comments'] += [{
            "name": name,
            "date": date,
            "comment": comment
        }]
        print(result['comments'])
        comments.update_one(
            {"article_id": ObjectId(article_id)},
            {"$set": {
            "comments": result['comments']
        }}, upsert=False)

def get_comments(article_id):
    comment_obj = comments.find_one({"article_id": ObjectId(article_id)})
    if comment_obj:
        return comment_obj['comments']
    return None

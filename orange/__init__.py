from flask import Flask, render_template, request, redirect, url_for
from utils import mongoUtils
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
@app.route("/home")
def root():
    articles_list = mongoUtils.get_n_stories(25)
    return render_template("home.html", articles_list = articles_list)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/article/<article_id>")
def article(article_id):
    print(mongoUtils.get_comments(article_id))
    return render_template("article.html", article_obj = mongoUtils.get_by_id(article_id), comments = mongoUtils.get_comments(article_id))

@app.route("/vote/<article_id>/<direction>")
def vote(article_id, direction):
    mongoUtils.update_votes(article_id, direction)
    return ""

@app.route("/comment/<article_id>", methods = ['POST'])
def comment(article_id):
    if not 'comment' in request.form:
        return redirect("article/"+article_id)

    if 'name' in request.form and request.form['name'] and request.form['name'] != "":
        name = request.form['name']
    else:
        name = "Anynomous"

    comment = request.form['comment']

    mongoUtils.add_comment(article_id, name, comment)

    return redirect("article/"+article_id+"#comments")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")

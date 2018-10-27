from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def root():
    return render_template("home.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")

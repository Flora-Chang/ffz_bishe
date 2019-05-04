import os
import json

from app import app
from flask import render_template
from flask import jsonify

users_info = json.load(open(os.path.join(os.getcwd(), "app/data/users_info.json"), "r"))


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/users_info.json", methods=["GET"])
def json():
    return jsonify(users_info)


@app.route("/rec_papers", methods=["GET"])
def rec_papers():
    return render_template("rec_papers.html")


@app.route("/rec_users", methods=["GET"])
def rec_users():
    return render_template("rec_users.html")


if __name__ == '__main__':
    app.run(debug=True)

import os
import json

from app import app
from flask import render_template
from flask import jsonify

users_info = json.load(open(os.path.join(os.getcwd(), "app/data/recommend.wuli.programs.json"), "r"))


@app.route('/')
@app.route('/neural.html')
def index():
    return render_template("neural.html")


@app.route('/mean')
@app.route('/mean.html')
def mean():
    return render_template("mean.html")


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

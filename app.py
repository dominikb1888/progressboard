from flask import Flask, abort, jsonify, render_template
from leaderboard import Leaderboard
import requests as rq
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# user_repos = json.load(open("user_repos.json"))
leaderboard = Leaderboard(org="DB-Teaching")
user_repos = leaderboard.user_repos


@app.route("/")
def heatmap():
    return render_template(
        "heatmap.html",
        user_repos=user_repos,
    )


@app.route("/api/v1/data")
def api_data():
    request = jsonify(leaderboard.data)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/repos")
def api_repos():
    request = jsonify(leaderboard.repos)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/user_repos")
def api_users():
    request = jsonify(leaderboard.user_repos)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/users/<string:user_name>")
def api_user(user_name):
    users = leaderboard.users
    user = [users[user] for user in users.keys() if user == user_name]
    if len(user) == 0:
        abort(404)
    request = jsonify(user[0])
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


if __name__ == "__main__":
    app.run()

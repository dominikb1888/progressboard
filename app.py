from flask import Flask, request, json, abort, jsonify, render_template
from leaderboard import Leaderboard
from collections import defaultdict
import requests as rq
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# user_repos = json.load(open("user_repos.json"))
leaderboard = Leaderboard(org="DB-Teaching")
user_repos = leaderboard.user_repos
repos = leaderboard.repos
data = leaderboard.data

@app.route("/")
def heatmap():
    return render_template(
        "heatmap.html",
        user_repos=user_repos,
    )

@app.route("/semester/<string:semester>")
def heatmap_semester(semester):
    semester_data = {'22W': ["1990Flori", "AKHILB007"], '22S': ["Aleksar05", "Alexandra18636"]} # Make this importable from a file
    users = semester_data[semester]

    return render_template(
        "heatmap_semester.html",
        user_repos = {user:user_repos[user] for user in users},
        semester = semester
    )




@app.route("/updates")
def updates():
    return render_template(
        "list.html",
        repos=repos,
    )



@app.route("/api/v1/data")
def api_data():
    request = jsonify(data)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/repos")
def api_repos():
    request = jsonify(repos)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/user_repos")
def api_users():
    request = jsonify(user_repos)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/user_repos/<string:semester>")
def api_users_semester(semester):
    semester_data = {'22W': ["1990Flori", "AKHILB007"], '22S': ["Aleksar05", "Alexandra18636"]} # Make this importable from a file

    if semester in semester_data.keys():
        users = semester_data[semester]
    else:
        abort(404)

    request = jsonify({user:user_repos[user] for user in users})
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

@app.route('/github_push', methods=['POST'])
def github_push():
    data = request.json
    header = request.headers.get("X-GitHub-Event")
    match header:
        case'push':
            pass
        case 'commit_comment':
            pass
        case _:
            pass

    print(f'Issue {data}')
    return data

if __name__ == "__main__":
    app.run()

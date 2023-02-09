from flask import Flask, request, json, abort, jsonify, render_template
from leaderboard import Leaderboard
from collections import defaultdict
import requests as rq
import json
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

# user_repos = json.load(open("user_repos.json"))
semester_data = json.load(open("dumps/semester_data.json"))
leaderboard = Leaderboard()
user_repos = leaderboard.user_repos
repos = leaderboard.repos
data = leaderboard.data

def filtered_commits(commits, lte, gte):
    ret = commits
    if lte is not None:
        ret = [commit for commit in commits if lte > datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")]
    if gte is not None:
        ret = [commit for commit in commits if gte < datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")]
    return ret



@app.route("/", methods=["GET", "POST"])
def heatmap():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
    else:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
    
    filtered_items = user_repos
    print(filtered_items)
    if end_date:
        val = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_items = {key: [
            {**item, 'commits': filtered_commits(item['commits'], val, None) } for item in values 
            if len(filtered_commits(item['commits'], val, None)) > 0
            ] for key, values in filtered_items.items() }
        filtered_items = {key: values for key, values in filtered_items.items() if len(values) > 0 }
    
    if start_date:
        val = datetime.strptime(start_date, '%Y-%m-%d')
        filtered_items = {key: [
            {**item, 'commits': filtered_commits(item['commits'], None, val) } for item in values 
            if len(filtered_commits(item['commits'], None, val)) > 0
            ] for key, values in filtered_items.items() }
        filtered_items = {key: values for key, values in filtered_items.items() if len(values) > 0 }
    print(filtered_items)
    
    return render_template(
        "heatmap.html",
        user_repos=filtered_items,
        start_date=start_date if start_date else "",
        end_date=end_date if end_date else "",
    )

@app.route("/semester/<string:semester>")
def heatmap_semester(semester):
    # semester_data = {'22W': ["1990Flori", "AKHILB007"], '22S': ["Aleksar05", "Alexandra18636"]} # Make this importable from a file
    users = semester_data[semester]

    return render_template(
        "heatmap_semester.html",
        user_repos = {user:user_repos[user] for user in users},
        semester = semester
    )




@app.route("/updates")
def updates():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    filtered_items = repos


    if end_date:
        val = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_items = [
            {**item, 'commits': filtered_commits(item['commits'], val, None) } for item in filtered_items 
            if len(filtered_commits(item['commits'], val, None)) > 0
        ] 
    
    if start_date:
        val = datetime.strptime(start_date, '%Y-%m-%d')
        filtered_items = [
            {**item, 'commits': filtered_commits(item['commits'], None, val) } for item in filtered_items 
            if len(filtered_commits(item['commits'], None, val)) > 0
        ]
    

    return render_template(
        "list.html",
        repos=filtered_items,
        start_date=start_date if start_date else "",
        end_date=end_date if end_date else "",
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
    # semester_data = {'22W': ["1990Flori", "AKHILB007"], '22S': ["Aleksar05", "Alexandra18636"]} # Make this importable from a file

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

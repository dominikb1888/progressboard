from flask import Flask, request, json, abort, jsonify, render_template
from leaderboard import Leaderboard
from collections import defaultdict
import requests as rq
import json
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

# user_repos = json.load(open("user_repos.json"))
semester_data = json.load(open("dumps/semester_data.json")) # Move semester_data to an importable file
leaderboard = Leaderboard()
user_repos = leaderboard.user_repos
repos = leaderboard.repos
data = leaderboard.data

def filtered_commits(commits, lte, gte): # Filter the commits list to get all the commits after gte and before lte
    ret = commits
    if lte is not None:
        ret = [commit for commit in commits if lte > datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")] # filter all the commits that are after lte
    if gte is not None:
        ret = [commit for commit in commits if gte < datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")] # filter all the commits that are before gte
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
        filtered_items = {key: [ # every user
            {
                **item, # Use the repo data and update the following fields
                'commits': filtered_commits(item['commits'], val, None) # remove all commits that are not inside the timeframe
            } for item in values # loop over repos
            if len(filtered_commits(item['commits'], val, None)) > 0 # only keep the repo if it has at least one commit in this time frame
            ] 
            for key, values in filtered_items.items() # for every user loop over repos
        } 
        filtered_items = {key: values for key, values in filtered_items.items() if len(values) > 0 } # remove users that don't have any active repos
    
    if start_date:
        val = datetime.strptime(start_date, '%Y-%m-%d')
        filtered_items = {key: [ # every user
            {
                **item, # Use the repo data and update the following fields
                'commits': filtered_commits(item['commits'], None, val) # remove all commits that are not inside the timeframe
            } for item in values 
            if len(filtered_commits(item['commits'], None, val)) > 0 # only keep the repo if it has at least one commit in this time frame
            ] 
            for key, values in filtered_items.items() # for every user loop over repos
        }
        filtered_items = {key: values for key, values in filtered_items.items() if len(values) > 0 } # remove users that don't have any active repos
    print(filtered_items)
    
    return render_template(
        "heatmap.html",
        user_repos=filtered_items,
        start_date=start_date if start_date else "", # return filter data so jinja can auto fill them
        end_date=end_date if end_date else "", # return filter data so jinja can auto fill them
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
            {
                **item, # Use the repo data and update the following fields
                'commits': filtered_commits(item['commits'], val, None)  # remove commits that are outside of the timeframe
            } for item in filtered_items  # loop over all repos
            if len(filtered_commits(item['commits'], val, None)) > 0 # only keep the repos that have active commits 
        ] 
    
    if start_date:
        val = datetime.strptime(start_date, '%Y-%m-%d')
        filtered_items = [
            {
                **item, # Use the repo data and update the following fields
                'commits': filtered_commits(item['commits'], None, val) # remove commits that are outside of the timeframe
            } for item in filtered_items # loop over all repos
            if len(filtered_commits(item['commits'], None, val)) > 0 # only keep the repos that have active commits 
        ]
    

    return render_template(
        "list.html",
        repos=filtered_items,
        start_date=start_date if start_date else "", # return filter data so jinja can auto fill them
        end_date=end_date if end_date else "", # return filter data so jinja can auto fill them
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

from flask import Flask, request, json, abort, jsonify, render_template
from leaderboard import Leaderboard
from collections import defaultdict
from copy import deepcopy
import requests as rq
import json
import sys
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["DEBUG"] = True

semester_data = json.load(open("semester_data.json")) # Move semester_data to an importable file
leaderboard = Leaderboard()

def filtered_commits(commits, lte, gte):
    ret = commits
    if lte is not None:
        ret = [commit for commit in ret if lte + timedelta(days=1) >= datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")] # filter all the commits that are after lte
    if gte is not None:
        ret = [commit for commit in ret if gte <= datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")] # filter all the commits that are before gte
    return ret


def filtered_repos(repos, lte, gte):
    return [
        repo for repo in [
            {**item, 'commits': filtered_commits(item['commits'], lte, gte) } for item in repos
        ] if len(repo['commits']) > 0 # only keep the repos with at least one commit
    ]


@app.route("/api/v1/data")
def api_data():
    request = jsonify(leaderboard.data)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/times")
def api_times():
    request = jsonify(leaderboard.times)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/repos")
def api_repos():
    request = jsonify(leaderboard.repos)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request

@app.route("/api/v1/semester_users")
def api_semester_users():
    sem_data = deepcopy(semester_data)
    for course in sem_data:
        student_dict = {}
        for student in course['students']:
            for student_data in leaderboard.users:
                if student.get('github_username','') == student_data['login']:
                    student_dict[student_data['login']] = student_data
        course['students'] = student_dict

    request = jsonify(sem_data)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request

@app.route("/api/v1/users")
def api_users():
    request = jsonify(leaderboard.users)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request

@app.route("/api/v1/semester_data")
def api_semester_data():
    request = jsonify(semester_data)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request

@app.route("/api/v1/semesters")
def api_semesters():
    semesters = [course['semester'] for course in semester_data]
    request = jsonify(semesters)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request

@app.route("/api/v1/courses")
def api_courses():
    semesters = [course['course'] for course in semester_data]
    request = jsonify(semesters)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request

@app.route("/api/v1/user_repos",  methods=["GET"])
def api_repos_all():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    filtered_items = leaderboard.user_repos
    lte, gte = None, None

    if end_date:
        lte = datetime.strptime(end_date, '%Y-%m-%d')
    if start_date:
        gte = datetime.strptime(start_date, '%Y-%m-%d')

    filtered_items = {key: filtered_repos(values, lte, gte) for key, values in filtered_items.items() }
    filtered_items = {key: values for key, values in filtered_items.items() if len(values) > 0 }

    response = jsonify(filtered_items)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/v1/user_repos/<string:user_name>")
def api_repos_user(user_name):
    logins = [user['login'] for user in leaderboard.users]
    if user_name in logins:
        request = jsonify(leaderboard.user_repos[user_name])
    else:
        abort(404)

    request.headers.add("Access-Control-Allow-Origin", "*")
    return request



@app.route('/gh_webhook', methods=['POST'])
def gh_webhook():
    data = request.json
    event = request.headers.get("X-GitHub-Event")
    match event:
        case 'push':
            leaderboard.gh.get_repo_resource('DB-Teaching', data['repository']['name'], 'repo')
            print(f"New Commit on {data['repository']['name']}", file=sys.stderr)
        case 'commit_comment':
            print(f"New Comment on {data['repository']['name']}", file=sys.stderr)
        case _:
            print(f"New event: {event}", file=sys.stderr)

    return 'OK'


if __name__ == "__main__":
    app.run()

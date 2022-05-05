from flask import Flask, abort, jsonify, render_template
import flask_profiler
from leaderboard import Leaderboard
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# You need to declare necessary configuration to initialize
# flask-profiler as follows:
app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {"engine": "sqlite"},
    "basicAuth": {"enabled": True, "username": "admin", "password": "admin"},
    "ignore": ["^/static/.*"],
}


leaderboard = Leaderboard(org="DB-Teaching")


@app.route("/")
def heatmap():
    return render_template(
        "heatmap.html",
        plot_dict=json.loads(leaderboard.heatmap),
        users=leaderboard.users,
    )


@app.route("/api/v1/data")
def api_data():
    request = jsonify(leaderboard.dataframe.to_dict(orient="records"))
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/repos")
def api_repos():
    request = jsonify(leaderboard.repos)
    request.headers.add("Access-Control-Allow-Origin", "*")
    return request


@app.route("/api/v1/users")
def api_users():
    request = jsonify(leaderboard.users)
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


flask_profiler.init_app(app)

if __name__ == "__main__":
    app.run()

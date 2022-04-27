from flask import Flask, abort, jsonify, render_template
from leaderboard import Leaderboard
import json

app = Flask(__name__)
leaderboard = Leaderboard(org="DB-Teaching")


@app.route("/")
def index():
    return render_template(
        "index.html",
        plot_json=leaderboard.heatmap,
        plot_dict=json.loads(leaderboard.heatmap),
        users=leaderboard.users,
    )


@app.route("/api/v1/data")
def api_data():
    return jsonify(leaderboard.dataframe.to_dict(orient="records"))


@app.route("/api/v1/repos")
def api_repos():
    return jsonify(leaderboard.repos)


@app.route("/api/v1/users")
def api_users():
    return jsonify(leaderboard.users)


@app.route("/api/v1/users/<string:user_name>")
def api_user(user_name):
    users = leaderboard.users
    user = [users[user] for user in users.keys() if user == user_name]
    if len(user) == 0:
        abort(404)
    return jsonify(user[0])


if __name__ == "__main__":
    app.run()

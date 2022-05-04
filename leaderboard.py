from collections import defaultdict
from dotenv import load_dotenv  # for python-dotenv method
from githubapi import GithubAPI

import json
import os
import pandas as pd
import re

import plotly as plt
import plotly.express as px

load_dotenv()  # for python-dotenv method


class Leaderboard:
    def __init__(
        self,
        user="dominikb1888",
        key=os.environ.get("GHTOKEN"),
        endpoint="https://api.github.com",
        org="DB-Teaching",
    ):
        self.gh = GithubAPI(user, key, endpoint)
        self.org = org
        self.repos = self.gh.get_org_resource(self.org, "repos")
        self.dataframe = self.get_table()
        self.users = self.get_users()
        self.leaderboard = self._gen_heatmap_abs()
        self.relative = self._gen_heatmap_rel()
        self.heatmap = self._gen_plot()

    def get_users(self):
        users = [
            user["login"]
            for user in self.gh.get_org_resource(self.org, "outside_collaborators")
        ]

        user_data = defaultdict(list)
        for repo in self.dataframe.to_dict(orient="records"):
            # if repo["user"]:
            for user in users:
                if user == repo["user"]:
                    user_data[user].append(repo)

        return user_data

    def get_table(self):
        df = []
        for repo in self.repos:
            if repo["name"] in ["python", "github"]:
                continue

            session, exercise = self._split_repo_name(repo["name"])
            runs = self.gh.get_repo_resource(self.org, repo["name"], "actions/runs")
            commits = self.gh.get_repo_resource(self.org, repo["name"], "commits")
            username = ""
            for user in self.gh.get_org_resource(self.org, "outside_collaborators"):
                if user["login"] in repo["name"]:
                    username = user["login"]

            df.append(
                {
                    "session": session,
                    "exercise": exercise,
                    "name": repo["name"],
                    "user": username if username else "dominikb1888",
                    "url": repo["html_url"],
                    "commits": len(commits),
                    "runs": len(runs),
                    "completed": sum([1 for w in runs if w["conclusion"] == "success"]),
                    "failed": sum([1 for w in runs if w["conclusion"] != "failure"]),
                }
            )

        df = pd.DataFrame(df)
        df.to_csv("leaderboard.csv")
        return df

    @staticmethod
    def _split_repo_name(name):
        splitlist = re.split("-|_", name, maxsplit=2)
        session, exercise, *_ = splitlist if len(splitlist) > 1 else (splitlist, 0, 0)
        return session, exercise

    def _gen_heatmap_abs(self):
        """create a version of the leaderboard with absolute values"""
        df = self.dataframe
        lb = (
            df[["user", "session", "exercise"]]
            .fillna(0)
            .pivot_table(
                columns="session",
                values="exercise",
                index="user",
                aggfunc="count",
                fill_value=0,
                margins=True,
                margins_name="Total",
            )
            .astype(int)
            .sort_values(by="Total", ascending=False)
        )

        return lb

    def _gen_heatmap_rel(self):
        """Creates a version of the leaderboard with relative data"""
        df = self.dataframe
        lb = self.leaderboard

        ex_count = (
            df[["session", "exercise"]]
            .groupby("session")
            .agg("nunique")
            .to_dict()["exercise"]
        )

        lb = lb[(lb["Total"] > 1) & (lb["Total"] < 150)]
        lb = lb[~lb.index.isin(["numbers", "list", "cipher", "search"])]

        rel = lb.copy(deep=True)
        for session in ex_count.keys():
            rel[session] = rel[session].map(
                lambda i: int(100 * (i / ex_count[session]))
            )

        return rel

    def _gen_plot(self):
        rel = self.relative
        lb = self.leaderboard

        fig = px.imshow(
            rel.iloc[1:, 0:14],
            color_continuous_scale=px.colors.sequential.Cividis_r,
            text_auto=True,
        )
        # sns.heatmap(rel.iloc[1:, 0:14], annot=lb.iloc[1:, 0:14], cmap="YlGnBu")

        fig.update_layout(width=1500, height=500)
        return json.dumps(fig, cls=plt.utils.PlotlyJSONEncoder)

    # def to_html(self):
    #     heatmap = self.heatmap()
    #     return heatmap.to_html()

    # def to_png(self):
    #     heatmap = self.heatmap()
    #     plt.savefig("leaderboard.png", dpi=400)

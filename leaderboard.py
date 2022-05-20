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
            user.get("login")
            for user in self.gh.get_org_resource(self.org, "outside_collaborators")
        ]

        user_data = defaultdict(list)
        for repo in self.dataframe.to_dict(orient="records"):
            # if repo["user"]:
            for user in users:
                if user == repo.get("user"):
                    user_data[user].append(repo)

        return user_data

    def get_table(self):
        df = []
        for repo in self.repos:
            if repo.get("name") in ["python", "github"]:
                continue

            session, exercise = self._split_repo_name(repo.get("name"))
            commits = self.gh.get_repo_resource(self.org, repo.get("name"), "commits")
            user_name, user_avatar, user_link = (None, None, None)
            for user in self.gh.get_org_resource(self.org, "outside_collaborators"):
                if user.get("login") in repo.get("name"):
                    user_name = user.get("login")
                    user_link = user.get("html_url")
                    user_avatar = user.get("avatar_url")

            df.append(
                {
                    "session": session,
                    "exercise": exercise,
                    "name": repo.get("name"),
                    "user": user_name if user_name else "dominikb1888",
                    "avatar": user_avatar,
                    "user_url": user_link,
                    "url": repo.get("html_url"),
                    "commits": len(commits),
                    "status": self.get_status(commits, repo),
                }
            )

        df = pd.DataFrame(df)
        df = df.sort_values(by=["name"])
        df.to_csv("leaderboard.csv")
        return df

    def get_status(self, commits, repo):
        """Returns the status of a repo based on workflow runs"""
        conclusions = []
        for commit in commits:
            if commit.get("commit", {}).get("author", {}).get("name") not in [
                "github-classroom[bot]",
                "github-classroom",
            ]:
                check_suite = self.gh.get_repo_commit_status(
                    self.org, repo.get("name"), commit.get("sha"), "check-suites"
                )
                if check_suite.get("total_count") > 0:
                    conclusions.append(
                        check_suite.get("check_suites", {})[0].get("conclusion")
                    )

        if len(conclusions) == 0:
            return "not-started"

        workflows = self.gh.get_repo_resource(
            self.org, repo.get("name"), "actions/runs"
        )

        if workflows:
            conclusions = [
                (run.get("run_started_at"), run.get("conclusion"), repo.get("name"))
                for run in workflows
            ]

            conclusions = [c for _, c, _ in conclusions]

            if all(c == "failure" for c in conclusions):
                return "failing"

            if conclusions[0] == "failure" and any(c == "success" for c in conclusions):
                return "rework"

            if any(c == "success" for c in conclusions):
                return "completed"

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
            .sort_values(by="user", ascending=True)
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

        fig = px.imshow(
            rel.iloc[0:, 0:14],
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

from github import Github
from collections import defaultdict, OrderedDict
import json
import pandas as pd
import plotly
import plotly.express as px
from dotenv import load_dotenv  # for python-dotenv method
import re

load_dotenv()  # for python-dotenv method

import os


class OrderedDefaultDict(OrderedDict):
    def __missing__(self, key):
        value = list()
        self[key] = value
        return value


class Leaderboard:
    def __init__(self, org="DB-Teaching", key=os.environ.get("GHTOKEN")):
        self.gh = Github(key)
        self.org = org
        self.repos = self._get_repos()
        self.dataframe = self._get_table()
        self.users = self._get_users()
        self.leaderboard = self._gen_heatmap_abs()
        self.relative = self._gen_heatmap_rel()
        self.heatmap = self._gen_plot()

    # def __repr__():
    #     return self.dataframe.to_markdown
    #     """ Creates Markdown Output for CLI or Github """
    #     # .apply(lambda row: "".join(["\u258F" * int(i) for i in row if i != '']), axis=1)
    #     # .to_markdown()
    def _get_repos(self):
        if not os.path.exists("repos.json"):
            repos = self.gh.get_organization(self.org).get_repos()
            with open("repos.json", "a", encoding="UTF-8") as f:
                json.dump(
                    [
                        repo.raw_data
                        for repo in repos
                        if repo.name not in ["python", "github"]
                    ],
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
        with open("repos.json", "r") as f:
            return json.loads(f.read())

    def _get_users(self):
        users = list(
            set(
                [
                    user.login
                    for user in self.gh.get_organization(
                        "DB-Teaching"
                    ).get_outside_collaborators()
                ]
            )
        )

        user_data = defaultdict(list)
        for repo in self.dataframe.to_dict(orient="records"):
            if repo["user"]:
                for user in users:
                    if user == repo["user"]:
                        user_data[user].append(repo)

        return user_data

    def _get_table(self):
        df = []
        if not os.path.exists("leaderboard.csv"):
            repos = self.repos
            for repo in repos:
                session, exercise = self._split_repo_name(repo["name"])
                repo_obj = self.gh.get_repo(repo["full_name"])
                runs = repo_obj.get_workflow_runs()
                commits = repo_obj.get_commits()
                df.append(
                    {
                        "session": session,
                        "exercise": exercise,
                        "name": repo["name"],
                        "user": repo["name"].split("-")[-1],
                        "url": repo["url"],
                        "commits": sum([1 for _ in commits]),
                        "runs": runs.totalCount,
                        "completed": sum(
                            [1 for w in runs if w.conclusion == "success"]
                        ),
                        "failed": sum([1 for w in runs if w.conclusion != "failure"]),
                        "updated_at": repo["updated_at"],
                    }
                )
            df = pd.DataFrame(df)
            df.to_csv("leaderboard.csv")
            return df

        df = pd.read_csv("leaderboard.csv")
        return df

    # TODO: Local Update from Github
    # def _check_update(self):
    #     for local_repo in pd.read_csv("leaderboard.csv"):
    #         if local_repo["updated"]:
    #             updated_local = local_repo["updated"]
    #         if repo["updated_at"] > updated_local:
    #             return False
    #     return True

    @staticmethod
    def _split_repo_name(name):
        splitlist = re.split("-|_", name, maxsplit=2)
        session, exercise, *rest = (
            splitlist if len(splitlist) > 1 else (splitlist, 0, 0)
        )
        return session, exercise

    def _gen_heatmap_abs(self, update=False):
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

    def _gen_heatmap_rel(self, update=False):
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
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # def to_html(self):
    #     heatmap = self.heatmap()
    #     return heatmap.to_html()

    # def to_png(self):
    #     heatmap = self.heatmap()
    #     plt.savefig("leaderboard.png", dpi=400)

from github import Github
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import os 



class Leaderboard():
    def __init__(org=DB-Teaching, key="", self):
        self.gh = Github(os.environ.get('GHTOKEN'))
        self.repos = self.gh.get_organization(self.org).get_repos()
        self.users = list(set([user.login for user in gh.get_organization("DB-Teaching").get_outside_collaborators()]))
        self.dataframe = self._get_table()
        self.to_csv = self._get_table.to_csv("leaderboard.csv")
        self.leaderboard = self.gen_heatmap_data()
        self.leaderboard_png = self._heatmap_to_png()

    # def __repr__():
    #     return self.dataframe.to_markdown
    #     """ Creates Markdown Output for CLI or Github """
    #     # .apply(lambda row: "".join(["\u258F" * int(i) for i in row if i != '']), axis=1)
    #     # .to_markdown()

    def _get_table(self):
        for repo in self.repos:
            runs = repo.get_workflow_runs()
            session, exercise = self._split_repo_name()
            self.columns = {
                "session": session,
                "exercise": exercise,
                "name": repo.name,
                "user": repo.name.split("-")[-1],
                "url": repo.url,
                "commits": sum([1 for commit in repo.get_commits()]),
                "runs": runs.totalCount,
                "completed": sum([1 for w in runs if w.conclusion == "success"]),
                "failed": sum([1 for w in runs if w.conclusion != "failure"]),
                "updated_at": repo["updated_at"],
            }

    # TODO: Local Update from Github
    # def _check_update(self):
    #     for local_repo in pd.read_csv("leaderboard.csv"):
    #         if local_repo["updated"]:
    #             updated_local = local_repo["updated"]
    #         if repo["updated_at"] > updated_local:
    #             return False
    #     return True

    def _split_repo_name(self):
        for repos in self.repos:
            splitlist = re.split("-|_", repo.name, maxsplit=2)
        session, exercise, *rest = (
            splitlist if len(splitlist) > 1 else (splitlist, 0, 0)
        )
        return session, exercise

    def _gen_heatmap_abs(self, update=False):
        """ create a version of the leaderboard with absolute values """
        df = self.dataframe
        df = df[df["session"] != "python"]
        df = df[df["session"] != "github"]
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



    def _gen_heatmap_rel(self.update=False):
        """ Creates a version of the leaderboard with relative data """
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
            rel[session] = rel[session].map(lambda i: int(100 * (i / ex_count[session])))

        return rel

    def _heatmap_to_png():
        rel, lb = print_table(update=True)
        sns.set(rc={"figure.figsize": (10, 8)})
        sns.heatmap(rel.iloc[1:, 0:14], annot=lb.iloc[1:, 0:14], cmap="YlGnBu")
        plt.savefig("leaderboard.png", dpi=400)

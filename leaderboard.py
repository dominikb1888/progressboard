from github import Github
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re


class Leaderboard():
    def __init__(org=DB-Teaching, key="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", self):
        self.gh = Github(key)
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
        self.repos = self.gh.get_organization(self.org).get_repos()
        self.users = list(set([user.login for user in gh.get_organization("DB-Teaching").get_outside_collaborators()] + ["yllkaninaj"]))
        self.dataframe = self._get_table()
        self.to_csv = self._get_table.to_csv("leaderboard.csv")


def _check_update(self):
    for local_repo in pd.read_csv("leaderboard.csv"):
        if local_repo["updated"]:
            updated_local = local_repo["updated"]
        if repo["updated_at"] > updated_local:
            return False
    return True


def _split_repo_name(self):
    for repos in self.repo:
       splitlist = re.split("-|_", repo.name, maxsplit=2)
       session, exercise, *rest = (
            splitlist if len(splitlist) > 1 else (splitlist, 0, 0)
        )
    return session, exercise


def prepare_table(update=False):

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
    # .apply(lambda row: "".join(["\u258F" * int(i) for i in row if i != '']), axis=1)
    # .to_markdown()
    return lb, df


def print_table(update=False):
    lb, df = prepare_table(get_table())

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

    return rel, lb


if __name__ == "__main__":
    rel, lb = print_table(update=True)
    sns.set(rc={"figure.figsize": (10, 8)})
    sns.heatmap(rel.iloc[1:, 0:14], annot=lb.iloc[1:, 0:14], cmap="YlGnBu")
    plt.savefig("leaderboard.png", dpi=400)

    print(lb.to_markdown())

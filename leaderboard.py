from github import Github
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re

gh = Github("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")


def check_local(repo):
    for local_repo in pd.read_csv("leaderboard.csv"):
        if local_repo["updated"]:
            updated_local = local_repo["updated"]
        if repo["updated_at"] > updated_local:
            return False
    return True


def get_table():
    table = []
    for repo in gh.get_organization("DB-Teaching").get_repos():
        if check_local(repo):
            continue

        splitlist = re.split("-|_", repo.name, maxsplit=2)
        session, exercise, *rest = (
            splitlist if len(splitlist) > 1 else (splitlist, 0, 0)
        )
        runs = repo.get_workflow_runs()
        table.append(
            {
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
        )
        print(repo.name)
    df = pd.DataFrame(table)
    df.to_csv("leaderboard.csv")

    return df


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

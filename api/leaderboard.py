from collections import defaultdict
import os
import re
from dotenv import load_dotenv
from githubapi import GithubAPI

load_dotenv()  # for python-dotenv method

class Leaderboard:
    def __init__(
        self,
        user=os.environ.get("GHUSER", "dominikb1888"), # use environment to change the user
        key=os.environ.get("GHTOKEN"),
        endpoint="https://api.github.com",
        org=os.environ.get("GHORG", "DB-Student-Repos"), # use environment to change the organization
    ):
        self.gh = GithubAPI(user, key, endpoint)
        self.org = org
        self.repos = self.gh.get_org_resource(self.org, "repos")
        self.users = [
            user for user in self.gh.get_org_resource(self.org, "outside_collaborators")
        ]
        self.data = self._get_table()

    @property
    def user_repos(self):
        user_data = defaultdict(list)
        for repo in self.data:
            # if repo["user"]:
            for user in self.users:
                if user.get("login") == repo.get("user"):
                    user_data[user.get("login")].append(repo)

        return user_data

    @property
    def times(self):
        return [
            commit['commit']['author']['date']
            for repo in self.data for commit in repo['commits']
        ]


    def _get_table(self):
        df = []
        for repo in self.repos:
            if repo.get("name") in ["python", "github"]:
                continue

            session, exercise = self._split_repo_name(repo.get("name"))
            commits = self.gh.get_repo_resource(self.org, repo.get("name"), "commits")
            user_name, user_avatar, user_link = (None, None, None)
            commit_url, comment_count = self.get_latest_commit(commits)

            repo['commits'] = commits # Add commits array to repo data

            for user in self.users:
                if user.get("login") in repo.get("name"):
                    user_name = user["login"]
                    user_link = user.get("html_url")
                    user_avatar = user.get("avatar_url")

            df.append(
                {
                    "avatar": user_avatar,
                    "exercise": exercise,
                    "latest_commit_comment_count": comment_count,
                    "latest_commit_url": commit_url if commit_url else repo['html_url'],
                    "name": repo.get("name"),
                    "session": session,
                    "status": self.get_status(commits, repo),
                    "url": repo.get("html_url"),
                    "user": user_name if user_name else "dominikb1888",
                    "user_url": user_link,
                    'commits': commits, # Add commits array to table
                }
            )

        return df

    def filter_bot_commits(self, commits):
        return [commit for commit in commits if commit.get("commit", {}).get("author", {}).get("name") not in [
                "github-classroom[bot]",
                "github-classroom",
            ]]

    def get_latest_commit(self, commits):
        ordered_commits = sorted(self.filter_bot_commits(commits), key=lambda d: d['commit']['author']['date'])
        if len(ordered_commits) > 0:
            url = ordered_commits[-1]['html_url']
            comment_count = ordered_commits[-1].get("comment_count", False)
            return url, comment_count
        else:
            return False, False


    def get_status(self, commits, repo):
        """Returns the status of a repo based on workflow runs"""
        conclusions = []
        shas = [commit['sha'] for commit in commits]
        check_suites = self.gh.get_multiple_commit_statuses(
                    self.org, repo.get("name"), shas, "check-suites"
                )
        for check_suite in check_suites:
            if isinstance(check_suite, dict) and check_suite.get("total_count", 0) > 0:
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

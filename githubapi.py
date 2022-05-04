from requests.auth import HTTPBasicAuth
from requests_cache import CachedSession
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import os

load_dotenv()


class GithubAPI:
    def __init__(
        self,
        user="dominikb1888",
        key=os.environ.get("GHTOKEN"),
        endpoint="https://api.github.com",
    ):
        self.user = user
        self.auth = HTTPBasicAuth(self.user, key)
        self.session = CachedSession("leaderboard")
        self.session.auth = self.auth
        self.endpoint = endpoint

    def _get(self, type="", resource=""):
        url = f"{self.endpoint}/{type}/{resource}"
        response = self.session.get(url)
        pages = [response.json()]
        if response.links.get("last"):
            last_url = response.links.get("last")["url"]
            query_dict = parse_qs(urlparse(last_url).query)
            params = {k: v[0] for k, v in query_dict.items()}
            for i in range(2, int(params["page"]) + 1):
                pages.append(self.session.get(f"{url}?page={i}").json())

        return self._flatten_results(pages, resource)

    @staticmethod
    def _flatten_results(pages, resource):
        if resource == "actions/runs":
            return [item for page in pages for item in page["workflow_runs"]]

        return [item for page in pages for item in page] if len(pages) > 1 else pages[0]

    def get_org_resource(self, org, resource):
        return self._get(f"orgs/{org}", resource)

        # actions/runs, commits

    def get_repo_resource(self, org, repo, resource):
        return self._get(f"repos/{org}/{repo}", resource)

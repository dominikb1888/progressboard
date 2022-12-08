from requests.auth import HTTPBasicAuth
from requests_cache import CachedSession, RedisCache
from requests_cache import DO_NOT_CACHE
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from datetime import timedelta
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
        base_url = endpoint + '/orgs/DB-Teaching'
        urls_expire_after = {
            base_url + '/repos': DO_NOT_CACHE,
            base_url + '/outside_collaborators': DO_NOT_CACHE,
            '*': 60,
        }
        backend = RedisCache(host='127.0.0.1', port=6379)
        self.session = CachedSession(
            "leaderboard",
            backend = backend,
            cache_control=False,  # Use Cache-Control response headers for expiration, if available
            allowable_codes=[200, 400],  # Cache 400 responses as a solemn reminder of your failures
            allowable_methods=["GET", "POST"],  # Cache whatever HTTP methods you want
            ignored_parameters=["api_key"],  # Don't match this request param, and redact if from the cache
            match_headers=True,
            stale_if_error=True,  # In case of request errors, use stale cache data if possi
            stale_while_revalidate=True,
            #urls_expire_after=urls_expire_after,
        )

        self.session.auth = self.auth
        self.endpoint = endpoint

    def _get(self, type="", resource="", query=""):
        url = f"{self.endpoint}/{type}/{resource}"
        response = self.session.get(url)
        print(response.url, response.from_cache)
        pages = [response.json()]
        if response.links.get("last"):
            last_url = response.links.get("last", {}).get("url")
            query_dict = parse_qs(urlparse(last_url).query)
            params = {k: v[0] for k, v in query_dict.items()}
            for i in range(2, int(params.get("page")) + 1):
                response = self.session.get(f"{url}?page={i}")
                print(response.url, response.from_cache)
                pages.append(response.json())

        return self._flatten_results(pages, resource)

    @staticmethod
    def _flatten_results(pages, resource):
        if resource == "actions/runs":
            return [item for page in pages for item in page.get("workflow_runs")]

        return [item for page in pages for item in page] if len(pages) > 1 else pages[0]

    def get_org_resource(self, org, resource):
        return self._get(f"orgs/{org}", resource)

        # actions/runs, commits

    def get_repo_resource(self, org, repo, resource):
        return self._get(f"repos/{org}/{repo}", resource)

    def get_repo_commit_status(self, org, repo, ref, resource):
        return self._get(f"repos/{org}/{repo}/commits/{ref}", resource)

    def get_repo_commit_file(self, org, repo, file, ref):
        return self._get(f"repos/{org}/{repo}/contents/{file}", query=ref)

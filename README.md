# ProgressBoard

## Building this App with Github Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=552555575)

Click on the green Code top right and create a new devcontainer and wait for the system to load and boot up, VS code editor will pop up. Use the terminal in the bottom for all further steps

1. Activate the environment (based on the shell.nix file):

        lorri shell

2. Start redis (redis is used as a caching backend for requests_cache)

        redis-server --daemonize yes

3. Run flask (flask is the web framework providing the API and the rendered HTML)

        flask run

Flask will then probe the redis cache and spin up the app once done. You can click on the link (<http://localhost:5000>) that shows up in the terminal window. A new browser window should open showing the output of the app.

## The App

### JSON Rest API

The app provides raw json data via the routes under /api/v1

- /api/v1/data
- /api/v1/user_repos
- /api/v1/users

### The HTML views

- / (Heatmap View grouped by user and session)
- /updates (Timeline Grid View sorted chronologically)

## Roadmap

See the projects and issues tab for some more ideas on how to develop the app

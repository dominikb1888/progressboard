# Building this App with Github Codespaces

Click on the green Code top right and create a new devcontainer and wait for the system to load and boot up, VS code editor will pop up. Use the terminal in the bottom for all further steps

1. Activate the environment:

        lorri shell

2. Start redis by typing

        redis-server --daemonize yes

3. Run flask

        flask run

Flask will then probe the redis cache and spin up the app once done. You can click on the link (<http://localhost:5000>) that shows up in the terminal window. A new browser window should open showing the output of the app.

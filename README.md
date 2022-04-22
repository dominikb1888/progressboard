# Building a Restful Web Application

## Create a new branch in the repo

After moving all old files to our '_archive' directory, we create new branch in our existing repo called 'app' and commit the blank status.

```bash
git commit -am 'initial, moved old files to separate dir'
git checkout app
git branch app
```

## Create a Python virtualenv and activate it

```bash
python3 -m venv app

. app/bin/activate.fish
source app/bin/activate
```

## Install dependencies and list them in requirements.txt

```bash
pip install pandas flask seaborn virtualenv

pip freeze > requirements.txt
```

## Create Flask app

Create a new app.y file and launch it:

```bash
vim app.py
```

Add the boilerplate code showing Hello World:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()
```


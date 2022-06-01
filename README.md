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
pip install pandas flask seaborn virtualenv pygithub python-dotenv

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

Commit the first version without much functionality

```bash
git commit -am 'initial webapp with flask boilerplate'
```


## Add the leaderboard class

```bash
git commit -am 'added first version of Leaderboard class'
git add leaderboard.py

cp _archive/leaderboard.py  .
```


## The early ProgressBoard class

```python
import json
from collections import Counter
import requests as rq

# Automatic Updates?!

class ProgressBoard():
  def __init__(self, res):
    self.data = rq.get(f"https://api.github.com/{res}/repos").json()
    self.names = [item['name'].split('-')[-1] for item in self.data]

  def __repr__(self):
    w = self._len_name() + 5
    return f"{'NAME':{w}}{'COUNT':5}\n" + "\n".join([f"{n:{w}}{i:5}" for n, i in self.count()])
  
  def load_data(self, file):
    with open(file) as json_file:
      data = json.load(json_file)
    return data

  def _len_name(self):
    return max([len(name) for name in self.names])

  def count(self, limit = 32):
    return Counter(self.names).most_common(limit)

ProgressBoard('orgs/DB-Teaching')
```

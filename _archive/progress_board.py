import json
from collections import Counter
import urllib.request as ur 

# Automatic Updates?!

class ProgressBoard():
  def __init__(self, res):
    self.data = json.loads(ur.urlopen(f"https://api.github.com/{res}/repos").read())
    self.names = [item['name'].split('-')[-1] for item in self.data]

  def __repr__(self):
    w = self._len_name() + 5
    return f"{'NAME':{w}}{'COUNT':5}\n" + "\n".join([f"{n:{w}}{i:5}" for n, i in self.count()])

  def _len_name(self):
    return max([len(name) for name in self.names])

  def count(self, limit = 32):
    return Counter(self.names).most_common(limit)

ProgressBoard("orgs/DB-Teaching")

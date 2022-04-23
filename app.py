from flask import Flask, render_template
from leaderboard import Leaderboard
import seaborn as sns
import matplotlib as plt
import plotly
import plotly.express as px
from io import BytesIO
import json

app = Flask(__name__)


@app.route("/")
def index():
    leaderboard = Leaderboard(org="DB-Teaching")
    lb = leaderboard.leaderboard
    rel = leaderboard.heatmap
    fig = px.imshow(rel.iloc[1:, 0:14])
    # sns.heatmap(rel.iloc[1:, 0:14], annot=lb.iloc[1:, 0:14], cmap="YlGnBu")

    fig.update_layout(width=1500, height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("index.html", plot_json=plot_json)


if __name__ == "__main__":
    app.run()

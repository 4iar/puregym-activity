from flask import Flask
from flask import render_template
from flask import Response
from database import Database

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gyms/<gym>/data")
def gym_data(gym):
    database = Database()
    data = database.get_hour_summary_data_as_tsv(gym)
    database.close()

    return Response(data, mimetype="text/tsv")


@app.route("/gyms/<gym>")
def gym_page(gym):
    return render_template("gym.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

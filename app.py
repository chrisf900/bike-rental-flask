from flask import render_template

from init import create_app
from mobility.bike.api import api

app = create_app()
api.init_app(app)


@app.route("/map")
def main():
    return render_template("mobility/bike/map.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

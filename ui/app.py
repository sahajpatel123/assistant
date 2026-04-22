from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hologram.html")

@app.route("/globe")
def globe():
    return render_template("globe.html")

@app.route("/api/news")
def get_news():
    # Keep the news API from before
    MOCK_NEWS = [
        {"lat": 38.9072, "lng": -77.0369, "headline": "New Tech Policy Passed in Washington", "region": "North America"},
        {"lat": 51.5074, "lng": -0.1278, "headline": "London Markets See Record Highs", "region": "Europe"}
    ]
    return jsonify(MOCK_NEWS)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
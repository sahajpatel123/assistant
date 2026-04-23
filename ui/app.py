from flask import Flask, render_template, jsonify, request
import random
import psutil
import sys
import os

# Add parent dir to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_engine import get_intent
from main import process_command # Might be tricky if it uses speak, but we can call it

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hologram.html")

@app.route("/globe")
def globe():
    return render_template("globe.html")

@app.route("/remote")
def remote():
    return render_template("remote.html")

@app.route("/api/news")
def get_news():
    MOCK_NEWS = [
        {"lat": 38.9072, "lng": -77.0369, "headline": "New Tech Policy Passed in Washington", "region": "North America"},
        {"lat": 51.5074, "lng": -0.1278, "headline": "London Markets See Record Highs", "region": "Europe"}
    ]
    return jsonify(MOCK_NEWS)

@app.route("/api/telemetry")
def telemetry():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return jsonify({"cpu": cpu, "ram": ram})

@app.route("/api/command", methods=["POST"])
def command():
    data = request.json
    cmd = data.get("command", "")
    if cmd:
        # Avoid blocking the web thread, ideally use a message queue
        # For this prototype, we'll just run the intent engine and call process_command
        try:
            import threading
            threading.Thread(target=process_command, args=(cmd,)).start()
            return jsonify({"status": "success", "message": "Command dispatched"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "No command provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
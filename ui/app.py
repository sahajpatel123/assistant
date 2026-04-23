import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from intel_manager import get_real_news
from flask import Flask, render_template, jsonify, request
import psutil
import sys
import os

# Add parent dir to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Tactical Response Buffer: Stores the last command and Christin's response
latest_status = {
    "command": "Awaiting voice command...",
    "response": "System Monitoring Active."
}


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
    topic = request.args.get("q")
    return jsonify(get_real_news(topic))


@app.route("/api/telemetry")
def telemetry():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    # Return telemetry + the latest status for UI updates
    return jsonify({
        "cpu": cpu,
        "ram": ram,
        "status": latest_status
    })


@app.route("/api/update_status", methods=["POST"])
def update_status():
    """Endpoint for the Brain (main.py) to push updates to the UI."""
    global latest_status
    data = request.json
    latest_status = {
        "command": data.get("command", ""),
        "response": data.get("response", "")
    }
    return jsonify({"status": "success"})


@app.route("/api/command", methods=["POST"])
def command():
    data = request.json
    cmd = data.get("command", "")
    if cmd:
        try:
            # Note: Importing process_command here might cause circular imports,
            # so we use a local import if needed or handle via the Brain
            # module.
            from main import process_command
            import threading
            threading.Thread(target=process_command, args=(cmd,)).start()
            return jsonify(
                {"status": "success", "message": "Command dispatched"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "No command provided"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)

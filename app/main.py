from flask import Flask, request, jsonify
import os, time, random

app = Flask(__name__)

# Current state
MODE = os.getenv("MODE", "stable")
VERSION = os.getenv("APP_VERSION", "1.0.0")
START_TIME = time.time()

chaos_config = {"mode": "normal", "rate": 0, "duration": 0}

@app.after_request
def add_headers(response):
    if MODE == "canary":
        response.headers["X-Mode"] = "canary"
    return response

@app.route('/')
def welcome():
    # Simulate slow chaos
    if chaos_config["mode"] == "slow":
        time.sleep(chaos_config["duration"])
    
    # Simulate error chaos
    if chaos_config["mode"] == "error" and random.random() < chaos_config["rate"]:
        return jsonify({"error": "chaos crash"}), 500

    return jsonify({
        "message": "Welcome to SwiftDeploy",
        "mode": MODE,
        "version": VERSION,
        "timestamp": time.time()
    })

@app.route('/healthz')
def healthz():
    uptime = time.time() - START_TIME
    return jsonify({"status": "healthy", "uptime": int(uptime)})

@app.route('/chaos', methods=['POST'])
def trigger_chaos():
    if MODE != "canary":
        return jsonify({"error": "Chaos only allowed in canary mode"}), 403
    
    data = request.json
    global chaos_config
    if data["mode"] == "recover":
        chaos_config = {"mode": "normal", "rate": 0, "duration": 0}
    else:
        chaos_config = data
    return jsonify({"status": "chaos updated", "config": chaos_config})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("APP_PORT", 3000)))

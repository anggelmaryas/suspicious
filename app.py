from flask import Flask, request, jsonify, render_template
import datetime
import os

app = Flask(__name__)

def load_blacklist():
    with open("blacklist.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

@app.route('/log', methods=['GET'])
def log_ip():
    ip_address = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blacklist = load_blacklist()
    is_suspicious = ip_address in blacklist

    with open("logs.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] IP: {ip_address} - {'SUSPICIOUS' if is_suspicious else 'OK'}\n")

    return jsonify({
        "ip": ip_address,
        "time": timestamp,
        "status": "SUSPICIOUS" if is_suspicious else "OK"
    })

@app.route('/dashboard')
def dashboard():
    logs = []
    if os.path.exists("logs.txt"):
        with open("logs.txt", "r") as f:
            for line in f:
                try:
                    time_part = line.split("]")[0].strip("[")
                    ip_part = line.split("IP:")[1].split("-")[0].strip()
                    status_part = line.strip().split(" - ")[-1]

                    logs.append({
                        "time": time_part,
                        "ip": ip_part,
                        "status": status_part
                    })
                except IndexError:
                    continue
    return render_template("dashboard.html", logs=logs)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

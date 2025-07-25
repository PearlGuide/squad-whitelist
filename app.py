import threading
import time
import requests
from flask import Flask, send_file

app = Flask(__name__)
CFG_FILE = "RemoteAdminListHosts.cfg"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/PearlGuide/squad-whitelist/main/RemoteAdminListHosts.cfg"

def update_cfg_periodically():
    while True:
        try:
            response = requests.get(GITHUB_RAW_URL)
            if response.status_code == 200:
                # Write atomically to avoid partial reads
                with open(CFG_FILE + ".tmp", "w") as f:
                    f.write(response.text)
                # Replace the old file
                import os
                os.replace(CFG_FILE + ".tmp", CFG_FILE)
                print(f"Updated {CFG_FILE} from GitHub")
            else:
                print(f"Failed to fetch: status {response.status_code}")
        except Exception as e:
            print(f"Error updating cfg: {e}")
        time.sleep(300)  # 5 minutes

@app.route("/")
def home():
    return "Squad whitelist server running."

@app.route(f"/{CFG_FILE}")
def serve_cfg():
    return send_file(CFG_FILE, mimetype="text/plain")

if __name__ == "__main__":
    # Start background thread for periodic updates
    thread = threading.Thread(target=update_cfg_periodically, daemon=True)
    thread.start()

    # Start Flask server
    app.run(host="0.0.0.0", port=10000)

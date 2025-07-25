import requests
from flask import Flask, Response

app = Flask(__name__)

# Raw GitHub URL of your RemoteAdminListHosts.cfg file
GITHUB_RAW_URL = "https://raw.githubusercontent.com/PearlGuide/squad-whitelist/main/RemoteAdminListHosts.cfg"

@app.route('/RemoteAdminListHosts.cfg')
def serve_cfg():
    try:
        r = requests.get(GITHUB_RAW_URL)
        r.raise_for_status()
        content = r.text
        return Response(content, mimetype='text/plain')
    except Exception as e:
        return Response(f"Error fetching config: {e}", status=500)

@app.route('/')
def home():
    return "Squad whitelist server running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

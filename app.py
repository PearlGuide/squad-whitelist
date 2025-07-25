from flask import Flask, Response
import requests

app = Flask(__name__)

# Direct link to raw remoteadminlist.cfg on GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/pearlaced/squad-whitelist/main/remoteadminlist.cfg"

@app.route('/')
def serve_whitelist():
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            content = response.text
            return Response(content, mimetype='text/plain')
        else:
            return f"Failed to fetch whitelist from GitHub. Status code: {response.status_code}", 500
    except Exception as e:
        return f"Error while fetching whitelist: {str(e)}", 500

if __name__ == '__main__':
    app.run()

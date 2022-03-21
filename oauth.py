import json
import key
import pprint
import requests

from flask import Flask
from flask import request

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=4)

@app.route('/')
def start_auth():
    url = f'http://www.strava.com/oauth/authorize?client_id={key.client_id}&response_type=code&redirect_uri=http://127.0.0.1:5000/exchange_token&approval_prompt=force&scope=activity:read_all,activity:write,read_all'
    return f"Click <a href={url}>here</a> to authorize."

@app.route('/exchange_token')
def exchange_token():
    """
curl -X POST https://www.strava.com/oauth/token \
                     -F client_id=79874 \
                     -F client_secret=7e31fb02782332c57f05575d27f007f44550911a \
                     -F code=f7579e422f9c3115fad848aa2a3d27c005f58eea \
                     -F grant_type=authorization_code
    """
    code = request.args.get("code")

    data = {
        'client_id': key.client_id,
        'client_secret': key.client_secret,
        'code': code,
        'grant_type': 'authorization_code'
    }

    url = 'https://www.strava.com/oauth/token'

    result = requests.post(url, data=data)
    f = open('secrets.json', 'w')
    json.dump(result.json(), f, indent=2)
    f.close()

    return f"Wrote auth secrets file"

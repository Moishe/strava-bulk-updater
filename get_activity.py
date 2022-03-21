import hashlib
import json
import requests

from os import path

def get_maybe_cached_url(url, data={}):
    filename = 'cache/' + hashlib.sha224(url.encode()).hexdigest()
    if path.exists(filename):
        return json.load(open(filename))

    headers = {"Authorization": "Bearer %s" % secrets['access_token']}
    result_json = requests.get(url, data=data, headers=headers).json()

    json.dump(result_json, open(filename, 'w'))

    return result_json

page = 1

f = open('secrets.json')
secrets = json.load(f)

while True:
    endpoint = "https://www.strava.com/api/v3/athlete/activities?page=%d" % (page)
    activities = get_maybe_cached_url(endpoint)
    if len(activities) == 0:
        break

    for activity in activities:
        if activity["type"] == 'EBikeRide': # and activity["gear_id"] == 'b7096971':
            print(activity["name"], activity["type"], activity["gear_id"], activity["start_date"])
            activity_url = "https://www.strava.com/api/v3/activities/%d" % activity['id']
            if False:
                detail_activity = get_maybe_cached_url(activity_url)
                print(json.dumps(detail_activity["gear"], indent=2))

            data = {
                'gear_id': 'b8233285'
            }
            headers = {"Authorization": "Bearer %s" % secrets["access_token"]}
            #result = requests.put(activity_url, data=data, headers=headers)

    page += 1

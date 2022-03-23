import collections
import hashlib
import json
import requests

from os import path

LANDSHARK = 'b220737'
FIREBIRD = 'b4258012'

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

used_gear = collections.defaultdict(list)

total_distance = 0

while True:
    endpoint = "https://www.strava.com/api/v3/athlete/activities?page=%d" % (page)
    activities = get_maybe_cached_url(endpoint)
    if len(activities) == 0:
        break

    for activity in activities:
        if activity["type"] == "VirtualRide" and activity["gear_id"] == FIREBIRD:
            print(activity['id'], activity["name"], activity["type"], activity["gear_id"], activity["start_date"], activity["distance"])
            total_distance += activity["distance"]
            used_gear[activity["gear_id"]].append(activity["name"])
            activity_url = "https://www.strava.com/api/v3/activities/%d" % activity['id']

            detail_activity = get_maybe_cached_url(activity_url)
            print(json.dumps(detail_activity["gear"], indent=2))

            data = {
                'gear_id': LANDSHARK
            }
            headers = {"Authorization": "Bearer %s" % secrets["access_token"]}
            result = requests.put(activity_url, data=data, headers=headers)

    page += 1

for id in used_gear.keys():
    url = "https://www.strava.com/api/v3/gear/%s" % id
    result = get_maybe_cached_url(url)
    print(id, result['brand_name'], result['model_name'])

print(total_distance)
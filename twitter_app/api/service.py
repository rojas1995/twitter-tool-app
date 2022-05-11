import os
import requests
import json




def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {os.getenv('BEARER_TOKEN')}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def get_data(params):

    url = "https://api.twitter.com/2/tweets/search/recent"


    response = requests.get(url, auth=bearer_oauth, params=params)

    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    #return response.json()
    response_json = json.dumps(response.json(), indent=4, sort_keys=True)
    with open('response.txt', 'w') as handle:
        handle.write(response_json)
        handle.write('===========================================')
        handle.write('\n')
    return response_json
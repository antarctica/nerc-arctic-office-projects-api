import requests

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# This client uses the testing version of the API, in production a stable version should be used.

auth_client_id = 'xxx'
auth_client_secret = 'xxx'
auth_token_scopes = ['api://2b3f5c55-1a7d-4e26-a9a7-5b56b0f612f1/.default']
auth_token_url = 'https://login.microsoftonline.com/d14c529b-5558-4a80-93b6-7655681e55d6/oauth2/v2.0/token'

api_base_url = 'https://api.bas.ac.uk/arctic-office-projects/testing'


def process_included_resources(included: list) -> dict:
    included_by_type_id = {}
    for _included in included:
        if _included['type'] not in included_by_type_id.keys():
            included_by_type_id[_included['type']] = {}
        included_by_type_id[_included['type']][_included['id']] = _included

    return included_by_type_id


try:
    # Get access token
    #

    auth_client = BackendApplicationClient(client_id=auth_client_id)
    auth_session = OAuth2Session(client=auth_client)
    auth_token = auth_session.fetch_token(
        token_url=auth_token_url,
        client_id=auth_client_id,
        client_secret=auth_client_secret,
        scope=auth_token_scopes
    )

    # Make API request for a single resource
    #

    response = requests.get(
        url=f"{ api_base_url }/projects/01D5M0CFQV4M7JASW7F87SRDYB",
        headers={'authorization': f"bearer {auth_token['access_token']}"}
    )

    # Process data
    #

    content = response.json()
    content['included'] = process_included_resources(content['included'])

    # Output data
    #

    print(f"Response HTTP Status Code: { response.status_code }")
    print("\n")
    print(f"Project: { content['data']['id'] }")
    print("-----------------------------------")
    print("\n")
    print(f"Title: '{ content['data']['attributes']['title'] }'")
    print("\n")
    print("Participants:")
    for participant in content['data']['relationships']['participants']['data']:
        participant = content['included'][participant['type']][participant['id']]
        person = content['included'][participant['relationships']['person']['data']['type']][participant['relationships']['person']['data']['id']]
        print(f"  * { person['attributes']['first-name'] } { person['attributes']['last-name'] } ({ participant['attributes']['investigative-role'] })")

except requests.exceptions.RequestException as e:
    print('HTTP Request failed')
    print(e)

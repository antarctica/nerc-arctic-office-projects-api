import requests

# This client uses the testing version of the API, in production a stable version should be used.

api_base_url = 'https://api.bas.ac.uk/arctic-office-projects/testing'

def process_included_resources(included: list) -> dict:
    included_by_type_id = {}
    for _included in included:
        if _included['type'] not in included_by_type_id.keys():
            included_by_type_id[_included['type']] = {}
        included_by_type_id[_included['type']][_included['id']] = _included

    return included_by_type_id

try:
    # Make API request for a single resource
    #

    response = requests.get(
        url=f"{ api_base_url }/projects/01D5M0CFQV4M7JASW7F87SRDYB"
    )
    content = response.json()
    content['included'] = process_included_resources(content['included'])

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

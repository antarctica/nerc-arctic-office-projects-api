import requests

# This client uses the testing version of the API, in production a stable version should be used.

api_base_url = 'https://api.bas.ac.uk/arctic-office-projects/testing'

try:
    # Make API request for a single resource
    #

    response = requests.get(
        url=f"{ api_base_url }/projects/01D5M0CFQV4M7JASW7F87SRDYB"
    )
    content = response.json()

    print(f"Response HTTP Status Code: { response.status_code }")
    print(f"Project ID: { content['id'] }")
    print("\n")
    print(f"Project [{ content['id'] }] Title: '{ content['data']['attributes']['title'] }'")

except requests.exceptions.RequestException as e:
    print('HTTP Request failed')
    print(e)

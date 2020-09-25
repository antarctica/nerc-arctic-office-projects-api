import json
import subprocess


def json_valid(filename):
    try:
        json.load(open(filename))
        return True
    except ValueError as error:
        print('Invalid json file: %s' % error)
        return False

def import_grants(file):
    with open(file) as json_file:
        data = json.load(json_file)
        for project in data['data']:
            subprocess.run(['flask', 'import', 'grant', 'gtr', project['grant-reference']])

json_filename = 'json/projects-2019-06-16.json'
if json_valid(json_filename):
    import_grants(json_filename)
    # python3 import-grants.py &> import.log

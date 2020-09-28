import json
import subprocess
import re  # nosec


def json_valid(filename):
    try:  # nosec
        json.load(open(filename))
        return True
    except ValueError as error:
        print('Invalid json file: %s' % error)
        return False


def grant_reference_valid(grant_reference):
    patterns = {
        'gtr': r'^[A-Z]{2}\/[A-Z0-9]{7}\/\d{1}$',
        'other': r'\d{7}'
    }
    for key, pattern in patterns.items():
        if re.match(pattern, grant_reference):
            return True
    return False


def import_grants(file):
    with open(file) as json_file:
        data = json.load(json_file)
        for project in data['data']:
            if grant_reference_valid(project['grant-reference']):  # nosec
                subprocess.run(['flask', 'import', 'grant', 'gtr',
                                project['grant-reference']], shell=False)
            else:
                print('invalid ref %s' % project['grant-reference'])

json_filename = 'json/projects-2019-06-16.json'
if json_valid(json_filename):
    import_grants(json_filename)
    # python3 import-grants.py &> import.log

import json
import subprocess  # nosec
import re


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
        'other': r'\d{5,7}'
    }
    for key, pattern in patterns.items():
        if re.match(pattern, grant_reference):
            return True
    return False


def import_grants(file):
    with open(file) as json_file:
        data = json.load(json_file)

        lead_project = False

        for project in data['data']:

            try:
                lead_project = project['lead-project']
                print(lead_project)
            except Exception:
                lead_project = False
                print('No lead-project')

            if grant_reference_valid(project['grant-reference']):  # nosec
                subprocess.run(['flask', 'import', 'grant',
                                'gtr', project['grant-reference']], lead_project, shell=False)


json_filename = '/usr/src/app/arctic_office_projects_api/bulk_importer/json/projects-2022-08-10.json'
if json_valid(json_filename):
    import_grants(json_filename)

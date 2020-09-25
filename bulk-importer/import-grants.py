import json
import subprocess


def import_grants(file):
    with open(file) as json_file:
        data = json.load(json_file)
        for project in data['data']:
            subprocess.run(
                ['flask',
                 'import',
                 'grant',
                 'gtr',
                 project['grant-reference']]
                )

import_grants('json/projects-2019-06-16.json')
# python3 import-grants.py &> import.log

import json
import os


def import_grants(file):
    with open(file) as json_file:
        data = json.load(json_file)
        for project in data['data']:
            cmd = 'flask import grant gtr %s' % (project['grant-reference'])
            os.system(cmd)


import_grants('json/projects-2019-06-16.json')
# python3 import-grants.py &> import.log

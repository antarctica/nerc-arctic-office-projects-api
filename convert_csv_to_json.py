import csv
import json

# id to start from number
id_counter = 504

csvFilePath = r'projects.csv'
jsonFilePath = r'projects.json'


def make_json(csvFilePath, jsonFilePath):

    data = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        for row in csvReader:
            row_list = list(row.items())

            lead_project = 0

            if (row_list[1][1] == 'Lead'):
                lead_project = 1

            json_block = {
                "id": int(row_list[0][1]),
                "parent-id": None,
                "lead-project": lead_project,
                "title": row_list[3][1],
                "grant-reference": row_list[2][1]

            }

            data.append(json_block)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


make_json(csvFilePath, jsonFilePath)

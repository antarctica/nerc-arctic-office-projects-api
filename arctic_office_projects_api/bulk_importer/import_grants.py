import csv
import re
import subprocess


FLASK = (
    "/var/opt/wsgi/.virtualenvs/"
    "arctic-office-projects-api/bin/flask"
)

APP_DIR = "/var/www/arctic-office-projects-api"


def grant_reference_valid(grant_reference):
    patterns = {
        "gtr": r"^[A-Z]{2}/[A-Z0-9]{7}/\d{1}$",
        "other": r"\d{5,7}",
    }

    for pattern in patterns.values():
        if re.match(pattern, grant_reference):
            return True

    return False


def gtr_csv_to_json(csv_file):
    data_list = []

    with open(
        csv_file,
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            if row["parent-id"] == "":
                row["parent-id"] = None
            else:
                row["parent-id"] = int(row["parent-id"])

            row["id"] = int(row["id"])
            row["lead-project"] = int(row["lead-project"])

            data_list.append(row)

    return {"data": data_list}


def import_grants(csv_file):
    projects_json = gtr_csv_to_json(csv_file)

    for project in projects_json["data"]:
        lead_project = "1" if project["lead-project"] == 1 else "0"
        grant_reference = project["grant-reference"]

        if not grant_reference_valid(grant_reference):
            print(f"Skipping invalid grant reference: {grant_reference}")
            continue

        print(
            f"Importing {grant_reference}, "
            f"lead project: {lead_project}",
            flush=True,
        )

        subprocess.run(
            [
                FLASK,
                "import",
                "grant",
                "gtr",
                grant_reference,
                lead_project,
            ],
            cwd=APP_DIR,
            check=True,
            shell=False,
        )


csv_file = (
    "/var/www/arctic-office-projects-api/"
    "arctic_office_projects_api/bulk_importer/csvs/"
    "all-projects-2024-10-17.csv"
)

import_grants(csv_file)
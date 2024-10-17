import csv
import subprocess  # nosec
import re


def grant_reference_valid(grant_reference):

    patterns = {"gtr": r"^[A-Z]{2}\/[A-Z0-9]{7}\/\d{1}$", "other": r"\d{5,7}"}
    for key, pattern in patterns.items():
        if re.match(pattern, grant_reference):
            return True
    return False


def gtr_csv_to_json(csv_file):

    data_list = []

    with open(csv_file, mode="r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Convert 'parent-id' empty strings to None
            if row["parent-id"] == "":
                row["parent-id"] = None
            else:
                row["parent-id"] = int(row["parent-id"])
            # Convert 'id' and 'lead-project' to integers
            row["id"] = int(row["id"])
            row["lead-project"] = int(row["lead-project"])
            data_list.append(row)

    # Create the final JSON structure
    projects_json = {"data": data_list}
    return projects_json


def import_grants(csv_file):

    projects_json = gtr_csv_to_json(csv_file)

    data = projects_json
    lead_project = "0"

    subprocess.run(["poetry", "install"])  # nosec

    for project in data["data"]:
        try:
            lead_project_bool = project["lead-project"]
            if lead_project_bool == 1:
                lead_project = "1"
            else:
                lead_project = "0"
        except Exception:
            lead_project = "0"
            print("No lead-project")

        if grant_reference_valid(project["grant-reference"]):  # nosec
            subprocess.run(  # nosec
                [
                    "poetry",
                    "run",
                    "flask",
                    "import",
                    "grant",
                    "gtr",
                    project["grant-reference"],
                    lead_project,
                ],
                shell=False,  # nosec
            )


csv_file = "/usr/src/app/arctic_office_projects_api/bulk_importer/csvs/all-projects-2024-10-17.csv"
import_grants(csv_file)

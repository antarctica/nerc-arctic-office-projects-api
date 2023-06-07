# Updating projects

### Single project import:

- see the README.md section about importing individual projects
```shell
$ flask import grant <grant_type> <grant_ref> <lead_project - 0 or 1 - optional>
```


- example:
```shell
$ flask import grant gtr NE/I028858/1 
```

### Bulk project import:

- In the JSON file, only the project reference & lead_project data are needed. The other fields are not required.
- get csv from gtr website
- check for project duplicates
- convert csv to json - link to repo for this
- set the lead-projects
- run the project locally - with docker
- run the bulk import script
- check the output to see whether or not any institions or topics need to be added.
- for institutions: https://ror.org/search

- make sure the correct json file is referenced in import_grants.py - approx line number 48

- in the Heroku dashboard, run a console & enter
```shell
$ python arctic_office_projects_api/bulk_importer/import_grants.py
```


###

- Projects without a reference - from: id 99  to: id 142
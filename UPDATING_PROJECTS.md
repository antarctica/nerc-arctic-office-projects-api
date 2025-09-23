# Updating projects

## API
There are a number of Post routes for adding data into the database.

### Postman collections
Import json collections into Postman from here:  
`postman_collections`  
Auth variables will need to be added. Most likely from Azure: `portal.azure.com`

### Set up
To initialise the database or update categories and organisations
- `/post-categories` - send with json payload: `arctic_office_projects_api/resources/science-categories.json`
- `/post-organisations` 
    - funders - send with json payload: `arctic_office_projects_api/resources/funder-organisations.json`
    - people - send with json payload: `arctic_office_projects_api/resources/people-organisations.json`

### Import single record:
- `/post-gtr-grant-single` - send with json payload:

```
{
    "lead-project": 0,
    "grant-reference": "NE/K000217/1"
}
```

### Import mulitple records:

- `/post-gtr-grant-bulk` - send with json payload:

```
[
 {
   "grant-reference": "NE/P006183/1",
   "lead-project": 0
 },
 {
   "grant-reference": "NE/P00590X/1",
   "lead-project": 0
 },
 {
   "grant-reference": "NE/P005985/1",
   "lead-project": 0
 }
]
```

## CLI

### Single project import:

- see the README.md section about importing individual projects
```shell
$ poetry run flask import grant <grant_type> <grant_ref> <lead_project - 0 or 1 - optional>
```


- example:
```shell
$ poetry run flask import grant gtr NE/N016092/2
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

###
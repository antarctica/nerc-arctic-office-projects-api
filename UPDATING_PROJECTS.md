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

### Update project_organisations:

- `/post-organisation-data` - send with json payload:
```
{
    "organisation_id": "C7FB1D09-3E85-4CFF-922E-65AD67C8F51B",
    "organisation_name": "THE JAMES HUTTON INSTITUTE",
    "organisation_ror": "https://ror.org/03rzp5127"
}
```

### Update project_person:

- `/post-person-data` - send with json payload:
```
{
    "name": "Steven Profile (Researcher)",
    "gtr_person": "E51FDDE8-EE5C-4B85-80FF-C03FB9B00D2U",
    "orcid": "http://orcid.org/0000-0000-0000-0000"
}
```

### Update project_topic:

- `/post-topic-data` - send with json payload:
```
{
    "topic_id": "71A8EA33-09DF-4E02-85BA-A9545564F72D",
    "topic_name": "Water+Quality",
    "gcmd_link_name": "WATER QUALITY",
    "gcmd_link_code": "gcmd.earthdata.nasa.gov/kms/concept/1ee8a323-f0ba-4a21-b597-50890c527c8e"
}

### Update project_subject:

- `/post-subject-data`  - send with json payload:
```
{
    "subject_text": "Wind Power",
    "gcmd_link_code": "gcmd.earthdata.nasa.gov/kms/concept/b3a95e10-1c1d-41cf-8802-8bb1d3a41353"
}

### Import errors

- `/exception-log` - shows the contents of this file where errors are logged: 
- Docker: `arctic_office_projects_api/bulk_importer/exception_log.txt`
- BAS server: `/var/www/arctic-office-projects-api/exception_log.txt`
- Defined by this env var: IMPORT_EXCEPTION_LOG


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


## Import issues

- Projects without a reference - from: id 99  to: id 142
- Project not found: In silico and Experimental Screening Platform for Characterising Environmental Impact of Impact of Industry Development in the Arctic (EXPECT), 2605032

###

## Missing funder orgs?
- Horizon Europe Guarantee
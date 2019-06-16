# NERC Arctic Office Projects API

API for NERC Arctic Office projects database.

See the [BAS API documentation](https://docs.api.bas.ac.uk/services/arctic-office-projects) for how to use this API.

## Purpose

This API is used to record details of projects related to the [NERC Arctic Office](https://www.arctic.ac.uk). This API
is primarily intended for populating the [projects database](https://www.arctic.ac.uk/research/projects-database) in 
the Arctic Office website but is designed for general use where applicable.

## Implementation

This API is implemented as a Python Flask application following the [JSON API](https://jsonapi.org) specification. 
A PostgreSQL database is used for storing information. OAuth is used for controlling access to this information, 
managed using Microsoft Azure.

### Configuration

Application configuration is set within `config.py`. Options use global or per-environment defaults which can be 
overridden if needed using environment variables, or a `.env` file (Dot Env) file. 

Options include values for application secrets, feature flags (used to enable to disable features) and connection 
strings (such as databases).

The application environment (development, production, etc.) is set using the `FLASK_ENV` environment variable. A sample 
dot-env file, `.env.example`, describes how to set any required, recommended or commonly changed options. See 
`config.py` for all available options.

### Data models

Data for this API is held in a PostgreSQL database. The database structure is managed using 
[alembic](https://alembic.sqlalchemy.org/en/latest/) migrations, defined in `migrations/`. 
[SQL Alchemy](https://www.sqlalchemy.org) is used to access the database within the application, using models defined 
in `arctic_office_projects_api/models.py`.

### Data representations

[Marshmallow](https://marshmallow.readthedocs.io) and 
[Marshmallow JSON API](https://marshmallow-jsonapi.readthedocs.io/en/latest/) are used to transform resources between a 
*storage* (database) and *access* (API) representation, using schemas defined in 
`arctic_office_projects_api/schemas.py`.

Examples of representation transformations include, hiding the database primary key and renaming unintuitive database 
field names to more useful attribute names.

Schemas in this application should inherit from `arctic_office_projects_api.schemas.Schema` with a meta property 
inherited from `arctic_office_projects_api.schemas.Schema.Meta`. These classes define custom functionality and 
defaults suitable for generating more complete JSON API responses.

#### Neutral IDs

Resources in this API are identified using a *neutral identifier* such as: `01D5M0CFQV4M7JASW7F87SRDYB`.
 
Neutral identifiers are persistent, unique, random and independent of how data is stored or processed, as this may 
change and introduce breaking limitations/requirements. They are implemented using Universally Unique Lexicographically 
Sortable Identifiers ([ULIDs](https://github.com/ulid/spec)).

Neutral identifiers are created as part of [Data loading](#data-loading).

### Data loading

Production data for this API is imported from a variety of sources.

In non-production environments, [Database seeding](#database-seeding) is used to create fake, but realistic, data in 
non-production environments.

#### Science categories

Science categories are used to categorise research projects, for example that a project relates to sea-ice.

These categories are defined in well-known schemes to ensure well considered and systematic coverage of general or 
discipline specific categories. Categories are structured into a hierarchy to allow navigation from general to more
specific terms, or inversely, to generalise a term.

The schemes used by this project are:

* the [Universal Decimal Classification (UDC) - Summary](http://www.udcsummary.info)
* the [NASA Global Change Master Directory (GCMD) - Earth Science keywords](https://earthdata.nasa.gov/earth-observation-data/find-data/gcmd/gcmd-keywords)
* the [UK Data Service - Humanities And Social Science Electronic Thesaurus (HASSET)](https://hasset.ukdataservice.ac.uk)

The UDC Summary scheme is used as a base scheme, covering all aspects of human knowledge. As this scheme is only a 
summary, it does not include detailed terms for any particular areas. The GCMD Earth Science keywords and UK Data 
Service HASSET schemes are used to provide additional detail for physical sciences and social sciences respectively, as
these are areas that the majority of research projects included in this API lie within.

These schemes and their categories are implemented as RDF graphs that describe properties about each category, such as
name, examples and aliases, and the relationships between categories using 'broader than' and 'narrower than' relations.

These graphs are expressed as RDF triples by each scheme authority (i.e. the UDC consortium, NASA and the UK Data 
Service respectively). A set of additional triples are used to link concepts (categories) between each concept scheme. 

| Scheme                      | Linked UDC Concept                       |
| --------------------------- | ---------------------------------------- |
| GCMD Earth Science keywords | *55 Earth Sciences. Geological sciences* |
| UK Data Service HASSET      | *3 Social Sciences*                      |

**Note:** These linkages are unofficial and currently very course, linking the top concept(s) of the Earth Science and
HASSET schemes to a single concept in the UDC.

A series of processing steps are used to load RDF triples/graphs from each scheme, generate linkages between schemes 
and export a series of categories and category schemes into a file that can be imported into this API using the 
`import categories` CLI command.

The categories and category schemes import file is included in this project as `resources/science-categories.json` 
and can imported without needing to perform any processing. See the [Usage](#importing-science-categories) section for 
more information.

If additional category schemes need to be included, or existing schemes require updating, the processing steps will 
need to be ran again to generate a replacement import file. See the [Development](#generating-category-import-files) 
section for more information.

**Note:** There is currently no support for updating a category scheme in cases where its categories have changed and
require re-mapping to project resources.

### Documentation

Usage and reference documentation for this API is hosted within the 
[BAS API Documentation project](https://gitlab.data.bas.ac.uk/WSF/api-docs). The sources for this documentation are 
held in this project. Through [Continuous Deployment](#continuous-deployment) they are uploaded to a relevant version 
of this service in the API docs project, and it's continuous Deployment process triggered to rebuild the documentation 
site with any changes.

| Documentation Type | Documentation Format   | Source                |
| ------------------ | ---------------------- | --------------------- |
| Usage              | Jekyll page (Markdown) | `docs/usage/usage.md` |
| Reference          | OpenAPI (Yaml)         | `openapi.yml`         |

**Note:** Refer to the 
[Documentation forms and types](https://gitlab.data.bas.ac.uk/WSF/api-docs#documentation-types-and-forms) section for
more information on how these documentation sources are processed by the BAS API Documentation project.

### Errors

Errors returned by this API are formatted according to the 
[JSON API error specification](https://jsonapi.org/format/#error-objects).

API Errors are implemented as application exceptions inherited from `arctic_office_projects_api.errors.ApiException`. 
This can return errors directly as Flask responses, or as a Python dictionary or JSON string.

Errors may be returned individually as they occur (such as fatal errors), or as a list of multiple errors at the same 
time (such as validation errors). See the [Returning an API error](#returning-an-API-error) section for how to return 
an error.

### Error tracking

To ensure the reliability of this API, errors are logged to 
[Sentry](https://sentry.io/antarctica/arctic-office-projects-api) for investigation and analysis.

Through [Continuous Deployment](#continuous-deployment), commits to the `master` branch create new *staging* Sentry 
releases. Tagged commits create new *production* releases.

### Health checks

Endpoints are available to allow the health of this API to be monitored. This can be used by load balancers to avoid
unhealthy instances or monitoring reporting tools to prompt repairs by operators.

#### [GET|OPTIONS] `/meta/health/canary`

Reports on the overall health of this service as a boolean *healthy/unhealthy* status.

Returns a `204 - NO CONTENT` response when healthy. Any other response should be considered unhealthy.

### Request IDs

To aid in debugging, all requests will include a `X-Request-ID` header with one or more values. This can be used to
trace requests through different services such as a load balancer, cache and other layers. Request IDs are managed by 
the [Request ID](https://pypi.org/project/flask-request-id-header/) middleware. The `X-Request-ID` header is returned 
to users and other components as a response header.

See the [Correlation ID](https://gitlab.data.bas.ac.uk/WSF/api-load-balancer#correlation-id) documentation for how the
BAS API Load Balancer handles Request IDs.

### Reverse proxying

It is assumed this API will be ran behind a reverse proxy / load balancer. This can present problems with generating
absolute URLs as the API does not know which protocol, host, port or path it is exposed to clients as.

I.e. using `flask.url_for('main.index', _external=True)`, the API may produce a URL of `http://localhost:1234`, but 
clients expect `https://api.bas.ac.uk/foo/`.

The [Reverse Proxy middleware](https://pypi.org/project/flask-reverse-proxy-fix/) is used to provide this missing 
context using [configuration options](#configuration) and HTTP headers.

| Component   | Configuration Method | Configuration Key      | Implemented by           | Example Value   |
| ----------- | -------------------- | ---------------------- | ------------------------ | --------------- |
| Protocol    | Configuration Option | `PREFERRED_URL_SCHEME` | Flask                    | `https`         |
| Host        | HTTP Header          | `X-Forwarded-Host`     | Reverse Proxy middleware | `api.bas.ac.uk` |
| Path prefix | Configuration Option | `SERVICE_PREFIX`       | Reverse Proxy middleware | `/foo/v1`       | 

### Authentication and authorisation

This service is protected by 
[Microsoft Azure's Active Directory OAuth endpoints](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-v2-protocols) 
using the [Flask Azure AD OAuth Provider](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth) 
for authentication and authorisation.

This API (as a service), and it's clients are registered as applications within Azure Active Directory. The app 
representing this service, defines *application* (rather than *delegated*) permissions that can be assigned to relevant
client applications.

Clients request access tokens from Azure, rather than this API, using the *Client Credentials* code flow.

Access tokens are structured as JSON Web Tokens (JWTs) and should be specified as a bearer token in the `authorization` 
header by clients.

Suitable permissions in either the 'NERC BAS WebApps' or 'NERC' Azure tenancy will be required to register applications
and assign permissions.

| Environment       | Azure Tenancy    |
| ----------------- | ---------------- |
| Local Development | NERC BAS WebApps |
| Staging           | NERC BAS WebApps |
| Production        | NERC             |

#### Available scopes

| Scope  | Type | Name | Description  |
| ------ | ---- | ---- | -------------| 
| -      | -    | -    | -            |

#### Registering API clients

See 
[these instructions](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth#registering-an-application-in-azure)
for how to register client applications. 

**Note:** It is not yet possible to register clients programmatically due to limitations with the Azure CLI and Azure
provider for Terraform.

**Note:** These instructions describe how to register a *client* of this API, see the [Setup](#setup) section for how 
to register this API itself as a *service*.

#### Assigning scopes to clients

See
[these instructions](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth#assigning-permissions-for-one-application-to-use-another)
for how to assign permissions defined by this API to client applications.

**Note:** It is not yet possible to assign permissions programmatically due to limitations with the Azure CLI and Azure
provider for Terraform.

## Usage

This section describes how to manage existing instances of this project in any environment. See the [Setup](#setup) 
section for how to create instances.

**Note:** See the [BAS API documentation](https://docs.api.bas.ac.uk/services/arctic-office-projects) for how to use 
this API.

For all new instances you will need to:

1. run [Database migrations](#run-database-migrations)
2. import [science categories](#importing-science-categories)

For development or staging environments you may also need to:

1. run [Database seeding](#run-database-seeding)

### Flask CLI

Many of the tasks needed to manage instances of this project use the [Flask CLI](http://flask.pocoo.org/docs/1.0/cli/).

To run flask CLI commands in a local development environment:

1. run `docker-compose up` to start the application and database containers
2. in another terminal window, run `docker-compose exec app ash` to launch a shell within the application container
3. in this shell, run `flask [command]` to perform a command

To run flask CLI commands in a staging and production environment:

1. navigate to the relevant Heroku application from the [Heroku dashboard](https://dashboard.heroku.com)
2. from the application dashboard, select *More* -> *Run Console* from the right hand menu
3. in the console overlay, enter `ash` to launch a shell within the application container
4. in this shell, run `flask [command]` to perform a command

**Note:** In any environment, run `flask` alone to list available commands and view basic usage instructions.

### Run database migrations

[Database migrations](#database-migrations) are used to control the structure of the application database for persisting
[Data models](#data-models).

The [Flask migrate](https://flask-migrate.readthedocs.io/en/latest/) package is used to provide a 
[Flask CLI](#flask-cli) command for running database migrations:

```shell
$ flask db [command]
```

To view the current (applied) migration:

```shell
$ flask db current
```

To view the latest (possibly un-applied) migration:

```shell
$ flask db head
```

To update an instance to the latest migration:

```shell
$ flask db upgrade
```

To un-apply all migrations (effectively emptying the database):

**WARNING:** This will drop all tables in the application database, removing any data.

```shell
$ flask db downgrade base
```

### Run database seeding

**Note:** This process only applies to instances in local development or staging environments.

[Database seeding](#database-seeding) is used to populate the application with fake, but realistic data.

A custom [Flask CLI](#flask-cli) command is included for running database seeding:

```shell
$ flask seed [command]
```

To seed predictable, stable, test data for use when [Testing](#testing):

```shell
$ flask seed predictable
```

To seed 100 random, fake but realistic, projects and related resources for use in non-production environments:

```shell
$ flask seed random
```

### Import data

A custom [Flask CLI](#flask-cli) command is included for importing various resources into the API:

```shell
$ flask import [resource] [command]
```

#### Importing science categories

To import [categories and category schemes](#science-categories) from a file:

```shell
$ flask import categories [path to import file]
```

For example:

```shell
$ flask import categories resources/science-categories.json
```

**Note:** The structure of the import file will be validated against the `resources/categories-schema.json` JSON Schema 
before import.

**Note:** Previously imported categories, identified by their *namespace* or *subject*, will be skipped if imported 
again. Their properties will not be updated.



## Setup

This section describes how to create new instances of this project in a given environment.

```shell
$ git clone https://gitlab.data.bas.ac.uk/web-apps/arctic-office-projects-api.git
$ cd arctic-office-projects-api
```

### Terraform remote state

For environments using Terraform, state information is stored remotely as part of 
[BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project.

Remote state storage will be automatically initialised when running `terraform init`, with any changes automatically 
saved to the remote (AWS S3) backend, there is no need to push or pull changes.

#### Remote state authentication

Permission to read and/or write remote state information for this project is restricted to authorised users. Contact
the [BAS Web & Applications Team](mailto:servicedesk@bas.ac.uk) to request access.

See the [BAS Terraform Remote State](https://gitlab.data.bas.ac.uk/WSF/terraform-remote-state) project for how these
permissions to remote state are enforced.

### Local development

Docker and Docker Compose are required to setup a local development environment of this API.

#### Local development - Docker Compose

If you have access to the [BAS GitLab instance](https://gitlab.data.bas.ac.uk), you can pull the application Docker 
image from the BAS Docker Registry. Otherwise you will need to build the Docker image locally.

```shell
# If you have access to gitlab.data.bas.ac.uk
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose pull
# If you don't have access
$ docker-compose build
```

Copy `.env.example` to `.env` and edit the file to set at least any required (uncommented) options.

To run the API using the Flask development server (which reloads automatically if source files are changed) and a local
PostgreSQL database:

```shell
$ docker-compose up
```

See the [Usage](#usage) section for instructions on how to configure and use the application instance.

#### Local development - database

To run application [Database migrations](#database-migrations) and [Database seeding](#database-seeding), open an
additional terminal to run:

```shell
# database migrations
$ docker-compose run app flask db upgrade
# database seeding
$ docker-compose run app flask seed --count 3
```

To connect to the database in a local development environment:

| Parameter | Value       |
| --------- | ----------- |
| Host      | `localhost` |
| Port      | `5432`      |
| Database  | `app`       |
| Username  | `app`       |
| Password  | `password`  |
| Schema    | `public`    |

To connect to the database using `psql` in a local development environment:

```shell
$ docker-compose exec app-db ash
$ psql -U app
= SELECT current_database();
> current_database 
> ------------------
> app
= \q
$ exit
```

#### Local development - auth

See 
[these instructions](https://gitlab.data.bas.ac.uk/web-apps/flask-extensions/flask-azure-oauth#registering-an-application-in-azure)
for how to register the application as a service.

* use `BAS NERC Arctic Office Projects API Testing` as the application name
* choose *Accounts in this organizational directory only* as the supported account type
* do not enter a redirect URL
* from the *API permissions* section of the registered application's permissions page:
    * remove the default 'User.Read' permission
* from the manifest page of the registered application:
    * change the `accessTokenAcceptedVersion` property from `null` to `2`
    * add an item, `api://[appId]`, to the `identifierUris` array, where `[appId]` is the value of the `appId` property
    * add these items to the `appRoles` property [1]

**Note:** It is not yet possible to register clients programmatically due to limitations with the Azure CLI and Azure
provider for Terraform.

**Note:** This describes how to register this API itself as a *service*, see the 
[Registering API clients](#registering-api-clients) section for how to register a *client* of this API.

Set the `AZURE_OAUTH_TENANCY`, `AZURE_OAUTH_APPLICATION_ID` and `AZURE_OAUTH_CLIENT_APPLICATION_IDS` options in the 
local `.env` file.

For testing the API locally, register and assign all permissions to a testing client:
    * see the [Registering API clients](#registering-api-clients) section to register a local testing API client
        * named `BAS NERC Arctic Office Projects API Client Testing`, using accounts in the home tenancy only, with no 
          redirect URL
    * see the [Assigning scopes to clients ](#assigning-scopes-to-clients) section to assign all permissions to this 
      client

[1] Application roles for the BAS NERC Arctic Office Projects API:

**Note:** Replace `[uuid]` with a UUID.

```json
{
  "appRoles": []
}
```

### Staging

Docker, Docker Compose and Terraform are required to setup the staging environment of this API.

Access to the *BAS Web & Applications* Heroku account is needed to setup the staging environment of this API.

**Note:** Make sure the `HEROKU_API_KEY` and `HEROKU_EMAIL` environment variables are set within your local shell.

#### Staging - Heroku
 
```shell
$ cd provisioning/terraform
$ docker-compose run terraform
$ terraform init
$ terraform apply
```

This will create a Heroku Pipeline, containing staging and production applications with a Heroku PostgreSQL database
add-on.

A config var (environment variable) will automatically be added to each application with it's corresponding database
connection string. Other non-sensitive config vars should be set using Terraform.

Once running, add the appropriate configuration to the 
[BAS API Load Balancer](https://gitlab.data.bas.ac.uk/WSF/api-load-balancer).

Configure the relevant variables in the GitLab [Continuous Deployment](#continuous-deployment) configuration to enable
the application Docker image to be deployed automatically.

See the [Usage](#usage) section for instructions on how to configure and use the deployed application instance.
 
##### Staging - Heroku sensitive config vars

Config vars should be set [manually](https://dashboard.heroku.com/apps/bas-arctic-projects-api-stage/settings) for 
sensitive settings. Other config vars should be set in Terraform.

| Config Var    | Config Value                        | Description                                         |
| ------------- | ----------------------------------- | --------------------------------------------------- |
| `SENTRY_DSN`  | *Available from Sentry*             | Identifier for application in Sentry error tracking |

#### Staging - database

Heroku will automatically run [Database migrations](#database-migrations) as part of a 
[Heroku release phase](https://devcenter.heroku.com/articles/release-phase).

The Docker Container used for this is defined in `Dockerfile.heroku-release`.

[Database seeding](#database-seeding) needs to be ran manually through the
[Heroku dashboard](https://dashboard.heroku.com/apps/bas-arctic-projects-api-stage):

1. select *More* -> *Run console* from the top-right
2. enter `flask seed --count 3` as the command

To connect to the staging environment database, expand the *Database Credentials* section of the 
[Heroku database settings](https://data.heroku.com/datastores/8d6bd297-680a-453a-8c2b-efd7b077bd3a#administration).

**WARNING!:** Heroku databases require SSL connections using a self-signed certificate. Currently SSL validation is 
disabled to allow connections. This is not ideal and should be used with caution.

If connecting from PyCharm, under the *advanced* tab for the data source, set the *sslfactory* parameter to 
`org.postgresql.ssl.NonValidatingFactory`.

#### Staging - documentation

To upload and publish documentation, follow the relevant setup instructions in the 
[BAS API Documentation project](https://gitlab.data.bas.ac.uk/WSF/api-docs/#adding-a-new-service-service-version).

#### Staging - auth

Use the same *BAS NERC Arctic Office Projects API Testing* application registered in the 
[Auth sub-section in the local development section](#local-development-auth).

### Production

Docker, Docker Compose and Terraform are required to setup the production environment of this API.

Access to the *BAS Web & Applications* Heroku account is needed to setup the staging environment of this API.

**Note:** Make sure the `HEROKU_API_KEY` and `HEROKU_EMAIL` environment variables are set within your local shell.

#### Production - Heroku

See the [Heroku sub-section in the staging section](#staging-heroku) for general instructions.

##### Production - Heroku sensitive config vars

Config vars should be set [manually](https://dashboard.heroku.com/apps/bas-arctic-projects-api-prod/settings) for 
sensitive settings. Other config vars should be set in Terraform.

| Config Var    | Config Value                        | Description                                         |
| ------------- | ----------------------------------- | --------------------------------------------------- |
| `SENTRY_DSN`  | *Available from Sentry*             | Identifier for application in Sentry error tracking |

#### Production - database

Heroku will automatically run [Database migrations](#database-migrations) as part of a 
[Heroku release phase](https://devcenter.heroku.com/articles/release-phase).

The Docker Container used for this is defined in `Dockerfile.heroku-release`.

To connect to the production environment database, expand the *Database Credentials* section of the 
[Heroku database settings](xxx).

**WARNING!:** Heroku databases require SSL connections using a self-signed certificate. Currently SSL validation is 
disabled to allow connections. This is not ideal and should be used with caution.

If connecting from PyCharm, under the *advanced* tab for the data source, set the *sslfactory* parameter to 
`org.postgresql.ssl.NonValidatingFactory`.

#### Production - documentation

To upload and publish documentation, follow the relevant setup instructions in the 
[BAS API Documentation project](https://gitlab.data.bas.ac.uk/WSF/api-docs/#adding-a-new-service-service-version).

#### Production - auth

Using the [Auth sub-section in the local development section](#local-development-auth), register an additional Azure
application with these differences:

* tenancy: *NERC*
* name: *BAS NERC Arctic Office Projects API*

## Development

This API is developed as a Flask application.

Environments and feature flags are used to control which elements of this application are enabled in different 
situations. For example in the development environment, Sentry error tracking is disabled and Flask's debug mode is on.

New features should be implemented with appropriate [Configuration](#configuration) options available. Sensible defaults 
for each environment, and if needed feature flags, should allow end-users to fine tune which features are enabled.

Ensure `.env.example` is kept up-to-date if any configuration options are added or changed.

Also ensure:

* [Integration tests](#integration-tests) are updated to prevent future regression
* [End-user documentation](#documentation) is updated
* if needed, [Database migrations](#database-migrations), including reverse migrations, are written for database 
  structure changes
* if needed, [Database seeding](#database-seeding) is in place for use in development environments and running tests

### Code Style

PEP-8 style and formatting guidelines must be used for this project, with the exception of the 80 character line limit.

[Flake8](http://flake8.pycqa.org/) is used to ensure compliance, and is ran on each commit through 
[Continuous Integration](#continuous-integration).

To check compliance locally:

```shell
$ docker-compose run app flake8 . --ignore=E501 --exclude migrations
```

### Dependencies

Python dependencies should be defined using Pip through the `requirements.txt` file. The Docker image is configured to
install these dependencies into the application image for consistency across different environments. Dependencies should
be periodically reviewed and updated as new versions are released.

To add a new dependency:

```shell
$ docker-compose run app ash
$ pip install [dependency]==
# this will display a list of available versions, add the latest to `requirements.txt`
$ exit
$ docker-compose down
$ docker-compose build
```

If you have access to the BAS GitLab instance, push the rebuilt Docker image to the BAS Docker Registry:

```shell
$ docker login docker-registry.data.bas.ac.uk
$ docker-compose push
```

### Dependency vulnerability scanning

To ensure the security of this API, all dependencies are checked against 
[Snyk](https://app.snyk.io/org/antarctica/project/6da1f928-3b7b-4b36-a83c-6586a057ad48/history) for vulnerabilities. 

**Warning:** Snyk relies on known vulnerabilities and can't check for issues that are not in it's database. As with all 
security tools, Snyk is an aid for spotting common mistakes, not a guarantee of secure code.

Some vulnerabilities have been ignored in this project, see `.snyk` for definitions and the 
[Dependency exceptions](#dependency-vulnerability-exceptions) section for more information.

Through [Continuous Integration](#continuous-integration), on each commit current dependencies are tested and a snapshot
uploaded to Snyk. This snapshot is then monitored for vulnerabilities.

#### Dependency vulnerability exceptions

This project contains known vulnerabilities that have been ignored for a specific reason.

* [Py-Yaml `yaml.load()` function allows Arbitrary Code Execution](https://snyk.io/vuln/SNYK-PYTHON-PYYAML-42159)
    * currently no known or planned resolution
    * indirect dependency, required through the `bandit` package
    * severity is rated *high*
    * risk judged to be *low* as we don't use the Yaml module in this application
    * ignored for 1 year for re-review
* [SQL Injection vulnerability where group_by accepts user input](https://snyk.io/vuln/SNYK-PYTHON-SQLALCHEMY-173678)
    * a fix is available, but is currently unreleased
    * direct dependency
    * severity is *high*
    * risk judged to be *low* as we don't use group by in any queries
    * ignored for 1 month to prompt check for released version containing fix

### Static security scanning

To ensure the security of this API, source code is checked against [Bandit](https://github.com/PyCQA/bandit) for issues 
such as not sanitising user inputs or using weak cryptography. 

**Warning:** Bandit is a static analysis tool and can't check for issues that are only be detectable when running the 
application. As with all security tools, Bandit is an aid for spotting common mistakes, not a guarantee of secure code.

Through [Continuous Integration](#continuous-integration), each commit is tested.

To check locally:

```shell
$ docker-compose run app bandit -r .
```

### Returning an API error

To return an API error, define an exception which inherits from the `arctic_office_projects_api.errors.ApiException`
exception.

For example:

```python
from arctic_office_projects_api.errors import ApiException

class ApiFooError(ApiException):
    """
    Returned when ...
    """
    title = 'Foo'
    detail = 'Foo details'
```

Arbitrary structured/additional data can be included in a `meta` property. This information can be error or error 
instance specific.

```python
from arctic_office_projects_api.errors import ApiException

class ApiFooError(ApiException):
    """
    Returned when ...
    """
    title = 'Foo'
    detail = 'Foo details'

    # error specific meta information
    meta = {
      'foo': 'bar'
    }

# Error instance specific meta information
error_instance = ApiFooError(meta={'foo': 'baz'})
```

See the `ApiException` class for other supported properties.

To return an API error exception as a flask response:

```python
from arctic_office_projects_api import create_app
from arctic_office_projects_api.errors import ApiException

app = create_app('production')

class ApiFooError(ApiException):
    """
    Returned when ...
    """
    title = 'Foo'
    detail = 'Foo details'

@app.route('/error')
def error_route():
    """
    Returns an error
    """

    error = ApiFooError()
    return error.response()
```

### Adding a Flask CLI command

[Flask CLI](#flask-cli) commands are used to expose processes and actions that control a Flask application. These 
commands may be provided by Flask (such as listing all application routes), by third-party modules (such as managing
[Database Migrations](#run-database-migrations)) or custom to this project (such as for [Importing data](#import-data)).

Custom/first-party commands are defined in `arctic_office_projects_api/commands.py`, registered in the `create_app()`
factory method.

**Note:** Ensure tests are added for any custom commands. See `tests/test_commands.py` for examples.

### Generating category import files

**Note:** This section is still experimental until it can be formalised as part of 
[#34](https://gitlab.data.bas.ac.uk/web-apps/arctic-office-projects-api/issues/34).

Experiments 6 and 7 of the [RDF Experiments](https://gitlab.data.bas.ac.uk/felnne/ref-experiments) project are used to:

* generate a series of a RDF triples linking the GCMD Earth Science keywords and UK Data Service HASSET schemes to the
  UDC Summary scheme (experiment 7)
* loading the concepts from the UDC, GCMD and HASSET schemes and producing a JSON file that can be imported into this
  project (experiment 6)

### Logging

In a request context, the default Flask log will include the URL and [Request ID](#request-ids) of the current request.
In other cases, these fields are substituted with `NA`.

**Note:** When not running in Flask Debug mode, only messages with a severity of warning of higher will be logged.

### Debugging

To debug using PyCharm:

* *Run* -> *Edit Configurations*
* *Add New Configuration* -> *Python*

In *Configuration* tab:

* Script path: `[absolute path to project]/manage.py`
* Python interpreter: *Project interpreter* (*app* service in project Docker Compose)
* Working directory: `[absolute path to project]`
* Path mappings: `[absolute path to project]=/usr/src/app`

### Database migrations

All structural changes to the application database must be made using 
[alembic](https://alembic.sqlalchemy.org/en/latest/) database migrations, defined in `migrations/`.

Migrations should be generated from changes to [Database models](#database-models), to prevent differences between the
model and the database, using the `db migrate` command. This will generate a new migration in `migrations/versions`,
which should be reviewed to remove the auto-generated comments and check the correct actions will be carried out.

All migrations must include a reverse/down migration, as these are used to reset the database when
[Testing](#integration-tests).

See the [Usage](#run-database-migrations) section for instructions on applying database migrations.

### Database models

All database access should use [SQL Alchemy](https://www.sqlalchemy.org) with models defined in 
`arctic_office_projects_api/models.py`. A suitable `__repr__()` method should be defined to aid in debugging. A suitable 
`seed()` method should be defined for [seeding](#database-seeding) each model.

### Database seeding

Database seeding is used to populate the application database with either:

1. predictable, stable, test data for use in [Testing](#testing)
2. random, fake but realistic, test data for use in development and staging environments

See the [Usage](#run-database-seeding) section for instructions on running database seeding.

#### Faker

[Faker](https://github.com/joke2k/faker) is a library for generating fake data. It includes a range of providers for 
coomon attributes such as dates, names, addresses etc. with localisation into various languages and locales (e.g. 
`en-GB`). Faker is recommended for creating random, fake, data when seeding.

##### Custom Faker providers

Where Faker does not provide a required attribute, a custom provider can be created. New providers should follow the
conventions established by the main Faker package. Custom providers should be defined in the 
`arctic_office_projects_api.main.faker.providers` module. When adding the custom provider to Faker, ensure the 
providers `Provider` class is added, rather than the module itself.

For example:

```python
from faker import Faker
from arctic_office_projects_api.main.faker.providers.person import Provider as Person

faker = Faker('en_GB')
faker.add_provider(Person)  # a custom provider

person_gender = faker.male_or_female()  # use of a custom provider
```

### Resource schemas

[Marshmallow](https://marshmallow.readthedocs.io) and 
[Marshmallow JSON API](https://marshmallow-jsonapi.readthedocs.io/en/latest/) are used to define schemas, in 
`arctic_office_projects_api/schemas.py`, that convert data between the form it's stored in (i.e. as a 
[Model](#database-models) instance), and the form it should be displayed within the API (as a resource).

Schemas and models do not necessarily have a 1:1 mapping. A model may be based on a subset of model instances (e.g. 
only those with a particular set of attributes), or may combine multiple models to give a more useful resource.

Typically, models do not expose fields specific to how data is stored for example, such as primary keys in databases.

#### Pagination support

Where a schema will return a large number of items, pagination is recommended. The 
`arctic_office_projects_api.schemas.Schema` class supports a limited form of pagination whilst it is added to 
Marshmallow JsonAPI more completely. 

Limitations include:

* only page based pagination is supported, as opposed to offset/limit and cursor methods
* only Flask SQL Alchemy 
  [Pagination](http://flask-sqlalchemy.pocoo.org/2.3/api/?highlight=pagination#flask_sqlalchemy.Pagination) objects are
  supported

When enabled this support will:

* extract items in the current page to use as input
* add links to the first, previous, current, next and last pages in the top-level links object

To use pagination:

* set the `many` and `paginate` schema options to true
* pass a Flask SQL Alchemy Pagination object to the `dump()` method

For example:

```python
from flask import request, jsonify

from arctic_office_projects_api import create_app
from arctic_office_projects_api.models import Person
from arctic_office_projects_api.schemas import PersonSchema

app = create_app('production')

@app.route('/people')
def people_list():
    # Determine the pagination page number from the request, or default to page 1
    page = request.args.get('page', type=int)
    if page is None:
        page = 1

    # Get a Pagination object based on the current pagination page number and a fixed page size
    people = Person.query.paginate(page=page, per_page=app.config['APP_PAGE_SIZE'])

    # Enable pagination support on schema
    payload = PersonSchema(many=True, paginate=True).dump(people)

    return jsonify(payload.data)
```

#### Related resources support

Relationships between schemas can be expressed using the `arctic_office_projects_api.schemas.Relationship` class. This
is a custom version of the [Marshmallow JSON API](https://marshmallow-jsonapi.readthedocs.io/en/latest/).

Additions made to the `arctic_office_projects_api.schemas.Schema` class allow *relationship* and *related resource* 
responses to be returned.

Limitations include:

* document and data level meta elements are not currently supported

##### Relationship responses 

A [relationship response](https://jsonapi.org/format/#fetching-relationships) returns the resource linkage between a 
resource and one or more other resource type.

For example, a Person resource may be related to one or more Participant resources:

```json
{
  "data": [
    {
      "id": "01D5T4N25RV2062NVVQKZ9NBYX",
      "type": "participants"
    }
  ],
  "links": {
    "related": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/participants",
    "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
  }
}
```

To return a relationship response:

* set the `resource_linkage` schema option to the related resource type

For example:

```python
from flask import request, jsonify
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from arctic_office_projects_api import create_app
from arctic_office_projects_api.models import Person
from arctic_office_projects_api.schemas import PersonSchema

app = create_app('production')

@app.route('/people/<person_id>/relationships/organisations')
def people_relationship_organisations(person_id: str):
    try:
        person = Person.query.filter_by(id=person_id).one()
        payload = PersonSchema(resource_linkage='organisation').dump(person)
        return jsonify(payload.data)
    except NoResultFound:
        return 'Not found error'
    except MultipleResultsFound:
        return 'Multiple resource conflict error'
```

##### Related resource responses

A [related resources response](https://jsonapi.org/format/#document-resource-object-related-resource-links) returns the
resources of a particular type related to a resource.

For example, a Person resource may be related to one or more Participant resources:

```json
{
  "data": [
    {
      "attributes": {
        "foo": "bar"
      },
      "id": "01D5T4N25RV2062NVVQKZ9NBYX",
      "links": {
        "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX"
      },
      "relationships": {
        "person": {
          "data": {
            "id": "01D5MHQN3ZPH47YVSVQEVB0DAE",
            "type": "people"
           },
           "links": {
             "related": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/people",
             "self": "http://localhost:9000/participants/01D5T4N25RV2062NVVQKZ9NBYX/relationships/people"
          }
        }
      },
      "type": "participants"
    }
  ],
    "links": {
      "self": "http://localhost:9000/people/01D5MHQN3ZPH47YVSVQEVB0DAE/relationships/participants"
  }
}
```

To return a related resource response:

* set the `related_resource` schema option to the related resource type
* set the `many_related` schema option to true where there may be multiple related resources (of a given type)

For example:

```python
from flask import request, jsonify
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from arctic_office_projects_api import create_app
from arctic_office_projects_api.models import Person
from arctic_office_projects_api.schemas import PersonSchema

app = create_app('production')

@app.route('/people/<person_id>/organisations')
def people_organisations(person_id: str):
    try:
        person = Person.query.filter_by(id=person_id).one()
        payload = PersonSchema(resource_resource='organisation').dump(person)
        return jsonify(payload.data)
    except NoResultFound:
        return 'Not found error'
    except MultipleResultsFound:
        return 'Multiple resource conflict error'
```

## Testing

### Integration tests

This project uses integration tests to ensure features work as expected and to guard against regressions and 
vulnerabilities.

The Python [UnitTest](https://docs.python.org/3/library/unittest.html) library is used for running tests using Flask's 
test framework. Test cases are defined in files within `tests/` and are automatically loaded when using the 
`test` Flask CLI command.

Tests are automatically ran on each commit through [Continuous Integration](#continuous-integration).

To run tests manually:

```shell
$ docker-compose run -e FLASK_ENV=testing app flask test
```

To run tests using PyCharm:

* *Run* -> *Edit Configurations*
* *Add New Configuration* -> *Python Tests* -> *Unittests*

In *Configuration* tab:

* Script path: `[absolute path to project]/tests`
* Python interpreter: *Project interpreter* (*app* service in project Docker Compose)
* Working directory: `[absolute path to project]`
* Path mappings: `[absolute path to project]=/usr/src/app`

**Note:** This configuration can be also be used to debug tests (by choosing *debug* instead of *run*).

#### Integration testing - databases

Where the application database is needed, a separate test database (`app_test`) will be used to prevent touching 
development data. [Database migrations](#database-migrations) and [Database seeding](#database-seeding) will be ran on
each test to setup, populate and tear down the database for each test.

#### Integration testing - auth

Where methods require authentication/authorisation locally issued tokens are used, using a temporary signing key.

### Continuous Integration

All commits will trigger a Continuous Integration process using GitLab's CI/CD platform, configured in `.gitlab-ci.yml`.

This process will run the application [Integration tests](#integration-tests).

Pip dependencies are also [checked and monitored for vulnerabilities](#dependency-vulnerability-scanning).

## Deployment

### Deployment - Local development

In development environments, the API is ran using the Flask development server through the project Docker container.

Code changes will be deployed automatically by Flask reloading the application where a source file changes.

See the [Local development](#local-development) sub-section in the [Setup](#setup) section for more information.

### Deployment - Staging

The staging environment is deployed on [Heroku](https://heroku.com) as an 
[application](https://dashboard.heroku.com/apps/bas-arctic-projects-api-stage) within a 
[pipeline](https://dashboard.heroku.com/pipelines/30f0864a-16e9-41c8-862d-866dd460ba20) in the `webapps@bas.ac.uk` 
shared account.

This Heroku application uses their 
[container hosting](https://devcenter.heroku.com/articles/container-registry-and-runtime) option running a Docker image 
built from the application image (`./Dockerfile`) with the application source included and development related features
disabled. This image (`./Dockerfile.heroku`) is built and pushed to Heroku on each commit to the `master` branch 
through [Continuous Deployment](#continuous-deployment).

An additional Docker image (`./Dockerfile.heroku-release`) is built to act as a 
[Release Phase](https://devcenter.heroku.com/articles/release-phase) for the Heroku application. This image is based on 
the Heroku application image and includes an additional script for running [Database migrations](#database-migrations). 
Heroku will run this image automatically before each deployment of this project.

### Deployment - Production

The production environment is deployed in the same way as the [Staging environment](#deployment-staging), using an
different Heroku [application](https://dashboard.heroku.com/apps/bas-arctic-projects-api-prod) as part of the same 
pipeline.

Deployments are also made through [Continuous Deployment](#continuous-deployment) but only on tagged commits.

### Continuous Deployment

A Continuous Deployment process using GitLab's CI/CD platform is configured in `.gitlab-ci.yml`. This will:

* build a Heroku specific Docker image using a 'Docker In Docker' (DIND/DND) runner and push this image to Heroku
* push [End-user documentation](#documentation) to the 
  [BAS API Documentation project](https://gitlab.data.bas.ac.uk/WSF/api-docs)
* create a Sentry release and associated deployment in the appropriate environment

This process will deploy changes to the *staging* environment on all commits to the *master* branch.

This process will deploy changes to the *production* environment on all tagged commits.

## Release procedure

### At release

For all releases:

1. create a release branch
2. if needed, build & push the Docker image
3. close release in `CHANGELOG.md`
4. push changes, merge the release branch into `master` and tag with version

The application will be automatically deployed into production using [Continuous Deployment](#continuous-deployment).

## Feedback

The maintainer of this project is the BAS Web & Applications Team, they can be contacted at: 
[servicedesk@bas.ac.uk](mailto:servicedesk@bas.ac.uk).

## Issue tracking

This project uses issue tracking, see the 
[Issue tracker](https://gitlab.data.bas.ac.uk/web-apps/arctic-office-projects-api/issues) for more 
information.

**Note:** Read & write access to this issue tracker is restricted. Contact the project maintainer to request access.

## License

© UK Research and Innovation (UKRI), 2019, British Antarctic Survey.

You may use and re-use this software and associated documentation files free of charge in any format or medium, under 
the terms of the Open Government Licence v3.0.

You may obtain a copy of the Open Government Licence at http://www.nationalarchives.gov.uk/doc/open-government-licence/

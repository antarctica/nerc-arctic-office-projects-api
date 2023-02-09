# NERC Arctic Office Projects API - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.4.2] 2023-02-09

### Added

* Ability to save and use GTR categories directly alongside the mapping of these to GCMD categories

### Changed

* Set projects in the bulk_importer .json to be unique & well-formed
* Update the project dependencies in the requirements.txt file

### Fixed

* Fix import bug whereby lead-projects are not correctly marked

## [0.4.1] 2022-05-10

### Changed

* Upgrade waitress python package to 1.4.3 - fix vulnerability in versions less than 1.4.0

## [0.4.0] 2022-04-22

### Fixed

* Added a condition to `arctic_office_projects_api/importers/gtr.py` to force the use of https://gtr.ukri.org:443 if http://internal-gtr-tomcat-alb-611010599.eu-west-2.elb.amazonaws.com:8080 is detected 

### Changed

* `only: - master` in `.gitlab-ci.yml to only deploy to staging if master branch is updated

## [Unreleased]

### Added

* JUnit test results support
* Additional people ORCID mappings
* Additional organisations for people
* Allowing GTR importer instances to accept a GTR resource URI
* Exceptions for unmapped GTR resources
* Unique database constraint for categorisations
* Organisation importer command
* Integration tests for custom CLI commands

### Fixed

* Support for unclassified grants in GTR importer
* Difference in handling GTR project topics compared to categories in GTR importer
* Application exception to act as a generic error class for all types of error, not just those at the API layer
* Table name on categorisations migration statement

### Changed

* Upgrading to a hobby Heroku application due to allow multiple processes to be ran
* Upgrading to a hobby basic Heroku database due to row count requirement
* Updating Heroku release script to load organisations
* Refactoring finding distinct GTR project category/topics in GTR importer
* Refactoring API exception to inherit from new application exception
* Refactoring importers into a package
* Refactoring commands into main application
* Refactoring standalone routes into a separate module
* Improving categories import file JSON Schema
* Renaming standalone route test cases to more clearly separate them from application tests

## [0.3.0] 2019-06-10

### Added

* Category, Category Scheme and Categorisation resources to categorise projects with subjects
* Updating Flask Azure OAuth provider (0.3.0)
* White listing Arctic Office Projects Manager staging application to use staging instance
* BAS API Docs OpenAPI extensions
* Methods in Projects Faker provider to decide whether a PI or CoI has worked on other projects before
* Updated Pip dependencies
* Instructions in README on how to access a `psql` prompt in development environments
* Refactoring README to add a usage section on how to run various Flask CLI commands
* Adding instructions on adding custom Flask CLI commands
* Adding project purpose

### Fixed

* Pinning `urllib3` dependency to later version to mitigate https://app.snyk.io/vuln/SNYK-PYTHON-URLLIB3-174464 
* Correcting OpenAPI specification
* Correcting project duration method in Projects Faker provider to generate end dates correctly
* Allowing related resources to have no items in Marshmallow schemas
* Marshmallow JSON API resource linkages where the related resource uses multiple words (e.g `foo-bar`)
* Correcting examples in README

### Changed

* Improving OpenAPI specification
* Improving End user documentation, including documenting identifiers and controlled values used
* Reimplementing database seeding using standalone class and expanded, generic, predictable resources 
* Importing Grant (Project) type enum from Grant provider, rather than duplicating in Project provider
* Faker Grant references are now dependent on the type of grant
* Refactoring resource routes into separate blueprints
* Refactoring resource tests into separate test cases
* Refactoring index and meta routes out of blueprints
* Refactoring main and meta blueprint utilities and errors into main application
* Refactoring RequestFormatter to standalone module
* Refactoring Faker providers out of blueprints

### Removed

* Proof of concept API changelog until this can be redeveloped as part of the BAS API Docs project

## [0.2.0] 2019-04-04

### Added

* Grant entity, representing a research grant
* Allocation entity, representing the relationship between a research project and a research grant
* Organisation entity, representing the relationship between a Grant and its funder, and an individual and their 
  organisation
* Basic seeding for Participants, linking Projects to random People
* Project acronym property
* Project abstract property
* Project publications property
* Project website property
* Project duration property
* Project access duration property
* Project country property
* Person Orcid ID property
* Person avatar property
* Whitelisting application id for test Arctic Office website integration
* Guidance on fake data in usage documentation

### Changed

* Improved project seeding to be more realistic at representing average and edge-case examples
* Refactored enum schema field to support any enumeration
* Refactored Person and Participant migrations into one
* Error for methods returning a single resource but find multiple changed from 409 Conflict to 422 Unprocessable Entity

### Fixed

* Working around inconsistent ordering for included items in tests
* Corrected links for JSON API resource relations
* Corrected underscores incorrectly being shown in API responses

## [0.1.0] 2019-03-18

### Added

* Basic Project and People resources, linked by a Participant resource
* Initial version, based on People (Sensitive) API

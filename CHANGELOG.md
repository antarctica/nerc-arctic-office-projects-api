# NERC Arctic Office Projects API - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

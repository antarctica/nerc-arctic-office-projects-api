# NERC Arctic Office Projects API - Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

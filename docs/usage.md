---
title: NERC Arctic Office Projects API - Usage
---

## General information

### Support

Limited, best effort, support is offered for using this API to integrate NERC Arctic Office Project information
into the Arctic Office website ([www.arctic.ac.uk](https://www.arctic.ac.uk)) as part of it's redevelopment.

Contact the [BAS Service Desk](mailto:servicedesk@bas.ac.uk) for support.

### Information handling

Reasonable policies and technical measures are in place to ensure information in this API is held and transferred 
securely. Where third parties are used to operate this API, we ensure they are used for a necessary task, with
measures in place to ensure they are used appropriately and securely.

Applicable services used by this API are:

* [Heroku](https://heroku.com) - for storing data and hosting the API
* [Sentry](https://sentry.io/) - for reporting API errors, which may include API responses

This API is provided by the [British Antarctic Survey](https://www.bas.ac.uk) on behalf of the 
Natural Environment Research Council [Arctic Office](https://www.arctic.ac.uk). Both BAS and NERC are part of 
[UK Research and Innovation](https://www.ukri.org).

If you have any questions about how information is used by this API please contact the 
[BAS Service Desk](mailto:servicedesk@bas.ac.uk) in the first instance. If you do not receive a reply within a few days
please contact the [BAS Freedom of Information Officer](foi@bas.ac.uk).

### Security disclosures

Please contact the [BAS Service Desk](mailto:servicedesk@bas.ac.uk) to disclose any security concerns with this API.

Contact us for instructions if you need to report any sensitive information.

### Versioning policy

This API is versioned. An API version must be specified as a URL prefix (e.g. `/v1/foo`).

Changes between versions are documented in the [Change log](../changelog).

Only the latest, stable, API version is [Supported](#support). When a new version is released, all previous versions 
are deprecated for a period of time to allow clients time to move to supported version before being retired and removed.

#### Testing version

For testing new features and changes, a non-stable, testing version (`/testing`)is available. This version should only 
be used for testing and may change any time. Separate credentials are required to use the testing version.

### Deprecation policy

Features may be deprecated in this API as it evolves. This may include changes to options, methods, resources and API
versions. Usually an alternative feature will be available but in some cases a feature may be removed without one.

As with API versions, deprecated features will be supported for a period of time for clients to move to an alternative,
before being retired/removed.

Deprecated features will be referenced in this documentation and the [Change log](../changelog).

### Information available

During initial development, all versions of this API use fake data, intended to be realistic but meaningless. This 
ensures any potentially sensitive information contained in real data is not exposed to unreliable and untested 
integrations.

In the future, stable versions of the API will have access to real data. The [Testing version](#testing-version) will 
always use fake data.

#### Fake data

Fake data is generated randomly using the [Faker](https://faker.readthedocs.io/en/master/) library, with custom methods 
added for resources in this API. Various ratios and weightings are used to generate mostly 'average' data as well as 
known extremes to allow for testing edge cases.

##### Fake data limitations

There are a number of general differences/limitations between fake and real data:

1. the number of fake date items is arbitrary and are created or removed in bulk, whereas the number of real data items 
   is variable, based on the current number of relevant projects
2. all fake data items may be removed and replaced with new items when changes are made to resource properties, whereas
   real data items will be added or removed gradually, with most remaining the same

See each resource for additional limitations.

## Technical information

### Standards support

This API follows the [JSON API](http://jsonapi.org/format/1.0/) standard, unless stated otherwise.

### Authentication and authorisation

Clients must be allowed access to information held by this API using OAuth tokens.

Clients must first be registered by contacting [Support](#support) to be granted suitable permissions and issued with a
client ID and secret.

### Content Types

This API supports the `application/json` content type only, unless stated otherwise.

This API supports `UTF-8` character encoding only, unless stated otherwise.

### Request IDs

All requests will include a `X-Request-ID` header to aid in debugging requests through different components.

If desired, a custom request ID can be specified by the client which will be used instead of, or in addition to a API
generated value.

**Note:** In some cases a client specified value will be ignored, ensure you do not rely on this value being returned.

**Note:** This header may include multiple values (multiple Request IDs) separated by a `,` with possible whitespace. 

### Data Types

#### String (data type)

String values are encoded as UTF-8.

Examples:

* `normal`
* `åccented`
* `emoji ❄️`

#### Date (data type)

Date values are encoded as [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) [strings](#string) (i.e. `YYYY-MM-DD`).

Examples:

* `1875-05-20`

#### Date range (data type)

Date range values are encoded as an object containing:
 
* a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date interval [string](#string) which covers the entire range 
  (i.e. `YYYY-MM-DD/YYYY-MM-DD`)
* a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date instant [string](#string) which marks the beginning of the
  range (i.e. `YYYY-MM-DD`)
* a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date instant [string](#string) which marks the end of the range 
  (i.e. `YYYY-MM-DD`)
  
Date ranges can be unbounded, on either or both sides, to indicate where a range has no end date for example. When 
unbounded, the relevant date instant will be `null` and the relevant part of date interval will be omitted.

Examples:

```json
{
  "interval": "1875-05-20/2002-04-14",
  "start_instance": "1875-05-20",
  "end_instance": "2002-04-14"
}
```

```json
{
  "interval": "/2002-04-14",
  "start_instance": null,
  "end_instance": "2002-04-14"
}
```

```json
{
  "interval": "1875-05-20/",
  "start_instance": "1875-05-20",
  "end_instance": null
}
```

### Pagination

API methods that return large numbers of items will use pagination to split items into a number of pages based on the
[JSON API specification](https://jsonapi.org/format/#fetching-pagination).

Pages are a fixed size of **10** items per page, with the `page` query parameter selecting a page. Responses will
include links to navigate between pages. Where a link isn't applicable (e.g. previous on the first page, its value will 
be `null`).

Pages start from `1`, where a page isn't specified, the first page will be assumed. Where a page doesn't exist, a 
*404 Not Found* error will be returned (e.g. if 4 pages exist but page 8 is requested, a 404 error will be returned).

For example:

```json
{
  "data": [],
  "links": {
    "first": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=1",
    "last": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=4",
    "next": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=2",
    "prev": null,
    "self": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=1"
  }
}
```

## Errors

Errors reported by this API follow the [JSON API](http://jsonapi.org/format/1.0/#errors) standard.

The `id` property will vary with each error using a UUID (version 4).

**Note:** Some API errors are automatically captured by an error tracking service.

## Resources

### Projects

Represents information about a research project.

#### Fake data limitations

* project acronym's don't relate to a projects title
* titles, abstracts, publications and other properties shared with corresponding grants are not the same
* projects are assigned to grants at random
* where publications are in a project, all are fake using the prefix 10.5555 and an 8 digit random suffix

### Participants

Represents information about an individuals involvement in a research project.

#### Fake data limitations

* projects will only use a subset of available participant roles (Principle Investigator and Co-Investigator)
* a random person will be chosen as the PI of a project
* a random number of CoIs (that are not the PI) may be chosen as Co-Is

### People

Represents information about an individual.

#### Fake data limitations

* ORCiD IDs are fake and can't be used to lookup additional information on a person
* Organisation allocations are made at random

### Grants

Represents information a research grant.

#### Fake data limitations

* grant references do not correspond to the format of each grant type
* grant funder's (organisations) are chosen at random
* all grants will use a status of either 'active' or 'closed'
* where publications are in a grant, all are fake using the prefix 10.5555 and an 8 digit random suffix
* titles, abstracts, publications and other properties shared with corresponding projects are not the same
* all grants total funds will be random within a range based on the grant type (i.e. not in multiples of 10, 100, etc.) 
* all grants have a 50% chance of having indirect funds
* all grants with indirect funds will be assigned 12% of the grants total funds

### Allocations

Represents information about how a research project is funded by grants.

#### Fake data limitations

* grants are related to projects at random

### Organisations

Represents information about an organisation, acting either as an agent (e.g. a funder) or an entity (e.g. that an 
individual belongs to).

#### Fake data limitations

* organisation acronym's don't relate to a organisation's name
* Grid IDs are fake and can't be used to lookup additional information on an organisation

---
title: NERC Arctic Office Projects API - Usage
---

## General information

### Support

Limited, best effort, support is offered for using this API to integrate project information into the NERC Arctic 
Office website ([www.arctic.ac.uk](https://www.arctic.ac.uk)) as part of it's redevelopment.

Contact the [BAS Service Desk](mailto:servicedesk@bas.ac.uk) for support.

### Information handling

This API is provided by the [British Antarctic Survey (BAS)](https://www.bas.ac.uk) on behalf of the 
Natural Environment Research Council (NERC) [Arctic Office](https://www.arctic.ac.uk). Both BAS and NERC are part of 
[UK Research and Innovation (URKI)](https://www.ukri.org), UKRI is the legal operator of this service.

Reasonable policies and technical measures are in place to ensure information in this API is held and transferred 
securely. Where third parties are used to operate this API, they are used for a necessary task and with measures in 
place to ensure they are used appropriately and securely.

Third party services used by this API are:

* [Heroku](https://heroku.com) - for storing data and hosting the API
* [Sentry](https://sentry.io/) - for monitoring API errors, which may include API responses

If you have any questions about how information is used by this API please contact the 
[BAS Service Desk](mailto:servicedesk@bas.ac.uk) in the first instance. If you do not receive a prompt reply please 
contact the [BAS Freedom of Information Officer](foi@bas.ac.uk).

### Security disclosures

Please contact the [BAS Service Desk](mailto:servicedesk@bas.ac.uk) to disclose any security concerns with this API.

Contact us for instructions if you need to report any sensitive information.

### Versioning policy

This API is versioned. An API version must be specified as a URL prefix (e.g. `/v1`).

Only the latest, stable, API version is [Supported](#support). When a new version is released, all previous versions 
are deprecated for a period of time to allow clients time to move to the new version before being retired and removed.

#### Testing version

For testing new features and changes, an unstable, testing, version (`/testing`) is available. The functionality and 
data in this version may change or break at any time. Separate credentials are required to use this version.

The testing version uses fake, but realistic, data subject to these limitations:

* the number of fake date items is arbitrary and are created or removed in bulk, whereas the number of real data items 
  is variable, based on the current number of relevant projects
* fake data may be removed or replaced with new data at any time whereas real data typically doesn't change often and 
  will be added or removed gradually
* project and organisation acronym's don't relate to a projects title
* project and grant publications are fake, using the reserved testing prefix `10.5555` and will not resolve
* project participant's will only use a subset of available participant roles (Principle or Co Investigator)
* project countries will always be *Svalbard and Jan Mayen* (`SJM`)
* people ORCID iDs are fake, and will not resolve
* organisation Grid IDs are fake, and will not resolve

### Deprecation policy

Features may be deprecated in this API as it evolves. This may include changes to options, methods, resources and API
versions. Usually an alternative feature will be available but in some cases a feature may be removed without one.

As with API versions, deprecated features will be supported for a period of time for clients to move to an alternative,
before being retired/removed. Deprecated features will be referenced in this documentation.

## Technical information

### Standards support

This API follows the [JSON API](http://jsonapi.org/format/1.0/) standard, unless stated otherwise.

### Content Types

This API supports the `application/json` content type only, unless stated otherwise.

This API supports `UTF-8` character encoding only, unless stated otherwise.

### Errors

Errors reported by this API follow the [JSON API](http://jsonapi.org/format/1.0/#errors) standard.

The `id` property will vary with each error using a UUID (version 4).

**Note:** Non-client API errors are captured automatically by an error tracking service. Persistent client errors can
be raised directly through [Support](#support).

### Request IDs

All requests will include a `X-Request-ID` header to aid in debugging requests through different components.

If desired, a custom request ID can be specified by the client which will be used instead of, or in addition to a API
generated value.

**Note:** In some cases a client specified value will be ignored, ensure you do not rely on this value being returned.

**Note:** This header may include multiple values (multiple Request IDs) separated by a `,` with possible whitespace. 

### Authentication and authorisation

Clients must be granted access to information held in this API using OAuth tokens.

Clients may be registered by contacting [Support](#support) to be granted suitable permissions and will be issued with 
a client ID and secret.

### Pagination

API methods that return large numbers of items will use pagination to split items into a number of pages based on the
[JSON API specification](https://jsonapi.org/format/#fetching-pagination).

Pages are fixed to **10** items, with the `page` query parameter selecting a page. Pages start from `1`, which will be 
used when a page isn't specified. Where a page doesn't exist, a *404 Not Found* error will be returned. 
 
Responses will include links to navigate between pages. Where a link isn't applicable (e.g. previous on the first page), 
its value will be `null`.

For example:

```json
{
  "links": {
    "first": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=1",
    "last": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=4",
    "next": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=2",
    "prev": null,
    "self": "https://api.bas.ac.uk/arctic-office-projects/v1/projects?page=1"
  }
}
```

### Data Types

#### String (data type)

String values are encoded as UTF-8.

Examples:

* `normal`
* `åccented`
* `emoji ❄️`

#### Decimal (data type)

Decimal values are encoded with a given precision (e.g. 2 decimal places).

Examples:

* `0.00`
* `-10.02`
* `100000000.20`

#### Date (data type)

Date values are encoded as [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) [strings](#string) (i.e. `YYYY-MM-DD`).

Examples:

* `1875-05-20`

#### Date range (data type)

Date range values are encoded as an object containing:
 
* a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date interval [string](#string-data-type) which covers the
  entire range (i.e. `YYYY-MM-DD/YYYY-MM-DD`)
* a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date instant [string](#string-data-type) which marks the 
  beginning of the range (i.e. `YYYY-MM-DD`)
* a [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date instant [string](#string-data-type) which marks the 
  end of the range (i.e. `YYYY-MM-DD`)
  
Date ranges can be unbounded, on either or both sides, to indicate where a range has no end date for example. When 
unbounded, the relevant date instant will be `null` and the relevant part of date interval will be replaced with `..`.

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
  "interval": "../2002-04-14",
  "start_instance": null,
  "end_instance": "2002-04-14"
}
```

```json
{
  "interval": "1875-05-20/..",
  "start_instance": "1875-05-20",
  "end_instance": null
}
```

#### Currency (data type)

Currency values are encoded as an object containing:

* a [decimal](#decimal-data-type) value with fixed precision of two decimal places (e.g. `12.70`)
* a currency object containing:
    * a [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency code [string](#string-data-type) (e.g. `GBP`)
    * the major currency unit symbol unicode escaped [string](#string-data-type) (e.g. `\u00a3` (`£`))

Examples:

```json
{
  "currency": {
    "iso-4217-code": "GBP",
    "major-symbol": "\u00a3"
  },
  "value": "123.40"
}
```
























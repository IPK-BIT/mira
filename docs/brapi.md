# BrAPI

To implement full compliance with MIAPPE, the following BrAPI endpoints need to be implemented:

 - GET /trials
 - GET /studies
 - GET /locations
 - GET /germplasm
 - GET /observationunits
 - GET /events
 - GET /samples
 - GET /variables

In the current version of MIRA, only a subset of those endpoints are supported. A detailed description and supported query parameters are listed below.

## Pagination

Detailed information about pagination in BrAPI can be found in its [documentation](https://plant-breeding-api.readthedocs.io/en/latest/docs/best_practices/Pagination.html). This section provides an overview of the specific implementation in MIRA.

When the data array contains no records, the pagination is ignored by returning:

    "pagination": {
        "totalCount": 0,
        "pageSize": 0,
        "totalPages": 0,
        "currentPage": 0
    }

All endpoints, except ``GET /serverinfo``, support the ``page`` and ``pageSize`` query parameters and are not listed in the following sections. Default values comply with BrAPIs recommendation of ``page=0`` and ``pageSize=1000``.

## BrAPI Core

### GET /serverinfo

Retrieve information about the server itself and avaible endpoints.

## BrAPI Phenotyping

### GET /observations

Retrieve all observations where there are measurements for the given observation variables. 
observationTimestamp should be ISO8601 format with timezone ``YYYY-MM-DDThh:mm:ss+hhmm``

Supported Query parameters:

|Parameter|Description|Type|
|---------|-----------|----|
|germplasmDbId|Use this parameter to only return results associated <br>with the given `Germplasm` unique identifier. <br/>Use `GET /germplasm` to find the list of available <br>`Germplasm` on a server.|string|
|observationUnitDbId|The unique ID of an Observation Unit|string|
|observationVariableDbId|The unique ID of an observation variable|string|

### GET /observationunits

Get a filtered set of Observation Units

Supported Query parameters:

|Parameter|Description|Type|
|---------|-----------|----|

### GET /variables

Call to retrieve a list of observationVariables available in the system.

Supported Query parameters:

|Parameter|Description|Type|
|---------|-----------|----|
|observationVariableDbId|Variable's unique ID|string|
|methodName|Human readable name for the method <br>MIAPPE V1.1 (DM-88) Method Name <br>of the method of observation|string|
|traitName|Human readable name for the scale <br>MIAPPE V1.1 (DM-88) Scale Name <br>of the scale of observation|string|
|scaleName|Human readable name for the trait <br>MIAPPE V1.1 (DM-88) Trait Name <br>of the trait of observation|string|
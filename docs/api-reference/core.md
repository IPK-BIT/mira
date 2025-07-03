# Core Module

## Trial

### GET /trials

**Supported Parameters**

| Data Type   | Parameter Name |Description                                                                                                                           |
| ----------- | -------------- |------------------------------------------------------------------------------------------------------------------------------------- |
| integer     | page           | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer     | pageSize       | The size of the pages to be returned. Default is `1000`.                                                                             |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1000,
      "totalCount": 1,
      "totalPages": 1
    },
    "status": [
      {
        "message": "Success",
        "messageType": "INFO"
      }
    ],
    "datafiles": []
  },
  "result": {
    "data": [
      {
        "active": null,
        "additionalInfo": null,
        "commonCropName": null,
        "contacts": null,
        "datasetAuthorships": [
          {
            "datasetPUI": null,
            "license": "ALL RIGHTS RESERVED BY THE AUTHORS",
            "publicReleaseDate": null,
            "submissionDate": null
          }
        ],
        "documentationURL": null,
        "endDate": null,
        "externalReferences": null,
        "programDbId": null,
        "programName": null,
        "publications": null,
        "startDate": null,
        "trialDbId": "bridge",
        "trialDescription": null,
        "trialName": "BRIDGE core1000",
        "trialPUI": null
      }
    ]
  }
}
```

### GET /trials/{trialDbId}

**Supported Parameters**

| Data Type   | Parameter Name |Description                     |
| ----------- | -------------- |------------------------------- |
| string      | trialDbId      | The internal trial identifier. |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1000,
      "totalCount": 1,
      "totalPages": 1
    },
    "status": [
      {
        "message": "Success",
        "messageType": "INFO"
      }
    ],
    "datafiles": []
  },
  "result": {
    "active": null,
    "additionalInfo": null,
    "commonCropName": null,
    "contacts": null,
    "datasetAuthorships": [
      {
        "datasetPUI": null,
        "license": "ALL RIGHTS RESERVED BY THE AUTHORS",
        "publicReleaseDate": null,
        "submissionDate": null
      }
    ],
    "documentationURL": null,
    "endDate": null,
    "externalReferences": null,
    "programDbId": null,
    "programName": null,
    "publications": null,
    "startDate": null,
    "trialDbId": "bridge",
    "trialDescription": null,
    "trialName": "BRIDGE core1000",
    "trialPUI": null
  }
}
```

## Study

### GET /studies

**Supported Parameters**

| Data Type   | Parameter Name |Description                                                                                                                           |
| ----------- | -------------- |------------------------------------------------------------------------------------------------------------------------------------- |
| integer     | page           | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer     | pageSize       | The size of the pages to be returned. Default is `1000`.                                                                             |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1000,
      "totalCount": 1,
      "totalPages": 1
    },
    "status": [
      {
        "message": "Success",
        "messageType": "INFO"
      }
    ],
    "datafiles": []
  },
  "result": {
    "data": [
      {
        "active": null,
        "additionalInfo": null,
        "commonCropName": null,
        "contacts": null,
        "culturalPractices": null,
        "dataLinks": null,
        "documentationURL": null,
        "endDate": null,
        "environmentParameters": null,
        "experimentalDesign": null,
        "externalReferences": null,
        "growthFacility": null,
        "lastUpdate": null,
        "license": null,
        "locationDbId": null,
        "locationName": null,
        "observationLevels": null,
        "observationUnitsDescription": null,
        "observationVariableDbIds": null,
        "seasons": null,
        "startDate": null,
        "studyCode": null,
        "studyDbId": "Barley Spike Investigation",
        "studyDescription": null,
        "studyName": "Barley Spike Investigation",
        "studyPUI": null,
        "studyType": null,
        "trialDbId": "bridge",
        "trialName": "BRIDGE core1000"
      }
    ]
  }
}
```

### GET /studies/{studyDbId}

**Supported Parameters**

| Data Type   | Parameter Name |Description                     |
| ----------- | -------------- |------------------------------- |
| string      | studyDbId      | The internal study identifier. |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1000,
      "totalCount": 1,
      "totalPages": 1
    },
    "status": [
      {
        "message": "Success",
        "messageType": "INFO"
      }
    ],
    "datafiles": []
  },
  "result": {
    "active": null,
    "additionalInfo": null,
    "commonCropName": null,
    "contacts": null,
    "culturalPractices": null,
    "dataLinks": null,
    "documentationURL": null,
    "endDate": null,
    "environmentParameters": null,
    "experimentalDesign": null,
    "externalReferences": null,
    "growthFacility": null,
    "lastUpdate": null,
    "license": null,
    "locationDbId": null,
    "locationName": null,
    "observationLevels": null,
    "observationUnitsDescription": null,
    "observationVariableDbIds": null,
    "seasons": null,
    "startDate": null,
    "studyCode": null,
    "studyDbId": "Barley Spike Investigation",
    "studyDescription": null,
    "studyName": "Barley Spike Investigation",
    "studyPUI": null,
    "studyType": null,
    "trialDbId": "bridge",
    "trialName": "BRIDGE core1000"
  }
}
```
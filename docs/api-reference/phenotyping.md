# Phenotyping Module

## Observation Units

### GET /observationunits

**Supported Parameters**

| Data Type   | Parameter Name |Description                                                                                                                           |
| ----------- | -------------- |------------------------------------------------------------------------------------------------------------------------------------- |
| integer     | page           | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer     | pageSize       | The size of the pages to be returned. Default is `1000`.                                                                             |
| string     | germplasmDbId   | Use this parameter to only return results associated with the given Germplasm unique identifier. Use `GET /germplasm` to find the list of available Germplasm on a server.|

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1,
      "totalCount": 996,
      "totalPages": null
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
        "additionalInfo": null,
        "crossDbId": null,
        "crossName": null,
        "externalReferences": null,
        "germplasmDbId": "HOR 4402",
        "germplasmName": "HOR 4402",
        "locationDbId": null,
        "locationName": null,
        "observationUnitDbId": "HOR 4402_1105630",
        "observationUnitName": "HOR 4402_1105630",
        "observationUnitPUI": null,
        "observationUnitPosition": null,
        "observations": null,
        "programDbId": null,
        "programName": null,
        "seedLotDbId": null,
        "seedLotName": null,
        "studyDbId": "Barley Spike Investigation",
        "studyName": "Barley Spike Investigation",
        "treatments": null,
        "trialDbId": "bridge",
        "trialName": "BRIDGE core1000"
      }
    ]
  }
}
```

### GET /observationunits/{observationUnitDbId}

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
      "pageSize": 1,
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
    "additionalInfo": null,
    "crossDbId": null,
    "crossName": null,
    "externalReferences": null,
    "germplasmDbId": "HOR 4402",
    "germplasmName": "HOR 4402",
    "locationDbId": null,
    "locationName": null,
    "observationUnitDbId": "HOR 4402_1105630",
    "observationUnitName": "HOR 4402_1105630",
    "observationUnitPUI": null,
    "observationUnitPosition": null,
    "observations": null,
    "programDbId": null,
    "programName": null,
    "seedLotDbId": null,
    "seedLotName": null,
    "studyDbId": "Barley Spike Investigation",
    "studyName": "Barley Spike Investigation",
    "treatments": null,
    "trialDbId": "bridge",
    "trialName": "BRIDGE core1000"
  }
}
```

## Observation Variables

### GET /variables

**Supported Parameters**

| Data Type   | Parameter Name |Description                                                                                                                           |
| ----------- | -------------- |------------------------------------------------------------------------------------------------------------------------------------- |
| integer     | page           | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer     | pageSize       | The size of the pages to be returned. Default is `1000`.                                                                             |
| string     | observationVariableDbId | Variable's unique ID |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1,
      "totalCount": 15,
      "totalPages": 15
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
        "additionalInfo": null,
        "commonCropName": null,
        "contextOfUse": null,
        "defaultValue": null,
        "documentationURL": null,
        "externalReferences": null,
        "growthStage": null,
        "institution": null,
        "language": null,
        "method": {
          "additionalInfo": null,
          "bibliographicalReference": null,
          "description": null,
          "externalReferences": null,
          "formula": null,
          "methodClass": null,
          "methodDbId": "Row-Type Estimation",
          "methodName": null,
          "methodPUI": null,
          "ontologyReference": null
        },
        "observationVariableDbId": "CONVAR",
        "observationVariableName": "Row-Type convarity",
        "observationVariablePUI": null,
        "ontologyReference": null,
        "scale": {
          "additionalInfo": null,
          "dataType": "Nominal",
          "decimalPlaces": null,
          "externalReferences": null,
          "ontologyReference": null,
          "scaleDbId": "1to5RowType",
          "scaleName": null,
          "scalePUI": null,
          "units": null,
          "validValues": {
            "categories": [
              {
                "label": "'convar. distichon'",
                "value": "1"
              },
              {
                "label": "'convar. deficiens'",
                "value": "2"
              },
              {
                "label": "'convar. labile'",
                "value": "3"
              },
              {
                "label": "'convar. intermedium'",
                "value": "4"
              },
              {
                "label": "'convar. vulgare/convar. hexastichon'",
                "value": "5"
              }
            ],
            "maximumValue": null,
            "minimumValue": null
          }
        },
        "scientist": null,
        "status": null,
        "submissionTimestamp": null,
        "synonyms": null,
        "trait": {
          "additionalInfo": null,
          "alternativeAbbreviations": null,
          "attribute": null,
          "attributePUI": null,
          "entity": null,
          "entityPUI": null,
          "externalReferences": null,
          "mainAbbreviation": null,
          "ontologyReference": null,
          "status": null,
          "synonyms": null,
          "traitClass": "morphological",
          "traitDbId": "Row-Type convarity",
          "traitDescription": null,
          "traitName": null,
          "traitPUI": null
        }
      }
    ]
  }
}
```

### GET /variables/{observationVariableDbId}

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
      "pageSize": 0,
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
    "additionalInfo": null,
    "commonCropName": null,
    "contextOfUse": null,
    "defaultValue": null,
    "documentationURL": null,
    "externalReferences": null,
    "growthStage": null,
    "institution": null,
    "language": null,
    "method": {
      "additionalInfo": null,
      "bibliographicalReference": null,
      "description": null,
      "externalReferences": null,
      "formula": null,
      "methodClass": null,
      "methodDbId": "Row-Type Estimation",
      "methodName": null,
      "methodPUI": null,
      "ontologyReference": null
    },
    "observationVariableDbId": "CONVAR",
    "observationVariableName": "Row-Type convarity",
    "observationVariablePUI": null,
    "ontologyReference": null,
    "scale": {
      "additionalInfo": null,
      "dataType": "Nominal",
      "decimalPlaces": null,
      "externalReferences": null,
      "ontologyReference": null,
      "scaleDbId": "1to5RowType",
      "scaleName": null,
      "scalePUI": null,
      "units": null,
      "validValues": {
        "categories": [
          {
            "label": "'convar. distichon'",
            "value": "1"
          },
          {
            "label": "'convar. deficiens'",
            "value": "2"
          },
          {
            "label": "'convar. labile'",
            "value": "3"
          },
          {
            "label": "'convar. intermedium'",
            "value": "4"
          },
          {
            "label": "'convar. vulgare/convar. hexastichon'",
            "value": "5"
          }
        ],
        "maximumValue": null,
        "minimumValue": null
      }
    },
    "scientist": null,
    "status": null,
    "submissionTimestamp": null,
    "synonyms": null,
    "trait": {
      "additionalInfo": null,
      "alternativeAbbreviations": null,
      "attribute": null,
      "attributePUI": null,
      "entity": null,
      "entityPUI": null,
      "externalReferences": null,
      "mainAbbreviation": null,
      "ontologyReference": null,
      "status": null,
      "synonyms": null,
      "traitClass": "morphological",
      "traitDbId": "Row-Type convarity",
      "traitDescription": null,
      "traitName": null,
      "traitPUI": null
    }
  }
}
```

## Observations

### GET /observations

**Supported Parameters**

| Data Type | Parameter Name |Description |
| -- | -- | -- |
| integer | page | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer | pageSize | The size of the pages to be returned. Default is `1000`. |
| string | studyDbId | Use this parameter to only return results associated with the given Study unique identifier. Use `GET /studies` to find the list of available Studies on a server. |
| string | germplasmDbId | Use this parameter to only return results associated with the given Germplasm unique identifier. Use `GET /germplasm` to find the list of available Germplasm on a server. |
| string | observationUnitDbId | The unique ID of an Observation Unit |
| string | observationVariableDbId | The unique ID of an observation variable |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1,
      "totalCount": 14925,
      "totalPages": 14925
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
        "additionalInfo": null,
        "collector": null,
        "externalReferences": null,
        "geoCoordinates": null,
        "germplasmDbId": "HOR 4402",
        "germplasmName": "HOR 4402",
        "observationDbId": "HOR 4402_1105630-SPIKE_LENGTH-Tue Sep 20 00:00:00 UTC 2016",
        "observationTimeStamp": "2016-09-20T00:00:00+00:00",
        "observationUnitDbId": "HOR 4402_1105630",
        "observationUnitName": null,
        "observationVariableDbId": "SPIKE_LENGTH",
        "observationVariableName": "Spike length",
        "season": null,
        "studyDbId": "Barley Spike Investigation",
        "studyName": "Barley Spike Investigation",
        "uploadedBy": null,
        "value": "9.0"
      }
    ]
  }
}
```

### GET /observations/{observationDbId}

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
      "pageSize": 1,
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
    "additionalInfo": null,
    "collector": null,
    "externalReferences": null,
    "geoCoordinates": null,
    "germplasmDbId": null,
    "germplasmName": null,
    "observationDbId": "HOR 4402_1105630-SPIKE_LENGTH-Tue Sep 20 00:00:00 UTC 2016",
    "observationTimeStamp": "2016-09-20T00:00:00+00:00",
    "observationUnitDbId": "HOR 4402_1105630",
    "observationUnitName": null,
    "observationVariableDbId": "SPIKE_LENGTH",
    "observationVariableName": null,
    "season": null,
    "studyDbId": null,
    "studyName": null,
    "uploadedBy": null,
    "value": "9.0"
  }
}
```

### GET /observations/table

**Supported Parameters**

| Data Type   | Parameter Name |Description                                                                                                                           |
| ----------- | -------------- |------------------------------------------------------------------------------------------------------------------------------------- |
| integer     | page           | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer     | pageSize       | The size of the pages to be returned. Default is `1000`.                                                                             |
| string     | studyDbId       | Use this parameter to only return results associated with the given Study unique identifier. Use `GET /studies` to find the list of available Studies on a server. |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1,
      "totalCount": 15,
      "totalPages": 15
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
      [
        "HOR 4402_1105630",
        "2016-09-20T00:00:00+00:00",
        "9.0",
        "1.0",
        "1.0",
        "3.0",
        "3.0",
        "2.0",
        "1.0",
        "18.5",
        "2.0",
        "1.0",
        "1.0",
        "5.0",
        "1.0",
        "None",
        "3.0"
      ]
    ],
    "headerRow": [
      "observationUnitDbId",
      "observationTimeStamp"
    ],
    "observationVariables": [
      {
        "observationVariableDbId": "SPIKE_LENGTH",
        "observationVariableName": "Spike length"
      },
      {
        "observationVariableDbId": "RACHILLA_HAIRS",
        "observationVariableName": "Rachilla hairs"
      },
      {
        "observationVariableDbId": "GLUME_COLOR",
        "observationVariableName": "Color of glumes"
      },
      {
        "observationVariableDbId": "AWNS_LATERAL",
        "observationVariableName": "Awns lateral spikelets"
      },
      {
        "observationVariableDbId": "SPIKE_DENSITY",
        "observationVariableName": "Spike density"
      },
      {
        "observationVariableDbId": "SPIKE_BRITTLENESS",
        "observationVariableName": "Spike brittleness"
      },
      {
        "observationVariableDbId": "AWNS_GLUMES",
        "observationVariableName": "Awns on glumes"
      },
      {
        "observationVariableDbId": "AWNS_LENGTH",
        "observationVariableName": "Awns length "
      },
      {
        "observationVariableDbId": "AWNS_ROUGHNESS",
        "observationVariableName": "Awns roughness"
      },
      {
        "observationVariableDbId": "GRAIN_HULL",
        "observationVariableName": "Grain hull / Cover of caryopses"
      },
      {
        "observationVariableDbId": "SPIKE_BRANCHING",
        "observationVariableName": "Spike branching"
      },
      {
        "observationVariableDbId": "CONVAR",
        "observationVariableName": "Row-Type convarity"
      },
      {
        "observationVariableDbId": "WIDTH_GLUMES",
        "observationVariableName": "Glume width"
      },
      {
        "observationVariableDbId": "GRAIN_COLOR",
        "observationVariableName": "Color of naked seeds"
      },
      {
        "observationVariableDbId": "AWNS_CENTRAL",
        "observationVariableName": "Awns central spikelets"
      }
    ]
  }
}
```


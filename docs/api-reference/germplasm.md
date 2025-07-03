# Germplasm Module

## Germplasm

### GET /germplasm

**Supported Parameters**

| Data Type   | Parameter Name |Description                                                                                                                           |
| ----------- | -------------- |------------------------------------------------------------------------------------------------------------------------------------- |
| integer     | page           | Used to request a specific page of data to be returned. The page indexing starts at 0 (the first page is 'page'= 0). Default is `0`. |
| integer     | pageSize       | The size of the pages to be returned. Default is `1000`.                                                                             |
| string      | germplasmDbId  | Use this parameter to only return results associated with the given Germplasm unique identifier. Use `GET /germplasm` to find the list of available Germplasm on a server. |
| string      | germplasmName  | Use this parameter to only return results associated with the given Germplasm by its human readable name. Use `GET /germplasm` to find the list of available Germplasm on a server. |

**Example Response**

```json linenums="1" title="Response Code 200"
{
  "metadata": {
    "pagination": {
      "currentPage": 0,
      "pageSize": 1,
      "totalCount": 1000,
      "totalPages": 1000
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
        "accessionNumber": null,
        "acquisitionDate": null,
        "additionalInfo": null,
        "biologicalStatusOfAccessionCode": null,
        "biologicalStatusOfAccessionDescription": null,
        "breedingMethodDbId": null,
        "breedingMethodName": null,
        "collection": null,
        "commonCropName": null,
        "countryOfOriginCode": null,
        "defaultDisplayName": null,
        "documentationURL": null,
        "donors": null,
        "externalReferences": null,
        "genus": "Hordeum",
        "germplasmDbId": "HOR 4402",
        "germplasmName": "HOR 4402",
        "germplasmOrigin": [
          {
            "coordinatesUncertainty": null,
            "coordinates": {
              "geometry": {
                "coordinates": [
                  21.6163888888888,
                  40.6830555555555
                ],
                "type": "Point"
              },
              "type": "Feature"
            }
          }
        ],
        "germplasmPUI": null,
        "germplasmPreprocessing": null,
        "instituteCode": null,
        "instituteName": null,
        "pedigree": null,
        "seedSource": null,
        "seedSourceDescription": "Internal seed lot ID of the IPK LIMS system",
        "species": "vulgare",
        "speciesAuthority": null,
        "storageTypes": null,
        "subtaxa": "vulgare",
        "subtaxaAuthority": null,
        "synonyms": null,
        "taxonIds": null
      }
    ]
  }
}
```

### GET /germplasm/{germplasmDbId}

**Supported Parameters**

| Data Type   | Parameter Name     | Description                        |
| ----------- | ------------------ | ---------------------------------- |
| string      | germplasmDbId      | The internal germplasm identifier. |


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
    "accessionNumber": null,
    "acquisitionDate": null,
    "additionalInfo": null,
    "biologicalStatusOfAccessionCode": null,
    "biologicalStatusOfAccessionDescription": null,
    "breedingMethodDbId": null,
    "breedingMethodName": null,
    "collection": null,
    "commonCropName": null,
    "countryOfOriginCode": null,
    "defaultDisplayName": null,
    "documentationURL": null,
    "donors": null,
    "externalReferences": null,
    "genus": null,
    "germplasmDbId": "HOR 4402",
    "germplasmName": null,
    "germplasmOrigin": null,
    "germplasmPUI": null,
    "germplasmPreprocessing": null,
    "instituteCode": null,
    "instituteName": null,
    "pedigree": null,
    "seedSource": null,
    "seedSourceDescription": null,
    "species": null,
    "speciesAuthority": null,
    "storageTypes": null,
    "subtaxa": null,
    "subtaxaAuthority": null,
    "synonyms": null,
    "taxonIds": null
  }
}
```
from typing import Annotated
from fastapi import APIRouter, Query
from resources import responses, schemas
from brapi.parameters import CommonsDep
import math
import dataload
from icecream import ic

router = APIRouter(
    prefix="/brapi/v2"
)

@router.get("/germplasm", response_model=responses.Response[schemas.Germplasm])
def get_germplasm(commons: CommonsDep, accessionNumber: Annotated[str|None, Query(description="test")] = None, germplasmDbId: str|None = None, genus: str|None = None, species: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 0

    results = []
    for _,biologicalMaterial in dataload.miappe.study.iterrows():
        totalCount+=1
        if(len(results)<pageSize and totalCount-1>=page*pageSize):
            origin = None
            if 'Characteristics[''Biological Material Latitude'']' in dataload.miappe.study.keys() and 'Characteristics[''Biological Material Longitude'']' in dataload.miappe.study.keys():
                coordinates = [
                    biologicalMaterial['Characteristics[''Biological Material Latitude'']'],
                    biologicalMaterial['Characteristics[''Biological Material Longitude'']']
                ]
                if 'Characteristics[''Biological Material Altitude'']' in dataload.miappe.study.keys():
                    coordinates.append(biologicalMaterial['Characteristics[''Biological Material Altitude'']'])
                origin = schemas.Origin(
                    coordinateUncertainty=biologicalMaterial['Characteristics[''Biological Material Coordinate Uncertainty'']']
                        if 'Characteristics[''Biological Material Coordinate Uncertainty'']' in dataload.miappe.study.keys()
                        else None,
                    coordinates=schemas.GeoCoordinates(
                        type='Feature',
                        geometry=schemas.Geometry(
                            coordinates=coordinates,
                            type='Point'
                        )
                    )
                )
            donors = None
            if 'Characteristics[''Material Source ID'']' in dataload.miappe.study.keys():
                donors=[schemas.Donor(
                    donorAccessionNumber=biologicalMaterial['Characteristics[''Material Source ID'']']
                )]
            results.append(schemas.Germplasm(
                accessionNumber=biologicalMaterial['Source Name'],
                genus=biologicalMaterial['Characteristics[''Genus'']']
                    if 'Characteristics[''Genus'']' in dataload.miappe.study.keys()
                    else None,
                species=biologicalMaterial['Characteristics[''Species'']']
                    if 'Characteristics[''Species'']' in dataload.miappe.study.keys()
                    else None,
                subtaxa=biologicalMaterial['Characteristics[''Infraspecific Name'']']
                    if 'Characteristics[''Infraspecific Name'']' in dataload.miappe.study.keys()
                    else None,
                germplasmOrigin=[origin],
                germplasmDbId=biologicalMaterial['Source Name'],
                germplasmName=biologicalMaterial['Source Name'],
                germplasmPreprocessing=biologicalMaterial['Characteristics[''Biological Material Preprocessing'']'] 
                    if 'Characteristics[''Biological Material Preprocessing'']' in dataload.miappe.study.keys() 
                    else None,
                donors=donors,
                seedSourceDescription=biologicalMaterial['Characteristics[''Material Source Description'']']
                    if 'Characteristics[''Material Source Description'']' in dataload.miappe.study.keys()
                    else None,
                storageTypes=None,
                germplasmPUI='',
                commonCropName='',
            ))

    pagination = schemas.Pagination(
        currentPage=page,
        pageSize=pageSize,
        totalCount=totalCount,
        totalPages=math.ceil(totalCount/pageSize)
    )
    return responses.Response(
        metadata=schemas.Metadata(
            datafiles=[],
            pagination=pagination,
            status=[schemas.Status(message="Request accepted, response successful", messageType="INFO")]
        ),
        result=responses.Result(
            data=results
        )
    )
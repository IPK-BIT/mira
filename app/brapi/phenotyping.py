from typing import Annotated
from fastapi import APIRouter, Depends, status
from resources import schemas, responses
import math
import pandas as pd

import dataload

from icecream import ic

async def common_parameters(page: int|None = None, pageSize: int|None = None):
    return {"page": page, "pageSize": pageSize}

CommonsDep = Annotated[dict, Depends(common_parameters)]

router = APIRouter(
    prefix="/brapi/v2"
)

@router.get("/observations", response_model=responses.Response[schemas.Observation], response_model_exclude_none=True)
def get_observations(commons: CommonsDep, germplasmDbId: str|None = None, observationUnitDbId: str|None = None, observationVariableDbId: str|None = None):
    #TODO Check if pagination is valid (cf. request page above total page count)
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 0
    
    tmp = pd.merge(dataload.miappe.datafile, pd.merge(dataload.miappe.assay, dataload.miappe.study, on="Sample Name"), on="Assay Name")
    try:
        observationVariableDbIds = observationVariableDbId.split(',')
    except:
        observationVariableDbIds = []
    try:
        tmp = tmp.loc[tmp["Source Name"].isin(germplasmDbId.split(','))]
    except:
        None
    try:
        tmp = tmp.loc[tmp["Assay Name"].isin(observationUnitDbId.split(','))]
    except:
        None
    results = []
    
    for _, row in tmp.iterrows():
        for _, trait in dataload.miappe.traitdefinitionfile.iterrows():
            if (len(observationVariableDbIds)==0 or trait["Variable ID"] in observationVariableDbIds):
                totalCount+=1
                if(len(results)<pageSize and totalCount-1>=page*pageSize):
                    try:
                        germplasmName = row["Characteristics[Material Source ID]"]
                    except:
                        germplasmName = None
                    try: 
                        observationTimeStamp = row["Date"]
                    except:
                        observationTimeStamp = None
                    results.append(schemas.Observation(
                        germplasmDbId           = row["Source Name"],
                        germplasmName           = germplasmName,
                        observationDbId         = row["Assay Name"]+"."+trait["Variable ID"],
                        observationTimeStamp    = observationTimeStamp,
                        observationUnitDbId     = row["Assay Name"],
                        observationUnitName     = row["Assay Name"],
                        observationVariableDbId = trait["Variable ID"],
                        observationVariableName = trait["Trait"],
                        studyDbId               = dataload.miappe.investigation["Study Identifier"][0],
                        value                   = str(row[trait["Variable ID"]])
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

@router.get("/observationunits", response_model=responses.Response[schemas.ObservationUnit], response_model_exclude_none=True)
def get_observationunits(commons: CommonsDep):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 0
    
    results=[]
    for _,observationUnit in dataload.miappe.assay.iterrows():
        totalCount+=1
        sample = None
        for _,studySample in dataload.miappe.study.iterrows():
            if sample is not None:
                break
            if studySample["Sample Name"]==observationUnit["Sample Name"]:
                sample=studySample
        #ic(sample)
        results.append(schemas.ObservationUnit(
            observationUnitDbId = observationUnit["Assay Name"],
            germplasmDbId       = sample["Source Name"],
            germplasmName       = sample["Characteristics[Infraspecific name]"],
            studyDbId           = dataload.miappe.investigation["Study Identifier"][0]
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

@router.get("/variables", response_model=responses.Response[schemas.ObservationVariable], response_model_exclude_none=True)
def get_variables(commons: CommonsDep, observationVariableDbId: str|None = None, methodName: str|None = None, traitName: str|None = None, scaleName: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 0
    try:
        observationVariableDbIds = observationVariableDbId.split(',')
    except:
        observationVariableDbIds = []
    try:
        methodNames = methodName.split(',')
    except:
        methodNames = []
    try:
        traitNames = traitName.split(',')
    except:
        traitNames = []
    try:
        scaleNames = scaleName.split(',')
    except:
        scaleNames = []
    results=[]
    for _, trait in dataload.miappe.traitdefinitionfile.iterrows():
        if len(observationVariableDbIds)>0 and trait["Variable ID"] not in observationVariableDbIds:
            break
        if len(methodNames)>0 and trait["Method"] not in methodNames:
            break
        if len(traitNames)>0 and trait["Trait"] not in traitNames:
            break
        if len(scaleNames)>0 and trait["Scale"] not in scaleNames:
            break
        try:
            traitOntology = schemas.Ontology(
                ontologyDbId=trait["Trait Source REF"],
                documentationLinks=[schemas.OntologyAnnotation(
                    URL=trait["Trait Accession Number"]
                )]
            )
        except:
            traitOntology = None
        try:
            methodOntology = schemas.Ontology(
                ontologyDbId=trait["Method Source REF"],
                documentationLinks=[schemas.OntologyAnnotation(
                    URL=trait["Method Accession Number"]
                )]
            )
        except:
            methodOntology = None
        try:
            scaleOntology = schemas.Ontology(
                ontologyDbId=trait["Scale Source REF"],
                documentationLinks=[schemas.OntologyAnnotation(
                    URL=trait["Scale Accession Number"]
                )]
            )
        except:
            scaleOntology = None

        valueRange = None
        unit = None
        if trait["Scale Type"] in ['nominal', 'ordinal']:
            valueRange = schemas.ValueRange(
                categories=[]
            )
            for value in trait["Method Description"].split(','):
                annotation = value.split(':')
                valueRange.categories.append(schemas.ValueAnnotation(
                    label=annotation[1][1:-1],
                    value=annotation[0]
                ))
        elif trait["Scale Type"] in ["numerical"]:
            unit = trait["Method Description"]

        totalCount+=1
        if(len(results)<pageSize and totalCount-1>=page*pageSize):
            results.append(schemas.ObservationVariable(
                observationVariableDbId=trait["Variable ID"],
                method=schemas.Method(
                    methodName=trait["Method"],
                    ontologyReference=methodOntology
                ),
                trait=schemas.Trait(
                    traitName=trait["Trait"],
                    ontologyReference=traitOntology
                ),
                scale=schemas.Scale(
                    scaleName=trait["Scale"],
                    validValues=valueRange,
                    dataType=trait["Scale Type"],
                    units=unit,
                    ontologyReference=scaleOntology
                )
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

@router.get("/events", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_events():
    return {
        "message": "not implemented"
    }
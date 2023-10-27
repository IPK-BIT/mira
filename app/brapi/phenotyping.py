from fastapi import APIRouter, status, Request
from resources import schemas, responses
from brapi.parameters import CommonsDep
import math
import pandas as pd
from dateutil import parser

import dataload

from icecream import ic

router = APIRouter(
    prefix="/brapi/v2"
)

@router.get("/observations", response_model=responses.Response[schemas.Observation])
def get_observations(commons: CommonsDep, germplasmDbId: str|None = None, observationUnitDbId: str|None = None, observationVariableDbId: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    results=[]

    df = pd.melt(dataload.miappe.datafile, id_vars=dataload.miappe.datafile.keys()[0:3],value_vars=dataload.miappe.datafile.keys()[3:], var_name='Variable ID')
    units = pd.merge(dataload.miappe.assay, dataload.miappe.study, on="Sample Name")
    if germplasmDbId:
        units = units.loc[units['Source Name'].isin(germplasmDbId.split(','))]
    if observationUnitDbId:
        units = units.loc[units['Assay Name'].isin(observationUnitDbId.split(','))]
    variables = dataload.miappe.traitdefinitionfile
    if observationVariableDbId:
        variables = variables.loc[variables['Variable ID'].isin(observationVariableDbId.split(','))]
    
    records = pd.merge(variables, pd.merge(df, units, on='Assay Name'), on='Variable ID').sort_values(by=['Assay Name', 'Variable ID'])
    totalCount=len(records)
    records = records.iloc[page*pageSize:page*pageSize+pageSize]

    for _, record in records.iterrows():
        results.append(schemas.Observation(
                    germplasmDbId=record['Source Name'],
                    germplasmName=record['Characteristics[''Material Source ID'']']
                        if 'Characteristics[''Material Source ID'']' in record.keys()
                        else None,
                    observationDbId=record['Assay Name']+'.'+record['Variable ID'],
                    observationTimeStamp = parser.parse(record['Date']).strftime("%Y-%m-%dT%H:%M:%SZ")
                        if 'Date' in record.keys()
                        else None,
                    observationUnitDbId=record['Assay Name'],
                    observationUnitName=record['Assay Name'],
                    observationVariableDbId = record['Variable ID'],
                    observationVariableName = record['Variable Name'],
                    studyDbId=dataload.miappe.investigation['Study Identifier'][0],
                    value=str(record['value'])
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

# @router.get('/observations/table', response_model=responses.Response[schemas.Table], deprecated=True)
# async def get_observations_as_table():
#     return

@router.get("/observationunits", response_model=responses.Response[schemas.ObservationUnit])
def get_observationunits(commons: CommonsDep, observationUnitDbId: str|None = None, observationUnitLevelName: str|None = None, germplasmDbId: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 0
    
    results=[]
    records = pd.merge(dataload.miappe.assay, dataload.miappe.study, on="Sample Name")
    if observationUnitDbId:
        records = records.loc[records['Assay Name'].isin(observationUnitDbId.split(','))]
    if observationUnitLevelName:
        records = records.loc[records['Characteristics[''Observation Unit Type'']'].isin(observationUnitLevelName.split(','))]
    if germplasmDbId:
        records = records.loc[records['Source Name'].isin(germplasmDbId.split(','))]
    totalCount=len(records)
    records = records.iloc[page*pageSize:page*pageSize+pageSize]
    for _, observationUnit in records.iterrows():
        results.append(schemas.ObservationUnit(
            observationUnitDbId = observationUnit['Assay Name'],
            observationUnitName=observationUnit['Assay Name'],
            germplasmDbId=observationUnit['Source Name'],
            germplasmName=observationUnit['Source Name'],
            observationUnitPosition=schemas.ObservationUnitPosition(
                observationLevel=schemas.ObservationLevel(
                    levelName=observationUnit['Characteristics[''Observation Unit Type'']']
                        if 'Characteristics[''Observation Unit Type'']' in records.keys()
                        else None
                )
            ),
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

@router.get("/variables2", response_model=responses.Response[schemas.ObservationVariable])
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
        if trait["Scale Type"] in ['Nominal', 'Ordinal']:
            valueRange = schemas.ValueRange(
                categories=[]
            )
            for value in trait["Method Description"].split(','):
                annotation = value.split(':')
                valueRange.categories.append(schemas.ValueAnnotation(
                    label=annotation[1][1:-1],
                    value=annotation[0]
                ))
        elif trait["Scale Type"] in ["Numerical"]:
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
                    scaleName=trait["Scale"] if type(trait["Scale"])==str else None,
                    validValues=valueRange,
                    dataType=trait["Scale Type"] if type(trait["Scale Type"])==str else None,
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

@router.get("/variables", response_model=responses.Response[schemas.ObservationVariable])
def get_variables(commons: CommonsDep, observationVariableDbId: str|None = None, methodName: str|None = None, traitName: str|None = None, scaleName: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    
    records = dataload.miappe.traitdefinitionfile
    if observationVariableDbId:
        records = records.loc[records['Variable ID'].isin(observationVariableDbId.split(','))]
    if methodName:
        records = records.loc[records['Method'].isin(methodName.split(','))]
    if traitName:
        records = records.loc[records['Trait'].isin(traitName.split(','))]
    if scaleName:
        records = records.loc[records['Scale'].isin(scaleName.split(','))]
    totalCount=len(records)
    records = records.iloc[page*pageSize:page*pageSize+pageSize]

    results=[]
    for _, record in records.iterrows():
        try:
            traitOntology = schemas.Ontology(
                ontologyDbId=record["Trait Source REF"],
                documentationLinks=[schemas.OntologyAnnotation(
                    URL=record["Trait Accession Number"]
                )]
            )
        except:
            traitOntology = None
        try:
            methodOntology = schemas.Ontology(
                ontologyDbId=record["Method Source REF"],
                documentationLinks=[schemas.OntologyAnnotation(
                    URL=record["Method Accession Number"]
                )]
            )
        except:
            methodOntology = None
        try:
            scaleOntology = schemas.Ontology(
                ontologyDbId=record["Scale Source REF"],
                documentationLinks=[schemas.OntologyAnnotation(
                    URL=record["Scale Accession Number"]
                )]
            )
        except:
            scaleOntology = None

        valueRange = None
        unit = None
        if record["Scale Type"] in ['Nominal', 'Ordinal']:
            valueRange = schemas.ValueRange(
                categories=[]
            )
            for value in record["Method Description"].split(','):
                annotation = value.split(':')
                valueRange.categories.append(schemas.ValueAnnotation(
                    label=annotation[1][1:-1],
                    value=annotation[0]
                ))
        elif record["Scale Type"] in ["Numerical"]:
            unit = record["Method Description"]

        results.append(schemas.ObservationVariable(
            observationVariableDbId=record["Variable ID"],
            method=schemas.Method(
                methodName=record["Method"],
                ontologyReference=methodOntology
            ),
            trait=schemas.Trait(
                traitName=record["Trait"],
                ontologyReference=traitOntology
            ),
            scale=schemas.Scale(
                scaleName=record["Scale"] if type(record["Scale"])==str else None,
                validValues=valueRange,
                dataType=record["Scale Type"] if type(record["Scale Type"])==str else None,
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
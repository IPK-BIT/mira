from fastapi import APIRouter, status
import dataload
from resources import responses, schemas
from brapi.parameters import CommonsDep
import math
from icecream import ic
from dateutil import parser

router = APIRouter(
    prefix="/brapi/v2"
)

@router.get('/serverinfo', response_model=responses.ServerInfoResponse, response_model_exclude_none=True)
def get_server_info():
    return responses.ServerInfoResponse(
        metadata=schemas.Metadata(
            datafiles=[],
            pagination=schemas.Pagination(
                currentPage = 0,
                pageSize    = 1000,
                totalCount  = 1,
                totalPages  = 1
            ),
            status=[
                schemas.Status(
                    message     = "Request accepted, response successful",
                    messageType = "INFO"
                )
            ]
        ),
        result=schemas.ServerInfo(
            calls=[
                schemas.Call(
                    contentTypes    = ["application/json"],
                    methods         = ["GET"],
                    service         = "observations",
                    versions        = ["2.1"]
                ),
                schemas.Call(
                    contentTypes    = ["application/json"],
                    methods         = ["GET"],
                    service         = "variables",
                    versions        = ["2.1"]
                ),
                schemas.Call(
                    contentTypes    = ["application/json"],
                    methods         = ["GET"],
                    service         = "observationunits",
                    versions        = ["2.1"]
                ),
                schemas.Call(
                    contentTypes    = ["application/json"],
                    methods         = ["GET"],
                    service         = "germplasm",
                    versions        = ["2.1"]
                ),
                schemas.Call(
                    contentTypes    = ["application/json"],
                    methods         = ["GET"],
                    service         = "trials",
                    versions        = ["2.1"]
                ),
                schemas.Call(
                    contentTypes    = ["application/json"],
                    methods         = ["GET"],
                    service         = "studies",
                    versions        = ["2.1"]
                ),
            ],
            contactEmail        = dataload.config['contact']['mail'],
            documentationURL    = dataload.config['server']['documentation'],
            location            = dataload.config['contact']['organization']['location'],
            organizationName    = dataload.config['contact']['organization']['name'],
            organizationURL     = dataload.config['contact']['organization']['url'],
            serverDescription   = dataload.config['server']['description'],
            serverName          = dataload.config['server']['name']
        )
    )

@router.get("/trials", response_model=responses.Response[schemas.Trial])
def get_trials(commons: CommonsDep):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 1
    results=[schemas.Trial(
        additionalInfo={"MIAPPE version": dataload.miappe.investigation['Comment[''MIAPPE version'']'][0]},
        datasetAuthorships=[schemas.Dataset(
            submissionDate=dataload.miappe.investigation['Investigation Submission Date'][0] 
                if 'Investigation Submission Date' in dataload.miappe.investigation.keys() 
                else None,
            publicReleaseDate=dataload.miappe.investigation['Investigation Public Release Date'][0] 
                if 'Investigation Public Release Date' in dataload.miappe.investigation.keys() 
                else None,
            license=dataload.miappe.investigation['Comment[''License'']'][0] 
                if 'Comment[''License'']' in dataload.miappe.investigation.keys() 
                else None
        )],
        publications=[schemas.Publication(
            publicationPUI=dataload.miappe.investigation['Investigation Publication DOI'][0] 
                if 'Investigation Publication DOI' in dataload.miappe.investigation.keys() 
                else None,
        )],
        trialDbId=dataload.miappe.investigation['Investigation Identifier'][0],
        trialName=dataload.miappe.investigation['Investigation Title'][0],
        trialDescription=dataload.miappe.investigation['Investigation Description'][0],
    )]
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
    
@router.get("/studies", response_model=responses.Response[schemas.Study])
def get_studies(commons: CommonsDep):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 1000
    totalCount = 1
    #TODO: Extend to multi study
    results=[schemas.Study(
        studyDbId=dataload.miappe.investigation['Study Identifier'][0],
        studyName=dataload.miappe.investigation['Study Title'][0],
        studyDescription=dataload.miappe.investigation['Study Descritpion'][0]
            if 'Study Description' in dataload.miappe.investigation.keys()
            else None,
        startDate=parser.parse(dataload.miappe.investigation['Comment[''Study Start Date'']'][0]).strftime("%Y-%m-%dT%H:%M:%SZ")
            if 'Comment[''Study Start Date'']' in dataload.miappe.investigation.keys()
            else None,
        endDate=parser.parse(dataload.miappe.investigation['Comment[''Study End Date'']'][0]).strftime("%Y-%m-%dT%H:%M:%SZ")
            if 'Comment[''Study End Date'']' in dataload.miappe.investigation.keys()
            else None
    )]
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
    
@router.get("/locations", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_locations():
    return {
        "message": "not implemented"
    }
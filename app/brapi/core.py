from fastapi import APIRouter, status
import dataload
from resources import responses, schemas

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

@router.get("/trials", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_trials():
    return {
        "message": "not implemented"
    }
    
@router.get("/studies", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_studies():
    return {
        "message": "not implemented"
    }
    
@router.get("/locations", status_code=status.HTTP_501_NOT_IMPLEMENTED, deprecated=True)
def get_locations():
    return {
        "message": "not implemented"
    }
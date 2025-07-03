from litestar import Controller, get
from math import ceil
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas import response
from db.models.models import Study as DbStudy
from db.schemas.core import Study

class StudyController(Controller):
    path="/studies"

    @get('/')
    async def get_all_studies(self, transaction: AsyncSession, pageSize: int|None = None, page: int|None = None) -> response.Response[Study]: 
        if not pageSize:
            pageSize = 1000
        if not page:
            page = 0
        
        query = select(DbStudy)
        query_results = (await transaction.execute(query)).scalars().all()
        total_count = len(query_results)

        query = query.offset(page * pageSize).limit(pageSize)
        query_results = (await transaction.execute(query)).scalars().all()

        result = []
        for s in query_results:
            result.append(Study(
                studyDbId=s.studyDbId,
                studyName=s.studyName,
                # studyDescription=s.studyDescription,
                # startDate=s.startDate,
                # endDate=s.endDate,
                # instituteName=s.instituteName,
                # locationName=s.locationName,
                trialDbId=s.trialDbId,
                trialName=s.trialName,
            ))

        return response.Response(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    totalCount=total_count,
                    totalPages=ceil(total_count/pageSize),
                    pageSize=pageSize,
                    currentPage=page,
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[],
            ),
            result=response.Result(data=result)
        )
    
    @get("/{studyDbId: str}/")
    async def get_one_study(self, transaction: AsyncSession, studyDbId: str) -> response.SingleResponse[Study]: 
        query = select(DbStudy).where(DbStudy.studyDbId == studyDbId)
        query_result = (await transaction.execute(query)).scalars().first()
        try:    
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        totalCount=1,
                        totalPages=1,
                        pageSize=1000,
                        currentPage=0,
                    ),
                    status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                    datafiles=[],
                ),
                result=Study(
                    studyDbId=query_result.studyDbId,
                    studyName=query_result.studyName,
                    # studyDescription=query_result.studyDescription,
                    # startDate=query_result.startDate,
                    # endDate=query_result.endDate,
                    # instituteName=query_result.instituteName,
                    # locationName=query_result.locationName,
                    trialDbId=query_result.trialDbId,
                    trialName=query_result.trialName,
                )
            )
        except:
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        totalCount=0,
                        totalPages=0,
                        pageSize=1000,
                        currentPage=0,
                    ),
                    status=[response.Message(message="Not Found", messageType=response.MESSAGETYPE.ERROR)],
                    datafiles=[],
                ),
                result=None
            )
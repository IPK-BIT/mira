import json
from litestar import Controller, get
from math import ceil
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas import response
from db.models.models import Trial as DbTrial
from db.schemas.core import Trial
from db.schemas import commons

class TrialController(Controller):
    path="/trials"

    @get('/')
    async def get_all_trials(self, transaction: AsyncSession, pageSize: int|None = None, page: int|None = None) -> response.Response[Trial]:
        if not pageSize:
            pageSize = 1000
        if not page:
            page = 0
        
        query = select(DbTrial)
        query_results = (await transaction.execute(query)).scalars().all()

        total_count = len(query_results)
        query = query.offset(page * pageSize).limit(pageSize)
        query_results = (await transaction.execute(query)).scalars().all()
        result = []
        for t in query_results:
            result.append(Trial(
                additionalInfo=t.additionalInfo,
                trialDbId=t.trialDbId,
                trialDescription=t.trialDescription,
                trialName=t.trialName,
                datasetAuthorships=[commons.Dataset(**dataset) for dataset in json.loads(t.datasetAuthorships)]
            ))

        return response.Response(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    currentPage=page,
                    pageSize=pageSize,
                    totalCount=total_count,
                    totalPages=ceil(total_count/pageSize),
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[]
            ),
            result=response.Result(data=result)
        )
    
    @get("/{trialDbId: str}/")
    async def get_one_trial(self, transaction: AsyncSession, trialDbId: str) -> response.SingleResponse[Trial]: 
        query = select(DbTrial).where(DbTrial.trialDbId == trialDbId)
        query_result = (await transaction.execute(query)).scalars().first()
        try:
            result = Trial(
                additionalInfo=query_result.additionalInfo,
                trialDbId=query_result.trialDbId,
                trialDescription=query_result.trialDescription,
                trialName=query_result.trialName,
                datasetAuthorships=[commons.Dataset(**dataset) for dataset in json.loads(query_result.datasetAuthorships)]
            )
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        currentPage=0,
                        pageSize=1000,
                        totalCount=1,
                        totalPages=1,
                    ),
                    status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                    datafiles=[]
                ),
                result=result
            )
        except:
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        currentPage=0,
                        pageSize=1000,
                        totalCount=0,
                        totalPages=0,
                    ),
                    status=[response.Message(message="Not Found", messageType=response.MESSAGETYPE.INFO)],
                    datafiles=[]
                ),
                result=None
            )
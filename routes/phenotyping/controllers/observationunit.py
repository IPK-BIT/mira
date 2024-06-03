from litestar import Controller, get

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas import response
from db.models.models import ObservationUnit as DbObservationUnit
from db.schemas.phenotyping import ObservationUnit

class ObservationUnitController(Controller):
    path = '/observationunits'
    
    @get('/')
    async def get_all_observationunits(self, transaction: AsyncSession, page: int|None = None, pageSize: int|None = None) -> response.Response[ObservationUnit]:
        if not page:
            page = 0
        if not pageSize:
            pageSize = 1000
        query = select(DbObservationUnit)
        query_results = (await transaction.execute(query)).scalars().all()
        total_count = len(query_results)
        query = query.offset(page * pageSize).limit(pageSize)
        query_results = (await transaction.execute(query)).scalars().all()
        results = []
        for u in query_results:
            results.append(ObservationUnit(
                observationUnitDbId=u.observationUnitDbId,
                observationUnitName=u.observationUnitName,
                observationUnitPUI=u.observationUnitPUI,
                germplasmDbId=u.germplasmDbId,
                germplasmName=u.germplasmName,
                trialDbId=u.trialDbId,
                trialName=u.trialName,
                studyDbId=u.studyDbId,
                studyName=u.studyName,
            ))
        return response.Response(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    pageSize=pageSize,
                    totalCount=total_count,
                    currentPage=page,
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[]
            ),
            result=response.Result(data=results)
        )
    
    @get('/{observationUnitDbId: str}/')
    async def get_one_observationunit(self, transaction: AsyncSession, observationUnitDbId: str) -> response.SingleResponse[ObservationUnit]:
        query = select(DbObservationUnit).where(DbObservationUnit.observationUnitDbId == observationUnitDbId)
        observation_unit = (await transaction.execute(query)).scalars().first()
        if not observation_unit:
            return response.SingleResponse(
                metadata=response.Metadata(
                    status=[response.Message(message="Observation unit not found", messageType=response.MESSAGETYPE.ERROR)],
                    datafiles=[]
                ),
                result=None
            )
        else: 
            return response.SingleResponse(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    pageSize=1,
                    totalCount=1,
                    totalPages=1,
                    currentPage=0,
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[]
            ),
            result=ObservationUnit(
                observationUnitDbId=observation_unit.observationUnitDbId,
                observationUnitName=observation_unit.observationUnitName,
                observationUnitPUI=observation_unit.observationUnitPUI,
                germplasmDbId=observation_unit.germplasmDbId,
                germplasmName=observation_unit.germplasmName,
                trialDbId=observation_unit.trialDbId,
                trialName=observation_unit.trialName,
                studyDbId=observation_unit.studyDbId,
                studyName=observation_unit.studyName,
            )
        )
    
from math import ceil

from litestar import Controller, get
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.schemas import response
from db.schemas.phenotyping import Observation
from db.models.models import Observation as DbObservation, ObservationUnit as DbObservationUnit, ObservationVariable as DbVariable

class ObservationController(Controller):
    path="/observations"
    
    @get('/')
    async def get_all_observations(self, transaction: AsyncSession
                                   , page: int|None = None
                                   , pageSize: int|None = None
                                   , observationVariableDbId: str|None = None
                                   , studyDbId: str|None = None
                                   , observationUnitDbId: str|None = None
                                   , germplasmDbId: str|None = None
    ) -> response.Response[Observation]: 
        if not page:
            page = 0
        if not pageSize:
            pageSize = 1000

        query = select(DbObservation)
        if observationVariableDbId:
            if ',' in observationVariableDbId:
                query = query.where(DbObservation.observationVariableDbId.in_(observationVariableDbId.split(',')))
            else:
                query = query.where(DbObservation.observationVariableDbId == observationVariableDbId)
        
        if studyDbId:
            if ',' in studyDbId:
                query = query.where(DbObservation.studyDbId.in_(studyDbId.split(',')))
            else:
                query = query.where(DbObservation.studyDbId == studyDbId)
        
        if observationUnitDbId:
            if ',' in observationUnitDbId:
                query = query.where(DbObservation.observationUnitDbId.in_(observationUnitDbId.split(',')))
            else:
                query = query.where(DbObservation.observationUnitDbId == observationUnitDbId)
        
        if germplasmDbId:
            if ',' in germplasmDbId:
                query = query.where(DbObservation.germplasmDbId.in_(germplasmDbId.split(',')))
            else:
                query = query.where(DbObservation.germplasmDbId == germplasmDbId)
        
        query_result = (await transaction.execute(query)).scalars().all()
        total_count = len(query_result)
        query = query.offset(page * pageSize).limit(pageSize)
        query_result = (await transaction.execute(query)).scalars().all()

        results = []
        for observation in query_result:
            results.append(Observation(
                germplasmDbId=observation.germplasmDbId,
                observationDbId = observation.observationDbId,
                observationTimeStamp = observation.observationTimeStamp,
                observationUnitDbId = observation.observationUnitDbId,
                observationVariableDbId = observation.observationVariableDbId,
                observationVariableName = observation.observationVariableName,
                studyDbId=observation.studyDbId,
                studyName=observation.studyName,
                value = observation.value,
            ))

        return response.Response(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    pageSize=pageSize,
                    totalCount=total_count,
                    totalPages=ceil(total_count/pageSize),
                    currentPage=page,
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[],
            ),
            result=response.Result(data=results)
        )
    
    @get('/table')
    async def get_all_observations_as_table(self, transaction: AsyncSession, page: int|None=None, pageSize: int|None=None, studyDbId: str|None = None) -> response.TableRespone:
        if not page:
            page = 0
        if not pageSize:
            pageSize = 1000

        q = select(DbObservationUnit).offset(page * pageSize).limit(pageSize)
        if studyDbId:
            q = q.where(DbObservationUnit.studyDbId == studyDbId)
        units = [u.observationUnitDbId for u in (await transaction.execute(q)).scalars().all()]

        query = select(DbObservation).where(DbObservation.observationUnitDbId.in_(units))
        
        query_result = (await transaction.execute(query)).scalars().all()
        total_count = len(query_result)

        variables = {}
        db_variables = (await transaction.execute(select(DbVariable).where(DbVariable.observationVariableDbId.in_([obs.observationVariableDbId for obs in query_result])))).scalars().all()
                
        for observation in query_result:
            variables[observation.observationVariableDbId] = next((v.observationVariableName for v in db_variables if v.observationVariableDbId == observation.observationVariableDbId), None)            
        
        table = []
        for u in units: 
            row = [u]
            try:
                row.append(max([obs.observationTimeStamp for obs in query_result if obs.observationUnitDbId == u]))
            except:
                row.append(None)
            for var_id, _ in variables.items():
                obs = next((obs for obs in query_result if obs.observationUnitDbId == u and obs.observationVariableDbId == var_id), None)
                if obs:
                    row.append(obs.value)
                else:
                    row.append(None)
            table.append(row)

        return response.TableRespone(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    pageSize=pageSize,
                    totalCount=total_count,
                    totalPages=ceil(total_count/pageSize),
                    currentPage=page,
                ),
                status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                datafiles=[],
            ),
            result=response.Table(
                data=table,
                headerRow=["observationUnitDbId", "observationTimeStamp"],
                observationVariables=[{'observationVariableDbId': var_id, 'observationVariableName': var_name} for var_id, var_name in variables.items()]
            )
        )
    
    @get('/{observationDbId: str}/')
    async def get_one_observation(self, transaction: AsyncSession, observationDbId: str|None = None) -> response.SingleResponse[Observation]:
        query = select(DbObservation).where(DbObservation.observationDbId == observationDbId)
        query_result = (await transaction.execute(query)).scalars().first()
        if not query_result:
            return response.SingleResponse(
                metadata=response.Metadata(
                    status=[response.Message(message="Not Found", messageType=response.MESSAGETYPE.ERROR)],
                ),
                result=None
            )
        else:
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        pageSize=1,
                        totalCount=1,
                        currentPage=0,
                        totalPages=1,
                    ),
                    status=[response.Message(message="Success", messageType=response.MESSAGETYPE.INFO)],
                    datafiles=[],
            ),
            result=Observation(
                observationDbId = query_result.observationDbId,
                observationTimeStamp = query_result.observationTimeStamp,
                observationUnitDbId= query_result.observationUnitDbId,
                observationVariableDbId = query_result.observationVariableDbId,
                value= query_result.value,
            )
        )
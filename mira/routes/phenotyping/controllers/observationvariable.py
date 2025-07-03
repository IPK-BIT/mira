from math import ceil
import json
from litestar import Controller, get

from db.schemas import response
from db.schemas.phenotyping import ObservationVariable, Method, Scale, Trait
from db.models.models import ObservationVariable as DbObservationVariable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class ObservationVariableController(Controller):
    path = '/variables'
    
    @get('/')
    async def get_all_variables(self, transaction: AsyncSession, pageSize: int|None = None, page: int|None = None, observationVariableDbId: str|None = None) -> response.Response[ObservationVariable]:
        if not pageSize:
            pageSize = 1000
        if not page:
            page = 0
        query = select(DbObservationVariable)
        if observationVariableDbId:
            query = query.where(DbObservationVariable.observationVariableDbId == observationVariableDbId)

        query_results = (await transaction.execute(query)).scalars().all()
        total_count = len(query_results)
        query = query.offset(page * pageSize).limit(pageSize)
        query_results = (await transaction.execute(query)).scalars().all()
        variables = []
        for db_variable in query_results:
            variables.append(ObservationVariable(
                observationVariableDbId=db_variable.observationVariableDbId,
                observationVariableName=db_variable.observationVariableName,
                observationVariablePUI=db_variable.observationVariablePUI,
                method=Method(**json.loads(db_variable.method)),
                scale=Scale(**db_variable.scale),
                trait=Trait(**json.loads(db_variable.trait)),
            ))
        return response.Response(
            metadata=response.Metadata(
                pagination=response.Pagination(
                    currentPage=page,
                    pageSize=pageSize,
                    totalCount=total_count,
                    totalPages=ceil(total_count/pageSize)
                ),
                status=[response.Message(messageType=response.MESSAGETYPE.INFO, message="Success")],
                datafiles=[]
            ),
            result=response.Result(data=variables)
        )
    
    @get('/{observationVariableDbId: str}/')
    async def get_one_variable(self, transaction: AsyncSession, observationVariableDbId: str) -> response.SingleResponse[ObservationVariable]:
        query = select(DbObservationVariable).where(DbObservationVariable.observationVariableDbId == observationVariableDbId)
        db_variable = (await transaction.execute(query)).scalars().first()
        if not db_variable:
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        currentPage=0,
                        pageSize=0,
                        totalCount=0,
                        totalPages=0
                    ),
                    status=[response.Message(messageType=response.MESSAGETYPE.ERROR, message="Variable not found")],
                    datafiles=[]
                )
            )
        else:
            variable = ObservationVariable(
                observationVariableDbId=db_variable.observationVariableDbId,
                observationVariableName=db_variable.observationVariableName,
                observationVariablePUI=db_variable.observationVariablePUI,
                method=Method(**json.loads(db_variable.method)),
                scale=Scale(**db_variable.scale),
                trait=Trait(**json.loads(db_variable.trait)),
            )
            return response.SingleResponse(
                metadata=response.Metadata(
                    pagination=response.Pagination(
                        currentPage=0,
                        pageSize=0,
                        totalCount=1,
                        totalPages=1
                    ),
                    status=[response.Message(messageType=response.MESSAGETYPE.INFO, message="Success")],
                    datafiles=[]
                ),
                result=variable
            )